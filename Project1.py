"""
Created on Mon Apr 11 16:39:51 2022

@author: Aniruddha Patil
"""

from flask import Flask,render_template,request
#,redirect,url_for
import mysql.connector
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random

app = Flask(__name__)



def sendEmailFunc(sender_address, receiver_address,passw, otp_):
    # Email body 
    mail_content = "Please find the verification code for getting details:" + str(otp_)
    
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address

    message['Subject'] = 'Verification code'
    
    message.attach(MIMEText(mail_content, 'plain'))
    session = smtplib.SMTP('smtp.gmail.com', 587)
    # session.ehlo()
    session.starttls() #enable security
    session.login(sender_address,passw) #login with mail_id and password
    text = message.as_string()
    
    session.sendmail(sender_address, receiver_address, text)
    
    session.close()
        

@app.route("/")
def message():        
    return render_template('Main_Page.html')


@app.route('/next_Response2',methods=['GET','POST'])
def next_Response2():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        my_database=mysql.connector.connect(host="localhost",user="",password="")
        my_cursor=my_database.cursor()
        
        my_cursor.execute("Use project")
        try:
            my_cursor.execute("SELECT * FROM details where username='"+username+"' and pass='"+password+"'")
            my_result = my_cursor.fetchall()
            
            if my_result == []:
                error_message="User is not registered!!"
                return render_template("Login.html",error =error_message)

            for x in my_result:
              if str(username) == x[0] and str(password) == x[1]:
                  print("Success!!")
                  otp_ = random.randint(100000, 999999)
                  print(otp_,"##")
                  sender_address = ""
                  receiver_address = ""
                  # receiver_address = x[2]

                  passw = ""
                  try:
                      sendEmailFunc(sender_address,receiver_address,passw,str(otp_))
                      global OTP
                      global Pwd
                      # Uname = str(username)
                      Pwd = str(password)
                      OTP= otp_
                  except:
                      print("Error while sending an email!")    
                  return render_template('Final_Verification.html')
              else:
                  print("Incorrect username or password!")
                  error_message = "Incorrect username or password!"
            
                  return render_template("Login.html",error =error_message)
        except:
            error_message = "Incorrect username or password!"
            
            return render_template("Login.html",error =error_message)
    
    return render_template("Login.html")

@app.route('/next_Response1',methods=['GET','POST'])
def next_Response1():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        mobile = request.form.get("mobile")
        
        # print(str(username), str(password),str(email),int(mobile))
        # username,password,email,mobile = "Aniruddha", "abcd","abc@gmail.com","9101010101"
        try:
            if len(str(int(mobile)))!=10:
                error_message="Mobile number is Invalid!!"
                return render_template("Registration.html",error=error_message)
        except:
            error_message = "Mobile number is Invalid!!"
            return render_template("Registration.html",error=error_message)
        else:
            my_database=mysql.connector.connect(host="localhost",user="root",password="")
            my_cursor=my_database.cursor()
            
            my_cursor.execute("Use project")
            try:
                sql = "INSERT INTO details(username,pass,email,mobile) VALUES(%s,%s,%s,%s)"
                val = (str(username), str(password),str(email),int(mobile))
                my_cursor.execute(sql, val)
                my_database.commit()
                my_cursor.close()
                print("Record inserted successfully in database")
                
                return render_template("Login.html")
            except:
                print("Already record present!")
                error_message = "Username or password or mobile number is already used!! Try with other."
                return render_template("Registration.html",error=error_message)
    else:
        return render_template("Registration.html")
        
    
@app.route('/verification',methods=['GET','POST'])
def verification():        
    if request.method == 'POST':
        otp = request.form.get("otp")
        if int(otp)==int(OTP):
            print(OTP,"Final success")
            my_database=mysql.connector.connect(host="localhost",user="",password="")
            my_cursor=my_database.cursor()
            
            my_cursor.execute("Use project")
            try:
                my_cursor.execute("SELECT * FROM details where pass='"+str(Pwd)+"'")
                my_result = my_cursor.fetchall()
                
                print(my_result[0][0])
                return render_template("Display_Details.html", uname=my_result[0][0],email=my_result[0][2],mobile=my_result[0][3])                    
            except:
                error_message= "Result not found!"
                return render_template('Final_Verification.html',error=error_message)
        else:
            error_message= "Incorrect OTP!!"
            return render_template('Final_Verification.html',error=error_message)

    return render_template('Main_Page.html')


if __name__=='__main__':
    app.run(host="localhost",port=5000,threaded=False)
    

