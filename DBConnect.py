import mysql.connector as mycon

def connect() : 
    #con=mycon.connect(host='bvj67gg8fecwpx9he6wn-mysql.services.clever-cloud.com',user='ud6sj5ow3oyzcj4b',password='YkjvfizxxHr7S93pLvjN',database='bvj67gg8fecwpx9he6wn')
    con=mycon.connect(host='mysql-28a7f9b8-text-summarization24.i.aivencloud.com',user='avnadmin',password='AVNS_mEhhLISRJLgrIHCyEuh',database='defaultdb',port=27411)
    return con
def getStates():
    conn = connect()
    #integrated security 
    cursor = conn.cursor() 
    cursor.execute('select state from statemaster;')
    data=cursor.fetchall()
    return data