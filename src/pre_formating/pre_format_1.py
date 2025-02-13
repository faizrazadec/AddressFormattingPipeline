"""
This module processes and cleans address data by removing duplicates, 
formatting text, and adjusting length constraints.
"""

import re
import pandas as pd

# Read the DataFrame from a CSV file
df = pd.read_csv("data/Updated ReCharge List - Sheet1 1.csv")
print("Original DataFrame:")
print(df)

# For demonstration purposes, limit the DataFrame to a subset of rows
# df = df[450:460]

# Lowercase all column names
df.columns = df.columns.str.lower()

# Lowercase all entries in the selected columns
columns_to_lower = [
    "company",
    "address_1",
    "address_2",
    "city",
    "province",
    "zip",
    "country",
    "phone",
]
df[columns_to_lower] = df[columns_to_lower].apply(
    lambda col: col.astype(str).str.lower()
)

def remove_duplicates(row):
    """
    Removes duplicate values from address fields based on company, city, province, zip, and country.

    Args:
        row (pd.Series): A row from the DataFrame containing address data.

    Returns:
        pd.Series: A tuple containing cleaned address_1 and address_2.
    """

    address_1 = str(row["address_1"])
    address_2 = str(row["address_2"])
    phone = str(row["phone"])

    # Values to remove
    values_to_remove = [
        row["company"],
        row["city"],
        row["province"],
        row["zip"],
        row["country"],
    ]

    # Remove values from address_1
    for value in values_to_remove:
        address_1 = re.sub(r"\b" + re.escape(value) + r"\b", "", address_1).strip(", ")

    # Remove values from address_2
    for value in values_to_remove:
        address_2 = re.sub(r"\b" + re.escape(value) + r"\b", "", address_2).strip(", ")

    # Remove words present in both address_1 and address_2 from address_1
    address_1_words = set(address_1.split())
    address_2_words = set(address_2.split())

    # Find words that are not in address_2
    unique_words = address_1_words - address_2_words

    # Join the unique words back into a string
    cleaned_address_1 = " ".join(unique_words)

    # Remove phone number from address_1 and address_2
    phone_pattern = re.escape(phone.replace("+", r"\+?"))
    cleaned_address_1 = re.sub(phone_pattern, "", cleaned_address_1).strip(", ")
    address_2 = re.sub(phone_pattern, "", address_2).strip(", ")

    # Additional step to remove any remaining phone numbers
    phone_patterns = [
        r"\+?\d{1,3}[-.\s]?\(?\d{1,4}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}",
        r"\+?\d{1,3}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}",
    ]
    for pattern in phone_patterns:
        cleaned_address_1 = re.sub(pattern, "", cleaned_address_1).strip(", ")
        address_2 = re.sub(pattern, "", address_2).strip(", ")

    return pd.Series([cleaned_address_1, address_2])

# Apply the function to the DataFrame
df[["address_1", "address_2"]] = df.apply(remove_duplicates, axis=1)

# Iterate over each row in the DataFrame to adjust address lengths
for index, data_row in df.iterrows():
    address_1 = data_row["address_1"]
    address_2 = data_row["address_2"]

    # Check if the conditions are met
    if len(address_1) < 34 and len(address_2) > 10:
        # Split address_2 by spaces, hyphens, and periods
        words = address_2.replace("-", " ").replace(".", " ").split()
        new_address_1 = address_1
        new_address_2 = []

        # Move words from address_2 to address_1
        for word in words:
            if len(new_address_1) + len(word) + 1 <= 35:
                new_address_1 += " " + word
            else:
                new_address_2.append(word)

        # Join the remaining words back into address_2
        new_address_2 = " ".join(new_address_2)

        # Update the DataFrame
        df.at[index, "address_1"] = new_address_1.strip()
        df.at[index, "address_2"] = new_address_2.strip()

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

# Convert cleaned entries back to PascalCase, excluding the 'phone' column
columns_to_convert = [
    "company",
    "address_1",
    "address_2",
    "city",
    "province",
    "zip",
    "country",
]
df[columns_to_convert] = df[columns_to_convert].apply(
    lambda col: col.astype(str).map(to_pascal_case)
)

print("\nCleaned and Adjusted DataFrame:")
print(df[["address_1", "address_2"]])

# Save the DataFrame to a CSV file
OUTPUT_FILE = "data/pre_formated.csv"
df.to_csv(OUTPUT_FILE, index=False)

print(f"\nDataFrame saved to {OUTPUT_FILE}")
