#coding=utf-8
import pandas as pd, sys, multiprocessing, time
from multiprocessing.pool import ThreadPool
#讀入情緒字庫和權重
def readfileWeight(name):
	words = []
	weight = []
	for line in open(name, 'r', encoding = 'UTF-8'):
		data = line.split("\t")
		if(len(data)== 2):
			words.append(data[0])
			weight.append(data[1].replace('\n', ''))
	return words,weight
#讀入情緒字庫
def readfile(name):
	list = []
	for line in open(name, 'r', encoding = 'UTF-8'):
		list.append(line.replace('\n', ''))
	return list
#匹對字庫(正)
def posmatch(source):
	global positivelist
	for target in positivelist:
		if(source == target):
			return 1;		
	return 0
#匹對字庫(負)
def negmatch(source):
	global negativelist
	for target in negativelist:
		if(source == target):
			return 1;		
	return 0
#批對開始
def start_match(source):
	pospool = ThreadPool(2)
	negpool = ThreadPool(2)
	words=source.split(' ')
	positive=sum(pospool.map(posmatch, words))#匹對正面字庫
	negative=sum(negpool.map(negmatch, words))#匹對負面字庫
	pospool.close()
	negpool.close()
	return positive,negative
	'''
	value = 0
	tmps=source.split(' ')
	global words,weight
	for tmp in tmps:
		num = 0
		for word in words:
			if(tmp == word):
				value = value + int(weight[num])
				num = num + 1
				break				
	return value
	'''
#輸出檔案
def writefile(source, destination) :
	num = 0
	f = open(destination,'a',encoding = 'utf8')
	for i in source: 
		f.write("index = " + str(num) + "\npositive = " + str(i[0]) + " negative = " + str(i[1]) + "\n")
		num = num + 1;
	f.close()
positivelist = readfile('AFINN\\positive-words-Chinese.txt')
negativelist = readfile('AFINN\\negative-words-Chinese.txt')
#(words, weight)= readfilewww('AFINN\\AFINN-111_V2.txt')
if __name__ == '__main__':
	source = pd.read_csv('jieba_test.txt', sep = '\t' ,header = None, encoding = 'utf8')
	source.columns = ['date','string']
	input = source['string'].tolist()
	multiprocessing.freeze_support()#防止windows崩潰
	pool_size = multiprocessing.cpu_count() - 1#cpu個數
	pool = multiprocessing.Pool(pool_size)#process pool
	startTime = time.time()
	resultList=pool.map(start_match,input)#start job
	pool.close()
	pool.join()
	endTime = time.time()
	writefile(resultList,"sentiment.txt")
	print ("used time is ", endTime - startTime)