# Data Explorer Web App 
[![GitHub release](https://img.shields.io/github/release/AnaMJaimeR/data_explorer_webapp.svg)](https://GitHub.com/AnaMJaimeR/data_explorer_webapp/releases/)

[![Docker 20.10](https://img.shields.io/badge/Docker-20.10-blue.svg)](https://docs.docker.com/get-docker/)
[![Python 3.8.2](https://img.shields.io/badge/python-3.8.2-blue.svg)](https://www.python.org/downloads/release/python-382/)

## Overview
The Data Explorer Web App is a Python containerised web application, built employing the Streamlit framework. This application allows the user to upload a CSV file to subsequently run a variety of calculations and methods on the inputted data set. The returned tables and visuals are ready to be analysed, aiming to help the user to easily perform an Exploratory Data Analysis (EDA) and get a deeper understanding of the uploaded data.

## Installation
To perform the installation process, you need to have git and docker installed on your computer and follow the next steps: 

1. Clone the repo

    ```bash
    git clone https://github.com/AnaMJaimeR/data_explorer_webapp.git
    ```

2. cd into the project root folder

    ```bash
    cd data_explorer_webapp
    ```

3. Build the Streamlit image

    ```bash
    docker build -t streamlit:latest .
    ```

4. Create docker container and run

    ```bash
    docker run --rm -it -p 8501:8501 streamlit:latest
    ```

## Run the app

After running the container, go to **http://localhost:8501/** to use the app.

## App interactivity

1. Upload a comma-separated values (CSV) file using the widget and explore the Overall section.

![Upload](demo/upload_mq.gif)

2. Choose the number of rows that you want to display in the slider.

![Slider](demo/slider_mq.gif)

3. Choose which columns need to be converted to DateTime type in the multiselect widget.

![Date](demo/date_mq.gif)

## Sections

* Overall: The Overall section provides the user with general information on the dataset such as the total number of columns and rows, duplicates and missing values. Equally important, it grants the user the possibility to specify which columns should be converted to DateTime type.

* Numeric: The Numeric section gives details on several statistics for each of the numeric columns, as well as an histogram.

* Text: The Text section gives details on the number of missing and unique values corresponding for each text column. Additionally, it specifies the number of rows with empty, only-uppercase and only-lowercase values, finalising with a bar chart of the frequencies.

* Date: The Date section give additional details about the DateTime columns, like the number of week and weekend days for each. Additionally, it displays a bar chart with the frequency of each date.

## Test the app
A series of tests were created to ensure app robustness. To run the tests follow the next steps:

1. If the Streamlit image has not been created

    ```bash
    docker build -t streamlit:latest .
    ```

2. Run the tests

    ```bash
    docker run --rm -it streamlit:latest bash -c 'python -m unittest'
    ```