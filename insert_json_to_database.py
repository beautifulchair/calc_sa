import config
import datebase as db
import json
import os

files = sorted(os.listdir("./data"))
print("\n".join(files))
for file_name in files:
    if (not file_name.endswith('.json')):
        print(f"data/{file_name} is not json file")
        continue
    with open(f"data/{file_name}", 'r') as f:
        data = json.load(f)

    db_name = config.db_name
    host = config.host
    user = config.user

    with db.Datebase(db_name, host, user) as db_sa:
        db_sa.insert("date", data["date"])
        db_sa.insert("time", data["time"])
        db_sa.do()
