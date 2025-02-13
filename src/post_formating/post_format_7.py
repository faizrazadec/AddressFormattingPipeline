"""
Post-Processing: Adjust Company Names

This script:
1. Removes special characters from company names.
2. Adjusts company names to a max of 10 characters using rules.
3. Saves the adjusted DataFrame to a CSV file.
"""

import re
import pandas as pd

# Sample DataFrame
data = {
    "formatted_company": [
        "CorporationABC",
        "Inc XYZ Inc XYZ",
        "IncXYZ456",
        "DEF Corp Limited",
    ],
    "formatted_address_1": [
        "Pr. Savanorių , Sav. Kauno 287a,c M.",
        "Bazán Pardo Ático De 1a Comtessa 13",
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
df = pd.read_csv("post_openai.csv")
# df = df[170:175]
print("Original DataFrame:")
print(df)

# Lowercase all column names
df.columns = df.columns.str.lower()

# Ensure all entries in the selected columns are strings
columns_to_convert = ["formatted_company"]
df[columns_to_convert] = df[columns_to_convert].astype(str)


# Function to remove special characters from the company name
def remove_special_characters(company):
    """
    Removes special characters from the company name.
    
    :param company: The original company name.
    :return: The cleaned company name.
    """
    return re.sub(r"[^a-zA-Z0-9\s]", "", company)


# Function to adjust the company name
def adjust_company_name(company):
    """
    Adjusts the company name to ensure it does not exceed 10 characters.

    1. Removes special characters.
    2. If the name contains only one word:
       - Extracts letters and digits separately.
       - Returns the first letter + digits (if applicable).
       - If no digits, truncates to 10 characters.
    3. If the name contains multiple words:
       - Tries to create an abbreviation based on word count.
       - Ensures the final name does not exceed 10 characters.
    
    :param company: The original company name.
    :return: The adjusted company name.
    """
    company = remove_special_characters(company)
    words = company.split()
    first_word = words[0]

    if len(words) == 1:
        match = re.match(
            r"([a-zA-Z]+)(\d+)", company
        )  # Extract alphabets and digits separately
        if match:
            first_letter = match.group(1)[0]  # First letter of the alphabetic part
            digits = match.group(2)  # Numeric part
            return first_letter + digits  # Concatenation
        elif len(first_word) > 10:
            company = company[:10]
            return company  # If there's only one word, return it as is
        return company  # Return as is if no match

    first_word = words[0]
    second_word = words[1]
    last_word = words[-1]

    # Check if the first word is less than 10 characters
    if len(company) > 10:
        if len(words) == 3:
            # If there are three words, pick the first alphabet of each word
            new_company = first_word[0] + second_word[0] + last_word[0]
        elif len(words) == 4:
            third_word = words[2]
            # If there are four words, pick the first alphabet of each word
            new_company = first_word[0] + second_word[0] + last_word[0] + third_word[0]
        else:
            # If the first word is less than 10 characters
            if len(first_word) < 10:
                new_company = first_word + second_word[0]
            elif len(first_word) > 10 and len(second_word) < 9:
                new_company = first_word[0] + " " + second_word
            else:
                new_company = first_word[0] + second_word[0]

        # If the total length is still greater than 10, remove the space
        if len(new_company) > 10:
            new_company = new_company.replace(" ", "")
            if len(new_company) > 10:
                new_company = new_company[:10]

        return new_company
    else:
        return company


# Apply the function to the company column
df["adjusted_company"] = df["formatted_company"].apply(adjust_company_name)

print("\nAdjusted DataFrame:")
print(df[["formatted_company", "adjusted_company"]])

# Save the adjusted DataFrame to a CSV file
OUTPUT_FILE = "post_openai.csv"
df.to_csv(OUTPUT_FILE, index=False)

print(f"\nAdjusted DataFrame saved to {OUTPUT_FILE}")
