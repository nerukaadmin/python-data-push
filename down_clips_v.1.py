import datetime
import subprocess as sub
import os
import numpy as np
import pandas as pd
import fnmatch
import re
import pymongo



client=pymongo.MongoClient("mongodb://192.168.3.246:27017/")
db=client["clip_stat"]
col1=db["recived_clips"]


stamp=datetime.datetime.now()
date=stamp.strftime("%Y-%m-%d")
time=stamp.strftime("%X")
path="/home/neo/Desktop/go/quality/Quality_"+date
files=os.listdir(path)
o_csv=[]
for csv in files:
	if fnmatch.fnmatch(csv,'*.csv'):
		o_csv.append(csv)
	else:
		print("Not a csv :%s"%csv)

approved=[]
for app_csv in o_csv:
	x=re.search("approved",app_csv)
	if x is not None:
		approved.append(app_csv)

commented=[]
for com_csv in o_csv:
	x=re.search("commented",com_csv)
	if x is not None:
		commented.append(app_csv)

temp=[]
for csv_app in approved:
	pro_name=re.sub('[^A-Z]','',csv_app)
	df=pd.read_csv(path+"/"+csv_app, index_col=False)
	df_s=df[['Clip','Received Date','Approved Date']]
	f_df=df_s.reset_index().values.tolist()
	print(pro_name)
	print(df_s)
	print(f_df)
	for val in f_df:	
		temp.append(val)
		for val2 in temp:
			print(pro_name)
			print(val2[1])
			print(val2[2])
			print(val2[3])
			in_dict={"site":"Meegoda","clip_name":val[1],"project":pro_name,"status":"approved","upload_date":val[2],"received_date":val[3]}
			col1.insert(in_dict)
			temp.clear()

			
temp2=[]
for csv_app in commented:
	pro_name=re.sub('[^A-Z]','',csv_app)
	df=pd.read_csv(path+"/"+csv_app, index_col=False)
	df_s=df[['Clip','Received Date','Return Date']]
	f_df=df_s.reset_index().values.tolist()
	print(pro_name)
	print(df_s)
	print(f_df)
	for val in f_df:	
		temp2.append(val)
		for val2 in temp2:
			print(pro_name)
			print(val2[1])
			print(val2[2])
			print(val2[3])
			in_dict={"site":"Meegoda","clip_name":val[1],"project":pro_name,"status":"commented","upload_date":val[2],"received_date":val[3]}
			col1.insert(in_dict)
			temp2.clear()			