"""
Post-Processing Formatter for Addresses

This script refines address formatting:
1. Cleans up special characters and truncates fields to required lengths.
2. Converts addresses to PascalCase where needed.
3. Ensures no double spaces in formatted addresses.
4. Adjusts address distribution between address_1 and address_2 for optimal readability.
"""

import re
import pandas as pd


def clean_address(address, limit):
    """Remove spaces around commas, periods, dashes, underscores
    and truncate the address to the given limit."""
    # Remove spaces around special characters if the address length exceeds the limit
    if len(address) > limit:
        address = re.sub(r"\s*([,.\-_])\s*", r"\1", address)
        return address[:limit]
    return address


def pascal_case(address):
    """Convert the address to PascalCase by removing spaces and capitalizing each word."""
    if isinstance(address, str):
        return "".join(word.capitalize() for word in address.split())
    return address  # If it's not a valid string (e.g., NaN), return as it is.


def clean_double_spaces(address):
    """Ensure no double spaces in the address."""
    if isinstance(address, str):  # Only apply re.sub if the address is a string
        return re.sub(r"\s+", " ", address).strip()
    return address  # Return the original address if it's not a valid string (e.g., NaN)


def post_format_address(df):
    """Process the addresses in the DataFrame based on the conditions provided."""
    for idx, row in df.iterrows():
        address_1 = str(row["formatted_address_1"]).strip()
        address_2 = str(row["formatted_address_2"]).strip()

        # Step 1: Clean address_1 if its length is greater than 35
        if len(address_1) > 35:
            df.at[idx, "formatted_address_1"] = clean_address(address_1, 35)

        # Step 2: Clean address_2 if its length is greater than 10
        if len(address_2) > 10:
            df.at[idx, "formatted_address_2"] = clean_address(address_2, 10)

        # Step 3: If address_2 is greater than 10 and address_1 is less than 34
        if len(address_2) > 10 and len(address_1) < 34:
            space_needed = 34 - len(address_1)
            if len(address_2) > space_needed:
                new_address_1 = address_1 + " " + address_2[:space_needed]
                new_address_2 = address_2[space_needed:]
                df.at[idx, "formatted_address_1"] = new_address_1.strip()
                df.at[idx, "formatted_address_2"] = new_address_2.strip()

        # Step 4: Remove spaces from address_2 if still greater than 10 (after PascalCase)
        if len(address_2) > 10:
            df.at[idx, "formatted_address_2"] = pascal_case(
                df.at[idx, "formatted_address_2"]
            )

        # Step 5: If address_1 is greater than 35, remove spaces from address_2
        if len(address_1) > 35:
            df.at[idx, "formatted_address_2"] = pascal_case(
                df.at[idx, "formatted_address_2"]
            )

        # Ensure there are no double spaces
        df.at[idx, "formatted_address_1"] = clean_double_spaces(
            df.at[idx, "formatted_address_1"]
        )
        df.at[idx, "formatted_address_2"] = clean_double_spaces(
            df.at[idx, "formatted_address_2"]
        )

    return df


# Load your DataFrame (Replace with actual file path)
dff = pd.read_csv("data/openai.csv")

# Call the post-format function to apply the logic
post_df = post_format_address(dff)

# Save the formatted DataFrame to a new CSV file
post_df.to_csv("data/post_openai.csv", index=False)

print("Address formatting completed and saved to formatted_addresses.csv")
