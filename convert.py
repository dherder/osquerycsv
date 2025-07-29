import os
import yaml
import csv

INPUT_DIR = "fleet/schema/tables"
OUTPUT_DIR = "schema"
OUTPUT_CSV = os.path.join(OUTPUT_DIR, "fleet_osquery_schema.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"🔍 Reading osquery schema files from: {INPUT_DIR}")

if not os.path.isdir(INPUT_DIR):
    print(f"❌ ERROR: Directory '{INPUT_DIR}' does not exist.")
    exit(1)

yaml_files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".yml")]
print(f"📄 Found {len(yaml_files)} YAML files.")

if not yaml_files:
    print("⚠️  No YAML files found. Exiting.")
    exit(0)

rows_written = 0

with open(OUTPUT_CSV, "w", newline="") as out_csv:
    writer = csv.writer(out_csv)
    writer.writerow(["table_name", "column_name", "datatype", "description"])

    for fname in yaml_files:
        path = os.path.join(INPUT_DIR, fname)
        try:
            with open(path, "r") as f:
                table = yaml.safe_load(f)
        except Exception as e:
            print(f"❌ Failed to parse {fname}: {e}")
            continue

        table_name = table.get("name", os.path.splitext(fname)[0])
        columns = table.get("columns", [])

        if not columns:
            print(f"⚠️  Skipping table '{table_name}' — no columns defined.")
            continue

        for col in columns:
            writer.writerow([
                table_name,
                col.get("name", ""),
                col.get("type", ""),
                (col.get("description") or "").replace("\n", " ")
            ])
            rows_written += 1

print(f"✅ Done! Wrote {rows_written} rows to {OUTPUT_CSV}")