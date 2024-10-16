import os

def adjust_gcode_file(filename, replacement_letter):
    # Ensure the replacement letter is valid
    if replacement_letter not in ['A', 'B', 'C', 'D']:
        raise ValueError("Replacement letter must be one of 'A', 'B', 'C', 'D'")

    # Get the script's directory and construct the file path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)

    with open(file_path, 'r') as file:
        lines = file.readlines()

    adjusted_lines = ["G75\n"]  # Start with G75
    process1_encountered = False  # Ensure this variable is defined at the beginning
    build_summary_encountered = False

    for line in lines:
        if not process1_encountered:
            if "; process Process1" in line:
                process1_encountered = True
            else:
                continue  # Skip all lines until "; process Process1" is encountered

        # Stop processing lines starting with ";" after "Build Summary"
        if line.startswith(";") and build_summary_encountered:
            continue
        if "Build Summary" in line:
            build_summary_encountered = True
            continue

        # Skip specific commands
        if any(cmd in line for cmd in ["M3", "M4", "M5", "M6", "T0", "T1", "T2", "T3", "M106"]):
            continue

        # Delete parts of the line containing "E" and ensure newline
        parts = line.split(" ")
        parts = [part for part in parts if not part.startswith("E")]
        line = " ".join(parts)
        if not line.endswith("\n"):
            line += "\n"

        # Replace "Z" with the specified letter and add "G91" before and "G90" after the line if needed
        if "G1 Z" in line:
            line = line.replace("Z", replacement_letter)
            adjusted_lines.append("G91\n")
            adjusted_lines.append(line)
            adjusted_lines.append("G90\n")
            continue

        if "Z =" in line:
            line = line.replace("Z", replacement_letter)
            continue

        adjusted_lines.append(line)

    # Add global commands
    adjusted_lines.insert(1, "$iglobal[0] = 1\n")  # Insert after G75
    adjusted_lines.append("$iglobal[0] = 0\n")

    # Writing to a new file
    revised_file_path = file_path.replace(".gcode", "_revised.gcode")
    with open(revised_file_path, 'w') as file:
        file.writelines(adjusted_lines)

    print(f"File adjusted and saved to: {revised_file_path}")

# Example usage
adjust_gcode_file('cole_nagata_test.gcode', 'C')
