FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script and Excel file into the container
COPY read_emp.py .
COPY List.xlsx .

# Run the script by default
CMD ["python", "read_emp.py"]
