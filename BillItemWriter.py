import pandas as pd
import argparse
import os

# Function to check if any of the required columns have an empty values. 
def checkMissingValues(df, required_columns=[]):

    # Create a hashmamp to store row numbers of empty rows
    missing_values = {}

    # Generate a warning if the required_columns list is empty
    if not required_columns:
        print("\033[93mWarning: required_columns list is empty\033[0m")
        return missing_values

    # Fine the rows that are empty for all columns
    empty_rows = df[df.isnull().all(axis=1)].index.tolist()

    # Loop through the required columns
    for column in required_columns:
        # Get the row numbers of empty rows for the current column
        empty_rows_for_column = df[df[column].isnull()].index.tolist()
        # Keep only rows that are not in the empty_rows list
        empty_rows_for_column = list(set(empty_rows_for_column) - set(empty_rows))

        # Add 2 to the row numbers to account for the header and the first row
        empty_rows_for_column = [x + 2 for x in empty_rows_for_column]

        # Add the column name and the row numbers to the hashmap if there are empty rows found. Sort the row numbers.
        if empty_rows_for_column:
            missing_values[column] = sorted(empty_rows_for_column)
    
    return missing_values

def main():
    print("Bill Items import script")

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", help="Path to the Excel file to import", type=str)
     # Add an optional argument to specify the sheet name
    parser.add_argument("-s", "--sheet_name", help="Name of the sheet to import", type=str, default="Billing")
    args = parser.parse_args()

    #check if file exists
    if not os.path.exists(args.file_path):
        # Print error message in red and exit
        print("\033[91mFile does not exist\033[0m")
        return

    file_path = args.file_path
    sheet_name = args.sheet_name


    # Check if sheet exists
    if sheet_name not in pd.ExcelFile(file_path).sheet_names:
        # Print error message in red and exit
        print("\033[91mSheet does not exist\033[0m")
        return


    # Read the Excel file
    df = pd.read_excel(file_path, sheet_name=sheet_name, usecols="A:U", parse_dates=['LOG_START_TIME'])

     # List of culumns that must not be empty
    required_columns = ["SERVICE_ID", "LOG_PI", "LOG_DETAILS", "LOG_START_TIME", "LOG_QUANTITY", "LOG_RATE","CHECKED"]

     # Check if any of the required columns have an empty values.
    missing_values = checkMissingValues(df, required_columns)
    
    if missing_values:
        # Print error message in red and exit
        print("\033[91mRequired values not found in the following rows\033[0m")
        # Print the row numbers for each column
        for column, rows in missing_values.items():
            print(column, ": ", rows)
        return

    # Drop rows with all empty cells
    df_clean = df.dropna(how="all") 

    # Print the number of rows that will be processed in green
    print("\033[92m{} rows will be processed\033[0m".format(len(df_clean)))

     # Make sure the CHECKED column values are equal to 1. If not, print an error message with row number and exit
    if not (df_clean["CHECKED"] == 1).all():
        print("\033[91mAll rows should be marked as checked. Please check the CHECKED column\033[0m")
        return

    # Extract the columns that we need
    df_data = df_clean.loc[:,["SERVICE_ID","LOG_PI", "LOG_DETAILS", "LOG_START_TIME", "LOG_QUANTITY", "LOG_RATE","LOG_NOTES"]]   

    # Convert the SERVICE_ID column to int
    df_data["SERVICE_ID"] = df_data["SERVICE_ID"].astype(int)

    # Convert the LOG_PI column to int
    df_data["LOG_PI"] = df_data["LOG_PI"].astype(int)

    # Convert LOG_START_TIME to string
    df_data["LOG_START_TIME"] = df_data["LOG_START_TIME"].dt.strftime("%Y-%m-%dT%H:%M:%S")

            

    rows_of_tuples = [tuple(x) for x in df_data.to_numpy()]

    print(rows_of_tuples)

if __name__ == "__main__":
    main()