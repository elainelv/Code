#!/usr/bin/python
# -*- coding: UTF-8 -*-
# File: readline-example-3.py
import linecache
import math
import pickle
from functools import cmp_to_key
from numpy import *
from openpyxl import Workbook
import sys
import logging

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def get_data(filename):
	flag = 0
	i = 1
	read_results=[]
	write_results=[]
	while 1:
		line = linecache.getline(filename,i)
		i = i+1
		#print(line)
		if not line:
			break

		if (line.find('arrive') != -1):
			flag = 1
			logging.debug('将要处理数据～ %s'%line)
			continue

		if (line.find('erase operations') != -1):
			flag = 0
			logging.debug('处理完成～')
			break

		if flag==1 :
			tmp=line.split()
			if  len(tmp) <= 1:
				logging.debug('something error occurs')
				break
			#print(tmp)
			if tmp[3]==1:
				write_results.append( (int(tmp[1]),int(tmp[2]),int(tmp[6])) )
			else:
				read_results.append( (int(tmp[1]),int(tmp[2]),int(tmp[6]))  )
	return (read_results,write_results)


def savexls(data,filename):
	wb = Workbook()
	flag = 0

	result = {}
	#logging.debug("data:")
	#logging.debug(data)
	for item in data:
		tmp=[]
		for it in data:

			#logging.debug("item:   it")
			#logging.debug((item,it))

			if(item[1] == it[1]) and ( (item[1] not in result)) :

				tmp.append( (it[0],it[2]) )
				#logging.debug(tmp)
		if( len(tmp) >0):
			result[ item[1] ]=tmp

	#logging.debug("result:")	
	#logging.debug(result)
	for item in result.items():
		if flag == 0:
			ws = wb.active
			logging.debug(item)
			ws.title = str(item[0])
			logging.debug(item)
			addr_list = [ i[0] for i in item[1]]
			latency_list = [ i[1] for i in item[1]]
			ws.append(addr_list)
			ws.append(latency_list)
			flag =1
		else:
			ws = wb.create_sheet(title=str(item[0]))

			addr_list = [ i[0] for i in item[1]]
			latency_list = [ i[1] for i in item[1]]
			ws.append(addr_list)
			ws.append(latency_list)		

	# Save the file
	wb.save(filename)

def main():

	filename = "USR_0_output"
	read_results=[]
	write_results=[]

	read_results,write_results = get_data(filename)

	savexls(read_results,"read.xlsx")

	savexls(write_results,"write.xlsx")




if __name__ == '__main__':

	main()
	#decompression()
	#test()