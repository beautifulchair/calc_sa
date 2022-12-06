import config
import datebase as db
import json

jsonfile_name = 'data/data_sample.json'

with open(jsonfile_name, 'r') as f:
    data = json.load(f)

db_name = config.db_name
host = config.host
user = config.user

with db.Datebase(db_name, host, user) as db_sa:
    db_sa.insert("date", data["date"])
    db_sa.insert("time", data["time"])
    db_sa.do()
