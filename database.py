from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped
import pandas as pd

class Base(DeclarativeBase):
    pass

def create_table_from_csv(file_path, table_name):

    df = pd.read_csv(file_path)
    if not df: 
        raise ValueError("The CSV file is empty or not found.")
    if df.empty:
        raise ValueError("The CSV file is empty.")
    
    # What if CSV has already been uploaded? 
    # check if table exists -> if yes, ask if they want to append, overwrite, or create new table 



    # Create type map for the table 
    type_map = {
            'int64': Integer,
            'object': String,
            'float64': Integer
        }
    try: 
        
    



