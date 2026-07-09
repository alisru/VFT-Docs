import duckdb

def check_parquet():
    conn = duckdb.connect()
    # Query one row for Albanese
    res = conn.execute("""
        SELECT date, displayName, name, "order", speech_no, "page.no", 
               CAST("time.stamp" AS VARCHAR) as timestamp, 
               "name.id", electorate, partyAbbrev, partyName, 
               SUBSTR(body, 1, 100) as body_snippet, 
               fedchamb_flag, question, answer, q_in_writing, div_flag, 
               uniqueID, gender, member, senator, interject
        FROM 'e:/Vector Field Theory/VFT Docs/_VFT MD/WWSUTRU/Australia/Aus_Kanon/corpus_1998_to_2025.parquet' 
        WHERE displayName = 'Albanese, Anthony'
        LIMIT 1
    """).fetchdf()
    print("Albanese sample row values:")
    print(res.iloc[0].to_dict())

if __name__ == '__main__':
    check_parquet()
