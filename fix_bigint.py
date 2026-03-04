import os
import re

model_dir = "app/model/wordpress"

pattern = re.compile(r'sa_type=BIGINT\(([^)]*),\s*sa_column_kwargs=\{"autoincrement": True\}\)')

for filename in os.listdir(model_dir):
    if not filename.endswith(".py"):
        continue
    filepath = os.path.join(model_dir, filename)
    with open(filepath, "r") as f:
        content = f.read()

    new_content = pattern.sub(r'sa_type=BIGINT(\1), sa_column_kwargs={"autoincrement": True}', content)

    if new_content != content:
        with open(filepath, "w") as f:
            f.write(new_content)
        print(f"Fixed {filename}")
