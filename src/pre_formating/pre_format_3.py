"""
Pre-Processing Script: Pascal Case & Address Formatting

This script processes `address_2` by:
1. Converting it to PascalCase.
2. Removing spaces if its length exceeds 10 characters.
3. Ensuring final formatting while maintaining constraints.

The processed data is saved to `data/pre_formated.csv`.
"""

import pandas as pd

# Read the DataFrame from a CSV file
df = pd.read_csv("data/pre_formated.csv")
print("Original DataFrame:")
print(df)

# Lowercase all column names
df.columns = df.columns.str.lower()


# Function to convert to PascalCase
def to_pascal_case(s):
    """
    Converts a string to PascalCase.

    Args:
        s (str): The input string.

    Returns:
        str: The formatted PascalCase string.
    """
    return " ".join(word.capitalize() for word in s.split())


# Ensure all entries in the selected columns are strings and convert to PascalCase
columns_to_convert = ["address_2"]
df[columns_to_convert] = df[columns_to_convert].astype(str).applymap(to_pascal_case)

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    address_2 = row["address_2"]

    # Check if the condition is met
    if len(address_2) > 10:
        # Remove all spaces
        new_address_2 = address_2.replace(" ", "")

        # Check if the length is within the limit after removing spaces
        if len(new_address_2) <= 10:
            # Update the DataFrame with the new value
            df.at[index, "address_2"] = new_address_2.strip()
        else:
            # Revert to the original value
            df.at[index, "address_2"] = address_2.strip()

print("\nAdjusted DataFrame:")
print(df[["address_1", "address_2"]])

# Save the adjusted DataFrame to a CSV file
OUTPUT_FILE = "data/pre_formated.csv"
df.to_csv(OUTPUT_FILE, index=False)

print(f"\nAdjusted DataFrame saved to {OUTPUT_FILE}")
