import pandas as pd
import os

def calculate_savings_totals(df1, df2, df3):
    try:
        # Calculate the total for each DataFrame
        total1 = df1["Saved"].sum()
        total2 = df2["Saved"].sum()
        total3 = df3["Saved"].sum()

        # Calculate the combined total
        combined_total = total1 + total2 + total3

        # Format totals as dollar amounts
        total1_formatted = "${:,.2f}".format(total1)
        total2_formatted = "${:,.2f}".format(total2)
        total3_formatted = "${:,.2f}".format(total3)
        combined_total_formatted = "${:,.2f}".format(combined_total)

        # Print the results
        print(f"Total savings for Contracts: {total1_formatted}")
        print(f"Total savings for Grants: {total2_formatted}")
        print(f"Total savings for Real Estate: {total3_formatted}")
        print(f"Combined total savings: {combined_total_formatted}")

        # Return the results for further use if needed
        return total1_formatted, total2_formatted, total3_formatted, combined_total_formatted
    except KeyError:
        print("Error: One or more DataFrames are missing the 'savings' column.")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    # Paths to the CSV files
    file1 = "./csv_output/DogeContractsSavingsTable.csv"
    file2 = "./csv_output/DogeGrantsSavingsTable.csv"
    file3 = "./csv_output/DogeRealEstateSavingsTable.csv"

    # Verify files exist
    if not os.path.exists(file1):
        print(f"Error: File '{file1}' not found.")
        exit(1)
    if not os.path.exists(file2):
        print(f"Error: File '{file2}' not found.")
        exit(1)
    if not os.path.exists(file3):
        print(f"Error: File '{file3}' not found.")
        exit(1)

    # Load DataFrames
    try:
        df1 = pd.read_csv(file1)
        df2 = pd.read_csv(file2)
        df3 = pd.read_csv(file3)

        # Calculate and print totals
        calculate_savings_totals(df1, df2, df3)
    except Exception as e:
        print(f"Error loading DataFrames: {e}")
        exit(1)
