"""
load_and_run.py - builds mubadala.db from the CSV warehouse, executes the
schema, loads every table, then runs all twelve analysis queries and writes
the results to 02_sql/query_results/.
"""
import os, re, sqlite3, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
WH   = os.path.join(ROOT, "01_data", "warehouse")
DB_FINAL = os.path.join(HERE, "mubadala.db")
# NOTE: the mounted workspace does not support SQLite file locking, so the
# database is built on local disk and then copied to its final home.
DB   = "/tmp/mubadala_build.db"
RES  = os.path.join(HERE, "query_results"); os.makedirs(RES, exist_ok=True)

if os.path.exists(DB): os.remove(DB)
con = sqlite3.connect(DB)
con.executescript(open(os.path.join(HERE,"01_create_schema.sql")).read())

order = ["dim_source","dim_platform","dim_sector","dim_geography","dim_asset_class",
         "fact_performance","fact_capital_flow","fact_asset_allocation","fact_credit_rating",
         "fact_holding","fact_transaction","fact_market_data","fact_gfs_financials",
         "fact_gfs_segment","fact_omv_financials","fact_whoop_metrics"]
print("Loading tables:")
for t in order:
    df = pd.read_csv(os.path.join(WH, t + ".csv"))
    df.to_sql(t, con, if_exists="append", index=False)
    print(f"  {t:26s} {len(df):>4} rows")

# referential integrity check
con.execute("PRAGMA foreign_keys = ON")
viol = con.execute("PRAGMA foreign_key_check").fetchall()
print(f"\nForeign-key violations: {len(viol)}")

# run the analysis queries
sql = open(os.path.join(HERE,"03_analysis_queries.sql")).read()
blocks = [b for b in re.split(r"\n(?=-- Q\d+ )", sql) if b.strip().startswith("-- Q")]
print(f"\nRunning {len(blocks)} analysis queries:")
summary = []
for b in blocks:
    qid = re.match(r"-- (Q\d+)", b).group(1)
    stmt = "\n".join(l for l in b.splitlines() if not l.strip().startswith("--")).strip()
    df = pd.read_sql_query(stmt, con)
    df.to_csv(os.path.join(RES, f"{qid}.csv"), index=False)
    summary.append((qid, len(df), ", ".join(df.columns[:4])))
    print(f"  {qid}: {len(df):>3} rows")
con.commit(); con.close()
import shutil; shutil.copy(DB, DB_FINAL)
pd.DataFrame(summary, columns=["query","rows","first_columns"]).to_csv(
    os.path.join(RES,"_index.csv"), index=False)
print("\nDatabase built at", DB_FINAL)
