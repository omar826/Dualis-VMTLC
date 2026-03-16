import os
import shutil
import subprocess
import sys

MAIN_SCRIPT = "chcverifynfuzz.py"
BENCHMARKS = ["BinaryTree", "Stack"]
MODES = [
    "ClassicalHornICE",
    "ContextualHornICE",
    "ClassicalLLMHornICE",
    "ContextualLLMHornICE",
    "ClassicalLLMFUZZ",
    "ContextualLLMFUZZ"
]

def clean_working_temp():
    file_dir = os.path.dirname(os.path.realpath(__file__))
    working_temp_dir = os.path.join(file_dir, "../benchmarks/working_temp")
    
    if os.path.exists(working_temp_dir):
        print(f"[*] Cleaning up working directory: {working_temp_dir}")
        for item in os.listdir(working_temp_dir):
            item_path = os.path.join(working_temp_dir, item)
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
            except Exception as e:
                print(f"[!] Failed to delete {item_path}. Reason: {e}")
    else:
        print(f"[*] Working directory {working_temp_dir} does not exist yet. Skipping cleanup.")

def run_pipeline(mode, benchmark):
    print(f"\n{'='*60}")
    print(f"KICKING THE TIRES: {benchmark} | {mode}")
    print(f"{'='*60}")
    
    clean_working_temp()
    
    command = [sys.executable, MAIN_SCRIPT, mode, benchmark]
    
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    
    captured_output = []
    while True:
        line = process.stdout.readline()
        if not line and process.poll() is not None:
            break
        if line:
            print(line, end="")
            captured_output.append(line)
            
    print(f"\n[{benchmark} | {mode}] --- SUMMARY OF FINAL SPECS (EXTERNAL ITERATIONS) ---")
    
    capturing_specs = False
    for line in captured_output:
        if "Iteration:" in line:
            print(f"\n{line.strip()}")
        elif "--- Generated Specs ---" in line:
            capturing_specs = True
            continue
        elif capturing_specs and line.strip() == "":
            capturing_specs = False
        elif capturing_specs and "No specs were generated" not in line:
            if not line.startswith("---") and not line.startswith("==="):
                print(line.strip())

def main():
    if not os.path.exists(MAIN_SCRIPT):
        print(f"[!] ERROR: Could not find '{MAIN_SCRIPT}'. Please update the MAIN_SCRIPT variable.")
        sys.exit(1)

    for benchmark in BENCHMARKS:
        for mode in MODES:
            run_pipeline(mode, benchmark)
            
    print("\n" + "="*60)
    print("All 'Kick-the-Tires' runs completed successfully.")
    print("="*60)

if __name__ == "__main__":
    main()
