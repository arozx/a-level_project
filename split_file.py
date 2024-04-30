def split_file(file_name, parts):
    with open(file_name, "r") as file:
        lines = file.readlines()

    total_lines = len(lines)
    lines_per_file = total_lines // parts

    for i in range(parts):
        start = i * lines_per_file
        end = (i + 1) * lines_per_file if i < parts - 1 else None
        with open(f"{file_name}_part{i+1}", "w") as file:
            file.writelines(lines[start:end])
