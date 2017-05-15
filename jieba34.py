#coding=utf-8
import pandas as pd
import jieba
import re
import sys
jieba.set_dictionary('dict.txt.big')#變更字典(繁體)
source = pd.read_csv('source.txt', sep = '\t', header = None, encoding = 'utf8')
source.columns = ['date','string']
print(type(source),file=sys.stderr)
f = open('jieba_test.txt','w',encoding = 'utf8')
for index in range(0,len(source.index)):
	if(type(source['string'][index])!=str):
		source['string'][index]=str(source['string'][index])#型態轉換=>str
	tmps = jieba.cut(source['string'][index], cut_all = False)
	source['string'][index] = ''
	for tmp in tmps:
		source['string'][index] += tmp + ' '
	#字串處理 清除數字標點符號
	source['string'][index] = re.sub("[\s+\.\!\/_,$%^*(+\"\'\d]+|[+——！，。？、~@#￥%……&*（）():：?+\d]+", " ",source['string'][index])  
	source['string'][index] = re.sub("[\s+]+", " ",source['string'][index])  
	print("index: "+str(index),file=sys.stderr)
	f.write(source['date'][index]+"\t"+source['string'][index]+"\n")
f.close()