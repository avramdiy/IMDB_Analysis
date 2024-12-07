from flask import Flask, jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)


# Define the path to your dataset
path = 'C:\\Users\\Ev\\Desktop\\Week 1 IMDB Analysis\\Week 1 IMDb movies.csv'  # Update with your dataset path

# Load dataset
df = pd.read_csv(path)

# Clean column names to avoid issues with spaces or special characters
df.columns = df.columns.str.strip()

# Columns to drop before starting the API
columns_to_drop = ["actors", "date_published", "description", "director", "worlwide_gross_income", "imdb_title_id", "metascore", "original_title", "production_company", "title", "usa_gross_income", "writer"]

# Drop the specified columns before starting the Flask API
df.drop(columns=columns_to_drop, inplace=True, errors='ignore')

# Cleaning function
def clean_data(df):
    # Drop duplicates
    df.drop_duplicates(inplace=True)

    # Clean the 'budget' column by removing non-numeric characters (e.g., dollar signs, commas, and other text)
    df['budget'] = df['budget'].replace({',': '', '$': '', ' ': '', '[a-zA-Z]': ''}, regex=True)

    # Convert the 'budget' column to numeric values, setting errors to 'coerce' so that invalid values become NaN
    df['budget'] = pd.to_numeric(df['budget'], errors='coerce')

    # Calculate the median of the 'budget' column, ignoring NaN values
    budget_median = df['budget'].median()

    # Replace NaN values in the 'budget' column with the median
    df['budget'].fillna(budget_median, inplace=True)

    # Check the data after cleaning
    print("Data types after cleaning:\n", df.dtypes)

    return df

# Clean the data before serving it
df = clean_data(df)

@app.route('/')
def home():
    return "Welcome to the IMDb Dataset API!"

# Endpoint to get the entire dataset
@app.route('/data', methods=['GET'])
def get_data():
    data = df.to_dict(orient='records')  # Convert rows to list of dictionaries
    return jsonify(data)

# Endpoint to get a sample of the data (first 5 rows)
@app.route('/data/sample', methods=['GET'])
def get_sample_data():
    sample_data = df.head().to_dict(orient='records')
    return jsonify(sample_data)

if __name__ == '__main__':
    # You can save the cleaned dataset if needed
    cleaned_file_path = 'cleaned_data.csv'
    df.to_csv(cleaned_file_path, index=False)

    print(f"Cleaned data saved to {cleaned_file_path}")
    
    # Start the Flask app
    app.run(debug=True)
