查询12306列车时刻

命令执行格式
python query_tickets.py [-gdzkt] from_station to_station date
[option]:非必选
	-g 高铁
	-d 动车
	-z 直达
	-k 普快
	-t 特快

from_station 和 to_station目前只支持拼音,后续研究下支持中文查询
date: 日期格式，yyyy-MM-dd


