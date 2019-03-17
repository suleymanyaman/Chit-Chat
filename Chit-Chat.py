from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import MySQLdb
import socket
from pydub import AudioSegment
from pydub.playback import play
from threading import Thread
import functools
import os
from PIL import Image
import io

app = QApplication(sys.argv)

s = socket.socket()
HOST=socket.gethostbyname(socket.gethostname())

PORT=5000
connection_status = "OFFLINE "


dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "notif.wav")
#mysong = AudioSegment.from_wav(filename)


#Frame 3

register_frame = QFrame()
register_frame.setWindowIcon(QIcon('envelope.ico'))
register_frame.setWindowTitle("Chit-Chat v1.0.")
register_box=QFormLayout(register_frame)
nickname = QLineEdit(register_frame)
nick_label=QLabel("Nickname:")
email= QLineEdit(register_frame)
email_label=QLabel("E-mail:")
age = QComboBox(register_frame)
age_label=QLabel("Age:")
password=QLineEdit(register_frame)
password.setEchoMode(QLineEdit.Password)
password_label = QLabel("Password:")
register_button=QPushButton("Register now")
return_button=QPushButton("Return to the main page")

for a in range(18,100):
    age.addItem(str(a))

male  = QRadioButton("Male")
female = QRadioButton("Female")


def open_reg():
    window.close()
    register_frame.show()

def open_main():
    register_frame.close()
    window.show()

return_button.clicked.connect(open_main)



def age_return():
    return age.currentText()

age.activated.connect(age_return)

register_box.addRow(nick_label,nickname)
register_box.addRow(email_label,email)
register_box.addRow(age_label,age)
register_box.addRow(male, female)
register_box.addRow(password_label, password)
register_box.addRow(register_button)
register_box.addRow(return_button)


def send_to_database():
    gender=""
    if male.isChecked():
        gender+="M"
    if female.isChecked():
        gender+="F"


    db = MySQLdb.connect(host="45.63.101.196", user="suleyman_yaman", passwd="19971234", db="suleyman_chitchat")
    conn = db.cursor()
    conn.execute("INSERT INTO chatmembers VALUES (%s,%s,%s,%s,%s)", (nickname.text(), password.text(), email.text(), age_return(),gender ))
    db.commit()
    msg  = QMessageBox()
    msg.setWindowTitle("Chit-Chat v1.0.")
    msg.setText("Congratulations! You have registered, now you can login.")
    msg.exec()



register_button.clicked.connect(send_to_database)

# Frame 2

chat_frame = QFrame()
chat_frame.setWindowIcon(QIcon('envelope.ico'))
chat_frame.setWindowTitle("Chit-Chat v1.0.")
msg_list = QListWidget(chat_frame)
msg_list.setGeometry(10,10,1200,550)



scroll = QScrollBar()
msg_area = QTextEdit(chat_frame)
msg_area.setGeometry(10,570,1200,100)
msg_area.setVerticalScrollBar(scroll)



send_button = QPushButton(chat_frame)
send_button.setText("Send")
send_button.setGeometry(1230,570, 100, 40)
send_button.setEnabled(True)


shuffle_button = QPushButton(chat_frame)
shuffle_button.setText("Shuffle")
shuffle_button.setGeometry(1230, 620, 100,40)

send_photo=QPushButton(chat_frame)
send_photo.setText("Send Photo")
send_photo.setGeometry(1230, 520, 100, 40)

def transition():
    global connection_status
    username = nickname_entry.text()
    pswd = password_entry.text()
    db = MySQLdb.connect(host="45.63.101.196", user="suleyman_yaman", passwd="19971234", db="suleyman_chitchat")
    conn = db.cursor()
    conn.execute("SELECT nickname, pssword FROM chatmembers WHERE nickname=%s AND pssword=%s ", (username, pswd))
    if conn.fetchone():
        try:
            s.connect((HOST, PORT))
            window.close()
            connection_status = "ONLINE"
            s.send(username.encode("utf-8"))
            chat_frame.show()

        except ConnectionRefusedError:
            connection_error=QMessageBox()
            connection_error.setWindowTitle("Network error")
            connection_error.setInformativeText("The server is not connected.")
            connection_error.setIcon(QMessageBox.Warning)
            connection_error.exec()

    else:
        credential_error = QMessageBox()
        credential_error.setWindowTitle("Credentials wrong")
        credential_error.setInformativeText("Either username or password is wrong.")
        credential_error.setIcon(QMessageBox.Critical)
        credential_error.exec()


def recv():
    global send_button
    while True:
        if connection_status == "ONLINE":
            data = s.recv(1024).decode("utf-8")
            if data == "You have been connected to someone!":
                send_button.setEnabled(True)
            if data == "Your partner has left the chat :(":
                send_button.setEnabled(False)


            if not data: sys.exit(0)
            msg_list.addItem(data)
            #play(mysong)



def send(event=None):
    message = msg_area.toPlainText()
    if connection_status == "ONLINE":
        s.send(message.encode('utf-8'))
        msg_area.clear()
        msg_list.addItem("Me:"+message)

def shuffle(event=None):
    timer = QTimer()
    s.send("?pRG=gmxHD74cEm".encode("utf-8"))
    timer.start(2000)

def sendphoto():
    dlg = QFileDialog()
    dlg.setFileMode(QFileDialog.AnyFile)
    img_dir = QStringListModel()

    if dlg.exec_():
        img_dir = dlg.selectedFiles()[0]
        data = open(r'{}'.format(img_dir),'rb').read()
        s.send(data)
        s.send(data)





def closeEvent(self, event):
    choice = QMessageBox.question(self, "Quit", "Do you want to quit Chit-Chat?", QMessageBox.Yes, QMessageBox.No)
    if choice == QMessageBox.Yes:
        s.send("4t7w!z%C".encode("utf-8"))
        event.accept()

    else:
        event.ignore()



shuffle_button.clicked.connect(shuffle)
shuffle_button.setShortcut("Ctrl+S")
send_button.clicked.connect(send)
send_button.setShortcut("Down")
send_photo.clicked.connect(sendphoto)

# Frame 1

window=QFrame()
window.setWindowIcon(QIcon('envelope.ico'))
window.setWindowTitle("Chit-Chat v1.0.")



fbox = QFormLayout()


l1=QLabel("Nickname:")
nickname_entry = QLineEdit(window)
nickname_entry.returnPressed.connect(transition)

l2=QLabel("Password:")
password_entry = QLineEdit(window)
password_entry.setEchoMode(QLineEdit.Password)
password_entry.returnPressed.connect(transition)


login = QPushButton(window)
login.setText("Login")
login.clicked.connect(transition)
login.setShortcut("Return")



register_button=QPushButton("Don't have an account?")
register_button.clicked.connect(open_reg)

fbox.addRow(l1, nickname_entry)
fbox.addRow(l2, password_entry)
fbox.addRow(login)
fbox.addRow(register_button)

window.setLayout(fbox)
window.show()


t1=Thread(target=recv)
t1.start()

chat_frame.closeEvent = functools.partial (closeEvent, chat_frame)



sys.exit(app.exec())


