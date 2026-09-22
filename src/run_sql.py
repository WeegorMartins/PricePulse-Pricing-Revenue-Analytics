import sys
import duckdb
from config.settings import DB_PATH

if len(sys.argv) != 2:
    raise SystemExit("Usage: python src/run_sql.py path/to/file.sql")

sql_path = sys.argv[1]
with open(sql_path, "r", encoding="utf-8") as f:
    sql = f.read()

con = duckdb.connect(str(DB_PATH))
con.execute(sql)
con.close()
print(f"Executed: {sql_path}")
