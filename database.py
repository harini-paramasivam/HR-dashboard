import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection parameters
DB_HOST = os.getenv("PGHOST")
DB_NAME = os.getenv("PGDATABASE")
DB_USER = os.getenv("PGUSER")
DB_PASSWORD = os.getenv("PGPASSWORD")
DB_PORT = os.getenv("PGPORT")

# Create a connection to the database
def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )

# Create the necessary tables if they don't exist
def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create employees table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id SERIAL PRIMARY KEY,
        age INTEGER,
        gender VARCHAR(10),
        department VARCHAR(100),
        education VARCHAR(100),
        location VARCHAR(100),
        salary INTEGER,
        performance INTEGER,
        years_service INTEGER
    )
    ''')
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print("Tables created successfully")

# Function to populate the database with sample data
def populate_sample_data(df):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM employees")
    count = cursor.fetchone()[0]
    
    # Only insert if table is empty
    if count == 0:
        # Convert dataframe to list of tuples for bulk insert
        data = [
            (
                row['Age'],
                row['Gender'],
                row['Department'],
                row['Education'],
                row['Location'],
                row['Salary'],
                row['Performance'],
                row['YearsService']
            )
            for _, row in df.iterrows()
        ]
        
        # Bulk insert data
        execute_values(
            cursor,
            '''
            INSERT INTO employees (
                age, gender, department, education, location, 
                salary, performance, years_service
            ) VALUES %s
            ''',
            data
        )
        
        conn.commit()
        print(f"Inserted {len(data)} records into employees table")
    else:
        print(f"Data already exists in employees table ({count} records)")
    
    cursor.close()
    conn.close()

# Function to retrieve all employees from the database
def get_all_employees():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()
    
    # Get column names
    column_names = [desc[0] for desc in cursor.description]
    
    cursor.close()
    conn.close()
    
    # Convert to DataFrame
    df = pd.DataFrame(rows, columns=column_names)
    
    # Rename columns to match our application
    column_mapping = {
        'id': 'ID',
        'age': 'Age',
        'gender': 'Gender',
        'department': 'Department',
        'education': 'Education',
        'location': 'Location',
        'salary': 'Salary',
        'performance': 'Performance',
        'years_service': 'YearsService'
    }
    
    df = df.rename(columns=column_mapping)
    
    return df

# Initialize the database (create tables if needed)
def init_database(sample_data_df=None):
    try:
        # Create tables
        create_tables()
        
        # Populate with sample data if provided
        if sample_data_df is not None:
            populate_sample_data(sample_data_df)
            
        return True
    except Exception as e:
        print(f"Database initialization error: {e}")
        return False