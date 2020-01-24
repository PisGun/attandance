from gpiozero import Button
import mysql.connector
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from RPLCD.i2c import CharLCD
from time import sleep
lcd = CharLCD('PCF8574', 0x27)

reader = SimpleMFRC522()

button = Button(21)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="password",
  database="school"
)
print(mydb)
mycursor = mydb.cursor()

def createDatabase(mycursor, name):
    mycursor.execute("CREATE DATABASE " + name)
    print("Database created")
#createDatabase(mycursor, "school")

def createTable(mycursor, table):
    mycursor.execute("CREATE TABLE " + table + "(studentid VARCHAR(255), classid INT, datetime DATETIME)")
    print("Table created")
#createTable(mycursor, "attendance")

def showTables(mycursor):
    mycursor.execute("SHOW TABLES")
    
    for row in mycursor:
        print(row)
#showTables(mycursor)

def addStudent(mycursor, fName, lName, nName):
    id,name = reader.read()
    q = "INSERT INTO students(id, firstname, lastname, nickname) VALUES('" + str(id) + "' , '" + fName + "', '" + lName + "', '" + nName + "')"
    print(q)
    mycursor.execute(q)
    mydb.commit()
#addStudent(mycursor, 'Siriwat', 'Jaichobchune', 'Vinze')
    
def addClassClub(mycursor, id, name, teacher):
    mycursor.execute("INSERT INTO classesClubs(id, name, teacher) VALUES('" + str(id) + "' , '" + name + "', '" + teacher + "')")

    mydb.commit()
#addClassClub(mycursor, 911, 'Robotics', 'Tim McBacon')
    
def showData(mycursor, table):
    mycursor.execute("SELECT * FROM "+ table)
    
    myresult = mycursor.fetchall()
    
    for x in myresult:
        print(x)
#showData(mycursor,"students")

def scanStudent(mycursor):
    #print("Scan your Card")
    lcd.write_string("Scan your Card\n\r")
    id,name = reader.read()
    mycursor.execute("SELECT * FROM students WHERE id = " + str(id))
    myresult = mycursor.fetchall()
    for x in myresult:
        lcd.clear()
        print(x[0]+ " : "+ str(id))
        lcd.write_string(x[3] + "\n\r" + x[1] + "\n\r" + x[2])
    #print("\nScan your Card")
    lcd.clear()
    return id


def findClassClub(mycursor):
    print("Which class?")
    classClub = input()
    mycursor.execute("SELECT id FROM classesClubs WHERE name = '" + classClub +"'")
    myresult = mycursor.fetchall()
    #print(myresult)
    classID = 123
    for x in myresult:
        classID = x[0]
    #print(classID)
    return classID
    #check same name and return id
    
def inputAttendance(mycursor, studentid, classid):
    q = "INSERT INTO attendance(studentid, classid, datetime) VALUES('" + str(studentid) + "' , " + str(classid) + ", NOW())"
    print(q)
    mycursor.execute(q)
    print("Checked")
    mydb.commit()

def checkAttendance(mycursor):
    print("Place ur card, then press the button to start checking attendance")
    sleep(3)
    classID = findClassClub(mycursor)
    while True:
        studentID = scanStudent(mycursor)
        print(studentID)
        if studentID == "Does NOT Exist":
            print(studentID)
            #PressButton to Check press again to check the next student
        else:
            inputAttendance(mycursor, studentID, classID)
            studentID = "Does NOT Exist"

try:
    showTables(mycursor)
    checkAttendance(mycursor)
    #showData(mycursor,"classesClubs")
    #inputAttendance(mycursor, 132, 1312)
    #findClassClub(mycursor)
    #scanStudent(mycursor)
    
finally:
    GPIO.cleanup()