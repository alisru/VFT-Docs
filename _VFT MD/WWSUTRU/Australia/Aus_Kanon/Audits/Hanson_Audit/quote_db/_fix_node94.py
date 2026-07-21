import sqlite3, datetime

DB = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db"
ARCH = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\Sources_Archive"
now = datetime.datetime.now().isoformat(timespec="seconds")

conn = sqlite3.connect(DB)

def read(fn):
    with open(fn, "r", encoding="utf-8") as f:
        return f.read()

cir_text = read(ARCH + r"\onenation_cir.txt")
p2001_text = read(ARCH + r"\onenation_2001.txt")

for key, url, arch_file, stype, text in [
    ("onenation_cir", "https://www.onenation.org.au/citizen-initiated-referenda",
     ARCH + r"\onenation_cir.txt", "party_platform", cir_text),
    ("onenation_2001", "https://parlinfo.aph.gov.au/parlInfo/search/display/display.w3p;orderBy=alphaAss;query=(Dataset:partypol,lcatalog,jrnart,jrnart88%20SearchCategory_Phrase:%22library%22)%20Party_Phrase:%22one%20nation%22;rec=13",
     ARCH + r"\onenation_2001.txt", "party_platform_historical", p2001_text),
]:
    conn.execute("""
        INSERT INTO hanson_sources (citation_key, archive_file, url, date_checked, full_text, source_type, status, node_count, last_checked)
        VALUES (?,?,?,?,?,?,?,?,?)
        ON CONFLICT(citation_key) DO UPDATE SET
            archive_file=excluded.archive_file, url=excluded.url, date_checked=excluded.date_checked,
            full_text=excluded.full_text, source_type=excluded.source_type, status=excluded.status,
            last_checked=excluded.last_checked
    """, (key, arch_file, url, now, text, stype, "verified", 1, now))

new_quote = ("One Nation will push for the introduction of a Citizens Initiated Referenda, "
             "enabling Australian citizens to put forward legislation or a referendum question "
             "without waiting for politicians to listen and act.")

cur = conn.execute("SELECT status FROM nodes WHERE node_id=94")
old_status = cur.fetchone()[0]

conn.execute("""
    UPDATE nodes SET citation_key='onenation_cir', quote_in_doc=?, is_literal_quote=1,
        status='verified', fuzzy_score=1.0, last_checked=?
    WHERE node_id=94
""", (new_quote, now))

conn.execute("""
    INSERT INTO status_history (node_id, old_status, new_status, changed_by, note, changed_at)
    VALUES (94, ?, 'verified', 'manual',
        'Replaced generic /policies hub citation with the specific Citizen Initiated Referenda policy page; quote content itself was already accurate to real One Nation policy, just mis-cited to a thin JS hub page. Cross-verified against the party''s Feb 2001 Queensland platform (ParlInfo HGH36) which carries the same Community Based Referenda (Citizens Initiated) commitment.',
        ?)
""", (old_status, now))

conn.commit()
print("node 94 updated:", old_status, "-> verified")
conn.close()
