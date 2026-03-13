import os
import re
import google.generativeai as genai
import subprocess
import sys
from dotenv import load_dotenv
import importlib
from z3 import *
import json
import shutil


script_location = os.path.dirname(os.path.abspath(__file__))

PROJECT_ROOT = os.path.dirname(script_location)

BENCHMARKS_DIR = os.path.join(PROJECT_ROOT, "benchmarks", "Classical")
SCRIPTS_DIR = os.path.join(PROJECT_ROOT, "scripts")
TEMPLATES_DIR = os.path.join(SCRIPTS_DIR, "templates")

LOGS_DIR = os.path.join(PROJECT_ROOT, "logs", "ClassicalLLM")

print(f"Project Root Detected: {PROJECT_ROOT}")
print(f"Benchmarks Directory: {BENCHMARKS_DIR}")

def read_file_content(filepath):
    """
    Reads the content of a file and returns it as a string.
    Handles potential FileNotFoundError and prints an error message.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred while reading '{filepath}': {e}")
        return None

def create_prompt_from_template(template_path, abst_path, chc_path, specs_path):
    """
    Generates a complete LLM prompt by substituting content from benchmark files
    into a main template file.
    """

    template_content = read_file_content(template_path)
    if template_content is None:
        return None

    abst_content = read_file_content(abst_path)
    chc_content = read_file_content(chc_path)
    specs_content = read_file_content(specs_path)

    if any(content is None for content in [abst_content, chc_content, specs_content]):
        print("\nAborting prompt creation due to one or more missing content files.")
        return None

    prompt = template_content.replace("[abstract]", abst_content)
    prompt = prompt.replace("[CHC]", chc_content)
    prompt = prompt.replace("[signatures]", specs_content)

    return prompt

def get_gemini_definitions(prompt_data, model_name="gemini-2.5-flash"):
    """
    Calls the Google Gemini API, correctly handling both single prompts and 
    translating OpenAI-style chat histories into the required Gemini format.
    """
    print(f"\n>>> Contacting Google Gemini API with model: {model_name}...")
    try:
        model = genai.GenerativeModel(model_name)

        
        if isinstance(prompt_data, list):
            # CASE 1: Input is a chat history (from refinement_loop)
            print("--- Detected chat history. Translating to Gemini format and using conversational mode. ---")
            

            gemini_history = []
            for message in prompt_data:
                gemini_history.append({
                    'role': message['role'],
                    'parts': [message['content']]
                })


            history_for_session = gemini_history[:-1]

            new_message = gemini_history[-1]['parts']
            
            chat = model.start_chat(history=history_for_session)
            response = chat.send_message(new_message)
            
        elif isinstance(prompt_data, str):

            print("--- Detected single prompt. Using direct generation mode. ---")
            response = model.generate_content(prompt_data)
            
        else:

            raise TypeError("prompt_data must be a list of chat messages or a single string.")


        if response.parts:
            text_content = "".join(part.text for part in response.parts)
        else:
            print("Warning: LLM response was empty or blocked.")
            if response.prompt_feedback:
                print(f"Prompt Feedback: {response.prompt_feedback}")
            return None


        text_content = re.sub(r'^```python\n', '', text_content.strip())
        text_content = re.sub(r'\n```$', '', text_content.strip())
        
        print("<<< Response received successfully from Gemini.")
        return text_content.strip()

    except Exception as e:
        print(f"An error occurred during the Gemini API call: {e}")
        return None


def get_llm_response(prompt_text, model_name):
    """
    Dispatches the request to the correct LLM provider based on the model name.
    """
    if model_name.startswith('gemini'):
        return get_gemini_definitions(prompt_text, model_name)
    else:
        print(f"FATAL ERROR: Unsupported model provider for model '{model_name}'.")
        print("Supported prefixes are 'gemini-'")
        return None
    


API_KEY = os.environ.get("API_KEY")

def get_llm_definitions(prompt_text, model_name="gemini-2.0-flash"):
    """Calls the Gemini API and returns the generated Z3Py code."""
    print(f"\n>>> Contacting Gemini API with model: {model_name}...")
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt_text)
        
        # Extract the text content from the response object
        if response.parts:
            text_content = "".join(part.text for part in response.parts)
        else:
            print("Warning: LLM response was empty or blocked.")
            if response.prompt_feedback:
                print(f"Prompt Feedback: {response.prompt_feedback}")
            return None

        # Clean markdown fences (like ```python ... ```) if the LLM adds them
        text_content = re.sub(r'^```python\n', '', text_content.strip())
        text_content = re.sub(r'\n```$', '', text_content.strip())
        
        print("<<< Response received successfully.")
        return text_content.strip()

    except Exception as e:
        print(f"An error occurred during the Gemini API call: {e}")
        return None
    




def execute_validity_checker(checker_script_name="validity_checker.py"):
    """
    Executes a specified Python script using a subprocess and captures its output.

    Args:
        checker_script_name (str): The name of the validity checker script to run.

    Returns:
        tuple: A tuple containing (full_output_string, success_boolean).
    """
    print(f"--- Executing '{checker_script_name}' ---")

    # Ensure the script to be run exists
    if not os.path.exists(checker_script_name):
        error_message = f"Error: The checker script '{checker_script_name}' was not found in this directory."
        print(error_message)
        return error_message, False

    try:
        python_executable = sys.executable

        process = subprocess.run(
            [python_executable, checker_script_name],
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
            encoding='utf-8',
            errors='ignore' 
        )


        full_output = process.stdout
        if process.stderr:
            full_output += "\n--- Errors ---\n" + process.stderr

        # Determine success by checking the output for specific failure keywords.
        is_success = False
        if "qwertyasdfg" in process.stdout:
            is_success = True

        return full_output, is_success

    except FileNotFoundError:
        # This handles the case where 'python3' command is not found.
        error_message = "Error: 'python3' command not found. Please ensure Python 3 is installed and in your PATH, or change the command in this script to 'python'."
        print(error_message)
        return error_message, False
    except subprocess.TimeoutExpired:
        error_message = f"Error: '{checker_script_name}' timed out after 60 seconds."
        print(error_message)
        return error_message, False
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        print(error_message)
        return error_message, False
    

def run_single_fuzz_test(benchmark_name, spec_to_test, spec_to_inject, mode):
    """
    Executes a single AFL++ test locally using subprocess.
    Determines success/failure by checking the local counterexample file.
    """
    # 1. Define the path to the fuzzer script (since it's in the same SCRIPTS_DIR)
    fuzzer_script_path = os.path.join(SCRIPTS_DIR, "run_single_fuzzer.py")
    
    print(f"\n--- Executing local run_single_fuzzer.py for '{spec_to_test}' ---")
    
    # 2. Execute the script using a list of arguments (safer than a raw string)
    try:
        # sys.executable ensures it uses the exact same Python environment (your venv!)
        cmd = [
            sys.executable, 
            fuzzer_script_path, 
            benchmark_name, 
            spec_to_test, 
            spec_to_inject, 
            mode
        ]
        
        process = subprocess.run(cmd, capture_output=True, text=True, check=False)
        
        print("\n--- Fuzzer Output (stdout) ---")
        if process.stdout:
            for line in process.stdout.splitlines():
                print(f"    [FUZZER] {line}")
                
        if process.stderr:
            print("\n--- Fuzzer Errors (stderr) ---")
            for line in process.stderr.splitlines():
                print(f"    [ERROR] {line}")

        # 3. Analyze Results by checking the local CE file
        print("\n--- Analyzing execution results by checking CE file ---")
        
        # NOTE: Mak e sure this path correctly points to where the fuzzer outputs the CE!
        # Assuming working_temp is generated inside your BENCHMARKS_DIR
        ce_path = os.path.join(BENCHMARKS_DIR, "working_temp", benchmark_name, f"{spec_to_test}CE.txt")   
        try:
            with open(ce_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # A real failure has more than 1 line (header + data).
            if len(lines) > 0:
                print(f"❌ TEST FAILED: Counterexample data found in '{os.path.basename(ce_path)}'.")
                return "".join(lines).strip() # Return the counterexample data
            else:
                print(f"✅ TEST PASSED: No counterexample data found in '{os.path.basename(ce_path)}'.")
                return None # Return None for success
                
        except FileNotFoundError:
            # If the CE file doesn't even exist, it's a definite pass.
            print(f"✅ TEST PASSED: No counterexample file was created.")
            return None # Return None for success

    except Exception as e:
        print(f"\nAn error occurred during the remote pipeline: {e}")
        return f"An exception occurred: {e}"




def translate_z3_to_cpp(z3_function_code, model_to_use, spec_name, benchmark_name, varpath ="varmap.txt" ): # <-- Add benchmark_name
    """
    Uses a new, clean, and highly specific LLM prompt to translate a single Z3
    function into a C++ infix expression, correctly mapping variable names based on a config file.
    """
    print(f"--- Translating function '{spec_name}' to C++ ---")


    variable_mapping_instructions = ""
    varmap_path = os.path.join(BENCHMARKS_DIR, benchmark_name, varpath)
    try:
        with open(varmap_path, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    parts = line.strip().split()
                    if len(parts) == 3 and parts[0] == spec_name:
                        py_param, cpp_var = parts[1], parts[2]
                        variable_mapping_instructions += f"- The Python parameter `{py_param}` corresponds to the C++ local variable `{cpp_var}`.\n"
    except FileNotFoundError:
        variable_mapping_instructions = "use the same variable names as in the Python code."

    if not variable_mapping_instructions:
         variable_mapping_instructions = "No special variable remapping is required. Use Python parameter names directly."

    translation_prompt = f"""You are an expert code translator. Your task is to convert the following Python Z3 function into a single-line C++ boolean expression.

                             **Crucial Variable Mapping Instructions:**
                             {variable_mapping_instructions}

                             **Translation Rules:**
                             - Map `And(a, b)` to `(a && b)`.
                             - Map `Or(a, b)` to `(a || b)`.
                             - Map `Not(a)` to `!a`.
                             - Map `Implies(a, b)` to `(!a || b)`.
                             - Map `If(cond, a, b)` to `(cond ? a : b)`.
                             - Use `==` for equality checks.
                             - Use `false` for the boolean literal false.
                             - Ensure the final output is ONLY the single-line C++ expression string, with no extra text, explanations, or code formatting.
                             - IMPORTANT: Do not wrap the expression in `cpp(...)`, backticks, or any other function call or formatting.

                             **Python Z3 function to translate:**
                             ```python
                             {z3_function_code}
                             ```
                             """
    cpp_expression = get_llm_response(translation_prompt, model_to_use)
    if cpp_expression:
        cpp_expression = cpp_expression.strip().replace("`", "")
        print(f"     Translation result: {cpp_expression}")
        return cpp_expression
    else:
        print("     ERROR: LLM returned no translation.")
        return "(false)"
    



PIPELINE_MODE = "ClassicalLLMHornICEFUZZ"

def run_translation_and_testing_pipeline(final_z3_code, original_chat_history, model_to_use, benchmark_name):
    """
    Orchestrates Phase 2 and 3: Translates Z3, runs tests, and now correctly
    reads and returns the actual counterexample data from the output files.
    """
    print("\n\n" + "="*20 + " PHASE 2: Translation & Testing " + "="*20)


    function_definitions = ["def " + f for f in final_z3_code.split("def ")[1:]]
    if not function_definitions:
        return "ERROR: Could not parse Z3 functions."


    specs_for_testing = []
    rewritten_specs_content = []
    SPECS_TO_SKIP_TRANSLATION = ("inv", "valid", "fail")
    for func_def in function_definitions:
        spec_name = func_def.split('(')[0][4:].strip()

        if spec_name.startswith(SPECS_TO_SKIP_TRANSLATION):
            continue 
        cpp_rule = translate_z3_to_cpp(func_def, MODEL_FOR_TRANSLATION, spec_name, benchmark_name)
        specs_for_testing.append((spec_name, cpp_rule))
        rewritten_specs_content.append(f"{spec_name}\n(placeholder for declaration)\n{cpp_rule}\n")


    rewritten_specs_path = os.path.join(BENCHMARKS_DIR, benchmark_name, "RewrittenSpecs.txt")
    with open(rewritten_specs_path, 'w') as f:
        f.write("\n".join(rewritten_specs_content))
    print(f"--- Wrote C++ specs to '{rewritten_specs_path}' ---")

    all_counterexamples = []
    any_failures = False
    
    for spec_name, spec_rule in specs_for_testing:
        
        counterexample_result = run_single_fuzz_test(
            benchmark_name, 
            spec_name, 
            spec_rule, 
            PIPELINE_MODE 
        )
        
        if counterexample_result:
            any_failures = True
            all_counterexamples.append(f"### Counterexample for: {spec_name} ###\n{counterexample_result}")


    if any_failures:
        print("\n--- Fuzzing complete. Consolidating all counterexample reports. ---")

        return "\n\n".join(all_counterexamples)
    else:
        print("\n--- Fuzzing complete. No counterexamples were found for any spec. ---")
        return None 


def save_definitions_file(code_content, output_filepath):
    """Saves the provided code content to the specified file."""
    print(f"--- Saving new definitions to '{output_filepath}' ---")
    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
    with open(output_filepath, 'w', encoding='utf-8') as f_out:
        f_out.write("# This file is auto-generated. Do not edit directly.\n\n")
        f_out.write("from z3 import *\n")
        f_out.write("# --- LLM Generated Definitions ---\n")
        f_out.write(code_content)
    print("Save complete.")


def get_all_benchmarks(benchmarks_dir_path):
    """
    Scans the benchmarks directory and returns a list of all subdirectories.
    Filters out non-directory files and common hidden folders.
    """
    print(f"\n--- Scanning for benchmarks in '{benchmarks_dir_path}' ---")
    try:
        all_entries = os.listdir(benchmarks_dir_path)
        benchmark_folders = [
            entry for entry in all_entries
            if os.path.isdir(os.path.join(benchmarks_dir_path, entry))
            and not entry.startswith('.') 
            and not entry.startswith('__') 
        ]
        print(f"Found {len(benchmark_folders)} benchmarks: {benchmark_folders}")
        return benchmark_folders
    except FileNotFoundError:
        print(f"FATAL ERROR: Benchmarks directory not found at '{benchmarks_dir_path}'")
        return []
    

def z3_refinement_cycle(conversation_history, model_to_use, benchmark_name):
    """
    Performs one cycle of Z3 spec generation and validation.
    Returns the valid Z3 code on success, or None on failure.
    """
    MAX_ATTEMPTS = 6 # Inner loop attempts
    for attempt in range(1, MAX_ATTEMPTS + 1):

        print(f"\n--- Z3 Refinement Attempt {attempt}/{MAX_ATTEMPTS} ---")


        # import json
        # print("\n" + "-"*20 + " CONVERSATION HISTORY (SENT TO LLM) " + "-"*20)

        # print(json.dumps(conversation_history, indent=2))
        # print("-" * 65 + "\n")


        llm_code = get_llm_response(conversation_history, model_to_use)
        if not llm_code: continue
        conversation_history.append({'role': 'model', 'content': llm_code})
        save_definitions_file(llm_code, os.path.join(BENCHMARKS_DIR, benchmark_name, "llm_definitions.py"))
        checker_output, is_success = execute_validity_checker(os.path.join(BENCHMARKS_DIR, benchmark_name, "validity_check_gen_ds.py"))
        if is_success:
            print("✅ Z3 Definitions passed validity check.")
            return llm_code
        else:
            print("❌ Z3 spec is not valid. Preparing feedback.")
            feedback = f"""The previous Z3 code was invalid. The validator failed with this output:

        {checker_output}
        Your task is to fix the code based on the validator's output.
        Respond with ONLY the complete, corrected, and runnable Python code for all functions.
        Do not include any explanations, apologies, introductory text, or markdown formatting like ```python.
        Your entire response must be valid Python code."""
            
            conversation_history.append({'role': 'user', 'content': feedback})
    return None

def save_final_logs(benchmark_name, conversation_history):
    """
    Saves the final conversation history and the generated C++ specs 
    to a dedicated logs folder for this benchmark.
    """
    # Create the specific log folder: logs/ClassicalLLM/benchmark_name
    target_dir = os.path.join(LOGS_DIR, benchmark_name)
    os.makedirs(target_dir, exist_ok=True)

    # 1. Save the conversation history as a formatted JSON file
    chat_file_path = os.path.join(target_dir, "conversation_history.json")
    try:
        with open(chat_file_path, 'w', encoding='utf-8') as f:
            json.dump(conversation_history, f, indent=4)
    except Exception as e:
        print(f"Error saving conversation history: {e}")

    # 2. Copy the final C++ specs from the benchmark folder
    # We grab RewrittenSpecs.txt which was generated in Phase 2
    source_specs_path = os.path.join(BENCHMARKS_DIR, benchmark_name, "RewrittenSpecs.txt")
    target_specs_path = os.path.join(target_dir, "final_cpp_specs.txt")
    
    try:
        if os.path.exists(source_specs_path):
            shutil.copy(source_specs_path, target_specs_path)
            print(f"\n Saved final conversation and C++ specs to: {target_dir}")
        else:
            print(f"\n Saved final conversation to: {target_dir} (No C++ specs were generated to save)")
    except Exception as e:
         print(f"Error saving C++ specs: {e}")

def run_complete_pipeline(model_to_use, benchmark_name):
    """The main 'grand loop' that orchestrates the entire pipeline."""
    # --- Initial Setup ---
    initial_prompt = create_prompt_from_template(
        os.path.join(TEMPLATES_DIR, 'Template.txt'), 
        os.path.join(BENCHMARKS_DIR, benchmark_name, 'Abstract.txt'), 
        os.path.join(BENCHMARKS_DIR, benchmark_name, 'CHC.smt2'), 
        os.path.join(BENCHMARKS_DIR, benchmark_name, 'Signature.txt')
    )
    if not initial_prompt: return
    
    conversation_history = [{'role': 'user', 'content': initial_prompt}]
    
    MAX_PIPELINE_ITERATIONS = 15
    for i in range(1, MAX_PIPELINE_ITERATIONS + 1):
        print("\n\n" + "="*25 + f" PIPELINE ITERATION {i} " + "="*25)
        
        # Phase 1: Get a valid Z3 spec
        valid_z3_code = z3_refinement_cycle(conversation_history, model_to_use, benchmark_name)
        if not valid_z3_code:
            print("\n❌ PIPELINE FAILED: Could not produce a valid Z3 spec.")
            break

        # Phase 2: Translate and Test
        
        counterexample_report = run_translation_and_testing_pipeline(valid_z3_code, conversation_history, model_to_use, benchmark_name)

        if not counterexample_report:
            print("\n\n✅✅✅ PIPELINE COMPLETE: Specs passed all tests! ✅✅✅")
            save_final_logs(benchmark_name, conversation_history)
            break
        

        # Phase 3: Feed counterexample back into the main chat history
        print("\n--- Testing found a flaw. Feeding counterexample back to Z3 refinement loop. ---")


        # Use regex to find ALL functions that have a counterexample report
        failed_functions = re.findall(r"### Counterexample for: (.*?) ###", counterexample_report)
        failed_functions = sorted(list(set(failed_functions)))





        
        
        feedback_prompt = f"""The previous Z3 specification was valid but failed testing.
**Test Summary:**
- Function that FAILED: {failed_functions}

**Failure Details:**
{counterexample_report}

**IMPORTANT:** You must provide the complete and corrected code for ALL functions, including the ones that passed. Do not omit any functions from your response.
You are also allowed to make changes to the invariants and PASSED functions (if needed) to satisfy the validity checks after correcting the FAILED functions.

Your task is to analyze the counterexample and provide a new, corrected version of the Z3 code to fix the logical flaw.
Respond with ONLY the complete, corrected, and runnable Python code for all functions.
Do not include any explanations, introductory text, or markdown formatting like ```python.
Your entire response must be valid Python code.


"""
        conversation_history.append({'role': 'user', 'content': feedback_prompt})

    else:
        print(f"\n❌ PIPELINE FAILED: Reached max iterations without a fully passing spec.")
        save_final_logs(benchmark_name, conversation_history)



import time
if __name__ == "__main__":
    # --- Environment and API Setup ---
    load_dotenv()
    gemini_api_key = os.environ.get("API_KEY")
    if gemini_api_key:
        genai.configure(api_key=gemini_api_key)

    
    # --- Model Selection ---
    MODEL_TO_USE = "gemini-2.5-pro"  
    MODEL_FOR_TRANSLATION = "gemini-2.5-flash"


    all_benchmarks_to_run = [
                             "AtomicHashMap1"]

    if not all_benchmarks_to_run:
        print("No benchmarks found to run. Exiting.")
    else:

        for i, benchmark_name in enumerate(all_benchmarks_to_run):
            print("\n\n" + "#" * 70)
            print(f"# STARTING BENCHMARK {i+1}/{len(all_benchmarks_to_run)}: {benchmark_name}")
            print("#" * 70 + "\n")
            start = time.time()

            try:

                run_complete_pipeline(MODEL_TO_USE, benchmark_name)

                print("\n" + "#" * 70)
                print(f"# SUCCESSFULLY COMPLETED BENCHMARK: {benchmark_name}")
                print("#" * 70 + "\n")
                end = time.time()
                elapsed_time = end - start
                print(f"Elapsed time for {benchmark_name}: {elapsed_time:.2f} seconds")

            except Exception as e:

                print("\n" + "!" * 70)
                print(f"! An unexpected error occurred while running benchmark: {benchmark_name}")
                print(f"! ERROR: {e}")

                print("! Moving to the next benchmark...")
                print("!" * 70 + "\n")

        print("\n\n" + "*" * 70)
        print("All benchmarks have been processed.")
        print("*" * 70)