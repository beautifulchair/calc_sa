import psycopg2
import os
from dotenv import load_dotenv
load_dotenv(override=True)

year = int(input("year= "))
month = int(input("month= "))

if ((year not in [2022, 2023]) or month not in range(1, 13)):
    print("exit: input suitable year and month")
    exit()

year_month = f"{year}_{month}"
view_time = f"time_{year_month}"
view_date = f"date_{year_month}"
view_result = f"result_{year_month}"
view_sum = f"sum_{year_month}"

with psycopg2.connect(host=os.getenv('DB_SA_HOST'), user=os.getenv("DB_SA_USER"), database=os.getenv("DB_NAME")) as conn:
    with conn.cursor() as cursor:
        def print_table(table):
            cursor.execute(f"Select * From {table}")
            rows = cursor.fetchall()
            for row in rows:
                print(row)
            print()

        cursor.execute(f"DROP VIEW IF EXISTS {view_sum}")
        cursor.execute(f"DROP VIEW IF EXISTS {view_result}")
        cursor.execute(f"DROP VIEW IF EXISTS {view_time}")
        cursor.execute(f"DROP VIEW IF EXISTS {view_date}")

        cursor.execute(f"""CREATE VIEW {view_time}
                            AS SELECT date, EXTRACT(HOUR FROM finish-start-rest)*60 + EXTRACT(MINUTE FROM finish-start-rest) As time
                            FROM time
                            WHERE EXTRACT(YEAR FROM date) = {year} AND EXTRACT(MONTH FROM date) = {month}""")
        # print_table(view_time)

        cursor.execute(f"""CREATE VIEW {view_date}
                            AS SELECT date, transportion*commute::int AS transportion, perhour
                            FROM date
                            WHERE EXTRACT(YEAR FROM date) = {year} AND EXTRACT(MONTH FROM date) = {month}""")
        # print_table(view_date)

        cursor.execute(f"""CREATE VIEW {view_result}
                            AS SELECT {view_date}.date, {view_time}.time/60::float, {view_date}.transportion::int,  {view_date}.perhour*{view_time}.time/60::float AS salary
                            FROM {view_date}
                            INNER JOIN {view_time}
                            ON {view_date}.date = {view_time}.date""")
        print_table(view_result)

        cursor.execute(f"""CREATE VIEW {view_sum}
                            AS SELECT SUM(transportion) AS transportion, SUM(salary) AS salary, SUM(transportion)+SUM(salary) AS sum
                            FROM {view_result}""")
        print_table(view_sum)
