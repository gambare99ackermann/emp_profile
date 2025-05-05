import pandas as pd
import json

def read_excel(file_path):
    try:
        # Read the Excel file into a DataFrame
        df = pd.read_excel(file_path)

        # Ensure required columns are present
        required_columns = ['Name','Company']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Missing column: {col}")

        # Convert to list of dicts (JSON-compatible)
        data = df[required_columns].to_dict(orient='records')
        return data

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    file_path = "employee_data.xlsx"  # Ensure this file is uploaded too
    employee_data = read_excel(file_path)
    print(json.dumps(employee_data, indent=2))
