text:
	python3 convert_txt_to_json.py

db:
	python3 insert_json_to_database.py

calc:
	python3 calc_sum_salary.py

show:	
	echo "table date" | psql db_sa
