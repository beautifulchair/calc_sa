import config
import datebase as db

host = config.host
user = config.user
db_name = config.db_name
table_date_name = config.table_date_name
table_time_name = config.table_time_name
default_transportion = config.default_transportion
default_perhour = config.default_perhour

with db.Datebase("db_sa", host, user) as db_sa:
    tb_date = db.Table(table_date_name, db_sa)
    date_id = db.Column("id", tb_date, "SERIAL")
    date_date = db.Column("date", tb_date, "DATE", is_pkey=True)
    date_commute = db.Column(
        "commute", tb_date, "BOOLEAN", is_nullable=True, default="true")
    date_transportsion = db.Column(
        "transportion", tb_date, "INTEGER", is_nullable=True, default=default_transportion)
    date_perhour = db.Column(
        "perhour", tb_date, "INTEGER", is_nullable=True, default=default_perhour)
    tb_date.set_columns(
        [date_id, date_date, date_commute, date_transportsion, date_perhour])

    tb_time = db.Table(table_time_name, db_sa)
    time_date = db.Column("date", tb_time, "DATE",
                          is_pkey=True, fkey=date_date)
    time_start = db.Column("start", tb_time, "TIME")
    time_finish = db.Column("finish", tb_time, "TIME")
    time_rest = db.Column("rest", tb_time, "INTERVAL",
                          default="00:00:00", is_nullable=True)
    tb_time.set_columns([time_date, time_start, time_finish, time_rest])

    db_sa.set_tables([tb_date, tb_time])
    db_sa.do()