import os
import pandas as pd
import pytest
from unittest.mock import patch
from sqlalchemy import create_engine, inspect, MetaData, Table, select, text
import database

@pytest.fixture
def setup_test_csv():
    """Create a test CSV file for testing."""
    data = {
        'id': [1, 2, 3, 4, 5],
        'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'age': [25, 30, 35, 40, 45],
        'salary': [50000.0, 60000.0, 70000.0, 80000.0, 90000.0]
    }
    df = pd.DataFrame(data)
    test_csv_path = 'test_data.csv'
    df.to_csv(test_csv_path, index=False)
    yield test_csv_path
    # Cleanup
    if os.path.exists(test_csv_path):
        os.remove(test_csv_path)

@pytest.fixture
def cleanup_db():
    """Clean up test database files after tests."""
    yield
    for db_file in ['test.db', 'test_new.db', 'test_append.db', 'test_overwrite.db', 'empty_table.db']:
        if os.path.exists(db_file):
            os.remove(db_file)

def test_create_table_from_csv(setup_test_csv, cleanup_db):
    """Test creating a new table from CSV."""
    # Create a new table
    with patch('builtins.input', return_value='1'):  # Mock any potential input
        table = database.create_table_from_csv(setup_test_csv, 'test')
    
    # Verify table was created
    engine = create_engine('sqlite:///test.db')
    inspector = inspect(engine)
    assert 'test' in inspector.get_table_names()
    
    # Verify columns and data
    metadata = MetaData()
    test_table = Table('test', metadata, autoload_with=engine)
    assert len(test_table.columns) == 4  # id, name, age, salary
    
    # SQLAlchemy 2.0 style query
    with engine.connect() as conn:
        result = conn.execute(select(test_table)).fetchall()
        assert len(result) == 5  # 5 rows should be in the table
        
        # Check column types using reflection
        columns = inspector.get_columns('test')
        column_types = {col['name']: str(col['type']) for col in columns}
        
        # Fix: Expected type is BIGINT (from pandas to_sql) instead of INTEGER
        assert 'BIGINT' in column_types['id'] or 'INTEGER' in column_types['id']
        assert 'TEXT' in column_types['name'] 
        assert 'BIGINT' in column_types['age'] or 'INTEGER' in column_types['age']
        assert 'FLOAT' in column_types['salary'] or 'REAL' in column_types['salary']

@patch('builtins.input', return_value='1')
def test_append_to_existing_table(mock_input, setup_test_csv, cleanup_db):
    """Test appending data to an existing table."""
    # First create a table
    database.create_table_from_csv(setup_test_csv, 'test_append')
    
    # Then append data to it
    database.create_table_from_csv(setup_test_csv, 'test_append')
    
    # Check the data count (should be double)
    engine = create_engine('sqlite:///test_append.db')
    with engine.connect() as conn:
        count = conn.execute(text("SELECT COUNT(*) FROM test_append")).scalar()
        assert count == 10  # 5 original rows + 5 appended rows

@patch('builtins.input', return_value='2')
def test_overwrite_existing_table(mock_input, setup_test_csv, cleanup_db):
    """Test overwriting an existing table."""
    # First create a table
    database.create_table_from_csv(setup_test_csv, 'test_overwrite')
    
    # Modify the CSV data
    df = pd.read_csv(setup_test_csv)
    df['age'] = df['age'] + 10  # Increment ages
    df.to_csv(setup_test_csv, index=False)
    
    # Overwrite the table
    database.create_table_from_csv(setup_test_csv, 'test_overwrite')
    
    # Check that table has 5 rows with updated ages
    engine = create_engine('sqlite:///test_overwrite.db')
    with engine.connect() as conn:
        # Check row count
        count = conn.execute(text("SELECT COUNT(*) FROM test_overwrite")).scalar()
        assert count == 5
        
        # Check ages were updated
        ages = conn.execute(text("SELECT age FROM test_overwrite")).fetchall()
        assert all(age[0] >= 35 for age in ages)  # All ages were incremented by 10

@patch('builtins.input', side_effect=['3', 'test_new'])
def test_create_new_table(mock_input, setup_test_csv, cleanup_db):
    """Test creating a new table when a table with the original name exists."""
    # First create a table
    database.create_table_from_csv(setup_test_csv, 'test')
    
    # Then try to create another with the same name, should create a new table with different name
    database.create_table_from_csv(setup_test_csv, 'test')
    
    # Check that both tables exist
    engine1 = create_engine('sqlite:///test.db')
    engine2 = create_engine('sqlite:///test_new.db')
    
    inspector1 = inspect(engine1)
    inspector2 = inspect(engine2)
    
    assert 'test' in inspector1.get_table_names()
    assert 'test_new' in inspector2.get_table_names()

def test_check_table(setup_test_csv, cleanup_db):
    """Test the check_table function."""
    # Create a table first
    with patch('builtins.input', return_value='1'):  # Mock input
        database.create_table_from_csv(setup_test_csv, 'test')
    
    # Test with existing table
    with patch('builtins.print') as mock_print:
        database.check_table('test')
        mock_print.assert_called()  # Should print table information
    
    # Test with non-existent table
    with pytest.raises(ValueError, match="Table nonexistent does not exist"):
        database.check_table('nonexistent')

def test_empty_csv(cleanup_db):
    """Test handling of empty CSV file."""
    # Create an empty CSV file with header but no data
    with open('empty.csv', 'w') as f:
        f.write('col1,col2,col3\n')  # Header only
    
    try:
        # The file has headers but no data
        with pytest.raises(ValueError) as excinfo:
            database.create_table_from_csv('empty.csv', 'empty_table')
        assert "empty" in str(excinfo.value).lower()
    finally:
        if os.path.exists('empty.csv'):
            os.remove('empty.csv')

if __name__ == '__main__':
    pytest.main(['-v'])