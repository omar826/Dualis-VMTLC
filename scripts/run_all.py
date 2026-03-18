import argparse
import subprocess
import multiprocessing
import os
import time
import sys
import re
from collections import defaultdict

def run_benchmark_pipeline(mode, benchmark):
    start_time = time.time()
    pid = os.getpid()
    print(f"\n[PID {pid}] Starting full pipeline for benchmark: '{benchmark}' | Mode: {mode}")

    output_directory = f"../logs/{mode}Pipeline_Logs/"
    os.makedirs(output_directory, exist_ok=True)

    log_file_path = os.path.join(output_directory, f"{benchmark}_pipeline.log")

    command = [sys.executable, "chcverifynfuzz.py", mode, benchmark]

    try:
        with open(log_file_path, 'w') as log_file:
            log_file.write(f"Running command: {' '.join(command)}\n")
            log_file.write(f"PID: {pid}\n")
            log_file.write("="*40 + "\n\n")

            subprocess.run(
                command,
                check=True,
                text=True,
                stdout=log_file,
                stderr=log_file
            )

        end_time = time.time()
        duration = end_time - start_time

        with open(log_file_path, 'a') as log_file_append:
            log_file_append.write(f"\nTotal Pipeline Duration: {duration:.2f}s\n")

        print(f"[PID {pid}] Finished successfully: '{benchmark}' ({mode}). Duration: {duration:.2f}s. See log: {log_file_path}")
    except subprocess.CalledProcessError:
        print(f"[PID {pid}] ERROR in pipeline for '{benchmark}' ({mode}). Check log for details: {log_file_path}")
    except FileNotFoundError:
        print(f"[PID {pid}] FATAL ERROR: Could not find the worker script 'chcverifynfuzz.py'.")
    except Exception as e:
        print(f"[PID {pid}] An unexpected error occurred for '{benchmark}' ({mode}): {e}")

def check_hornice_success(mode, benchmark):
    log_path = os.path.join("..", "logs", f"{mode}Pipeline_Logs", f"{benchmark}_pipeline.log")

    if not os.path.exists(log_path):
        return False, f"Missing log file: {log_path}"

    try:
        with open(log_path, 'r') as f:
            content = f.read()
            if "ERROR: HornICE timed out." in content:
                return False, "FAILED: HornICE timed out during learning."

            if "FATAL ERROR" in content or "Traceback" in content:
                return False, "FAILED: Internal script error or crash detected."

        return True, "Success"
    except Exception as e:
        return False, f"Error reading log: {e}"

def check_cvc5_success(mode, benchmark):
    log_path = os.path.join("..", "logs", f"{mode}Pipeline_Logs", f"{benchmark}_pipeline.log")

    if not os.path.exists(log_path):
        return False, f"Missing log file: {log_path}"

    try:
        with open(log_path, 'r') as f:
            content = f.read()
            if "ERROR: CVC5 timed out." in content:
                return False, "FAILED: CVC5 timed out during learning."

            if "FATAL ERROR" in content or "Traceback" in content:
                return False, "FAILED: Internal script error or crash detected."

        return True, "Success"
    except Exception as e:
        return False, f"Error reading log: {e}"

def check_seahorn_success(mode, benchmark):
    log_path = os.path.join("..", "logs", f"{mode}Pipeline_Logs", f"{benchmark}_pipeline.log")

    if not os.path.exists(log_path):
        return False, f"Missing log file: {log_path}"

    try:
        with open(log_path, 'r') as f:
            content = f.read()

            # Catch wrapper script crashes first
            if "FATAL ERROR" in content or "Traceback" in content:
                return False, "FAILED: Internal script error or crash detected."

            # Grep for the exact solver outputs
            if "completed: UNSAT" in content or "UNSAT" in content:
                return True, "UNSAT (Safe)"
            elif "completed: SAT" in content or "SAT" in content:
                return True, "SAT (Unsafe)"
            else:
                return False, "FAILED: No SAT/UNSAT result found (Likely Timeout)."

    except Exception as e:
        return False, f"Error reading log: {e}"

def get_rewritten_specs(mode, benchmark):
    spec_path = os.path.join("..", "benchmarks", f"{mode}_working_temp", benchmark, "RewrittenSpecs.txt")

    if not os.path.exists(spec_path):
        return "N/A: RewrittenSpecs.txt was not generated."

    try:
        with open(spec_path, 'r') as f:
            content = f.read().strip()
            return content if content else "(Empty spec file)"
    except Exception as e:
        return f"Error reading specs: {e}"

def parse_metrics_from_log(mode, benchmark):
    """Extracts Iterations (External/Internal) and Time from the log file."""
    log_path = os.path.join("..", "logs", f"{mode}Pipeline_Logs", f"{benchmark}_pipeline.log")

    metrics = {"status": "MISSING", "E": 0, "I": 0, "T": 0.0}
    if not os.path.exists(log_path):
        return metrics

    try:
        with open(log_path, 'r') as f:
            content = f.read()

            if "ERROR: HornICE timed out." in content or "FATAL ERROR" in content or "TIMEOUT" in content:
                metrics["status"] = "TO"
            else:
                metrics["status"] = "PASS"

            ext_match = re.search(r"Total External Iterations:\s*(\d+)", content)
            if ext_match: metrics["E"] = int(ext_match.group(1))

            int_match = re.search(r"Total Internal Iterations:\s*(\d+)", content)
            if int_match: metrics["I"] = int(int_match.group(1))

            time_match = re.search(r"Total Pipeline Duration:\s*([\d\.]+)s", content)
            if time_match:
                metrics["T"] = float(time_match.group(1)) / 60.0

    except Exception:
        metrics["status"] = "ERROR"

    return metrics

def generate_text_table(table_data, benchmark_list, modes_run):
    """Generates a plain text ASCII table for the evaluation results."""
    b_width = max([len(b) for b in benchmark_list] + [20]) + 2
    m_width = max([len(m) for m in modes_run] + [16]) + 2

    lines = []

    header1 = f"{'Benchmark'.ljust(b_width)}|" + "|".join([m.center(m_width) for m in modes_run]) + "|"
    header2 = f"{''.ljust(b_width)}|" + "|".join(["E+I      T(m)".center(m_width) for m in modes_run]) + "|"
    separator = "-" * len(header1)

    lines.extend([separator, header1, header2, separator])

    for bench in benchmark_list:
        row_str = f"{bench.ljust(b_width)}|"
        has_data = False

        for mode in modes_run:
            metrics = table_data.get(bench, {}).get(mode, {"status": "MISSING"})

            if metrics["status"] == "TO":
                cell = f"{metrics['E']}+{metrics['I']}       TO"
                has_data = True
            elif metrics["status"] == "PASS":
                cell = f"{metrics['E']}+{metrics['I']}     {metrics['T']:.2f}"
                has_data = True
            else:
                cell = "-        -"

            row_str += cell.center(m_width) + "|"

        if has_data:
            lines.append(row_str)

    lines.append(separator)
    return "\n".join(lines)

def main():
    print("=" * 43)
    print(" Running Benchmarks in Parallel")
    print("=" * 43 + "\n")

    parser = argparse.ArgumentParser(
        description="Run benchmark pipelines in parallel.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""\
        Example usage:
        Run specific modes on specific benchmarks:
        python3 %(prog)s -m ClassicalHornICE ContextualHornICE -b Stack BinaryTree -p 4

        Run multiple modes on all benchmarks:
        python3 %(prog)s -m ClassicalLLMHornICE ContextualLLMHornICE -b all -p 8
        """
    )
    parser.add_argument(
        "-m", "--modes",
        nargs="+",
        required=True,
        choices=[
            'ClassicalHornICE',
            'ClassicalLLMHornICE',
            'ContextualHornICE',
            'ContextualLLMHornICE',
            'ClassicalCVC5',
            'ContextualCVC5',
            'ContextualSeaHorn'
        ],
        help="The execution modes (learners) to run (space-separated)."
    )
    parser.add_argument(
        "-b", "--benchmarks",
        nargs="+",
        required=True,
        help="The list of benchmarks to run (space-separated), or 'all' to run all allowed non-timeouts."
    )
    parser.add_argument(
        "-p", "--processes",
        type=int,
        default=1,
        help="Number of processes. -1 uses all cores. Default is 1."
    )
    args = parser.parse_args()

    MODE_BENCHMARKS = {
        'ClassicalHornICE': [
            "AlternatingList", "BinaryHeap2", "BinaryTree", "BlueWhite",
            "Calender", "DLL_Circular", "FlatHashMap1", "Max",
            "Min", "NormalFilterQueue", "PriorityFilterQueue",
            "SkipList2", "SkipList3", "SkipList5", "SkipList7",
            "Stack", "StockOrder", "TokenBucket1", "TokenBucket2"
        ],
        'ContextualHornICE': [
            "AlternatingList", "AtomicHashMap4", "AtomicHashMap5",
            "AtomicLinkedList1", "BinaryHeap2", "BinaryTree", "BlueWhite",
            "Calender", "DLL_Circular", "DLL_Token", "FlatHashMap1",
            "FlatHashMap2", "FlatHashMap3", "FlatHashMap4", "Max",
            "Min", "Multimap1", "NormalFilterQueue", "PriorityFilterQueue",
            "ProcessQueue", "RedBlackTree", "SkipList1", "SkipList2",
            "SkipList3", "SkipList5", "SkipList6", "SkipList7", "Stack",
            "StockOrder", "TokenBucket1", "TokenBucket2"
        ],
        'ClassicalLLMHornICE': [
            "AlternatingList", "BinaryHeap2", "BinaryTree", "BlueWhite",
            "Calender", "DLL_Circular", "DLL_Token", "FlatHashMap2",
            "LruCache1", "Max", "Min", "Multimap1", "Multiset1",
            "NormalFilterQueue", "PriorityFilterQueue", "ProcessQueue",
            "SkipList2", "SkipList3", "SkipList5", "SkipList7", "Stack",
            "StockOrder", "TokenBucket1", "TokenBucket2", "TokenBucket3"
        ],
        'ContextualLLMHornICE': [
            "AlternatingList", "AtomicHashMap4", "AtomicLinkedList1",
            "BinaryHeap2", "BinaryTree", "BlueWhite", "Calender",
            "DLL_Circular", "DLL_Token", "FlatHashMap1", "FlatHashMap2",
            "FlatHashMap3", "Max", "Min", "Multimap1", "Multiset1",
            "NormalFilterQueue", "PriorityFilterQueue", "ProcessQueue",
            "RedBlackTree", "SkipList1", "SkipList2", "SkipList3",
            "SkipList5", "SkipList6", "SkipList7", "Stack", "StockOrder",
            "TokenBucket1", "TokenBucket2", "TokenBucket3"
        ],
        'ContextualCVC5' : ["AtomicHashMap1", "AtomicHashMap2",
            "AtomicHashMap4", "AtomicHashMap5", "BinaryHeap2", "BinaryTree",
            "Calender", "Multimap1", "NormalFilterQueue", "SkipList2",
            "SkipList3", "SkipList5", "SkipList7", "StockOrder",
            "TokenBucket1", "TokenBucket3"
        ],
        'ClassicalCVC5' : ["AtomicHashMap1", "AtomicLinkedList1",
            "BinaryHeap2", "BinaryTree", "Calender","NormalFilterQueue",
            "RedBlackTree","StockOrder", "TokenBucket1", "TokenBucket3"
        ],
        # others timeout or found counterexample but were false
        # positives.
        'ContextualSeaHorn':[
            "AtomicLinkedList2", "FlatHashMap2", "BlueWhite",
            "TokenBucket1", "TokenBucket2", "NormalFilterQueue", "PriorityFilterQueue"
        ]
    }

    ALL_BENCHMARKS = [
        "AlternatingList", "AtomicHashMap1", "AtomicHashMap2", "AtomicHashMap3",
        "AtomicHashMap4", "AtomicHashMap5", "AtomicLinkedList1", "AtomicLinkedList2",
        "BinaryHeap1", "BinaryHeap2", "BinaryTree", "BlueWhite", "Calender",
        "DLL_Circular", "DLL_Token", "FlatHashMap1", "FlatHashMap2", "FlatHashMap3",
        "FlatHashMap4", "FlatHashSet", "LruCache1", "Max", "Min", "Multimap1",
        "Multimap2", "Multiset1", "Multiset2", "NormalFilterQueue",
        "PriorityFilterQueue", "ProcessQueue", "RedBlackTree", "SkipList1",
        "SkipList2", "SkipList3", "SkipList4", "SkipList5", "SkipList6",
        "SkipList7", "Stack", "StockOrder", "TokenBucket1", "TokenBucket2", "TokenBucket3"
    ]

    tasks = []
    for mode in args.modes:
        allowed_for_mode = MODE_BENCHMARKS.get(mode, ALL_BENCHMARKS)

        if "all" in [b.lower() for b in args.benchmarks]:
            target_benchmarks = allowed_for_mode
        else:
            target_benchmarks = [b for b in args.benchmarks if b in allowed_for_mode]
            missing = [b for b in args.benchmarks if b not in allowed_for_mode]
            if missing:
                print(f"Warning: {missing} skipped for '{mode}' (Not in allowed list).")

        for b in target_benchmarks:
            tasks.append((mode, b))

    if not tasks:
        print("Error: No valid benchmarks selected to run. Exiting.")
        sys.exit(1)

    if args.processes == -1:
        num_processes = os.cpu_count()
    else:
        num_processes = max(1, args.processes)

    num_processes = min(num_processes, len(tasks))

    print(
        f"Queueing {len(tasks)} tasks using {num_processes} processes...\n"
    )

    with multiprocessing.Pool(processes=num_processes) as pool:
        try:
            pool.starmap(run_benchmark_pipeline, tasks)
        except KeyboardInterrupt:
            print("\nCaught KeyboardInterrupt, terminating workers.")
            pool.terminate()
            pool.join()
            sys.exit(1)

    summary_report_path = "evaluation_summary.txt"
    cvc5_report_path = "cvc5_summary.txt"
    seahorn_report_path = "seahorn_summary.txt"

    modes_run = set([m for m, b in tasks])
    has_alllearners = any('cvc5' not in m.lower() and 'seahorn' not in m.lower() for m in modes_run)
    has_cvc5 = any('cvc5' in m.lower() for m in modes_run)
    has_seahorn = any('seahorn' in m.lower() for m in modes_run)

    with open(summary_report_path, "a") as f_alll, \
         open(cvc5_report_path, "a") as f_cvc5, \
         open(seahorn_report_path, "a") as f_sea:

        if has_alllearners:
            f_alll.write("="*70 + "\n")
            f_alll.write(" ARTIFACT EVALUATION SUMMARY REPORT \n")
            f_alll.write(f" Generated on: {time.ctime()}\n")
            f_alll.write("="*70 + "\n\n")

        if has_cvc5:
            f_cvc5.write("="*70 + "\n")
            f_cvc5.write(" CVC5 EVALUATION SUMMARY REPORT\n")
            f_cvc5.write(f" Generated on: {time.ctime()}\n")
            f_cvc5.write("="*70 + "\n\n")

        if has_seahorn:
            f_sea.write("="*70 + "\n")
            f_sea.write(" SEAHORN EVALUATION SUMMARY REPORT\n")
            f_sea.write(f" Generated on: {time.ctime()}\n")
            f_sea.write("="*70 + "\n\n")

        checker_map = {
            'hornice': check_hornice_success,
            'llmhornice': check_hornice_success,
            'cvc5' : check_cvc5_success,
            'seahorn' : check_seahorn_success
        }

        for mode, benchmark in tasks:
            learner_key = 'hornice'
            if 'cvc5' in mode.lower(): learner_key = 'cvc5'
            if 'seahorn' in mode.lower(): learner_key = 'seahorn'

            check_func = checker_map.get(learner_key)
            is_ok, message = check_func(mode, benchmark) if check_func else (True, "No check defined")

            if learner_key == 'cvc5':
                status = "Yes" if is_ok else f"No ({message})"
                f_cvc5.write(f"Mode: {mode.ljust(20)} | Benchmark: {benchmark.ljust(22)} | Spec Generated: {status}\n")

            elif learner_key == 'seahorn':
                status = message if is_ok else f"No ({message})"
                f_sea.write(f"Mode: {mode.ljust(20)} | Benchmark: {benchmark.ljust(22)} | Proof Generated: {status}\n")

            else:
                f_alll.write(f"[TASK] Mode: {mode} | Benchmark: {benchmark}\n")
                f_alll.write("-" * 40 + "\n")

                if is_ok:
                    specs = get_rewritten_specs(mode, benchmark)
                    f_alll.write("STATUS: PASS\n")
                    f_alll.write(f"SPECS:\n{specs}\n")
                else:
                    f_alll.write(f"STATUS: FAIL ({message})\n")

                f_alll.write("-" * 70 + "\n\n")

        hornice_modes = [m for m in args.modes if 'cvc5' not in m.lower() and 'seahorn' not in m.lower()]
        # if hornice_modes:
        #     f_alll.write("\n" + "="*70 + "\n")
        #     f_alll.write(" PERFORMANCE METRICS TABLE (HornICE Variants)\n")
        #     f_alll.write("="*70 + "\n\n")

        #     table_data = defaultdict(dict)
        #     for mode, benchmark in tasks:
        #         if mode in hornice_modes:
        #             metrics = parse_metrics_from_log(mode, benchmark)
        #             table_data[benchmark][mode] = metrics

        #     text_table = generate_text_table(table_data, ALL_BENCHMARKS, hornice_modes)
        #     f_alll.write(text_table + "\n\n")

    print(f"\n[!] Evaluation complete. Check output files: {summary_report_path}, {cvc5_report_path}, {seahorn_report_path}")

if __name__ == "__main__":
    main()
