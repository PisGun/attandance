import mysql.connector
#import the Flask library
from flask import Flask


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="password",
  database="school"
)
print(mydb)
mycursor = mydb.cursor()
def showData(mycursor, table):
    mycursor.execute("SELECT * FROM "+ table)  
    myresult = mycursor.fetchall()
    return myresult
def studentName(mycursor, studentID):
    mycursor.execute("SELECT * FROM students WHERE id = '" + studentID +"'" )  
    myresult = mycursor.fetchall()
    return myresult
def className(mycursor, classID):
    mycursor.execute("SELECT * FROM classesClub WHERE id = '" + classID +"'" )  
    myresult = mycursor.fetchall()
    return myresult

        
#create the app: __name__ is always "__main__"
app = Flask(__name__)
#create a function that is run when the URL is opened
#type http://localhost:5000 into the browser on the pi
@app.route("/")
def home():
#whatever you return is shown in the browser
#select 1 field put in table
    data = showData(mycursor, "attendance")
    tableInWeb = "<center><table><tr><th>StudentID</th><th>ClassID</th><th>Time</th></tr>"
    for y in data[0]:
        student = studentName(mycursor, str(y))
    for x in data:
        tableInWeb = tableInWeb + "<tr><td> " + str(student) + "</td><td> " + str(x[1]) + "</td><td>" + str(x[2]) + "</td></tr>"

    return "<h1><center> HTML is a programming LANGUAGE </center></h1>" + tableInWeb + "</table></center>"
#Start the app, this should be the last line
if __name__ == "__main__":
    app.run()
