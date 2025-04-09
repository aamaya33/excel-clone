from database import create_table_from_csv, check_table

# Add this at the end of main.py
def cli_main():
    """Entry point for CLI command."""
    try:
        print("Excel Clone - CSV to SQLite Tool")
        # Add your CLI interface logic here
        csv_path = input("Enter path to CSV file: ")
        table_name = input("Enter table name: ")
        create_table_from_csv(csv_path, table_name)
        check_table(table_name)
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    return 0

if __name__ == "__main__":
    cli_main()