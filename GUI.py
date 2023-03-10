# code ref--> 1. https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/#key-loading
# code ref--> 2. Chat GPT

from tkinter import *
from tkinter import ttk, messagebox


import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
from datetime import date


GUI = Tk()
GUI.title("MyCertificate-B6322113")
GUI.geometry("700x700")
GUI.iconbitmap("ca.ico")

FONT30 = ("Angsana New", 30)
FONT20 = ("Angsana New", 20)

data_list = []
index = 0


############################ config tab#########################
Tab = ttk.Notebook(GUI)
Tab.pack(fill=BOTH, expand=1)

T1 = Frame(Tab)
T2 = Frame(Tab)


icon_tab1 = PhotoImage(file="tab1.png")
icon_tab2 = PhotoImage(file="tab2.png")


Tab.add(T1, text="signature", image=icon_tab1, compound="left")
Tab.add(T2, text="vertify", image=icon_tab2, compound="left")


#################### signature func###########################
def validate_input(event=None):

    try:
        sc = int(v_sc.get())
        if sc < 60 or sc > 100:
            text = "Please enter a score between 60 and 100"
            messagebox.showwarning("warning", text)

        else:
            Append()
    except:
        text = "Please enter a interger number"
        messagebox.showwarning("warning", text)


def Append(event=None):
    global index
    index += 1
    sname = v_sname.get()
    sid = v_sid.get()
    pname = v_pname.get()
    exdate = v_exdate.get()
    sc = v_sc.get()

    data_list = [sname, sid, pname, exdate, sc]
    SHA_512(data_list)


def SHA_512(data_list):
    # join str before sha512
    joinstr = "".join(data_list)
    print("joinstr>>>", joinstr)
    hashed_string = hashlib.sha512(joinstr.encode('utf-8')).digest()
    print("hashed_string>>>", hashed_string)

    with open("Certificate{}.txt".format(index), "w") as file:
        for i in range(4):
            file.write('{}\n'.format(data_list[i]))
        file.write(data_list[-1])

    data_list.clear()

    # return hashed_string
    Signature(hashed_string)


def Signature(msg):
    # Load private key previouly generated
    with open('private_key.pem', 'rb') as file:
        private_pem = file.read()
        private_key = load_pem_private_key(private_pem, password=None)
        print("private_key", private_key)

    # signing
    signature = private_key.sign(
        msg,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA512()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA512()
    )

    with open("Signature{}.txt".format(index), "wb") as file:
        file.write(signature)

    text = "Project certificate has been issued successfully."
    messagebox.showinfo("success", text)

    ############### clear textbox###################
    v_sname.set("")
    v_pname.set("")
    v_exdate.set("")
    v_sc.set("")
    v_sid.set("")
    v_result.set("")
    ############### fix cursor at E1################
    E1.focus()

############################## Tab1 signature################################


L = Label(T1, text="Certificate Issuance Program", font=FONT30)
L.pack(pady=20)

L = Label(T1, text="Student Name", font=FONT20)
L.pack()
v_sname = StringVar()
E1 = ttk.Entry(T1, textvariable=v_sname, font=FONT20)
E1.pack(pady=5)

L = Label(T1, text="Student ID", font=FONT20)
L.pack()
v_sid = StringVar()
E2 = ttk.Entry(T1, textvariable=v_sid, font=FONT20)
E2.pack(pady=5)

L = Label(T1, text="Project Name", font=FONT20)
L.pack()
v_pname = StringVar()
E3 = ttk.Entry(T1, textvariable=v_pname, font=FONT20)
E3.pack(pady=5)

L = Label(T1, text="Date Of Experied (YYYY-MM-DD)", font=FONT20)
L.pack()
v_exdate = StringVar()
E4 = ttk.Entry(T1, textvariable=v_exdate, font=FONT20)
E4.pack(pady=5)

L = Label(T1, text="Please enter a score between 60 and 100", font=FONT20)
L.pack()
v_sc = StringVar()
E5 = ttk.Entry(T1, textvariable=v_sc, validate="key",
               validatecommand=validate_input, font=FONT20)
E5.pack(pady=5)
E5.bind("<Return>", validate_input)  # press enter  will be submit

B1 = ttk.Button(T1, text="submit", command=validate_input)
B1.pack(pady=20, ipadx=20, ipady=10)

v_result = StringVar()
result = ttk.Label(T1, textvariable=v_result, foreground="green")


##################################### tab2 verify #############################################

def Verification(event=None):
    ver_index = _ver_index.get()
    with open('public_key.pem', 'rb') as file:
        public_pem = file.read()
        public_key = load_pem_public_key(public_pem)

    try:
        with open("Certificate{}.txt".format(ver_index), "r") as file:
            list_certificate = file.read().split("\n")

        with open("Signature{}.txt".format(ver_index), "rb") as file:
            signature = file.read()  # digest2
    except:
        text = "There is no such certificate."
        messagebox.showerror("error", text)
        _ver_index.set("")

    # check date of expired
    today = str(date.today())
    date_of_expired = list_certificate[3]

    if date_of_expired <= today:
        text = "your certificate has been expired"
        messagebox.showerror("expired", text)

    else:

        try:
            # hash certificate in order to get Digest 1
            joinstr = "".join(list_certificate)
            digest1 = hashlib.sha512(joinstr.encode('utf-8')).digest()

            print("hashed_string>>>", digest1)
            print("joinstr>>>", joinstr)
            print("digest1>>>", digest1)

            public_key.verify(
                signature,
                digest1,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA512()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA512()
            )
            # print("your signature is valid")
            text = "your signature is valid"
            messagebox.showinfo("Valid", text)

        except:

            # print("your signature is invalid")
            text = "your signature is invalid"
            messagebox.showwarning("Invalid", text)

    _ver_index.set("")

############################ end verify func############################


L = Label(T2, text="Verify The Certificate", font=FONT30)
L.pack(pady=20)

L = Label(T2, text="Please enter the index to verify the signature\n for example \"Certificate0\" = index 0 (enter 0)", font=FONT30)
L.pack(pady=50)

_ver_index = StringVar()
E3 = ttk.Entry(T2, textvariable=_ver_index, font=FONT20)
E3.pack(pady=20)
E3.focus()
E3.bind("<Return>", Verification)

B2 = ttk.Button(T2, text="verify", command=Verification)
B2.pack(pady=20, ipadx=20, ipady=10)

GUI.mainloop()
