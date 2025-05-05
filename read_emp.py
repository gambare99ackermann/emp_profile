from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

@app.route("/enrich", methods=["POST"])
def enrich_employee_profiles():
    try:
        file = request.files['file']
        df = pd.read_excel(file)

        # Check required columns
        required_columns = ['Name', 'Company']
        for col in required_columns:
            if col not in df.columns:
                return jsonify({"error": f"Missing column: {col}"}), 400

        data = df[required_columns].to_dict(orient='records')
        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
