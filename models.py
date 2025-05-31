import mysql.connector as mycon
import base64
import os
from DBOperations import *
 
import urllib.request
 
import re
import fitz  # PyMuPDF for PDFs
import PyPDF2
from docx import Document  
 
import functools 
"""
def connect() : 
    con=mycon.connect(host='bvj67gg8fecwpx9he6wn-mysql.services.clever-cloud.com',user='ud6sj5ow3oyzcj4b',password='YkjvfizxxHr7S93pLvjN',database='bvj67gg8fecwpx9he6wn')
    return con
"""
def connect() : 
    #con=mycon.connect(host='bvj67gg8fecwpx9he6wn-mysql.services.clever-cloud.com',user='ud6sj5ow3oyzcj4b',password='YkjvfizxxHr7S93pLvjN',database='bvj67gg8fecwpx9he6wn')
    con=mycon.connect(host='mysql-28a7f9b8-text-summarization24.i.aivencloud.com',user='avnadmin',password='AVNS_mEhhLISRJLgrIHCyEuh',database='defaultdb',port=27411)
    return con
def login1(userid="NA",pass1="NA") : 
    val='NA'
    auth="failed"
    conn = connect()    
    cursor = conn.cursor()
    args = [userid,pass1]
    args1=cursor.callproc('userlogin1', args)
    print("Return value:", args1)
    for result in cursor.stored_results():
        val=result.fetchall()
        auth="success"
        print(result.fetchall())
    conn.commit()
     
    conn.close()
    return auth
def getStates():
    conn = connect()
    #integrated security 
    cursor = conn.cursor() 
    cursor.execute('select state from statemaster;')
    data=cursor.fetchall()
    conn.close()
    return data
 
def getUsers():
    conn = connect()
    #integrated security 
    cursor = conn.cursor() 
    cursor.execute('select usernm,mobileno,emailid,addr,pincode from userdetails;')
    data=cursor.fetchall()
    conn.close()
    return data
def getHistory(userid="NA"):
    conn = connect()
    #integrated security 
    cursor = conn.cursor() 
    cursor.execute("select * from summarydetails where userid='"+userid+"'")
    data=cursor.fetchall()
    conn.close()
    return data 
def getCities(state="NA"):
    conn = connect()
    #integrated security 
    cursor = conn.cursor() 
    cursor.execute("select city from cities where state='"+state+"'")
    data=cursor.fetchall()
    conn.close()
    return data
 
def login(userid="NA",pass1="NA") : 
    val='NA'
    conn = connect()    
    cursor = conn.cursor()
    args = [userid,pass1]
    args1=cursor.callproc('userlogin', args)
    print("Return value:", args1)
    for result in cursor.stored_results():
        val=result.fetchall()
        print(result.fetchall())
    conn.commit()
 
    conn.close()
    return val
 

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

def insertUser(userid='NA',pass1='NA',name='NA',addr='NA',pincode='NA',mobile="NA",email="NA",gender="Na",dob="NA",state="NA",city="NA",photo="NA") : 
    val='NA'
    conn = connect()    
    cursor = conn.cursor()
    args = [userid,pass1,name,mobile,email,city,state,gender,addr,dob,pincode,photo]
    args1=cursor.callproc('insertUser', args)
    #print("Return value:", args1)
    #for result in cursor.stored_results():
       # val=result.fetchall()
        #print(result.fetchall())
    conn.commit()
    conn.close()
    #print(val[0])
def handle_uploaded_file2(f, userid):
    #  Ensure file has a valid name
    filename = os.path.basename(f.filename)  # Use f.filename instead of f.name
    print("Received filename:", filename)

    #  Check if the filename contains an extension
    if '.' in filename:
        nm, ext = filename.rsplit('.', 1)  # Use rsplit to avoid multiple dots issue
    else:
        print("Error: File does not have an extension")
        return None  # Return None or handle the error appropriately

    print(f"Filename: {nm}, Extension: {ext}")

    # Define the save path correctly
    save_path = os.path.join("../TextSummarizationApp/static/Photos", f"{userid}.{ext}")
    
    # Save file in binary write mode
    with open(save_path, 'wb+') as destination:
        for chunk in f:
            destination.write(chunk)  # In Flask, files are iterables

    print(f"File saved at: {save_path}")
    #return save_path  # Return the saved file path for reference
    return userid+"."+ext
def extract_text(file_path,userid):
    """Extracts text from PDF, TXT, and DOCX files while removing special characters."""
    text = ""
    file_path=os.path.join("../TextSummarizationApp/static/Documents/", userid)+"/"+file_path
    ext = file_path.lower().rsplit(".", 1)[-1]
    print("ext="+ext)
    print("file_path="+file_path)

    try:
        if ext == "pdf":
            with fitz.open(file_path) as pdf:
                text = "\n".join([page.get_text() for page in pdf])
        
        elif ext == "docx":
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])

        elif ext == "txt":
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()

        else:
            raise ValueError("Unsupported file format")

        # Clean text: Remove special symbols
        text = re.sub(r"[^a-zA-Z0-9\s]", "", text)

    except Exception as e:
        print(f"Error extracting text: {e}")
        return None

    return text.strip()

 
 
def handle_uploaded_file3(f,userid):
    id=getMaxId_Doc()
    filename = os.path.basename(f.filename)  # Use f.filename instead of f.name
    print("Received filename:", filename)

    #  Check if the filename contains an extension
    if '.' in filename:
        nm, ext = filename.rsplit('.', 1)  # Use rsplit to avoid multiple dots issue
    else:
        print("Error: File does not have an extension")
        return None  # Return None or handle the error appropriately

    print(f"Filename: {nm}, Extension: {ext}")
     # Define the user's directory path
    user_folder = os.path.join("../TextSummarizationApp/static/Documents", userid)
    
    # Create the directory if it doesn't exist
    os.makedirs(user_folder, exist_ok=True)

    # Define the save path correctly
    save_path = os.path.join("../TextSummarizationApp/static/Documents/"+userid.strip()+"/", f"{str(id)}.{ext}")
    
    # Save file in binary write mode
    with open(save_path, 'wb+') as destination:
        for chunk in f:
            destination.write(chunk)  # In Flask, files are iterables

    print(f"File saved at: {save_path}")
    # Extract text from the file
    

    #return save_path  # Return the saved file path for reference 
    return str(id)+"."+ext; 
def updatePass(userid='NA',pass1='NA') : 
    val='NA'
    conn = connect()    
    cursor = conn.cursor()
    args = [userid,pass1]
    args1=cursor.callproc('updatePass', args)
    #print("Return value:", args1)
    #for result in cursor.stored_results():
       # val=result.fetchall()
        #print(result.fetchall())
    conn.commit()
    conn.close()
 
def getEmail(userid="NA"):
    conn = connect()
    #integrated security 
    cursor = conn.cursor() 
    cursor.execute("select emailid from userdetails where userid='"+userid+"';")
    email="NA"
    for row in cursor: 
        email=row[0]
        print(email)
    conn.close()
    return email 
 