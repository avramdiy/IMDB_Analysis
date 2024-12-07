from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# Define the path to your dataset (local or URL)
path = 'C:\\Users\\Ev\\Desktop\\Week 1 IMDB Analysis\\Week 1 IMDb movies.csv'  # Update with your dataset URL or local path

# Load dataset
df = pd.read_csv(path)

# Cleaning function
def clean_data(df):
    # Drop duplicates
    df.drop_duplicates(inplace=True)

    # Handle missing values (fill numerical columns with the mean)
    df.fillna(df.mean(), inplace=True)

    # Check data types and convert if needed
    print(df.dtypes)

    return df

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

# Endpoint to clean the dataset (handle missing values, drop duplicates)
@app.route('/data/clean', methods=['GET'])
def clean_data_api():
    global df  # Access the global DataFrame
    df = clean_data(df)  # Clean the data
    # Save cleaned data for further analysis
    df.to_csv('cleaned_data.csv', index=False)
    return "Dataset cleaned and saved successfully!"

if __name__ == '__main__':
    app.run(debug=True)
