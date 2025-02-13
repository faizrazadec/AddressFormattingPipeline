"""
Post-Processing: Remove Spaces in Long Addresses

This script:
1. Removes all spaces from `formatted_address_1` if its length exceeds 35 characters.
2. Saves the adjusted DataFrame to a CSV file.
"""

import pandas as pd

# Sample DataFrame
data = {
    "Company": ["ABC Corp", "XYZ Inc", "LMN Ltd", "DEF Corp"],
    "formatted_address_1": [
        "Pr. Savanorių , Sav. Kauno 28 7a, M.",
        "Bazán Pardo Ático De 1a Comtessa 13",
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

# Create DataFrame
# df = pd.DataFrame(data)
df = pd.read_csv("data/post_openai.csv")
df = df[170:175]
print("Original DataFrame:")
print(df)

# Lowercase all column names
df.columns = df.columns.str.lower()

# Ensure all entries in the selected columns are strings
columns_to_convert = ["formatted_address_1", "formatted_address_2"]
df[columns_to_convert] = df[columns_to_convert].astype(str)


# Function to remove all spaces from address_1 if its length is greater than 35
def remove_all_spaces_if_long(address_1):
    """
    Removes all spaces from the address if its length exceeds ADDRESS_1_LIMIT.

    :param address: The original address string.
    :return: Modified address string with spaces removed if it exceeds ADDRESS_1_LIMIT.
    """
    if len(address_1) > 35:
        address_1 = address_1.replace(" ", "")
    return address_1


# Create a new column for the adjusted address
df["formatted_address_1_no_space"] = df["formatted_address_1"].apply(
    remove_all_spaces_if_long
)

print("\nAdjusted DataFrame:")
print(df[["formatted_address_1", "formatted_address_1_no_space"]])

# # Save the adjusted DataFrame to a CSV file
# output_file = 'post_openai.csv'
# df.to_csv(output_file, index=False)

# print(f"\nAdjusted DataFrame saved to {output_file}")
