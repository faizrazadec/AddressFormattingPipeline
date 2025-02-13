"""
Post-Processing Address Formatter

This script:
1. Converts `address_2` values exceeding 10 characters into PascalCase.
2. Removes spaces, dots, and commas.
3. Ensures the transformed value is within 10 characters; otherwise, keeps the original.
"""

import re
import pandas as pd

# Sample DataFrame
data = {
    "Company": ["ABC Corp", "XYZ Inc", "LMN Ltd", "DEF Corp"],
    "Address_1": [
        "123 main st, new york, 10001, usa, abc corp, +1234567890",
        "456 elm st, los angeles, 90001, usa, xyz inc, 1234567890",
        "789 oak st, chicago, 60601, usa, lmn ltd, +9876543210",
        "101 pine st, san francisco, 94101, usa, def corp, +1122334455",
    ],
    "Address_2": [
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
    return "".join(word.capitalize() for word in s.split())


# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    address_2 = row["address_2"]

    # Check if the condition is met
    if len(address_2) > 10:
        # Remove all spaces, dots, and commas
        new_address_2 = re.sub(r"[ ,.-]", "", address_2)

        # Convert to PascalCase
        new_address_2 = to_pascal_case(new_address_2)

        # Check if the length is within the limit after removing spaces, dots, and commas
        if len(new_address_2) <= 10:
            # Update the DataFrame with the new value
            df.at[index, "address_2"] = new_address_2.strip()
        else:
            # Revert to the original value
            df.at[index, "address_2"] = address_2.strip()

print("\nAdjusted DataFrame:")
print(df[["address_1", "address_2"]])

# Save the adjusted DataFrame to a CSV file
OUTPUT_FILE = "data/post_openai.csv"
df.to_csv(OUTPUT_FILE, index=False)

print(f"\nAdjusted DataFrame saved to {OUTPUT_FILE}")
