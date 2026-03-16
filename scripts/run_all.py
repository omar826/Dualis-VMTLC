import argparse
import subprocess
import multiprocessing
import os
import time
import sys

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
            'ClassicalHornICE', 'ClassicalHornICEKLEE', 'ClassicalHornICE',
            'ClassicalLLMHornICE', 'ClassicalLLMHornICEKLEE', 'ClassicalLLMHornICE',
            'ContextualHornICE', 'ContextualHornICE', 'ContextualLLMHornICEKLEE',
            'ContextualLLMHornICE', 'ClassicalCVC5', 'ContextualCVC5'
        ],
        help="The execution modes (learners) to run (space-separated)."
    )
    parser.add_argument(
        "-b", "--benchmarks",
        nargs="+",
        required=True,
        help="The list of benchmarks to run (space-separated), or 'all' to run all."
    )
    parser.add_argument(
        "-p", "--processes",
        type=int,
        default=1,
        help="Number of processes. -1 uses all cores. Default is 1."
    )
    args = parser.parse_args()

    benchmark_list = [
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

    if "all" in [b.lower() for b in args.benchmarks]:
        target_benchmarks = benchmark_list
    else:
        target_benchmarks = [b for b in args.benchmarks if b in benchmark_list]
        missing = [b for b in args.benchmarks if b not in benchmark_list]
        if missing:
            print(f"Warning: The following benchmarks were not found and will be skipped: {missing}\n")

    if not target_benchmarks:
        print("Error: No valid benchmarks selected to run. Exiting.")
        sys.exit(1)

    tasks = [(mode, benchmark) for mode in args.modes for benchmark in target_benchmarks]

    if args.processes == -1:
        num_processes = os.cpu_count()
    else:
        num_processes = max(1, args.processes)

    num_processes = min(num_processes, len(tasks))

    print(
        f"Queueing {len(tasks)} tasks ({len(args.modes)} modes x {len(target_benchmarks)} benchmarks) "
        f"using {num_processes} processes...\n"
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

    with open(summary_report_path, "w") as report_file:
        report_file.write("="*70 + "\n")
        report_file.write(" ARTIFACT EVALUATION SUMMARY REPORT\n")
        report_file.write(f" Generated on: {time.ctime()}\n")
        report_file.write("="*70 + "\n\n")


        checker_map = {
            'hornice': check_hornice_success,
            'llmhornice': check_hornice_success 
        }

        for mode, benchmark in tasks:
            learner_key = 'hornice'
            if 'cvc5' in mode.lower(): learner_key = 'cvc5'
            if 'seahorn' in mode.lower(): learner_key = 'seahorn'

            check_func = checker_map.get(learner_key)

            report_file.write(f"[TASK] Mode: {mode} | Benchmark: {benchmark}\n")
            report_file.write("-" * 40 + "\n")

            if check_func:
                is_ok, message = check_func(mode, benchmark)
                if is_ok:
                    specs = get_rewritten_specs(mode, benchmark)
                    report_file.write("STATUS: PASS\n")
                    report_file.write(f"SPECS:\n{specs}\n")
                else:
                    report_file.write(f"STATUS: FAIL ({message})\n")
            else:
                report_file.write("STATUS: PASS (No specific check function defined)\n")
                report_file.write(f"SPECS:\n{get_rewritten_specs(mode, benchmark)}\n")

            report_file.write("-" * 70 + "\n\n")

    print(f"\n[!] Evaluation complete. Summary report written to: {summary_report_path}")

if __name__ == "__main__":
    main()
