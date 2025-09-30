 Self-Service Data Cleaning Web App

This project is a web application built with Python and Streamlit, designed to be a self-service tool for data cleaning and preparation. It empowers users, even those without technical skills, to upload raw Excel files, apply cleaning and standardization rules, and download a ready-to-use CSV file for analysis in BI tools like Power BI.

 Features

* **Interactive Web Interface**: A clean and intuitive UI built with Streamlit.
* **File Upload**: Supports direct upload of Excel (`.xlsx`) files.
* **Data Preview**: Immediately displays the first few rows of the uploaded data for quick validation.
* **Dynamic Column Selection**: Reads the uploaded file and presents the user with a multi-select widget to choose exactly which columns to keep in the final dataset.
* **Automated Data Cleaning & Standardization**:
    * **Column Name Standardization**: Automatically trims whitespace, replaces spaces with underscores, removes special characters, and allows the user to choose between `UPPERCASE` or `lowercase` formats via a checkbox.
    * **Text Data Cleaning**: Cleans text columns by trimming whitespace, standardizing capitalization (`.str.title()`), and properly handling null/empty values by replacing them with 'N/A'.
* **Live Preview**: Shows a real-time preview of the cleaned and transformed data based on the user's selections.
* **CSV Download**: Provides a download button to export the final, clean dataset as a `.csv` file, ready for ingestion into Power BI or other BI tools.
* **Performance Optimization**: Uses Streamlit's `session_state` to cache the uploaded file, ensuring a fast and responsive user experience when applying filters and selections, even with large files.

 Key Technologies Used

* **Python**: The core programming language.
* **Pandas**: For all data manipulation, cleaning, and transformation tasks.
* **Streamlit**: To build and run the interactive web application.

 How it Works

The application follows a simple but powerful ETL (Extract, Transform, Load) logic:

1.  **Extract**: The user uploads an Excel file, which is loaded into a Pandas DataFrame. The DataFrame is cached in the `session_state` to improve performance.
2.  **Transform**: The user interacts with the sidebar widgets to select columns and choose formatting options. The script then applies a series of cleaning functions to the data based on these selections.
3.  **Load**: The final, cleaned DataFrame is displayed on the screen and made available for download as a CSV file.

This project demonstrates not only data processing skills but also the ability to build user-centric data products that solve real-world business problems.
