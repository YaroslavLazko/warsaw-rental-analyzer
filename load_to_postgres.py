import pandas as pd
from sqlalchemy import create_engine

def load_data_to_postgres():
    csv_file = "warsaw_rentals_cleaned.csv"
    
    print(f"Loading cleaned data from '{csv_file}'...")
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"Error: The file '{csv_file}' was not found. Please run the cleaning script first.")
        return

    # --- DATABASE CONFIGURATION ---
    # Update these variables to match your local PostgreSQL setup
    db_user = "postgres"           # Default PostgreSQL username
    db_password = "CfifGhjwrsd0258*"
    db_host = "localhost"          # Running on your local machine
    db_port = "5432"               # Default PostgreSQL port
    db_name = "warsaw_rentals"       # The database you just created in pgAdmin
    
    # Create the connection string (SQLAlchemy format)
    engine_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    print(f"Connecting to PostgreSQL database '{db_name}' at {db_host}...")
    try:
        # Create the database engine
        engine = create_engine(engine_url)
        
        # Define the table name
        table_name = "warsaw_rentals"
        print(f"Uploading {len(df)} rows to table '{table_name}'...")
        
        # Upload the dataframe to PostgreSQL
        # if_exists='replace' means it will drop the table if it exists and create a new one.
        # index=False prevents pandas from writing the row indices as a separate column.
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        
        print("-" * 50)
        print("Success! Data upload completed.")
        print("You can now open pgAdmin, refresh your database, and check the table.")
        print("-" * 50)
        
    except Exception as e:
        print(f"\nDatabase error occurred: {e}")
        print("Please check your password, port, and database name.")

if __name__ == "__main__":
    load_data_to_postgres()