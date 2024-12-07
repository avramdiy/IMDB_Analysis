# IMDb Dataset Analysis API

This project provides a Flask-based API to interact with and clean the IMDb dataset. It allows users to view, clean, and download the dataset via various endpoints.

## Dataset

The dataset used in this project is the IMDb Movies dataset, which can be downloaded from the following link:

- [Download IMDb dataset (CSV)](https://www.kaggle.com/datasets/simhyunsu/imdbextensivedataset?resource=download)

## Getting Started

### Prerequisites

You need to have **Python 3.11** installed and the following packages:

- Flask
- Pandas

### Installation

1. Clone this repository:
   ```bash
   git clone <repository_url>


### Documented Commits & Purposes

First Commit : Initialized clean_data.py, requirements.txt, venv, README.txt with FlaskAPI and routes

Second Commit : Explored features to analyze, dropped a majority of irrelevant columns, and adjusted the "budget" feature to replace NaN and unfiltered string values with $0.00 values.
