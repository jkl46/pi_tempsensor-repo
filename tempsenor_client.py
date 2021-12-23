import socket
import time
import sys
import mysql.connector

HOST = '192.168.0.189'
PORT = 5353

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="nerdygadgets"
    )
except:
    print("Unable to connect to database\nCheck configuration!")
    sys.exit(1)

cursor = db.cursor()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
first_record = False

def archive_temp():
    # Select old record
    cursor.execute("""
        INSERT INTO coldroomtemperatures_archive
        SELECT * FROM coldroomtemperatures
        WHERE ColdRoomSensorNumber = 5; 
    """)

    # Delete old record
    cursor.execute(f"DELETE FROM coldroomtemperatures WHERE ColdRoomSensorNumber = 5")

    # # Commit change
    db.commit()
    print("Temperature archived!")
    return 0

def insert_temp(temp):
    ColdRoomTemperatureID = str(365348)
    ColdRoomSensorNumber = str(5)
    RecordedWhen = "now()"
    Temperature = str(temp)
    ValidFrom = "now()"
    ValidTo = "now()"

    # Insert record
    cursor.execute(f"INSERT INTO coldroomtemperatures VALUES (\
        {ColdRoomTemperatureID}, {ColdRoomSensorNumber}, {RecordedWhen}, {Temperature}, {ValidFrom}, {ValidTo});")

    db.commit()
    print(f"Temperature: {temp} commited!")
    return 0

if __name__ == "__main__":
    s.connect((HOST, PORT))
    
    cursor.execute("SELECT COUNT(*) FROM coldroomtemperatures \
        WHERE ColdRoomSensorNumber = 5")
    for x in cursor:
        if x[0] == 0:
            first_record = True

    while 1:
        time.sleep(3)
        s.send("T".encode('utf-8'))
        temp = s.recv(255).decode('utf-8')
        if first_record:
            insert_temp(temp)
            first_record = False
        else:
            archive_temp()
            insert_temp(temp)