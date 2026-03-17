import os
import importlib.util
import inspect
import z3

PROJECT_ROOT = os.getcwd()
BENCHMARKS_DIR = os.path.join(PROJECT_ROOT, "benchmarks")
VETTED_DIR = os.path.join(PROJECT_ROOT, "logs_old", "Vetted_Specs")
REPORT_PATH = os.path.join(PROJECT_ROOT,"scripts", "implication_report.txt")


TARGET_BENCHMARKS = [ "AlternatingList", "BinaryTree", "BlueWhite",
                       "Calender", "DLL_Circular", "DLL_Token", "Max", "Min", "TokenBucket1", "TokenBucket2", "TokenBucket3",
                       "Stack", "StockOrder",  "Multimap1", "Multimap2", 
                       "Multiset1", "Multiset2", "AtomicHashMap1","AtomicHashMap2", "AtomicHashMap3", "AtomicHashMap4",
                       "AtomicHashMap5", "AtomicLinkedList1", "SkipList1", "SkipList2", "SkipList3", "SkipList4",
                       "SkipList5", "SkipList6", "SkipList7", "BinaryHeap1", "BinaryHeap2",  "NormalFilterQueue",
                       "PriorityFilterQueue", "ProcessQueue", "RedBlackTree","FlatHashMap1",
                       "FlatHashMap2", "FlatHashMap3", "FlatHashMap4", "FlatHashMap", "AtomicLinkedList2"
                       
                        ]

def load_module_from_path(module_name, file_path):
    """Dynamically loads a Python file as a module."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def check_implication(vetted_expr, generated_expr):
    """Returns True if A => B is proven mathematically."""
    solver = z3.Solver()

    solver.add(vetted_expr)
    solver.add(z3.Not(generated_expr))
    
    result = solver.check()
    return result == z3.unsat

def run_implication_checks():
    modes = ["Classical", "Contextual"]
    
    with open(REPORT_PATH, "w") as report:

        report.write("="*75 + "\n")
        report.write(" MATHEMATICAL IMPLICATION REPORT (Z3)\n")
        report.write("="*75 + "\n\n")
        report.write("IMPORTANT NOTES & CAVEATS:\n")
        report.write("1) The generated specs evaluated here represent the *last* spec generated\n")
        report.write("   by the LLM for that benchmark, independent of whether the run passed or failed.\n")
        report.write("2) If Vetted => Generated: The generated specification is logically implied by\n")
        report.write("   the ground truth, meaning the generated spec is correct.\n")
        report.write("3) If Not Implying: This does *not* necessarily mean the generated contracts\n")
        report.write("   are incorrect. It simply means Z3 could not prove a strict logical\n")
        report.write("   implication, which requires further manual inspection.\n")
        report.write("4) If you have not run some benchmark yet, it may be using an older generated spec for the implications check.\n")
        report.write("="*75 + "\n\n")

        for mode in modes:
            report.write(f"\n{'#'*30} {mode.upper()} PIPELINE {'#'*30}\n\n")
            print(f"\n--- Processing {mode} Pipeline ---")
            
            for benchmark in TARGET_BENCHMARKS:
                report.write(f"[TASK] Benchmark: {benchmark}\n")
                report.write("-" * 50 + "\n")
                
                vetted_path = os.path.join(VETTED_DIR, mode, f"{benchmark}.py")
                generated_path = os.path.join(BENCHMARKS_DIR, mode, benchmark, "llm_definitions.py")
                

                if not os.path.exists(vetted_path):
                    report.write("  [!] STATUS: Skipped - No Vetted Spec found for this benchmark.\n\n")
                    continue
                

                if not os.path.exists(generated_path):
                    report.write("  [!] STATUS: Skipped - No Generated Spec (llm_definitions.py) found.\n\n")
                    continue

                try:
                    vetted_mod = load_module_from_path(f"vetted_{benchmark}", vetted_path)
                    gen_mod = load_module_from_path(f"gen_{benchmark}", generated_path)
                    

                    funcs = [f for f in dir(vetted_mod) if inspect.isfunction(getattr(vetted_mod, f))]
                    funcs_processed = 0
                    
                    for func_name in funcs:

                        if func_name.startswith('_') or hasattr(z3, func_name) or func_name.startswith("inv"):
                            continue
                            
                        vetted_func = getattr(vetted_mod, func_name)
                        gen_func = getattr(gen_mod, func_name, None)
                        
                        if not gen_func:
                            report.write(f"  ? Function '{func_name}': Missing in generated specs.\n")
                            continue
                            
                        funcs_processed += 1
                        
                        # 1. Inspect arguments to create Z3 variables dynamically
                        args = inspect.getfullargspec(vetted_func).args
                        z3_vars = {arg: z3.Int(arg) for arg in args}
                        
                        # 2. Evaluate functions to get Z3 Boolean Expressions
                        v_expr = vetted_func(**z3_vars)
                        g_expr = gen_func(**z3_vars)
                        
                        # 3. Prove Implications
                        v_implies_g = check_implication(v_expr, g_expr)
                        g_implies_v = check_implication(g_expr, v_expr)
                        
                        # 4. Determine Status
                        if v_implies_g and g_implies_v:
                            status = "LOGICALLY EQUIVALENT (V <=> G)"
                        elif v_implies_g:
                            status = "SUBSUMED (V => G) [Generated is correct but weaker]"
                        elif g_implies_v:
                            status = "STRICTER (G => V) [Generated is stronger]"
                        else:
                            status = "NOT IMPLYING (Requires manual inspection)"
                            
                        report.write(f"  -> {func_name}: {status}\n")
                    
                    if funcs_processed == 0:
                        report.write("  [!] No valid Z3 functions found to compare.\n")
                        
                except Exception as e:
                    report.write(f"  [!] Error processing functions: {e}\n")
                
                report.write("\n")

    print(f"\n[!] Implication checks complete. Report saved to: {REPORT_PATH}")

if __name__ == "__main__":
    run_implication_checks()