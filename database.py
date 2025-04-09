from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Date, inspect, MetaData, Table, select, text

from sqlalchemy.orm import DeclarativeBase, Session
import pandas as pd

class Base(DeclarativeBase):
    pass

def create_table_from_csv(file_path, table_name):

    df = pd.read_csv(file_path)
    if df.empty:
        raise ValueError("The CSV file is empty.")


    # Create type map for the table 
    type_map = {
            'int64': Integer,
            'object': String(255),  # Adding default length for strings
            'float64': Float,
            'bool': Boolean,
            'datetime64[ns]': DateTime,
            'date': Date,
            'category': String(255)
        }
    
    try: 
        engine = create_engine(f'sqlite:///{table_name}.db')
        
        inspector = inspect(engine)
        metadata = MetaData()

        # TODO: REFACTOR THIS 
        # tables = inspector.get_table_names()
        if table_name in inspector.get_table_names():
            # temporary logic to test 
            print(f"The table {table_name} already exists. What would you like to do?")
            print("1. Append data")
            print("2. Overwrite data")
            print("3. Create a new table")
            choice = input("Enter your choice (1/2/3): ")

            if choice == '1':
                # append data
                print("Appending data to the existing table.")
                existing_table = Table(table_name, metadata, autoload_with=engine)
                df.to_sql(table_name, engine, if_exists='append', index=False)
                return existing_table
            
            elif choice == '2': 
                print("Overwriting data in the existing table.")
                existing_table = Table(table_name, metadata, autoload_with=engine)
                # Drop the existing table
                existing_table.drop(engine)
                metadata.remove(existing_table)
                # Create a new table
                cols = []
                for i, (col_name, dtype) in enumerate(df.dtypes.items()):
                    col_type = type_map.get(str(dtype), String(255))
                    is_primary_key = i == 0
                    cols.append(Column(col_name, col_type, primary_key=is_primary_key))
                table = Table(table_name, metadata, *cols)
                metadata.create_all(engine)
                df.to_sql(table_name, engine, if_exists='replace', index=False)
                return table
            
            elif choice == '3':
                print("Creating a new table.")
                new_name = input("Enter the new table name: ")
                cols = []
                for i, (col_name, dtype) in enumerate(df.dtypes.items()):
                    col_type = type_map.get(str(dtype), String(255))
                    is_primary_key = i == 0
                    cols.append(Column(col_name, col_type, primary_key=is_primary_key))
                new_engine = create_engine(f'sqlite:///{new_name}.db')
                table = Table(new_name, metadata, *cols)
                metadata.create_all(new_engine)
                df.to_sql(new_name, new_engine, if_exists='replace', index=False)
                return table
        else:
            cols = [] 

            for i, (col_name, dtype) in enumerate(df.dtypes.items()):
                col_type = type_map.get(str(dtype), String(255))  # Default to String if type not found
                is_primary_key = i == 0
                cols.append(Column(col_name, col_type, primary_key=is_primary_key))
            
            table = Table(table_name, metadata, *cols)
            metadata.create_all(engine)

            # Insert data into the table I LOEV YOU SQLALCHEMY 
            df.to_sql(table_name, engine, if_exists='replace', index=False)

            return table
    except Exception as e: 
        raise ValueError(f"An error occurred while creating the table: {e}")


    # What if CSV has already been uploaded? 
    # check if table exists -> if yes, ask if they want to append, overwrite, or create new table 

def check_table(table_name):
    try: 
        engine = create_engine(f'sqlite:///{table_name}.db')

        inspector = inspect(engine)
        if table_name not in inspector.get_table_names():
            raise ValueError(f"Table {table_name} does not exist.")
        metadata = MetaData()
        table = Table(table_name, metadata, autoload_with=engine)

        session = Session(engine)
        stmt = select(table)
        result = session.execute(stmt).fetchall()

        if not result: 
            print(f"The table {table_name} is empty.")
        else: 
            columns = table.columns.keys()
            print(f"The table {table_name} has data:")
            print(f"{columns}")
            for row in result:
                print(row)
    except Exception as e:
        raise ValueError(f"An error occurred while checking the table: {e}")
