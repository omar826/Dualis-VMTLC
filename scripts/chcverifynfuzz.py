import os
import subprocess
import sys
import shutil
import time
import argparse
import re
import signal

import processspecs as pspec

class BasePipeline:
    def __init__(self, benchmark_name, mode, deep_fuzz=False, test_only=False):
        print(f"Initializing pipeline for benchmark: '{benchmark_name}'")
        self.benchmark_name = benchmark_name
        self.mode = mode
        self.deep_fuzz = deep_fuzz
        self.test_only = test_only

        self.contract_type = 'classical' if 'classical' in self.mode.lower() else 'contextual'

        self.tester = 'FUZZ'
        self.harness_ext = "_fuzz"

        self.verifier_name = 'cvc5' if 'cvc5' in self.mode.lower() else 'hornice'
        use_der_verifier = 'llm' in self.mode.lower()

        file_dir = os.path.dirname(os.path.realpath(__file__))

        self.chc_verifier_path = "chc_verifier_der" if use_der_verifier else "chc_verifier"
        self.cvc5_path = "cvc5"

        base_benchmarks_path = os.path.join(file_dir, "../benchmarks")
        self.classical_benchmark_dir = os.path.join(
            base_benchmarks_path, "Classical", self.benchmark_name
        )
        self.contextual_benchmark_dir = os.path.join(
            base_benchmarks_path, "Contextual", self.benchmark_name
        )

        self.working_dir = os.path.join(
            base_benchmarks_path, f"{self.mode}_working_temp", self.benchmark_name
        )
        self.logs_path = os.path.join(file_dir, "../logs")

        self.chc_file_original = self._get_path(f"{self.benchmark_name}.smt2")
        self.working_chc_file = os.path.join(
            self.working_dir, f"{self.benchmark_name}.smt2"
        )
        self.old_chc_file = os.path.join(
            self.working_dir, f"{self.benchmark_name}old.smt2"
        )
        self.new_chc_file = os.path.join(
            self.working_dir, f"{self.benchmark_name}new.smt2"
        )

        self.mode_log_dir = os.path.join(self.logs_path, f"{self.mode}Pipeline_Logs")
        self.internal_log_dir = os.path.join(self.mode_log_dir, f"internal_{self.benchmark_name}")
        os.makedirs(self.internal_log_dir, exist_ok=True)

        self.external_iteration_count = 0
        self.internal_iteration_stats = []
        self.total_unique_testcases = 0

        self.HI_TIMEOUT = 1000
        self.CVC5_TIMEOUT = 1000
        self.SEAHORN_TIMEOUT = 1000
        self.TIMEOUT = 10

        self.mappings_valid = self._load_and_validate_attribute_mappings()

    def _get_path(self, filename):
        if self.contract_type == 'contextual':
            specific_path = os.path.join(self.contextual_benchmark_dir, filename)
            if os.path.exists(specific_path):
                return specific_path

        return os.path.join(self.classical_benchmark_dir, filename)

    def _convert_ce(self, relation, ce_filename):
        raise NotImplementedError("Subclasses must implement '_convert_ce'")

    def _run_fuzzing_and_convert(self, specs_map):
        if self.contract_type == 'classical':
            for relation in specs_map.keys():
                if relation.startswith(("inv", "valid")): continue
                harness_base = f"{relation}{self.harness_ext}"
                ce_file = f"{relation}CE.txt"
                self._write_spec_to_harness(f"{harness_base}.cpp", {relation: specs_map[relation]})

                result = self._run_fuzz(harness_base, ce_file)
                if result is False:
                    return False

                self._convert_ce(relation, ce_file)

        elif self.contract_type == 'contextual':
            harness_base = f"{self.benchmark_name}{self.harness_ext}"
            ce_file = f"{harness_base}CE.txt"
            self._write_spec_to_harness(f"{harness_base}.cpp", specs_map)

            result = self._run_fuzz(harness_base, ce_file)
            if result is False:
                return False
            self._convert_ce(self.benchmark_name, ce_file)
        return True

    def _load_and_validate_attribute_mappings(self):
        self.variable_map = {}
        self.derived_attributes = {}
        mapping_file_path = self._get_path("Attributes.txt")

        print(f"   -> Loading and validating attributes from: {mapping_file_path}")
        if not os.path.exists(mapping_file_path):
            print("      -> WARNING: Attributes.txt not found. Cannot perform sanity checks.")
            return True

        try:
            with open(mapping_file_path, 'r') as f:
                lines = [line for line in f if line.strip() and not line.strip().startswith('#')]

            i = 0
            if lines and lines[0].strip().isdigit() and len(lines[0].strip().split()) == 1:
                i = 1

            while i < len(lines):
                header = lines[i].strip().split()
                relation, num_primary, num_derived = header[0], int(header[1]), int(header[2])
                i += 1

                if i + num_primary + num_derived > len(lines):
                    print(f"      -> FATAL ERROR in Attributes.txt for '{relation}':")
                    print(f"         Header expects {num_primary} primary + {num_derived} derived,")
                    print(f"         but the file ends prematurely.")
                    return False

                primary_vars_by_index = {}
                for j in range(num_primary):
                    idx, var = lines[i+j].strip().split()
                    primary_vars_by_index[int(idx)] = var

                self.variable_map[relation] = [primary_vars_by_index[k] for k in range(num_primary)]

                derived_exprs = []
                for j in range(num_derived):
                    derived_exprs.append(lines[i + num_primary + j].strip())

                self.derived_attributes[relation] = derived_exprs
                i += num_primary + num_derived

            print("      -> Validation successful. Attribute file is consistent.")
            return True
        except Exception as e:
            print(f"      -> FATAL ERROR: Could not parse or validate Attributes.txt: {e}")
            return False

    def _write_spec_to_harness(self, harness_filename, specs_to_write):
        print(f"   -> Writing new specs to harness: {harness_filename}...")
        source_harness_file = self._get_path(harness_filename)
        working_harness_file = os.path.join(self.working_dir, harness_filename)

        if not os.path.exists(source_harness_file):
            print(f"      -> ERROR: Harness file not found at '{source_harness_file}'")
            return

        updated_lines = []
        try:
            with open(source_harness_file, 'r') as f:
                lines = f.readlines()

            for line in lines:
                if self.contract_type == "contextual":
                    match = re.match(r"(\s*)bool\s+expr_(\w+)\s*=\s*.*;", line)
                elif self.contract_type == "classical":
                    match = re.match(r"(\s*)bool\s+expr\s*=\s*.+;", line)
                if match:
                    indentation = match.group(1)
                    if self.contract_type == "contextual":
                        relation_name = match.group(2)
                    elif self.contract_type == "classical":
                        relation_name = harness_filename.replace("_fuzz.cpp", "")
                    spec_content = specs_to_write.get(relation_name, "false")
                    if self.contract_type == "contextual":
                        new_line = f"{indentation}bool expr_{relation_name} = {spec_content};\n"
                    elif self.contract_type == "classical":
                        new_line = f"{indentation}bool expr = {spec_content};\n"
                    updated_lines.append(new_line)
                else:
                    updated_lines.append(line)

            with open(working_harness_file, 'w') as f:
                f.writelines(updated_lines)
            print(f"      -> Successfully created working copy '{working_harness_file}'.")
        except Exception as e:
            print(f"      -> ERROR: Failed to read/write harness file: {e}")

    def _run_fuzz(self, harness_basename, ce_filename):
        process_name = f"AFL++({harness_basename})"
        print(f"   -> Starting {process_name} with a {self.TIMEOUT}-second timeout...")

        src_path = os.path.join(self.working_dir, f"{harness_basename}.cpp")
        base_no_ext, ext = os.path.splitext(src_path)
        executable = base_no_ext

        input_dir = os.path.join(self.working_dir, "afl_in")
        output_dir = os.path.join(self.working_dir, "afl_out")

        os.makedirs(input_dir, exist_ok=True)
        src_seed_dir = self._get_path("in")
        for filename in os.listdir(src_seed_dir):
            src_seed_path = os.path.join(src_seed_dir, filename)
            if os.path.isfile(src_seed_path):
                shutil.copy2(src_seed_path, input_dir)

        print(f"   -> Building AFL-instrumented binary: {executable}")
        os.environ["AFL_LLVM_CMPLOG"] = "1"
        os.environ['AFL_I_DONT_CARE_ABOUT_MISSING_CRASHES'] = "1"
        build_cmd = [
            "afl-clang-fast++",
            "-std=c++20",
            "-I/usr/include/c++/11/", "-I/usr/include/x86_64-linux-gnu/c++/11/",
            "-g", "-O2",
            "-o", executable, src_path,
            "-L/usr/lib/gcc/x86_64-linux-gnu/11/"
        ]

        try:
            build_process = subprocess.Popen(build_cmd,
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE,
                                             text=True)
            build_stdout, build_stderr = build_process.communicate(timeout=120)
            if build_process.returncode != 0:
                print(f"   -> ERROR: Failed to build AFL binary: {build_stderr}")
                return False
        except Exception as e:
            print(f"   -> ERROR: Failed to build AFL binary: {e}")
            return False

        env = dict(os.environ)
        env.update({
            "FUZZING":"1",
            "AFL_NO_UI":"1",
            "AFL_DONT_OPTIMIZE":"1",
            "AFL_CMPLOG_ONLY_NEW":"1",
            "AFL_DEBUG_CHILD":"1",
            "AFL_IGNORE_PROBLEMS":"1",
            "AFL_I_DONT_CARE_ABOUT_MISSING_CRASHES":"1",
            "AFL_LLVM_CMPLOG" : "1",
            "AFL_LLVM_LAF_ALL" : "1",
            "AFL_SKIP_CPUFREQ" : "1"
        })
        command = ["afl-fuzz",
                   "-i", input_dir,
                   "-o", output_dir,
                   "-t", "2000",
                   "-p", "exploit" ,
                   "-V", str(self.TIMEOUT),
                   executable]

        if ce_filename:
            command.append(os.path.join(self.working_dir, ce_filename))

        process = None
        try:
            process = subprocess.Popen(command,
                                       stdout=subprocess.DEVNULL,
                                       stderr=subprocess.PIPE,
                                       env = env,
                                       text=True)
            _, stderr = process.communicate(timeout=self.TIMEOUT)

            if process.returncode == 0:
                print(f"   -> {process_name} completed successfully.")
                return self._check_fuzz_crashes(output_dir, executable, ce_filename)
            else:
                print(f"   -> ERROR: {process_name} failed with exit code {process.returncode}.")
                if stderr:
                    print(f"      AFL++ Error Output:\n{stderr}")
                return self._check_fuzz_crashes(output_dir, executable, ce_filename)
        except subprocess.TimeoutExpired:
            print(f"   -> {process_name} finished its fuzzing session.")
            if process:
                process.terminate()
                process.communicate()
            return self._check_fuzz_crashes(output_dir, executable, ce_filename)
        except Exception as e:
            print(f"   -> FATAL ERROR during {process_name}: {e}")
            return False

    def _check_fuzz_crashes(self, output_dir, executable, ce_filename=None):
        print("   -> Checking fuzzing outputs for counterexamples...")
        dirs = ["crashes", "queue", "hangs"]

        ce_filepath = os.path.join(self.working_dir, ce_filename) if ce_filename else None

        for fuzz_dir in dirs:
            print (f"Checking {fuzz_dir}")
            crashes_dir = os.path.join(output_dir, "default", fuzz_dir)
            if not os.path.exists(crashes_dir):
                continue

            crash_files = [f for f in os.listdir(crashes_dir) if f.startswith("id:")]
            if not crash_files:
                continue

            print(f"   -> Found {len(crash_files)} crash reports. Testing reproducibility...")

            for crash_file in crash_files:
                crash_path = os.path.join(crashes_dir, crash_file)
                try:
                    run_cmd = f'{executable} {os.path.join(self.working_dir, ce_filename)} < {crash_path}'
                    process = subprocess.Popen(
                        run_cmd,
                        shell=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.PIPE)

                    _, stderr = process.communicate(timeout=5)

                    if process.returncode != 0:
                        print(f"   -> CRASH REPRODUCED with {crash_file}")

                except subprocess.TimeoutExpired:
                    continue
                except Exception:
                    continue

        return True

    def _run_test_only(self):
        print("\n" + "="*20 + " RUNNING TEST-ONLY MODE " + "="*20)
        if not os.path.exists(self.working_dir):
            print(f"   -> ERROR: Working directory not found: {self.working_dir}")
            print(f"   -> Please run a normal pipeline first to generate the executables.")
            return False

        self.TIMEOUT = 900
        print(f"   -> Deep fuzzing timeout set to {self.TIMEOUT} seconds.")

        harnesses = []
        for file in os.listdir(self.working_dir):
            if file.endswith(f"{self.harness_ext}.cpp"):
                harnesses.append(file[:-4])

        if not harnesses:
            print(f"   -> ERROR: No harness files (*{self.harness_ext}.cpp) found in {self.working_dir}.")
            return False

        print(f"   -> Found {len(harnesses)} harness(es) to test: {', '.join(harnesses)}")

        for harness_basename in harnesses:
            if self.contract_type == 'classical':
                relation = harness_basename.replace(self.harness_ext, "")
                ce_file = f"{relation}CE.txt"
            else:
                relation = self.benchmark_name
                ce_file = f"{harness_basename}CE.txt"

            self._run_fuzz(harness_basename, ce_file)
            self._convert_ce(relation, ce_file)

        print("\n" + "="*22 + " Test-Only Finished " + "="*21)
        return True    

    def _dump_iteration_artifacts(self):
        raise NotImplementedError("Subclasses must implement the 'dump' method.")

    def run(self):
        raise NotImplementedError("Subclasses must implement the 'run' method.")


class HornICEPipeline(BasePipeline):
    def __init__(self, benchmark_name, mode, deep_fuzz=False, test_only=False):
        super().__init__(benchmark_name, mode, deep_fuzz, test_only)
        self.chc_file_original = self._get_path(f"{self.benchmark_name}.smt2")
        self.working_chc_file = os.path.join(
            self.working_dir, f"{self.benchmark_name}.smt2"
        )
        self.old_chc_file = os.path.join(
            self.working_dir, f"{self.benchmark_name}old.smt2"
        )
        self.new_chc_file = os.path.join(
            self.working_dir, f"{self.benchmark_name}new.smt2"
        )

        self.declarations, self.rules, self.queries = [], [], []
        self.ce_rules = []

        self.internal_iteration_stats = []
        self.HI_TIMEOUT = 1000

    def _specs_changed(self):
        print("   -> Checking if specs have changed...")
        if not os.path.exists(self.old_chc_file):
            print("      -> Old CHC file not found. First iteration.")
            return True
        result = subprocess.run(["diff", self.old_chc_file, self.new_chc_file], capture_output=True)
        if result.returncode == 0:
            print("      -> CHC files are identical. Pipeline has converged.")
            return False
        else:
            print("      -> CHC files are different. Continuing iteration.")
            return True

    def _parse_chc_file(self):
        self.declarations, self.rules, self.queries = [], [], []
        print(f"   -> Parsing CHC file: {self.working_chc_file}")
        try:
            with open(self.working_chc_file, 'r') as f:
                for line in f:
                    stripped = line.strip()
                    if stripped.startswith(";;") or not stripped: continue
                    if stripped.startswith(("(declare-rel", "(declare-var", "(define-fun")):
                        self.declarations.append(stripped)
                    elif stripped.startswith("(rule"):
                        self.rules.append(stripped)
                    elif stripped.startswith("(query"):
                        self.queries.append(stripped)
            return True
        except FileNotFoundError:
            print(f"   -> FATAL ERROR: CHC file not found at '{self.chc_file_original}'.")
            return False

    def _update_chc_file(self):
        print("   -> Updating CHC file with new counterexamples...")
        try:
            with open(self.new_chc_file, 'w') as f:
                for item in self.declarations: f.write(f"{item}\n")
                f.write('\n')
                for new_rule in self.ce_rules:
                    if new_rule not in self.rules: f.write(f"{new_rule}\n")
                f.write('\n')
                for item in self.rules: f.write(f"{item}\n")
                f.write('\n')
                for item in self.queries: f.write(f"{item}\n")
            return True
        except IOError as e:
            print(f"   -> FATAL ERROR: Could not write to new CHC file '{self.new_chc_file}': {e}")
            return False

    def _convert_ce(self, relation_from_loop, ce_filename):
        print(f"   -> Converting counterexamples for '{relation_from_loop}'...")
        ce_file = os.path.join(self.working_dir, ce_filename)
        if not os.path.exists(ce_file):
            print("      -> No counterexample file found.")
            return

        newly_found_rules = 0
        try:
            with open(ce_file, 'r') as file:
                for line_num, line in enumerate(file, 1):
                    line = line.strip()
                    if not line or not (line.startswith('(') and line.endswith(')')):
                        continue

                    content = line[1:-1].strip()

                    try:
                        relation_part, assignments_part = content.split(' ', 1)
                    except ValueError:
                        print(f"      -> WARNING: Skipping malformed line {line_num} in '{os.path.basename(ce_file)}'.")
                        continue

                    relation_from_file = relation_part.strip()
                    assignments = assignments_part.split(',')

                    ce_vars = []
                    ce_vals = []
                    valid_assignment = True
                    for part in assignments:
                        try:
                            var, val = part.split("=")
                            ce_vars.append(var.strip())
                            ce_vals.append(val.strip())
                        except ValueError:
                            print(f"      -> WARNING: Skipping malformed assignment '{part}' in '{os.path.basename(ce_file)}' on line {line_num}.")
                            valid_assignment = False
                            break

                    if not valid_assignment:
                        continue

                    expected_var_order = self.variable_map.get(relation_from_file)
                    if not expected_var_order:
                        print(f"      -> WARNING: No mapping found for relation '{relation_from_file}'. Cannot validate.")
                        continue

                    if ce_vars != expected_var_order:
                        print(f"      -> FATAL ERROR in '{os.path.basename(ce_file)}' line {line_num}:")
                        print(f"         Variable order mismatch for relation '{relation_from_file}'.")
                        print(f"         Expected: {expected_var_order}")
                        print(f"         Actual:   {ce_vars}")
                        continue

                    rule = "(rule (=> (and"
                    for i in range(len(ce_vars)):
                        rule += f" (= {ce_vars[i]} {ce_vals[i]})"
                    rule += f") ({relation_from_file}"
                    for var in ce_vars:
                        rule += f" {var}"
                    rule += ")))"

                    if rule not in self.ce_rules:
                        self.ce_rules.append(rule)
                        newly_found_rules += 1

            if newly_found_rules > 0:
                self.total_unique_testcases += newly_found_rules
                print(f"      -> Found and validated {newly_found_rules} new rules.")
        except Exception as e:
            print(f"      -> ERROR: Could not process file '{ce_file}': {e}")

    def _analyze_hornice_log(self, log_path):
        print(f"   -> Analyzing HornICE log file: {os.path.basename(log_path)}")
        max_iter = -1
        try:
            with open(log_path, 'r') as f:
                for line in f:
                    if "Learning Iteration:" in line:
                        num = int(line.split(":")[-1].strip())
                        if num > max_iter: max_iter = num

            internal_iterations = max_iter + 1
            if internal_iterations > 0:
                self.internal_iteration_stats.append(internal_iterations)
                print(f"      -> Found {internal_iterations} internal iterations.")
            else:
                print("      -> No internal learning iterations found in log.")
        except Exception as e:
            print(f"      -> Could not analyze log file '{log_path}': {e}")

    def _run_hornice(self):
        process_name = "HornICE"
        print(f"   -> Starting {process_name} with a {self.HI_TIMEOUT}-second timeout...")

        output_genspec_path = os.path.join(self.working_dir, "GenSpec.txt")

        command = [
            os.path.join(self.chc_verifier_path),
            "-b",
            self.working_chc_file,
            output_genspec_path
        ]

        temp_der_attrs_file = os.path.join(self.working_dir, "Attributes.txt")

        if "der" in os.path.basename(self.chc_verifier_path):
            print("      -> Found derived attributes. Creating temporary Attributes.txt  file.")
            try:
                with open(temp_der_attrs_file, 'w') as f:
                    content_lines = []
                    for relation, exprs in self.derived_attributes.items():
                        primary_vars = self.variable_map.get(relation, [])
                        content_lines.append(f"{relation} {len(primary_vars)} {len(exprs)}")
                        for i, var in enumerate(primary_vars):
                            content_lines.append(f"{i} {var}")
                        for expr in exprs:
                            content_lines.append(expr)
                    f.write("\n".join(content_lines))
                command.append(temp_der_attrs_file)
            except Exception as e:
                print(f"      -> FATAL ERROR: Could not create temporary Attributes.txt: {e}")
                return False

        log_path = os.path.join(self.internal_log_dir, f"iter_{self.external_iteration_count}.log")
        print(f"      -> Logging {process_name} output to {os.path.basename(log_path)}")

        success = False
        process = None
        try:
            with open(log_path, 'w') as log_file:
                process = subprocess.Popen(command, stdout=log_file, stderr=log_file, text=True)
            process.communicate(timeout=self.HI_TIMEOUT)

            if process.returncode == 0:
                print(f"   -> {process_name} completed successfully.")
                self._analyze_hornice_log(log_path)
                success = True
            else:
                print(f"   -> ERROR: {process_name} failed with exit code {process.returncode}.")
        except subprocess.TimeoutExpired:
            print(f"   -> ERROR: {process_name} timed out. Terminating.")
            if process:
                process.kill()
                process.communicate()
        except Exception as e:
            print(f"   -> FATAL ERROR during {process_name}: {e}")
        finally:
            if "der" in os.path.basename(self.chc_verifier_path) and os.path.exists(temp_der_attrs_file):
                os.remove(temp_der_attrs_file)

        return success

    def run(self):
        if self.test_only:
            self._run_test_only()
            return

        if not os.path.exists(self.chc_file_original):
            print(f"FATAL ERROR: No .smt2 file found for benchmark '{self.benchmark_name}'")
            return

        os.makedirs(self.working_dir, exist_ok=True)
        shutil.copy(self.chc_file_original, self.working_chc_file)

        is_final_phase = False
        try:
            shutil.copy(self.working_chc_file, self.old_chc_file)
            while True:
                self.external_iteration_count += 1
                print("\n" + "="*20 + f" Iteration: {self.external_iteration_count} " + "="*20)

                if not is_final_phase:
                    self.TIMEOUT = min(10 * self.external_iteration_count * 2, 500) 
                else:
                    print("   -> [FINAL VERIFICATION] Running 15-minute deep fuzzing phase...")
                    self.TIMEOUT = 900
                print (f"TIMEOUT : {self.TIMEOUT}")

                if not self._parse_chc_file(): return
                if not self._run_hornice(): break

                pspec.formatSpecs(self.working_dir, self.verifier_name)
                if not pspec.finalSpecs:
                    print("FATAL ERROR: No specs generated. Stopping.")
                    break

                specs_map = {spec[0]: spec[2] for spec in pspec.finalSpecs}

                if self._run_fuzzing_and_convert(specs_map) is False:
                    break

                if not self._update_chc_file(): break

                self._dump_iteration_artifacts()

                if not self._specs_changed(): 
                    if self.deep_fuzz and not is_final_phase:
                        print("   -> Short fuzzing converged. Stepping up to 15-minute deep fuzzing.")
                        is_final_phase = True
                        shutil.copy(self.new_chc_file, self.old_chc_file)
                        shutil.copy(self.new_chc_file, self.working_chc_file)
                        continue
                    else:
                        print("   -> 15-minute deep fuzzing converged. Pipeline complete.")
                        break
                else:
                    if is_final_phase:
                        print("   -> Deep fuzzing found a counterexample! Reverting to rapid learning.")
                shutil.copy(self.new_chc_file, self.old_chc_file)
                shutil.copy(self.new_chc_file, self.working_chc_file)

        finally:
            print("\n" + "="*20 + " Finalizing Pipeline " + "="*20)

        print("\n" + "="*22 + " Pipeline Finished " + "="*21)
        print(f"Total External Iterations: {self.external_iteration_count}")
        print(f"Total Unique Test Cases Found: {self.total_unique_testcases}")

        if self.internal_iteration_stats:
            total = sum(self.internal_iteration_stats)
            count = len(self.internal_iteration_stats)
            print(f"Total Internal Iterations: {total}")
            print(f"  - Min: {min(self.internal_iteration_stats)}")
            print(f"  - Max: {max(self.internal_iteration_stats)}")
            print(f"  - Avg: {total / count:.2f}")

    def _dump_iteration_artifacts(self):
        print("\n" + "="*15 + " Artifacts This Iteration " + "="*15)

        print("\n--- Generated Specs ---")
        if pspec.finalSpecs:
            for rel, _, rule in pspec.finalSpecs:
                print(f"  {rel}: {rule}")
        else:
            print("  (No specs were generated)")

        print("\n--- New Test Cases Found ---")
        if self.contract_type == 'classical':
            found_any = False
            for relation, _, _ in pspec.finalSpecs:
                if not relation.startswith(("inv", "valid")):
                    ce_file = os.path.join(self.working_dir, f"{relation}CE.txt")
                    if os.path.exists(ce_file):
                        with open(ce_file, "r") as f:
                            content = f.read().strip()
                            if content:
                                found_any = True
            if not found_any: print("  (None)")
        elif self.contract_type == 'contextual':
            ce_file = os.path.join(self.working_dir, f"{self.benchmark_name}ContCE.txt")
            if os.path.exists(ce_file):
                with open(ce_file, "r") as f:
                    content = f.read().strip()
                    if content: print(content)
                    else: print("  (None)")
            else: print("  (None)")

        print("\n--- Updated CHCs (for next iteration) ---")
        if os.path.exists(self.new_chc_file):
            with open(self.new_chc_file, "r") as f:
                print(f.read().strip())
        else:
            print("  (Could not be generated)")

        print("=" * 62)

class CVC5Pipeline(BasePipeline):
    def __init__(self, benchmark_name, mode, deep_fuzz=False, test_only=False):
        super().__init__(benchmark_name, mode, deep_fuzz, test_only)
        self.CVC5_TIMEOUT = 1000
        self.sygus_original_file = self._get_path(f"{self.benchmark_name}.sy")
        self.working_sygus_file = os.path.join(
            self.working_dir, f"{self.benchmark_name}.sy"
        )
        self.new_sygus_file = os.path.join(
            self.working_dir, f"{self.benchmark_name}new.sy"
        )
        self.old_sygus_file = os.path.join(
            self.working_dir, f"{self.benchmark_name}old.sy"
        )

        self.logic, self.constraints, self.synthfuns, self.declarations, self.definitions, self.ce_constraints, self.goal = [], [], [], [], [], [], []

        print(f"Total External Iterations: {self.external_iteration_count}")
        print(f"Total Unique Test Cases Found: {self.total_unique_testcases}")

    def _specs_changed(self):
        print("   -> Checking if specs have changed...")
        if not os.path.exists(self.old_sygus_file):
            print("      -> Old SYGUS file not found. First iteration.")
            return True
        result = subprocess.run(["diff", self.old_sygus_file, self.new_sygus_file], capture_output=True)
        if result.returncode == 0:
            print("      -> SYGUS files are identical. Pipeline has converged.")
            return False
        else:
            print("      -> SYGUS files are different. Continuing iteration.")
            return True

    def _parse_sygus_file(self):
        self.logic, self.constraints, self.synthfuns, self.declarations, self.definitions, self.ce_constraints, self.goal = [], [], [], [], [], [], []
        print(f"   -> Parsing SYGUS file: {self.working_sygus_file}")
        try:
            with open(self.working_sygus_file, 'r') as f:
                for line in f:
                    stripped = line.strip()
                    if stripped.startswith(";;") or not stripped: continue
                    if stripped.startswith(("(set-logic")):
                        self.logic.append(stripped)
                    if stripped.startswith(("(synth-fun")):
                        self.synthfuns.append(stripped)
                    if stripped.startswith(("(declare-var")):
                        self.declarations.append(stripped)
                    elif stripped.startswith("(define-fun"):
                        self.definitions.append(stripped)
                    elif stripped.startswith("(constraint"):
                        self.constraints.append(stripped)
                    elif stripped.startswith("(check-synth"):
                        self.goal.append(stripped)
            return True
        except FileNotFoundError:
            print(f"   -> FATAL ERROR: SYGUS file not found at '{self.sygus_original_file}'.")
            return False

    def _update_sygus_file(self):
        print("   -> Updating CHC file with new counterexamples...")
        try:
            with open(self.new_sygus_file, 'w') as f:
                for item in self.logic: f.write(f"{item}\n")
                f.write('\n')
                for item in self.synthfuns: f.write(f"{item}\n")
                f.write('\n')
                for item in self.declarations: f.write(f"{item}\n")
                f.write('\n')

                for item in self.definitions: f.write(f"{item}\n")
                if self.definitions: f.write('\n')

                for new_constraint in self.ce_constraints:
                    if new_constraint not in self.constraints: f.write(f"{new_constraint}\n")
                f.write('\n')
                for item in self.constraints: f.write(f"{item}\n")
                f.write('\n')
                for item in self.goal: f.write(f"{item}\n")
            return True
        except IOError as e:
            print(f"   -> FATAL ERROR: Could not write to new CHC file '{self.new_sygus_file}': {e}")
            return False

    def _convert_ce(self, relation, ce_filename):
        print(f"   -> Converting counterexamples for '{relation}'...")
        ce_file = os.path.join(self.working_dir, ce_filename)
        if not os.path.exists(ce_file):
            print("      -> No counterexample file found.")
            return

        newly_found_constraints = 0
        try:
            with open(ce_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or not (line.startswith('(') and line.endswith(')')):
                        continue

                    content = line[1:-1].strip()
                    try:
                        relation_part, assignments_part = content.split(' ', 1)
                    except ValueError:
                        print(f"      -> WARNING: Skipping malformed line in '{os.path.basename(ce_file)}'.")
                        continue

                    relation_from_file = relation_part.strip()

                    values = [val.split('=')[-1].strip() for val in assignments_part.split(',')]
                    f_values = [re.sub(r'-(\d+)', r'(- \1)', val) for val in values]

                    constraint = f"(constraint ({relation_from_file} {' '.join(f_values)}))"

                    if constraint not in self.ce_constraints:

                        self.ce_constraints.append(constraint)
                        newly_found_constraints += 1

            if newly_found_constraints > 0:
                self.total_unique_testcases += newly_found_constraints
                print(f"       -> Found and validated {newly_found_constraints} new constraints.")
        except Exception as e:
            print(f"      -> ERROR: Could not process CE file '{ce_filename}': {e}")

    def _run_cvc5(self):
        process_name = "CVC5"
        print(f"   -> Starting {process_name} with a {self.HI_TIMEOUT}-second timeout...")

        output_genspec_path = os.path.join(self.working_dir, "GenSpec.txt")

        if not os.path.exists(self.working_sygus_file):
            print(f"      -> FATAL ERROR: SyGuS input file not found at '{self.working_sygus_file}'")
            return False

        command = [
            self.cvc5_path,
            "--produce-models",
            "--sygus-add-const-grammar",
            self.working_sygus_file
        ]
        log_path = os.path.join(self.internal_log_dir, f"iter_{self.external_iteration_count}.log")
        print(f"      -> Logging {process_name} output to {os.path.basename(log_path)}")


        success = False
        process = None
        try:
            with open(log_path, 'w') as log_file:
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate(timeout=self.HI_TIMEOUT)

            if process.returncode == 0:
                with open(output_genspec_path, 'w') as f:
                    f.write(stdout)
                print(f"   -> {process_name} completed successfully.")
                success = True
            else:
                print(f"   -> ERROR: {process_name} failed with exit code {process.returncode}.")
                print(f"      -> Error Output:\n{stderr}")
                success = False        
        except subprocess.TimeoutExpired:
            print(f"   -> ERROR: {process_name} timed out. Terminating.")
            if process:
                process.kill()
                process.communicate()
            success = False
        except Exception as e:
            print(f"   -> FATAL ERROR during {process_name}: {e}")
            success = False
        return success

    def run(self):
        if self.test_only:
            self._run_test_only()
            return

        if not os.path.exists(self.sygus_original_file):
            print(f"FATAL ERROR: No SyGuS (.sy) file found for benchmark '{self.benchmark_name}'")
            return

        os.makedirs(self.working_dir, exist_ok=True)
        shutil.copy(self.sygus_original_file, self.working_sygus_file)

        is_final_phase = False
        try:
            shutil.copy(self.working_sygus_file, self.old_sygus_file)
            while True:
                self.external_iteration_count += 1
                print("\n" + "="*20 + f" Iteration: {self.external_iteration_count} " + "="*20)

                if not is_final_phase:
                    self.TIMEOUT = min(10 * self.external_iteration_count * 2, 500) 
                else:
                    print("   -> [FINAL VERIFICATION] Running 15-minute deep fuzzing phase...")
                    self.TIMEOUT = 900
                print (f"TIMEOUT : {self.TIMEOUT}")

                if not self._parse_sygus_file(): return
                if not self._run_cvc5(): break

                pspec.formatSpecs(self.working_dir, self.verifier_name)
                if not pspec.finalSpecs:
                    print("FATAL ERROR: No specs generated. Stopping.")
                    break

                specs_map = {spec[0]: spec[2] for spec in pspec.finalSpecs}

                if self._run_fuzzing_and_convert(specs_map) is False:
                    break

                if not self._update_sygus_file(): break

                self._dump_iteration_artifacts()

                if not self._specs_changed():
                    if self.deep_fuzz and not is_final_phase:
                        print("   -> Short fuzzing converged. Stepping up to 15-minute deep fuzzing.")
                        is_final_phase = True
                        shutil.copy(self.new_sygus_file, self.old_sygus_file)
                        shutil.copy(self.new_sygus_file, self.working_sygus_file)
                        continue
                    else:
                        print("   -> 15-minute deep fuzzing converged. Pipeline complete.")
                        break
                else:
                    if is_final_phase:
                        print("   -> Deep fuzzing found a counterexample! Reverting to rapid learning.")
                        is_final_phase = False
                        self.TIMEOUT = 900

                shutil.copy(self.new_sygus_file, self.old_sygus_file)
                shutil.copy(self.new_sygus_file, self.working_sygus_file)

        finally:
            print("\n" + "="*20 + " Finalizing Pipeline " + "="*20)

        print("\n" + "="*22 + " Pipeline Finished " + "="*21)
        print(f"Total External Iterations: {self.external_iteration_count}")
        print(f"Total Unique Test Cases Found: {self.total_unique_testcases}")

    def _dump_iteration_artifacts(self):
        print("\n" + "="*15 + " Artifacts This Iteration " + "="*15)

        print("\n--- Generated Specs ---")
        if pspec.finalSpecs:
            for rel, _, rule in pspec.finalSpecs:
                print(f"  {rel}: {rule}")
        else:
            print("  (No specs were generated)")

        print("\n--- New Test Cases Found ---")
        if self.contract_type == 'classical':
            found_any = False
            for relation, _, _ in pspec.finalSpecs:
                if not relation.startswith(("inv", "valid")):
                    ce_file = os.path.join(self.working_dir, f"{relation}CE.txt")
                    if os.path.exists(ce_file):
                        with open(ce_file, "r") as f:
                            content = f.read().strip()
                            if content:
                                found_any = True
            if not found_any:
                print("  (None)")
        elif self.contract_type == 'contextual':
            ce_file = os.path.join(self.working_dir, f"{self.benchmark_name}ContCE.txt")
            if os.path.exists(ce_file):
                with open(ce_file, "r") as f:
                    content = f.read().strip()
                    if content:
                        print(content)
                    else:
                        print("  (None)")

        print("\n--- Updated SYGUS (for next iteration) ---")
        if os.path.exists(self.new_sygus_file):
            with open(self.new_sygus_file, "r") as f:
                print(f.read().strip())
        else:
            print("  (Could not be generated)")

        print("=" * 62)

class SeaHornPipeline(BasePipeline):
    def __init__(self, benchmark_name, mode):
        super().__init__(benchmark_name, mode)
        self.c_file_path = self._get_path(f"{self.benchmark_name}_sea.cpp")

        self.working_c_file = os.path.join(self.working_dir, f"{self.benchmark_name}_sea.cpp")

        # self.seahorn_log_file = os.path.join(self.logs_path, "seahorn_baselines.log")

        self.mode_log_dir = os.path.join(self.logs_path, self.mode)
        os.makedirs(self.mode_log_dir, exist_ok=True)
        self.benchmark_log_file = os.path.join(self.mode_log_dir, f"{self.benchmark_name}.log")

    def _run_seahorn(self):
        process_name = f"SeaHorn({self.benchmark_name})"
        print(f"   -> Starting {process_name} with a {self.SEAHORN_TIMEOUT}-second timeout...")

        if not os.path.exists(self.working_c_file):
            print(f"      -> ERROR: Source file not found at '{self.c_file_path}'.")
            with open(self.benchmark_log_file, "w") as b_log:
                b_log.write(f"ERROR: Source file not found at '{self.c_file_path}'.\n")
            return "FILE_NOT_FOUND"

        command = [
            "sea", "pf", 
            "-m64", 
            self.working_c_file
        ]

        try:
            process = subprocess.Popen(command, 
                                       stdout=subprocess.PIPE, 
                                       stderr=subprocess.PIPE, 
                                       text=True,
                                       start_new_session=True)
            stdout, stderr = process.communicate(timeout=self.SEAHORN_TIMEOUT)

            with open(self.benchmark_log_file, "w") as b_log:
                b_log.write(f"Command: {' '.join(command)}\n\n")
                b_log.write("=== STDOUT ===\n")
                b_log.write(stdout if stdout else "(none)\n")
                b_log.write("\n=== STDERR ===\n")
                b_log.write(stderr if stderr else "(none)\n")

            if process.returncode == 0 and "unsat" in stdout.lower():
                print(f"   -> {process_name} completed: UNSAT (Safe).")
                return "UNSAT"
            elif "sat" in stdout.lower():
                print(f"   -> {process_name} completed: SAT (Counterexample found).")
                return "SAT"
            else:
                print(f"   -> ERROR: {process_name} returned unknown status.")
                if stderr:
                    print(f"      SeaHorn Error Output:\n{stderr}")
                return "ERROR"

        except subprocess.TimeoutExpired:
            print(f"   -> ERROR: {process_name} timed out.")
            if process:
                try:
                    os.killpg(os.getpgid(process.pid), signal.SIGKILL)
                except ProcessLookupError:
                    pass
                process.communicate()

            with open(self.benchmark_log_file, "w") as b_log:
                b_log.write(f"=== TIMEOUT EXPIRED after {self.SEAHORN_TIMEOUT} seconds ===\n")
                
            return "TIMEOUT"
        except Exception as e:
            print(f"   -> FATAL ERROR during {process_name}: {e}")
            with open(self.benchmark_log_file, "w") as b_log:
                b_log.write(f"=== FATAL ERROR ===\n{e}\n")
            return "ERROR"

    def run(self):
        print("\n" + "="*20 + " Running SeaHorn Baseline " + "="*20)

        if not os.path.exists(self.c_file_path):
            print(f"FATAL ERROR: No source file found for benchmark '{self.benchmark_name}' at {self.c_file_path}")
            return

        os.makedirs(self.working_dir, exist_ok=True)
        os.makedirs(self.logs_path, exist_ok=True)

        shutil.copy(self.c_file_path, self.working_c_file)
        print(f"   -> Copied source file to working directory.")

        result = self._run_seahorn()

        log_entry = f"Benchmark: {self.benchmark_name} | Mode: {self.contract_type} | Result: {result}\n"
        # with open(self.seahorn_log_file, "a") as log_file:
        #     log_file.write(log_entry)

        # print(f"   -> Result logged to {self.seahorn_log_file}")
        print("\n" + "="*22 + " Pipeline Finished " + "="*21)


def main():
    parser = argparse.ArgumentParser(description="Run a Verification-Modulo-Testing pipeline.")
    parser.add_argument(
        "mode",
        choices=[
            'ClassicalHornICE',
            'ClassicalLLMHornICE',
            'ContextualHornICE',
            'ContextualLLMHornICE',
            'ClassicalCVC5',
            'ContextualCVC5',
            'ContextualSeaHorn'
        ],
        help="The execution mode for the pipeline."
    )
    parser.add_argument("benchmark", help="The name of the benchmark to run.")
    parser.add_argument("--deep-fuzz", action="store_true", help="Run 15-minute deep fuzzing explicitly after convergence.")
    parser.add_argument("--test-only", action="store_true", help="Skip learning and only run 15-minute fuzzing on existing executables.")
    
    args = parser.parse_args()

    print("\n" + "="*40)
    print(f"         Starting Pipeline for: {args.benchmark} (Mode: {args.mode})")
    print("="*40)

    if 'hornice' in args.mode.lower():
        pipeline = HornICEPipeline(
            benchmark_name=args.benchmark,
            mode=args.mode,
            deep_fuzz=args.deep_fuzz,
            test_only=args.test_only
        )
    elif 'cvc5' in args.mode.lower():
        pipeline = CVC5Pipeline(
            benchmark_name=args.benchmark,
            mode=args.mode,
            deep_fuzz=args.deep_fuzz,
            test_only=args.test_only
        )
    elif 'seahorn' in args.mode.lower():
        pipeline = SeaHornPipeline(
            benchmark_name=args.benchmark,
            mode=args.mode
        )
    else:
        print(f"FATAL ERROR: Unknown mode '{args.mode}'")
        return

    start_time = time.process_time()
    pipeline.run()
    end_time = time.process_time()

    elapsed_time = end_time - start_time
    print(f"pipeline.run() took {elapsed_time:.4f} seconds.")

if __name__ == "__main__":
    main()
