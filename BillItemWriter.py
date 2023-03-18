import pandas as pd

def main():
    print("Bill Items import script")

    file_path = "testfile.xlsx"

    df = pd.read_excel(file_path, sheet_name="Billing", usecols="A:Q")

    df_clean = df.dropna(how="all") 

    df_data = df_clean.loc[:,["SERVICE_ID","LOG_PI", "LOG_DETAILS", "LOG_START_TIME", "LOG_QUANTITY", "LOG_RATE","LOG_NOTES"]]

    df_data["SERVICE_ID"] = df_data["SERVICE_ID"].astype(int)

    rows_of_tuples = [tuple(x) for x in df_data.to_records(index=False)]

    print(rows_of_tuples)

if __name__ == "__main__":
    main()