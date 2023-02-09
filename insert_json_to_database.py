import database as db
import json
import os
from dotenv import load_dotenv
load_dotenv(override=True, dotenv_path=".env.local")
db_name = os.getenv("DB_NAME")
host = os.getenv("DB_SA_HOST")
user = os.getenv("DB_SA_USER")

files = sorted(os.listdir("./data"))
print("\n".join(files))
for file_name in files:
    if (not file_name.endswith('.json')):
        print(f"data/{file_name} is not json file")
        continue
    with open(f"data/{file_name}", 'r') as f:
        data = json.load(f)

    with db.Datebase(db_name, host, user) as db_sa:
        db_sa.insert("date", data["date"])
        db_sa.insert("time", data["time"])
        db_sa.do()
