import re
import json

textfile_name = 'data/data_sample.txt'
jsonfile_name = 'data/data.json'

# read from data.txt, and write to text
with open(textfile_name, 'r') as f:
    lines = f.readlines()
text = "_".join(lines)
text = text.replace('\n', '')

# find data from text
p_date = re.compile(r'.*勤務日：([0-9]+)-([0-9]+)-([0-9]+).*')
p_comute = re.compile(r'.*出勤の別：(出社|リモート).*')
p_start = re.compile(r'.*開始時間：([0-9]+):([0-9]+).*')
p_finish = re.compile(r'.*終了時間：([0-9]+):([0-9]+).*')
p_rest = re.compile(r'.*休憩時間：([0-9]+):([0-9]+).*')

m_date = p_date.match(text)
m_comute = p_comute.match(text)
m_start = p_start.match(text)
m_finish = p_finish.match(text)
m_rest = p_rest.match(text)

date_list = list(m_date.groups())
comute_list = list(m_comute.groups())
start_list = list(m_start.groups())
finish_list = list(m_finish.groups())
rest_list = list(m_rest.groups())

# make dict
d_dict = {'date': {'year': date_list[0], 'month': date_list[1], 'day': date_list[2]},
          'comute': comute_list[0] == '出社',
          'start': {'hour': start_list[0], 'minute': start_list[1]},
          'finish': {'hour': finish_list[0], 'minute': finish_list[1]},
          'rest': {'hour': rest_list[0], 'minute': rest_list[1]}}
"""		
d_dict2 = {'date_year': date_list[0],'date_month': date_list[1], 'date_day': date_list[2],
		'comute': comute_list[0]=='出社',
		'start_hour': start_list[0], 'start_minute': start_list[1],
		'finish_hour': finish_list[0], 'finish_minute': finish_list[1], 
		'rest_hour': rest_list[0], 'minute_rest': rest_list[1]}
"""

# convert dict to json
with open(jsonfile_name, mode="w") as f:
    json.dump(d_dict, f, indent=4)