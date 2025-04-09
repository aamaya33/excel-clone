from database import create_table_from_csv, check_table

# Create Table 
create_table_from_csv('test.csv', 'test')
check_table('test')
# Append table 
create_table_from_csv('test.csv', 'test')
check_table('test')

# Overwrite table 
create_table_from_csv('test.csv', 'test')
check_table('test')

# Create new table 
create_table_from_csv('test.csv', 'test')
check_table('poopoo')