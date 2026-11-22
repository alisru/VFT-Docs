import sqlite3, time

con = sqlite3.connect('data/chats.sqlite')
t0 = time.time()
con.execute("INSERT INTO chunks_fts(chunks_fts) VALUES('rebuild')")
con.commit()
print(f"Rebuild took: {(time.time() - t0)*1000:.1f} ms")
con.close()


