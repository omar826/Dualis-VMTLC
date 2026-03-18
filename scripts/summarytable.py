import os
import re
from collections import defaultdict

def generate_status_matrix(input_file):
    if not os.path.exists(input_file):
        print(f"Error: Could not find {input_file}")
        return None

    # results[benchmark][mode] = status
    results = defaultdict(dict)
    unique_modes = set()
    benchmarks_ordered = []
    
    # stats[mode][status] = count
    stats = defaultdict(lambda: {"PASS": 0, "FAIL": 0})

    current_mode = None
    current_bench = None

    # Regex for: [TASK] Mode: ... | Benchmark: ...
    task_pattern = re.compile(r"^\[TASK\]\s*Mode:\s*(?P<mode>.*?)\s*\|\s*Benchmark:\s*(?P<bench>.*?)\s*$")
    # Regex for: STATUS: PASS or STATUS: FAIL (...)
    status_pattern = re.compile(r"^STATUS:\s*(?P<status>\w+)")

    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            
            # 1. Match Task Header
            task_match = task_pattern.match(line)
            if task_match:
                current_mode = task_match.group("mode")
                current_bench = task_match.group("bench")
                unique_modes.add(current_mode)
                if current_bench not in benchmarks_ordered:
                    benchmarks_ordered.append(current_bench)
                continue

            # 2. Match Status Result
            status_match = status_pattern.match(line)
            if status_match and current_mode and current_bench:
                status = status_match.group("status").upper()
                results[current_bench][current_mode] = status
                
                if status in ["PASS", "FAIL"]:
                    stats[current_mode][status] += 1
                
                # Reset until next [TASK]
                current_mode = None
                current_bench = None

    if not unique_modes:
        print("No valid tasks found in the file.")
        return None

    sorted_modes = sorted(list(unique_modes))
    
    # Determine widths
    b_col_width = max(len(b) for b in benchmarks_ordered) + 2 if benchmarks_ordered else 20
    m_col_width = max(max(len(m) for m in sorted_modes), 15) + 2

    # Formatting
    total_line_width = b_col_width + 3 + (len(sorted_modes) * (m_col_width + 3))
    double_sep = "=" * total_line_width
    single_sep = "-" * total_line_width

    output = []
    output.append(double_sep)
    header = f"{'Benchmark'.ljust(b_col_width)} | " + " | ".join(m.center(m_width) for m, m_width in zip(sorted_modes, [m_col_width]*len(sorted_modes)))
    output.append(header)
    output.append(double_sep)

    # Data Rows
    for bench in benchmarks_ordered:
        row = f"{bench.ljust(b_col_width)} | "
        cells = []
        for mode in sorted_modes:
            status = results[bench].get(mode, "N/A")
            cells.append(status.center(m_col_width))
        row += " | ".join(cells)
        output.append(row)

    output.append(single_sep)

    # Totals
    pass_row = f"{'TOTAL PASS'.ljust(b_col_width)} | " + " | ".join(str(stats[m]["PASS"]).center(m_col_width) for m in sorted_modes)
    fail_row = f"{'TOTAL FAIL'.ljust(b_col_width)} | " + " | ".join(str(stats[m]["FAIL"]).center(m_col_width) for m in sorted_modes)
    
    output.append(pass_row)
    output.append(fail_row)
    output.append(double_sep)

    return "\n".join(output)

if __name__ == "__main__":
    # Path logic to find file in the same directory as script
    base_path = os.path.dirname(os.path.abspath(__file__))
    input_filename = os.path.join(base_path, "evaluation_summary.txt")
    output_filename = os.path.join(base_path, "status_matrix.txt")

    result_table = generate_status_matrix(input_filename)
    
    if result_table:
        print(result_table)
        with open(output_filename, "w") as f:
            f.write(result_table)
        print(f"\n[!] Success: Matrix saved to {output_filename}")
