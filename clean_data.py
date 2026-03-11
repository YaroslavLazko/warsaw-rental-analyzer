import pandas as pd

def clean_real_estate_data(input_file, output_file):
    print(f"Loading data from '{input_file}'...")
    # Read the raw CSV file
    df = pd.read_csv(input_file)
    
    print(f"Initial number of rows: {len(df)}")
    
    # 1. Remove duplicates
    df_cleaned = df.drop_duplicates(subset=['id'], keep='first')
    print(f"Rows after removing duplicates: {len(df_cleaned)}")
    
    # 2. Basic cleaning of missing values
    df_cleaned = df_cleaned.dropna(subset=['price', 'area'])
    print(f"Rows after dropping missing price/area: {len(df_cleaned)}")
    
    # 3. Data type conversion
    df_cleaned['price'] = pd.to_numeric(df_cleaned['price'], errors='coerce')
    df_cleaned['area'] = pd.to_numeric(df_cleaned['area'], errors='coerce')
    
    # --- FIXED: Map string room counts to integers ---
    room_mapping = {
        'ONE': 1, 
        'TWO': 2, 
        'THREE': 3, 
        'FOUR': 4,
        'FIVE': 5, 
        'SIX': 6, 
        'SEVEN': 7, 
        'EIGHT': 8,
        'NINE': 9, 
        'TEN': 10, 
        'MORE': 10  # Treat 'MORE' as 10 (or 5+ depending on context, but 10 is a safe upper bound integer)
    }
    
    # Convert to string, uppercase to match the dictionary, replace, then convert to numeric
    df_cleaned['rooms'] = df_cleaned['rooms'].astype(str).str.upper().replace(room_mapping)
    df_cleaned['rooms'] = pd.to_numeric(df_cleaned['rooms'], errors='coerce').fillna(0).astype(int)
    
    # Save the cleaned dataset
    df_cleaned.to_csv(output_file, index=False, encoding='utf-8')
    print(f"\nCleaned data successfully saved to: '{output_file}'")
    
    # Display short statistics for verification
    print("\nPrice statistics (PLN):")
    print(df_cleaned['price'].describe().round(2))
    
    print("\nRooms distribution:")
    print(df_cleaned['rooms'].value_counts())

if __name__ == "__main__":
    raw_file = "warsaw_rentals_raw.csv"
    cleaned_file = "warsaw_rentals_cleaned.csv"
    
    clean_real_estate_data(raw_file, cleaned_file)