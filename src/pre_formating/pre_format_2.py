"""
Merged Pre-Formatter Module

This script processes, cleans, and formats address data by:
1. Removing duplicates and redundant information.
2. Adjusting `address_1` and `address_2` to comply with length constraints.
3. Cleaning up spaces around punctuation.
4. Converting necessary fields to PascalCase.

The final processed data is saved to `data/pre_formated.csv`.
"""

import re
import pandas as pd

# Read the DataFrame from a CSV file
df = pd.read_csv("data/pre_formated.csv")
print("Original DataFrame:")
print(df)

# Lowercase all column names
df.columns = df.columns.str.lower()

# Ensure all entries in the selected columns are strings
columns_to_convert = ["address_1", "address_2"]
df[columns_to_convert] = df[columns_to_convert].astype(str)

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    address_1 = row["address_1"]
    address_2 = row["address_2"]

    # Check if the conditions are met
    if len(address_1) > 35 and len(address_2) <= 10:
        # Remove spaces before and after commas, dots, and hyphens
        address_1 = re.sub(r"\s*,\s*", ",", address_1)
        address_1 = re.sub(r"\s*\.\s*", ".", address_1)
        address_1 = re.sub(r"\s*-\s*", "-", address_1)

        # Update the DataFrame
        df.at[index, "address_1"] = address_1.strip()

    elif len(address_1) <= 35 and len(address_2) > 10:
        address_2 = re.sub(r"\s*,\s*", ",", address_2)
        address_2 = re.sub(r"\s*\.\s*", ".", address_2)
        address_2 = re.sub(r"\s*-\s*", "-", address_2)

        # Update the DataFrame
        df.at[index, "address_2"] = address_2.strip()
    elif len(address_1) > 35 and len(address_2) > 10:
        # Remove spaces before and after commas, dots, and hyphens
        new_address_1 = re.sub(r"\s*,\s*", ",", address_1)
        new_address_1 = re.sub(r"\s*\.\s*", ".", new_address_1)
        new_address_1 = re.sub(r"\s*-\s*", "-", new_address_1)

        new_address_2 = re.sub(r"\s*,\s*", ",", address_2)
        new_address_2 = re.sub(r"\s*\.\s*", ".", new_address_2)
        new_address_2 = re.sub(r"\s*-\s*", "-", new_address_2)

        # Check if the lengths are within the limits after removing spaces
        if len(new_address_1) <= 35 and len(new_address_2) <= 10:
            # Update the DataFrame with the new values
            df.at[index, "address_1"] = new_address_1.strip()
            df.at[index, "address_2"] = new_address_2.strip()
        else:
            # Revert to the original values
            df.at[index, "address_1"] = address_1.strip()
            df.at[index, "address_2"] = address_2.strip()

print("\nAdjusted DataFrame:")
print(df[["address_1", "address_2"]])

# Save the adjusted DataFrame to a CSV file
OUTPUT_FILE = "data/pre_formated.csv"
df.to_csv(OUTPUT_FILE, index=False)

print(f"\nAdjusted DataFrame saved to {OUTPUT_FILE}")
