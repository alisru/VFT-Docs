import duckdb
import os

def main():
    parquet_path = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\corpus_1998_to_2025.parquet"
    if not os.path.exists(parquet_path):
        print("Parquet file does not exist")
        return
        
    con = duckdb.connect()
    # Let's see what unique displayNames exist matching Hanson
    names = con.execute("SELECT DISTINCT displayName FROM read_parquet(?) WHERE displayName ILIKE '%Hanson%'", [parquet_path]).fetchall()
    print("Hanson matches:", names)
    
    # Also let's check how many total rows match Hanson
    count = con.execute("SELECT COUNT(*) FROM read_parquet(?) WHERE displayName ILIKE '%Hanson%'", [parquet_path]).fetchone()
    print("Total rows:", count)

if __name__ == "__main__":
    main()
