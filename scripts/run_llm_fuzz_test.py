# --- Replace the main function in run_llm_fuzz_test.py on the SERVER ---

import sys
import os
import argparse
import json # Need json to parse the input string
from chcverifynfuzz import HornICEPipeline, CVC5Pipeline

def main():
    parser = argparse.ArgumentParser(description="Run a single AFL++ test harness (Contextual or Classical).")
    parser.add_argument("benchmark_name", help="The name of the benchmark.")
    # This argument now receives either a single spec name (Classical)
    # OR a JSON string dictionary of all specs (Contextual)
    parser.add_argument("spec_info", help="Spec name (Classical) or JSON map of specs (Contextual).")
    # This argument is now OPTIONAL, only used in Classical mode
    parser.add_argument("spec_rule", nargs='?', help="C++ expression string (Classical mode only).")
    parser.add_argument("mode", help="Pipeline mode (e.g., 'ContextualLLMHornICEFUZZ').")
    parser.add_argument("--timeout", type=int, default=10, help="Fuzzer timeout in seconds.")

    args = parser.parse_args()

    print(f"--- [LLM FUZZ DRIVER] Running for: {args.benchmark_name} (Mode: {args.mode}) ---")

    try:
        # 1. Instantiate the pipeline object
        if 'hornice' in args.mode.lower():
            pipeline = HornICEPipeline(benchmark_name=args.benchmark_name, mode=args.mode)
            pipeline.TIMEOUT = args.timeout
        else:
            print(f"FATAL ERROR: Unknown base mode in '{args.mode}'")
            sys.exit(1)

        # 2. Create working directory
        os.makedirs(pipeline.working_dir, exist_ok=True)

        # 3. Determine if Classical or Contextual and prepare harness
        if 'contextual' in args.mode.lower():
            print("--- Contextual Mode Detected ---")
            harness_basename = f"{args.benchmark_name}{pipeline.harness_ext}" # e.g., BinaryTreeCont_fuzz
            # Parse the JSON string back into a dictionary
            try:
                specs_to_write = json.loads(args.spec_info)
                if not isinstance(specs_to_write, dict):
                    raise ValueError("Input spec_info is not a valid JSON dictionary.")
            except (json.JSONDecodeError, ValueError) as e:
                print(f"FATAL ERROR: Could not parse specs_map_json argument: {e}")
                sys.exit(1)
            # The library's function handles injecting multiple specs if given a dict
            pipeline._write_spec_to_harness(f"{harness_basename}.cpp", specs_to_write)
            ce_filename = f"{harness_basename}CE.txt" # Contextual CE file name

        elif 'classical' in args.mode.lower():
            print("--- Classical Mode Detected ---")
            if not args.spec_rule:
                print("FATAL ERROR: spec_rule argument is required for Classical mode.")
                sys.exit(1)
            spec_name = args.spec_info # In classical, spec_info is just the name
            harness_basename = f"{spec_name}{pipeline.harness_ext}" # e.g., insert_fuzz
            specs_to_write = {spec_name: args.spec_rule}
            pipeline._write_spec_to_harness(f"{harness_basename}.cpp", specs_to_write)
            ce_filename = f"{spec_name}CE.txt" # Classical CE file name
        
        else:
             print(f"FATAL ERROR: Could not determine mode (Classical/Contextual) from '{args.mode}'")
             sys.exit(1)

        # 4. Run the fuzzer (the library handles the rest)
        result = pipeline._run_fuzz(harness_basename, ce_filename)

        # 5. Manually check for crash evidence
        crashes_dir = os.path.join(pipeline.working_dir, "afl_out", "default", "crashes")
        crashes_found = False
        if os.path.isdir(crashes_dir) and any(f.startswith("id:") for f in os.listdir(crashes_dir)):
            crashes_found = True

        # 6. Report TRUE status
        if crashes_found:
            print("\n[LLM FUZZ DRIVER] ❌ Fuzzing FAILED. Crash files found.")
            sys.exit(1)
        else:
            print("\n[LLM FUZZ DRIVER] ✅ Fuzzing complete. No crashes found.")
            sys.exit(0)

    except Exception as e:
        print(f"\n[LLM FUZZ DRIVER] An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

# Ensure the main execution block is present
if __name__ == "__main__":
    main()