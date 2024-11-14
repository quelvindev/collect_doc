  <h1> 📊 Exporting data from Google Sheets to CSV </h1>

This Python project extracts data from a Google Sheets file, performs a series of ETL (Extract, Transform, Load) processes to clean and format the data, and exports it as a CSV file. It leverages pandas for data manipulation, and allows seamless data import from publicly accessible Google Sheets.

<h2>🚀 Project Overview</h2>

- **Import Data:** Retrieves data from a publicly accessible Google Sheets URL.
- **Transform Data:** Cleans and formats the data by removing empty rows and columns, promoting column headers, and formatting specific values.
- **Export Data:** Saves the transformed data to a CSV file for further analysis.


📂 Project Structure

```bash
.
├── main.py             # Application startup script
├──  collect.py         # File that loads, cleans and exports data
├── keys.py             # Ignored in .gitignore
└── controle_bonus.csv  # Output CSV file after transformation
```

<h2>📋 Process Flow</h2>

1. Import Data
The import_data() function uses pandas.read_html() to import data directly from the Google Sheets link:

```bash
data = pd.read_html("https://docs.google.com/spreadsheets/d/.../pubhtml", encoding='latin1')
```

2. Data Collection and Concatenation
The collect_data() and join_data() functions gather the data into a single DataFrame for easy transformation.

3. ETL Process
Column Removal: Drops unnecessary columns to simplify the dataset.
Header Promotion: Sets the first row as the header for the DataFrame.
Value Formatting: Replaces semicolons (;) with colons (:) in specific columns.

4. Export Data
The cleaned data is saved to a CSV file, controle_bonus.csv, using the export_data() function.

<h2>🛠️ Code Example</h2>

```bash
# DATA CLEANING
def etl2_data():
    df = join_data()
    if df.shape[1] > 0:
        df = df.drop(df.columns[0], axis=1)
    df.columns = df.iloc[0]
    df = df[df[df.columns[0]] != "Data"].reset_index(drop=True)
    df = df.dropna(axis=1, how='all').dropna(how='all')
    df[df.columns[1]] = df[df.columns[1]].str.replace(";", ":")
    return df
```
📦 Installation and Usage
1. Clone the Repository:

```bash
git clone https://github.com/your-username/google-sheets-etl.git
cd collect_doc
```
2. Install Required Libraries:
```bash
lxml==5.3.0
numpy==2.1.3
pandas==2.2.3
python-dateutil==2.9.0.post0
pytz==2024.2
six==1.16.0
tzdata==2024.2
```

3. Run the Script:
```bash
python main.py
```

4. Check the Output: The output CSV file controle_bonus.csv will be in the project directory

🔍 Example Output
Here is an example of the transformed data that will be exported to controle_bonus.csv:


|    Date     | Hr. Chegada|    Nota       |
| :---:       | :---:      | :---:         |
|2024-01-01   |	  08:00    |   297332      |
|2024-01-02   |	  10:00    |   297346      |
|2024-01-03   |	  08:45    |   989856      |


📝 Notes
- Ensure that the Google Sheets link is public and accessible.
- Modify the Google Sheets URL in the import_data() function if needed.


Happy Data Processing! 🥂

