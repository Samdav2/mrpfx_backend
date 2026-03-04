import os
import re

model_dir = "app/model/wordpress"

# Regex to find: something = Field(..., primary_key=True, ...)
# We want to add sa_column_kwargs={"autoincrement": True} if not already present
for filename in os.listdir(model_dir):
    if not filename.endswith(".py"):
        continue
    filepath = os.path.join(model_dir, filename)
    with open(filepath, "r") as f:
        content = f.read()

    # We look for lines containing `primary_key=True`
    new_lines = []
    for line in content.split("\n"):
        if "primary_key=True" in line and "Field(" in line:
            if "sa_column_kwargs" not in line:
                # Add it before the closing parenthesis of Field(...)
                # This could be tricky if it's multi-line, but let's assume single line
                line = re.sub(r'(Field\([^)]+)(?=\))', r'\1, sa_column_kwargs={"autoincrement": True}', line)
        new_lines.append(line)

    new_content = "\n".join(new_lines)
    if new_content != content:
        with open(filepath, "w") as f:
            f.write(new_content)
        print(f"Updated {filename}")
