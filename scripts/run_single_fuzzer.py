# File: /home/omarmuhammad/RapNLearn/scripts/run_single_fuzzer.py

import sys
import os
import argparse
from chcverifynfuzz import HornICEPipeline 

def main():
    parser = argparse.ArgumentParser(description="Run a single AFL++ test harness.")
    parser.add_argument("benchmark_name", help="The name of the benchmark to run.")
    parser.add_argument("spec_name", help="The name of the spec/function to test (e.g., 'insert').")
    parser.add_argument("spec_rule", help="The C++ boolean expression string to inject.")
    parser.add_argument("mode", help="The pipeline mode (e.g., 'ClassicalLLMHornICEFUZZ').")
    
    parser.add_argument("--timeout", type=int, default=10, help="Fuzzer timeout in seconds.")
    args = parser.parse_args()

    print(f"--- [REMOTE] Running Single Fuzzer for: {args.benchmark_name}/{args.spec_name} ---")

    try:

        pipeline = HornICEPipeline(benchmark_name=args.benchmark_name, mode=args.mode)

        pipeline.TIMEOUT = args.timeout
        
        os.makedirs(pipeline.working_dir, exist_ok=True)
        ce_file_path = os.path.join(pipeline.working_dir, f"{args.spec_name}CE.txt")
        if os.path.exists(ce_file_path):
            os.remove(ce_file_path)
        harness_basename = f"{args.spec_name}{pipeline.harness_ext}"
        specs_to_write = {args.spec_name: args.spec_rule}
        pipeline._write_spec_to_harness(f"{harness_basename}.cpp", specs_to_write)

        result = pipeline._run_fuzz(harness_basename, f"{args.spec_name}CE.txt")

        if result is True:
            print("\n[REMOTE] ✅ Fuzzing complete. No crashes found.")
            sys.exit(0)
        else:
            print("\n[REMOTE] ❌ Fuzzing FAILED. Crashes were likely found.")
            sys.exit(1)

    except Exception as e:
        print(f"\n[REMOTE] An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()