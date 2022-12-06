import config
import datebase as db
import json

jsonfile_name = 'data/data_sample.json'

with open(jsonfile_name, 'r') as f:
    data = json.load(f)

date = f"{int(data['date']['year']):04}-{int(data['date']['month']):02}-{int(data['date']['day']):02}"
commute = f"{data['comute']}"
start = f"{int(data['start']['hour'])}:{int(data['start']['minute'])}"
finish = f"{int(data['finish']['hour'])}:{int(data['finish']['minute'])}"
rest = f"{int(data['rest']['hour'])}:{int(data['rest']['minute'])}"

db_name = config.db_name
host = config.host
user = config.user

with db.Datebase(db_name, host, user) as db_sa:
    db_sa.insert("date", {"date": date})
    db_sa.insert("time", {"date": date, "start": start,
                 "finish": finish, "rest": rest})
    db_sa.do()
