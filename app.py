from flask import Flask, render_template, request, redirect, url_for, session, flash,jsonify
import random
import ast
from datetime import date
import models
from sendMail import *
from DBOperations import *  
app = Flask(__name__)
app.secret_key = "text_summarization2024"  # Set a unique, strong secret key
@app.context_processor
def inject_session():
    return dict(session=session)
@app.route('/')  
def index():
    data=models.getStates()
    return render_template("index.html",list=data)
@app.route('/home')  
def home():
    data=models.getStates()
    return render_template("index.html",list=data)
@app.route('/upload')  
def upload():
    return render_template("upload.html")
 
@app.route("/user")
def user():
    if "userid" not in session:
        return redirect(url_for("index"))
    userid = session["userid"]  
    data = models.getHistory(userid)
    return render_template("user.html", list=data, session=session)

@app.route("/admin")
def admin(): 
    if "userid" not in session:
        return redirect(url_for("index"))
    data = models.getUsers()
    return render_template("admin.html", list=data, session=session)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/otpverification", methods=["POST"])
def otpverification1():
    if request.method == 'POST':
        userid = request.form.get("userid")  
        email = request.form.get("email")  
        otp = request.form.get("otp")  
        otp1 = session.get("otp")
        pass1 = str(random.randint(1111, 9999))
        if otp == otp1:
            models.updatePass(userid, pass1)
            sendMail.sendotp1(pass1, email)
            return render_template("Success.html", mess="Password Sent on Email Successfully...") 
        else:
            return render_template("Success.html", mess="OTP Authentication Failed!!")

@app.route("/sendotp", methods=["POST"])
def sendotp():
    if request.method == 'POST':
        docid = request.form.get("docid")  
        docpath = request.form.get("docpath")  
        seckey = request.form.get("seckey")  
        emailid = session.get("emailid")
        otp = str(random.randint(1111, 9999))
        session["otp"] = otp
        sendMail.sendotp(otp, emailid)
        today = date.today()
        dt = today.strftime("%d/%m/%Y")
        models.insertUsageLog(session["userid"], 'email', dt)
        return render_template("otpauth.html", docid=docid, docpath=docpath, seckey=seckey, session=session)

@app.route("/Cities")
def Cities():
    data = models.getCities(request.args.get("state"))    
    return render_template("cities.html", list=data)

@app.route("/login/", methods=["POST"])
def login():
    if request.method == "POST":
        userid = request.form.get("userid")
        pass1 = request.form.get("pass")
        val = models.login(userid, pass1)
        
        if val and len(val) > 0:
            session["user"] = {"userid": val[0][0], "utype": val[0][3], "username": val[0][2]}
            session["userid"] = val[0][0]
            session["utype"] = val[0][3]
            session["emailid"] = models.getEmail(val[0][0])
            
            if val[0][3] == "admin":
                return redirect(url_for("admin"))
            elif val[0][3] == "user":
                return redirect(url_for("user"))
            else:
                return render_template("Success.html", mess="Authentication Failed!!")
        else:
            return render_template("Success.html", mess="Authentication Failed!!")

@app.route("/registeruser/", methods=["POST"])
def register_user():
    if request.method == "POST":
        userid = request.form.get("userid")   
        usernm = request.form.get("usernm")
        pswd = request.form.get("pswd")
        emailid = request.form.get("emailid")
        mobileno = request.form.get("mobileno")
        gender = request.form.get("gender")
        pincode = request.form.get("pincode")
        addr = request.form.get("addr")
        state = request.form.get("state")
        cities = request.form.get("cities")
        dob = request.form.get("dob")
        print(dob)
        file = request.files.get("file")
        photo = models.handle_uploaded_file2(file, userid)  
        
        models.insertUser(userid, pswd, usernm, addr, pincode, mobileno, emailid, gender, dob, state, cities, photo)
        
    return render_template("Success.html", mess="Your Registration Done Successfully...")

@app.route("/uploaddoc/", methods=["POST"])
def uploaddoc1():
    if "userid" not in session:
        return redirect(url_for("index"))
    if request.method == 'POST':
        userid = session['userid'] 
        title = request.form.get("title")
        print(title)
        doc = models.handle_uploaded_file3(request.files['file'], userid)
        id, ext = doc.split('.')
        id1 = int(id.strip())
        filedata=models.extract_text(doc,userid)
        insertSummaryDetails(id1,userid,title,doc,filedata)
        
     
    
    return render_template("Success1.html", mess="Document Uploaded Successfully...",link="/user")
# Route to get document details
@app.route('/documents', methods=['GET'])
def get_documents():
    try:
        conn = models.connect()   
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT summaryId, userid, title, doc_path, dt FROM summarydetails")
        documents = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('documents.html', documents=documents)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to fetch summary details by summaryId
@app.route('/Summary', methods=['GET'])
def get_summary():
    try:
        if request.method == 'GET':
            userid = session['userid'] 
            summaryId = request.args.get("summaryId")
            type1 = request.args.get("type")
            conn = models.connect()   
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT "+type1+" FROM summarydetails WHERE summaryId ="+str(summaryId))
            print("SELECT summary1, summary2, summary3 FROM summarydetails WHERE summaryId  ="+(str(summaryId)))
            summary = cursor.fetchone()
            print(summary)
            summary_text = summary[type1].decode('utf-8')

            print(summary_text)
            cursor.close()
            conn.close()
            return render_template("show.html", mess=summary_text)
    except Exception as e:
        print(str(e))
        return render_template("show.html", mess="No Summary Available")

if __name__ == '__main__':
    app.run(debug=True)
