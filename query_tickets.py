# coding: utf-8
"""Train tickets query via command-line.

Usage:
	    tickets [-gdtkz] <from> <to> <date>

Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达

Example:
    tickets beijing shanghai 2016-08-25
"""

from docopt import docopt
from stations_code import stations_code
import requests
from prettytable import PrettyTable


class TrainInfo(object):
	#header = 'train station time duration first second softsleep hardsleep hardsit'.split()
	#header = ['train', 'station', 'time', 'duration', 'first', 'second', 'softsleep', 'hardsleep', 'hardsit']
	header = ['车次', '起始站', '出发到达时间', '历时',	'商务座', '特等座', '一等座', '二等座', '高级软卧', ' 软卧', '硬卧', '软座', '硬座',  '无座', '其他']

	def __init__(self,rows,trainTypeList):
		self.rows = rows
		self.trainTypeList = trainTypeList

	def _get_duration(self,row):
		duration = row.get('lishi').replace(':', unicode('小时','utf-8')) + unicode('分','utf-8')
		#duration = row.get('lishi').replace(':', 'h') + 'm'
		if duration.startswith('00'):
			return duration[4:]
		if duration.startswith('0'):
			return duration[1:]
		return duration

	@property
	def trains(self):
		for row in self.rows:
			if(self.trainTypeList.__len__() > 0 and row['station_train_code'][0:1].lower() not in self.trainTypeList):
				continue
			train = [
				#车次
				row['station_train_code'],
				#起始站
				row['from_station_name'] + '\n' + row['to_station_name'],
				#出发到达时间
				row['start_time'] + '\n' + row['arrive_time'],
				#历时
				self._get_duration(row),
				#商务座
				row['swz_num'],
				#特等座
				row['tz_num'],
				#一等座
				row['zy_num'],
				#二等座
				row['ze_num'],
				#高级软卧
				row['gr_num'],
				#软卧
				row['rw_num'],
				#硬卧
				row['yw_num'],
				#软座
				row['rz_num'],
				#硬座
				row['yz_num'],
				#无座
				row['wz_num'],
				#其他
				row['qt_num']
			]
			yield train

	def pretty_print(self):
		pt = PrettyTable(self.header)

#		pt._set_field_names(self.header)
		pt.align['train'] = '1'
		pt.padding_width = 1
		for train in self.trains:
			pt.add_row(train)
		print(pt)
			
trainTypeListAll = ['-g','-d','-t','-k','-z']

def getTrainType(arguments):
	trainTypeListQuery = [] 
	for trainType in trainTypeListAll:
		trainTypeIsQuery = arguments[trainType]
		if(trainTypeIsQuery):
			trainTypeListQuery.append(trainType[1:].lower())
	return trainTypeListQuery

def queryTickets():
	"""command-line interface"""
	arguments = docopt(__doc__)
	from_station = stations_code.get(arguments['<from>'])
	to_station = stations_code.get(arguments['<to>'])
	date = arguments['<date>']
	trainTypeList = getTrainType(arguments)
	url = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate={}&from_station={}&to_station={}'.format(date, from_station, to_station)

	r = requests.get(url,verify=False)
#	print(r.json())
	rows = r.json()['data']['datas']
	trains = TrainInfo(rows,trainTypeList)
	trains.pretty_print()

if __name__ == '__main__':
	queryTickets()

