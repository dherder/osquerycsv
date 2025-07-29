import os
import csv
import yaml

INPUT_DIR = "osquery/specs"
OUTPUT_DIR = "schema"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "osquery_schema.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(OUTPUT_FILE, mode="w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["table_name", "column_name", "type", "description"])

    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".table"):
            filepath = os.path.join(INPUT_DIR, filename)
            with open(filepath, "r") as f:
                table = yaml.safe_load(f)

            table_name = table.get("name", os.path.splitext(filename)[0])
            for column in table.get("columns", []):
                writer.writerow([
                    table_name,
                    column.get("name", ""),
                    column.get("type", ""),
                    column.get("description", "").replace("\n", " ")
                ])

print(f"Exported to {OUTPUT_FILE}")