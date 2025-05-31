 
from DBConnect import  *
import base64
import os
import mysql.connector as mycon
from Selective import  *
from Abstractive1 import * 
from Abstractive2 import *
import models
def connect() : 
    #con=mycon.connect(host='bvj67gg8fecwpx9he6wn-mysql.services.clever-cloud.com',user='ud6sj5ow3oyzcj4b',password='YkjvfizxxHr7S93pLvjN',database='bvj67gg8fecwpx9he6wn')
    con=mycon.connect(host='mysql-28a7f9b8-text-summarization24.i.aivencloud.com',user='avnadmin',password='AVNS_mEhhLISRJLgrIHCyEuh',database='defaultdb',port=27411)
    return con
 
    
 
def insertSummaryDetails(id=0,userid='NA',title='NA',filename='NA',filedata="NA") : 
    val='NA'
    conn = connect()    
    cursor = conn.cursor()
    print("iiiid= ")
    print(id)
     
    text = models.extract_text(filename,userid)
    print(text)
    print("length="+(str(len(text))))
    parts = []
    max_length=2500
    while len(text) > max_length:
        parts.append(text[:max_length])  # Take first 3000 characters
        text = text[max_length:]  # Remove those characters from text

    if text:  # Add remaining text if any
        parts.append(text)
    
    
    summary1=""
    summary2="NA"
    summary3="NA"
    # Print each part
    for i, part in enumerate(parts, 1):
        print(f"Part {i} (Length {len(part)}):\n{part}\n{'-'*40}")
        summary1=summary1+getSummary_Google(part)+" "
        
 
         
        #summary2=getSummary_FaceBookDS(text)
        #summary3=getSelectiveSummary(text)
    summary2="NA"
    #summary3="NA"
    args = [int(id),userid,title,filename,summary1,summary2,summary3]
    args1=cursor.callproc('InsertSummaryDetails', args)
    #print("Return value:", args1)
    for result in cursor.stored_results():
        val=result.fetchall()
        #print(result.fetchall())
    conn.commit()
    conn.close()
    #print(val[0])
    return "true"

    
 
def getMaxId_Doc():
    conn = connect()
    #integrated security 
    cursor = conn.cursor() 
    cursor.execute('select (ifnull(max(summaryId),1000)+1) as mxid from summarydetails;')
    mxid=0
    for row in cursor: 
        mxid=row[0]
        print(int(mxid)+1)
    conn.close()
    return mxid    

def convertToBase64(message='NA') :
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    print(base64_message)
    return base64_message

def convertFromBase64(base64_message='NA') :
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')
    print(message)
    return message

 