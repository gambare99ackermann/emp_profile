import os
import pandas as pd
import requests

def enrich_employee_profiles(input_path, output_path, api_key):
    try:
        df = pd.read_excel(input_path)

        required_columns = ['Name', 'Company']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Missing column: {col}")

        emails, titles = [], []

        for _, row in df.iterrows():
            name_parts = str(row['Name']).split()
            if len(name_parts) < 2:
                emails.append("")
                titles.append("")
                continue

            first_name = name_parts[0]
            last_name = name_parts[-1]
            company = str(row['Company'])

            response = requests.post(
                "https://api.peopledatalabs.com/v5/person/enrich",
                headers={"X-API-Key": api_key},
                json={
                    "first_name": first_name,
                    "last_name": last_name,
                    "company": company
                }
            )

            if response.status_code == 200:
                data = response.json()
                emails.append(data.get('email', ''))
                titles.append(data.get('job_title', ''))
            else:
                emails.append("")
                titles.append("")

        df['Email'] = emails
        df['Job Title'] = titles
        df.to_excel(output_path, index=False)
        print(f"Enriched file saved to {output_path}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    input_path = os.getenv("INPUT_FILE", "List.xlsx")
    output_path = os.getenv("OUTPUT_FILE", "Enriched_List.xlsx")
    pdl_api_key = os.getenv("PDL_API_KEY", "")

    if not pdl_api_key:
        raise ValueError("PDL_API_KEY environment variable is not set.")

    enrich_employee_profiles(input_path, output_path, pdl_api_key)
