"""
Post-Processing Address Formatter

This script processes address fields in a CSV file:
1. Cleans up special characters (removes spaces around commas, dots, and hyphens).
2. Ensures the length constraints for address fields
(35 characters for address_1, 10 for address_2).
3. Filters out invalid characters and ensures proper formatting.
"""

import pandas as pd
import regex as re

# Sample DataFrame
data = {
    "Company": ["ABC Corp", "XYZ Inc", "LMN Ltd", "DEF Corp"],
    "formatted_address_1": [
        "Pr. Savanorių , Sav. Kauno 287a, M.",
        "456 elm st, los angeles, 90001, usa, xyz inc, 1234567890",
        "789 oak st, chicago, 60601, usa, lmn ltd, +9876543210",
        "101 pine st, san francisco, 94101, usa, def corp, +1122334455",
    ],
    "formatted_address_2": [
        "apt 101 st,",
        "suite 202, los angeles, 90001, usa, xyz inc, 1234567890",
        "floor 303, chicago, 60601, usa, lmn ltd, +9876543210",
        "unit 404, san francisco, 94101, usa, def corp, +1122334455",
    ],
    "City": ["New York", "Los Angeles", "Chicago", "San Francisco"],
    "Province": ["NY", "CA", "IL", "CA"],
    "Zip": ["10001", "90001", "60601", "94101"],
    "Country": ["USA", "USA", "USA", "USA"],
    "Phone": ["+1234567890", "1234567890", "+9876543210", "+1122334455"],
}

# Read the DataFrame from a CSV file
df = pd.read_csv("data/post_openai.csv")
# df = pd.DataFrame(data)
print("Original DataFrame:")
print(df)
# df = df[35:40]
# Lowercase all column names
df.columns = df.columns.str.lower()

# Ensure all entries in the selected columns are strings
columns_to_convert = ["formatted_address_1", "formatted_address_2"]
df[columns_to_convert] = df[columns_to_convert].astype(str)


# Function to check if the string contains only allowed characters
def contains_only_allowed_characters(s):
    """Removes spaces before and after commas, dots, and hyphens."""
    return re.match(r"^[A-Za-z0-9 ,.-]+$", s) is not None


# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    address_1 = row["formatted_address_1"]
    address_2 = row["formatted_address_2"]

    # Check if the conditions are met
    if len(address_1) > 35 and len(address_2) <= 10:
        # Remove spaces before and after commas, dots, and hyphens
        address_1 = re.sub(r"\s*,\s*", ",", address_1)
        address_1 = re.sub(r"\s*\.\s*", ".", address_1)
        address_1 = re.sub(r"\s*-\s*", "-", address_1)

        # Update the DataFrame
        df.at[index, "formatted_address_1"] = address_1.strip()

    elif not contains_only_allowed_characters(address_1):
        # Remove spaces before and after commas, dots, and hyphens
        address_1 = re.sub(r"\s*,\s*", ",", address_1)
        address_1 = re.sub(r"\s*\.\s*", ".", address_1)
        address_1 = re.sub(r"\s*-\s*", "-", address_1)

        # Update the DataFrame
        df.at[index, "formatted_address_1"] = address_1.strip()

    elif len(address_1) <= 35 and len(address_2) > 10:
        address_2 = re.sub(r"\s*,\s*", ",", address_2)
        address_2 = re.sub(r"\s*\.\s*", ".", address_2)
        address_2 = re.sub(r"\s*-\s*", "-", address_2)

        # Update the DataFrame
        df.at[index, "formatted_address_2"] = address_2.strip()
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
            df.at[index, "formatted_address_1"] = new_address_1.strip()
            df.at[index, "formatted_address_2"] = new_address_2.strip()
        else:
            # Revert to the original values
            df.at[index, "formatted_address_1"] = address_1.strip()
            df.at[index, "formatted_address_2"] = address_2.strip()

print("\nAdjusted DataFrame:")
print(df[["formatted_address_1", "formatted_address_2"]])

# Save the adjusted DataFrame to a CSV file
OUTPUT_FILE = "data/post_openai.csv"
df.to_csv(OUTPUT_FILE, index=False)

print(f"\nAdjusted DataFrame saved to {OUTPUT_FILE}")
