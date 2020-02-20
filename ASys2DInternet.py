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
    mycursor.execute("SELECT firstname FROM students WHERE id = '" + studentID +"'" )  
    myresult = mycursor.fetchall()
    return myresult

def className(mycursor, classID):
    mycursor.execute("SELECT name FROM classesClubs WHERE id = '" + classID +"'" )  
    myresult = mycursor.fetchall()
    return myresult
        
#create the app: __name__ is always "__main__"
app = Flask(__name__)

@app.route("/")
def home():
    data = showData(mycursor, "attendance")
    tableInWeb = "<center><table><tr><th>Name      </th><th>Class</th><th>Time</th></tr>"
    for x in data:
        student = studentName(mycursor, str(x[0]))
        classname = className(mycursor, str(x[1]))
        tableInWeb = tableInWeb + "<tr><td> " + str(student[0][0]) + "</td><td> " + str(classname[0][0]) + "</td><td>" + str(x[2]) + "</td></tr>"

    return "<h1><center> Attendance Table </center></h1>" + tableInWeb + "</table></center>"
#Start the app, this should be the last line
if __name__ == "__main__":
    app.run()
