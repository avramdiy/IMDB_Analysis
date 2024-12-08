from flask import Flask, jsonify, send_file
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'templates'), static_folder=os.path.join(os.getcwd(), 'static'))

# Define the path to your dataset
path = 'C:\\Users\\Ev\\Desktop\\Week 1 IMDB Analysis\\Week 1 IMDb movies.csv'  # Update with your dataset path

# Load dataset
df = pd.read_csv(path)

# Clean column names to avoid issues with spaces or special characters
df.columns = df.columns.str.strip()

# Columns to drop before starting the API
columns_to_drop = [
    "actors", "language", "country", "date_published", "description", "director", 
    "worlwide_gross_income", "imdb_title_id", "metascore", "original_title", 
    "production_company", "title", "usa_gross_income", "writer"
]

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

# One-hot encoding function
def one_hot_encode_genres(df):
    # Ensure 'genre' column is present
    if 'genre' in df.columns:
        # Split multi-genre entries into separate columns
        genres_expanded = df['genre'].str.get_dummies(sep=',')
        print(f"One-hot encoded genres:\n{genres_expanded.head()}")
        
        # Combine one-hot encoded genres with the original DataFrame
        df = pd.concat([df, genres_expanded], axis=1)
        df.drop(columns=['genre'], inplace=True)  # Drop the original 'genre' column
    else:
        print("The 'genre' column is missing!")
    
    return df

# Clean the data before serving it
df = clean_data(df)
df = one_hot_encode_genres(df)

# Function to generate the bar chart
def create_genre_ratings_chart(df):
    # Identify the one-hot encoded genre columns (numeric columns except 'avg_vote')
    genre_columns = df.select_dtypes(include=[np.number]).columns.drop('avg_vote')

    # Calculate the weighted average IMDb rating for each genre
    average_ratings_by_genre = {
        genre: (df[genre] * df['avg_vote']).sum() / df[genre].sum()
        for genre in genre_columns
    }

    # Convert to a pandas Series and sort
    average_ratings_series = pd.Series(average_ratings_by_genre).sort_values(ascending=False)

    # Generate the bar chart
    plt.figure(figsize=(12, 6))
    average_ratings_series.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('Average IMDb Ratings by Genre', fontsize=16)
    plt.xlabel('Genres', fontsize=14)
    plt.ylabel('Average IMDb Rating', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Ensure the static directory exists
    static_dir = 'static'
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

    # Save the chart to the static directory
    chart_path = os.path.join(static_dir, 'AverageIMDbRatingsByGenre.png')
    plt.savefig(chart_path)
    plt.close()
    return chart_path


# Create the chart when the server starts
chart_path = create_genre_ratings_chart(df)

from flask import Flask, jsonify, render_template, url_for

@app.route('/')
def home():
    # Generate the URL for the static image
    chart_url = url_for('static', filename='AverageIMDbRatingsByGenre.png')
    
    # Render the template and pass the image URL
    return render_template('home.html', chart_url=chart_url)


@app.route('/chart')
def chart():
    return send_file(chart_path, mimetype='image/png')

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
    # Save the cleaned dataset if needed
    cleaned_file_path = 'cleaned_data.csv'
    df.to_csv(cleaned_file_path, index=False)

    print(f"Cleaned data saved to {cleaned_file_path}")
    
    # Start the Flask app
    app.run(debug=True)
