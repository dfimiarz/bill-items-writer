import pandas as pd
import argparse
import os

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
    df = pd.read_excel(file_path, sheet_name=sheet_name, usecols="A:Q", parse_dates=['LOG_START_TIME'])

    # Drop rows with all empty cells
    df_clean = df.dropna(how="all") 

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