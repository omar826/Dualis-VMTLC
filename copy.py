import os
import shutil

PROJECT_ROOT = os.getcwd() # Run this from your Dualis root
BENCHMARKS_DIR = os.path.join(PROJECT_ROOT, "benchmarks")
VETTED_DIR = os.path.join(PROJECT_ROOT, "logs_old", "Vetted_Specs")

def setup_vetted_specs():
    modes = ["Classical", "Contextual"]
    
    for mode in modes:
        mode_source_dir = os.path.join(BENCHMARKS_DIR, mode)
        mode_target_dir = os.path.join(VETTED_DIR, mode)
        
        if not os.path.exists(mode_source_dir):
            continue
            
        os.makedirs(mode_target_dir, exist_ok=True)
        
        # Add an __init__.py so Python can import from this folder
        with open(os.path.join(mode_target_dir, "__init__.py"), "w") as f:
            pass 

        for benchmark in os.listdir(mode_source_dir):
            source_file = os.path.join(mode_source_dir, benchmark, "llm_definitions.py")
            
            if os.path.exists(source_file):
                # Save it as benchmark_name.py (e.g., SkipList2.py)
                target_file = os.path.join(mode_target_dir, f"{benchmark}.py")
                shutil.copy(source_file, target_file)
                print(f"✅ Vetted: Copied {mode}/{benchmark} specs.")

if __name__ == "__main__":
    setup_vetted_specs()
    print("\n[!] Finished setting up Vetted Specs.")