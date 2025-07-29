import os
import yaml
import csv

INPUT_DIR ="fleet/schema/tables"
OUTPUT_DIR = "schema"
OUTPUT_CSV = os.path.join(OUTPUT_DIR, "fleet_osquery_schema.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(OUTPUT_CSV, "w", newline="") as out_csv:
    writer = csv.writer(out_csv)
    writer.writerow(["table_name", "column_name", "datatype", "description"])

    for fname in os.listdir(INPUT_DIR):
        if not fname.endswith(".yaml"):
            continue
        with open(os.path.join(INPUT_DIR, fname), "r") as f:
            try:
                table = yaml.safe_load(f)
            except Exception as e:
                print(f"Failed to parse {fname}: {e}")
                continue
            table_name = table.get("name", os.path.splitext(fname)[0])
            for col in table.get("columns", []):
                writer.writerow([
                    table_name,
                    col.get("name", ""),
                    col.get("type", ""),
                    (col.get("description") or "").replace("\n", " ")
                ])
