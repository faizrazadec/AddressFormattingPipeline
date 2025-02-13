"""
Post-Processing Address Formatter (Final Step)

This script:
1. Moves excess words from `formatted_address_2` to `formatted_address_1` if space allows.
2. Ensures length limits of 35 characters for
`formatted_address_1` and 10 for `formatted_address_2`.
3. Strips unnecessary spaces and maintains formatting consistency.

"""

import pandas as pd

# Read the DataFrame from a CSV file
df = pd.read_csv("data/post_openai.csv")
print("Original DataFrame:")
print(df)

# Lowercase all column names
df.columns = df.columns.str.lower()

# Ensure all entries in the selected columns are strings
columns_to_convert = ["formatted_address_1", "formatted_address_2"]
df[columns_to_convert] = df[columns_to_convert].astype(str)

# Iterate over each row in the DataFrame to adjust address lengths
for index, row in df.iterrows():
    address_1 = row["formatted_address_1"]
    address_2 = row["formatted_address_2"]

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
        df.at[index, "formatted_address_1"] = new_address_1.strip()
        df.at[index, "formatted_address_2"] = new_address_2.strip()

print("\nCleaned and Adjusted DataFrame:")
print(df[["formatted_address_1", "formatted_address_2"]])

# Save the DataFrame to a CSV file
OUTPUT_FILE = "data/post_openai.csv"
df.to_csv(OUTPUT_FILE, index=False)

print(f"\nDataFrame saved to {OUTPUT_FILE}")
