"""
Post-Processing Address Formatter

This script:
1. Moves the last word from `formatted_address_1` to the start of `formatted_address_2`
   if `formatted_address_1` exceeds 35 characters.
2. Ensures `formatted_address_2` does not exceed 10 characters after modification.
3. Saves the adjusted DataFrame to a CSV file.
"""

import pandas as pd

# Sample DataFrame
data = {
    "Company": ["ABC Corp", "XYZ Inc", "LMN Ltd", "DEF Corp"],
    "formatted_address_1": [
        "Pr. Savanorių , Sav. Kauno 287a,c M.",
        "BazÃ¡n Pardo Ãtico De 1a Comtessa 13",
        "789 oak st, chicago, 60601, usa, lmn ltd, +9876543210",
        "101 pine st, san francisco, 94101, usa, def corp, +1122334455",
    ],
    "formatted_address_2": [
        "apt,",
        "X",
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
# df = df[170:175]
print("Original DataFrame:")
print(df)

# Lowercase all column names
df.columns = df.columns.str.lower()

# Ensure all entries in the selected columns are strings
columns_to_convert = ["formatted_address_1", "formatted_address_2"]
df[columns_to_convert] = df[columns_to_convert].astype(str)


# Function to move the last word from address_1 to the start of address_2
def move_last_word(address_1, address_2):
    """
    Moves the last word from `address_1` to the start of `address_2`
    if `address_1` is too long and `address_2` can accommodate it.
    """
    words_1 = address_1.split()
    words_2 = address_2.split()

    # Try moving the last word from address_1 to address_2
    last_word = words_1.pop()
    new_address_2 = " ".join([last_word] + words_2)

    # Check if the length of the new address_2 exceeds 10
    if len(new_address_2) <= 10:
        return " ".join(words_1), new_address_2

    # Try moving the second last word from address_1 to address_2
    second_last_word = words_1.pop()
    new_address_2 = " ".join([second_last_word] + words_2)

    # Check if the length of the new address_2 exceeds 10
    if len(new_address_2) <= 10:
        return " ".join(words_1), new_address_2

    # If both attempts fail, return the original addresses
    return address_1, address_2


# Create new columns for the adjusted addresses
df["formatted_address_1_1"] = df["formatted_address_1"]
df["formatted_address_2_1"] = df["formatted_address_2"]

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    address_1 = row["formatted_address_1"]
    address_2 = row["formatted_address_2"]

    # Check if the length of address_1 is more than 35
    if len(address_1) >= 35:
        # Move the last word from address_1 to the start of address_2
        new_address_1, new_address_2 = move_last_word(address_1, address_2)

        # Update the DataFrame
        df.at[index, "formatted_address_1_1"] = new_address_1.strip()
        df.at[index, "formatted_address_2_1"] = new_address_2.strip()

print("\nAdjusted DataFrame:")
print(df[["formatted_address_1_1", "formatted_address_2_1"]])

# Save the adjusted DataFrame to a CSV file
OUTPUT_FILE = "post_openai.csv"
df.to_csv(OUTPUT_FILE, index=False)

print(f"\nAdjusted DataFrame saved to {OUTPUT_FILE}")
