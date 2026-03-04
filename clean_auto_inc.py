import os

model_dir = "app/model/wordpress"

def process_file(filepath):
    with open(filepath, "r") as f:
        content = f.read()

    new_lines = []
    changed = False
    for line in content.split("\n"):
        original_line = line

        # 1. Strip out ALL existing sa_column_kwargs completely
        line = line.replace(', sa_column_kwargs={"autoincrement": True}', '')
        line = line.replace(' sa_column_kwargs={"autoincrement": True}', '')

        # 2. Add it back safely ONLY to INT fields
        if "primary_key=True" in line and ("int =" in line or "Optional[int] =" in line or "ID: Optional[int]" in line) and "Field(" in line:
            # Safely replace primary_key=True with the kwargs added
            if 'sa_column_kwargs={"autoincrement": True}' not in line:
                line = line.replace("primary_key=True", 'primary_key=True, sa_column_kwargs={"autoincrement": True}')

        new_lines.append(line)
        if line != original_line:
            changed = True

    if changed:
        with open(filepath, "w") as f:
            f.write("\n".join(new_lines))
        print(f"Cleaned {os.path.basename(filepath)}")

for filename in os.listdir(model_dir):
    if filename.endswith(".py"):
        process_file(os.path.join(model_dir, filename))
