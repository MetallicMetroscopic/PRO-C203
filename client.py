import socket
from tkinter import *
from threading import Thread

# nickname = input("Choose your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

client.connect((ip_address, port))

print("Connected with the server...")

class GUI:
    def __init__(self):
        self.window = Tk()
        self.window.withdraw()
        
        self.login = Toplevel()
        self.login.title("login")
        self.login.resizable(width=False, height=False)
        self.login.configure(width=400, height=600)

        self.pls = Label(self.login, text="Please login to continue", justify=CENTER, font="Helvetica 14 bold")
        self.pls.place(relheight=0.15, relx=0.2, rely=0.07)

        self.labelName = Label(self.login, text="Name: ", font="Helvetica 12")
        self.labelName.place(relheight=0.2, relx=0.1, rely=0.2)

        self.entryName = Entry(self.login, font="Helvetica 14")
        self.entryName.place(relwidth=0.4, relheight=0.06, relx=0.25, rely=0.268)
        self.entryName.focus()

        self.go = Button(self.login, text="Go!", font="Helvetica 14 bold", command=lambda: self.goAhead(self.entryName.get()))
        self.go.place(relx=0.4, rely=0.5)

        self.window.mainloop()

    def goAhead(self, name):
        self.login.destroy()
        # self.name = name
        self.layout(name)

        rcv = Thread(target=self.receive)
        rcv.start()

    def layout(self, name):
        self.name = name
        self.window.deiconify()

        self.window.title("Chat Room")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=470, height=550)

        self.labelHead = Label(self.window, bg="#17202A", fg="#EAECEE", text=self.name, font="Helvetica 13 bold", pady=5)
        self.labelHead.place(relwidth=1)
        
        self.line = Label(self.window, width=450, bg="#ABB2B9")
        self.line.place(relwidth=1, relheight=0.012, rely=0.07)

        self.textCons = Text(self.window, width=20, height=2, bg="#17202A", fg="#EAECEE", font="Helvetica 14", pady=5, padx=5)
        self.textCons.place(relheight=0.745, relwidth=1, rely=0.02)

        self.labelBottom = Label(self.window, bg="#ABB2B9", height=18)
        self.labelBottom.place(relwidth=1, rely=0.825)

        self.entryMsg = Entry(self.labelBottom, bg="#2C3E50", fg="#EAECEE", font="Helvetica 13")
        self.entryMsg.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.entryMsg.focus()

        self.buttonMsg = Button(self.labelBottom, text="Send", font="Helvetica 10 bold", width=20, bg="#ABB2B9", command= lambda: self.sendButton(self.entryMsg.get()))
        self.buttonMsg.place(relwidth=0.22, relheight=0.06, relx=0.07, rely=0.08)
        
        self.textCons.config(cursor="arrow")
        self.scrollBar = Scrollbar(self.textCons)
        self.scrollBar.place(relheight=1, relx=0.974)
        self.scrollBar.config(command= self.textCons.yview())

        self.textCons.config(state=DISABLED)

    def sendButton(self, msg):
        self.textCons.config(state=DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, END)

        snd = Thread(target=self.write())
        snd.start()
        
    def showMsg(self, message):
        self.textCons.config(state=NORMAL)
        self.textCons.insert(END, message+"\n\n")
        self.textCons.config(state=DISABLED)
        self.textCons.see(END)

    def receive(self):
        while True:
            try:
                message = client.recv(2048).decode('utf-8')
                if message == 'NICKNAME':
                    client.send(self.name.encode('utf-8'))
                else:
                    self.showMsg(message)
            except:
                print("An error occured!")
                client.close()
                break

    def write(self):
        self.textCons.config(status=DISABLED)
        while True:
            message = (f"{self.name}: {self.msg}")
            client.send(message.encode('utf-8'))
            self.showMsg(message)
            break

# receive_thread = Thread(target=receive)
# receive_thread.start()
# write_thread = Thread(target=write)
# write_thread.start()

g = GUI()