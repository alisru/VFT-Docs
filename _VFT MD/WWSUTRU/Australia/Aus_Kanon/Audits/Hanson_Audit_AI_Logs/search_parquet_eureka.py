import duckdb
import os

def main():
    parquet_path = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\corpus_1998_to_2025.parquet"
    if not os.path.exists(parquet_path):
        print("Parquet file does not exist")
        return
        
    con = duckdb.connect()
    # Search for Eureka in the body column of any speech by Hanson or anyone
    results = con.execute("""
        SELECT date, displayName, body 
        FROM read_parquet(?) 
        WHERE body ILIKE '%Eureka%' AND displayName ILIKE '%Hanson%'
    """, [parquet_path]).fetchall()
    
    print(f"Found {len(results)} matches for Eureka by Hanson:")
    for date, name, body in results:
        print(f"Date: {date}, Speaker: {name}")
        print(f"Snippet: {body[:300]}...")

if __name__ == "__main__":
    main()
