"""
Reshape a single-row CSV of names into a single-column CSV.

Input: 'names.csv' with names in one row
Output: 'names_reshaped.csv' with each name in its own row
"""

import csv

# Input and output file paths
input_file = "../customer_data/names.csv"
output_file = "../customer_data/names_reshaped.csv"

# Read names from the single-row CSV
with open(input_file, "r", newline="") as f:
    reader = csv.reader(f)
    row = next(reader)  # Read the first (and only) row

# Write names into a single-column CSV
with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)
    for name in row:
        writer.writerow([name])

print(f"Reshaped {len(row)} names from {input_file} into {output_file}")
