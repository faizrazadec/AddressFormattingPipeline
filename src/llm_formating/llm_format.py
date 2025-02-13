"""
Main Processing Script: Address Formatting with OpenAI API

This script processes addresses in a CSV file using OpenAI GPT-4o-mini.
It:
1. Checks if address fields exceed character limits.
2. Calls OpenAI API for reformatting if needed.
3. Saves the updated results to `data/openai.csv`.
"""

import os
import json
import regex as re
import pandas as pd
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from llm_formating.system_prompt import SYSTEM_PROMPT

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini", api_key=openai_api_key)

# Read CSV file
df = pd.read_csv("data/pre_formated.csv")

# Address field limits
ADDRESS_1_LIMIT = 35
ADDRESS_2_LIMIT = 10


def clean_llm_response(response_text):
    """Remove JSON formatting markers from the LLM response."""
    cleaned_text = re.sub(r"```json|```", "", response_text).strip()
    return cleaned_text


# Loop through addresses
for idx, row in df.iterrows():
    address_1 = str(row["address_1"])
    address_2 = str(row["address_2"])

    # Check if the lengths are within the limits
    if len(address_1) <= ADDRESS_1_LIMIT and len(address_2) <= ADDRESS_2_LIMIT:
        # Directly copy the addresses to the formatted fields
        df.at[idx, "formatted_address_1"] = address_1
        df.at[idx, "formatted_address_2"] = address_2
        df.at[idx, "formatted_company"] = row["company"]
    else:
        columns_to_convert = [
            "company",
            "address_1",
            "address_2",
            "city",
            "province",
            "zip",
            "country",
        ]
        row_dict = row[columns_to_convert].to_dict()
        row_json = json.dumps(row_dict, ensure_ascii=False, indent=4)
        print(row_json)

        # Send the system prompt and row JSON to the model
        system_message = SystemMessage(content=SYSTEM_PROMPT)
        user_message = HumanMessage(content=row_json)

        response = llm.invoke([system_message, user_message])
        response_content = response.content.strip()
        print(response_content)

        try:
            # Parse the JSON string response
            cleaned_llm_text = clean_llm_response(response_content)
            formatted_response = json.loads(cleaned_llm_text)

            # Store response in new columns
            df.at[idx, "formatted_address_1"] = formatted_response.get("address_1", "")
            df.at[idx, "formatted_address_2"] = formatted_response.get("address_2", "")
            df.at[idx, "formatted_company"] = formatted_response.get("company", "")

            # Convert to string and handle NaN or None values safely
            formatted_address_1 = str(formatted_response.get("address_1", "") or "")
            formatted_address_2 = str(formatted_response.get("address_2", "") or "")
            formatted_company = str(formatted_response.get("company", "") or "")

            print(
                f"Row {idx} - Length of formatted_address_1: {len(formatted_address_1)}"
            )
            print(
                f"Row {idx} - Length of formatted_address_2: {len(formatted_address_2)}"
            )
            print(f"Row {idx} - Length of formatted_company: {len(formatted_company)}")

            print(f"Row {idx}: formatted")

        except json.JSONDecodeError as e:
            print(f"Row {idx}: Failed to parse JSON response: {e}")
            print(f"Response content: {response_content}")

# Save the updated DataFrame to a new CSV file
df.to_csv("data/openai.csv", index=False)
print("Processing complete. Updated file saved.")
