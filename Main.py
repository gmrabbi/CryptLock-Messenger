import os
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import webbrowser
import csv


root = Tk()
root.title("CryptLock Messenger") 
root.geometry("500x400")
root.resizable(True, False)
root.config(background="#89CFF0")


btn_bg_clr = "#B9D9EB"
btn_fg_clr = "#0040FF"
Ent_bg_clr = "#A3C1AD"
Ent_fg_clr = "#000000"
lbl_bg_clr = "#89CFF0"
lbl_fg_clr = "#36454F"
upd_btn_fg_clr = "#A3C1AD"
upd_btn_bg_clr = "#D70040"

home_menu_clr = ""
about_menu_clr = ""
exit_menu_clr = "red"

btn_width = 3

login_flag = 0


path = r"."
with open(f"{path}\Login_data.csv", "a"):
    pass

try:
    os.mkdir(os.path.join(path, "All_User"))
except FileExistsError:
    pass

curent_user = ""

lgn_user_lst  = list()
lgn_pswd_lst = list()

sndr_lst = list()
recv_lst = list()
mess_lst = list()


total_user_lst = list()
total_user_lst_cmb = list()


def update_combox():
    global total_user_lst_cmb, total_user_lst,curent_user
    with open(f"{path}\All_User\{curent_user}.csv", "r") as file:
        data = csv.reader( file )
        for gml in data:
            if(gml[0].split("@")[0] not in total_user_lst_cmb):
                total_user_lst_cmb.append(gml[0].split("@")[0])
            



def find_folder():
    global total_user_lst, path

    # Specify the path to the folder you want to search in
    folder_path = os.path.join(path, "All_User")

    # Use os.listdir() to get a list of all files and folders in the directory
    contents = os.listdir(folder_path)

    # Use a list comprehension to filter out only the files (not directories)
    files = [item for item in contents if os.path.isfile(
        os.path.join(folder_path, item))]

    # Print the list of file names
    for name in files:
        if(name not in total_user_lst):
            total_user_lst.append(name[:-4])
    


find_folder()

def Update_list():
    global lgn_user_lst, lgn_pswd_lst     
    data = open(f"{path}\Login_data.csv", "r")
    
    for part in csv.reader(data):
        if(part[0] not in lgn_user_lst):
            lgn_user_lst.append(part[0])
            lgn_pswd_lst.append(part[1])
    data.close()


def Encrypted_mess(txt, sckt_key, rec_gml):
    global total_user_lst,path
    
    # update toatal user list noww
    find_folder()
    mess = txt.split(" ")
    key = sckt_key

    ln = len(key)
    msg_lst = list()
    en_mess =""
    n = 0
    for word in mess:
        ms = ""
        for lat in word:
            if(n >= ln):
                n = 0
            ms += chr(ord(lat) + n )
            n += 1
            # if(lat == "\n"):
            #     continue
        msg_lst.append(ms)

    for i in msg_lst:
        en_mess = (en_mess + i) + " "
        
    en_mess = en_mess[:-1]
    
    pth = os.path.join(path, "All_User")
    
    if (rec_gml.split("@")[0] in total_user_lst):
        message =  open(f"{pth}\\{rec_gml.split('@')[0]}.csv", "a")
        message.write(f"{gml_ent.get()},{en_mess}")
        message.write("\n")
        message.close()
        messagebox.showinfo("Encryption", f"Sender: {gml_ent.get()}\nReceiver:{rec_gml}\n\nMessage sent:{en_mess}")
        
        Emsg_txt.delete(0.0, END)
        Ekey_ent.delete(0, END)
        rgml_ent.delete(0, END)
        
        C_mode()
    else:
        messagebox.showerror("User Not Fount", f"{rec_gml}\nInvalid Receiver Gmail")


# send function 
def send_data():
    txt = Emsg_txt.get(1.0, END) 
    sckt_key = Ekey_ent.get()
    rec_gml = rgml_ent.get()
    Encrypted_mess(txt, sckt_key, rec_gml)

# Encrypt element
Ekey = rec_gml = ""
Emsg_lbl = Label(root, text="Message: ", bg=lbl_bg_clr,
                 fg=lbl_fg_clr, borderwidth=btn_width, font=("Arial", 12, "bold"))
Emsg_txt = Text(root, width=30, height=10,  bg=Ent_bg_clr,
                fg="#000000", borderwidth=btn_width, font=("Arial", 12, "bold"))
Ekey_lbl = Label(root, text="Key: ",  bg=lbl_bg_clr,
                 fg=lbl_fg_clr, borderwidth=btn_width, font=("Arial", 12, "bold"))
Ekey_ent = Entry(root,  bg=Ent_bg_clr, fg=Ent_fg_clr,
                 borderwidth=btn_width, font=("Arial", 12, "bold"),width=30)
rgml_lbl = Label(root, text="Receiver Gmail: ", bg=lbl_bg_clr,
                      fg=lbl_fg_clr, borderwidth=btn_width, font=("Arial", 12, "bold"))
rgml_ent = Entry(root,  bg=Ent_bg_clr, fg=Ent_fg_clr,
                 borderwidth=btn_width, font=("Arial", 12, "bold"), width=30)
ENext_btn = Button(root, text="Next>>", cursor="hand2", bg=btn_bg_clr, fg=btn_fg_clr,
                   borderwidth=btn_width, font=("Arial", 12, "bold"), command=send_data)
# btn width

def Encrypt():
    ch_mode.place_forget()
    enc_btn.place_forget()
    dec_btn.place_forget()
    
    
    Emsg_lbl.place(relx=0.2, rely=0.2)
    Emsg_txt.place(relx=0.4, rely=0.2)
    Ekey_lbl.place(relx=0.2, rely=0.7)
    Ekey_ent.place(relx=0.4, rely=0.7)
    rgml_lbl.place(relx=0.1, rely=0.8)
    rgml_ent.place(relx=0.4, rely=0.8)
    ENext_btn.place(relx=0.7, rely=0.9)

# Decrypt element

# Decrypt main part
def D_Next():
    key = Dkey_ent.get()
    n = 0
    ms = ""
    msg_lst = list()
    for word in Dmsg_txt.get(1.0, END).split(" "):
        de_mess = ""
        for lat in word:
            if(n >= len(key)):
                n = 0
            de_mess += chr(ord(lat) - n)
            n += 1
        msg_lst.append( de_mess )
        msg_lst.append(" ")
            
    for i in msg_lst:
        if(i==" "):
            ms+= " "
        else:
            ms += i
            
    Dmsg_txt.delete(0.0, END)
    Dkey_ent.delete(0, END)
    messagebox.showinfo("Decrypt", f"Your message \n\n{ms[:-2]}")
    

Dmsg_lbl = Label(root, text="Message : ", bg=lbl_bg_clr,
                 fg=lbl_fg_clr, borderwidth=btn_width, font=("Arial", 12, "bold"))
Dmsg_txt = Text(root, width=30, height=10, bg=Ent_bg_clr,
                fg="#000000", borderwidth=btn_width, font=("Arial", 12, "bold"))
Dkey_lbl = Label(root, text="Key : ", bg=lbl_bg_clr,
                 fg=lbl_fg_clr, borderwidth=btn_width, font=("Arial", 12, "bold"))
Dkey_ent = Entry(root, bg=Ent_bg_clr, fg=Ent_fg_clr,
                 borderwidth=btn_width, font=("Arial", 12, "bold"), width=30)
Dbtn = Button(root, text="Decrypt", cursor="hand2", bg=btn_bg_clr, fg=btn_fg_clr,
              borderwidth=btn_width, font=("Arial", 12, "bold"), command=D_Next)



def Decrypt():
   
    Sgml_lbl.place_forget()
    Sgml_ent.place_forget()
    DNxt_btn.place_forget()
    
        
    
    Dmsg_lbl.place(relx=0.1, rely=0.2)
    Dmsg_txt.place(relx=0.27, rely=0.2)
    Dkey_lbl.place(relx=0.1, rely=0.7)
    Dkey_ent.place(relx=0.27, rely=0.7)
    Dbtn.place(relx=0.7, rely=0.8)


Sgml_lbl = Label(root, text="Sender : ", bg=lbl_bg_clr,
                 fg=lbl_fg_clr, borderwidth=btn_width, font=("Arial", 12, "bold"))
# Sgml_ent = Entry(root, textvariable=sndr_gmail)
find_folder()

        

  

def load_mess():
    mess = ""
    gml = Sgml_ent.get()
    
    file = open(f"{path}\All_User\{curent_user}.csv", "r")
    data = csv.reader(file)
    for i in data:
        if(i[0].split("@")[0] == gml ):
            mess = i[1]
    file.close()
    Dmsg_txt.insert(0.0, mess)
    Sgml_ent.delete(0, END)
    
    Decrypt()


DNxt_btn = Button(root, text="Next>>", cursor="hand2", bg=btn_bg_clr, fg=btn_fg_clr,
                  borderwidth=btn_width, font=("Arial", 12, "bold"), command=load_mess)

Sgml_ent = ttk.Combobox(root, background="#FFFDD0", foreground="#6495ED", font=("Arial", 12, "bold"))




def Find_sndr():
    ch_mode.place_forget()
    enc_btn.place_forget()
    dec_btn.place_forget()
    
    update_combox()
    Sgml_ent.config(values=total_user_lst_cmb)
    
    

    Sgml_lbl.place(relx=0.1, rely=0.2)
    Sgml_ent.place(relx=0.3, rely=0.2)
    # fnd_lbl.place(relx=0.4, rely=0.3)
    DNxt_btn.place(relx=0.7, rely=0.65)
    
       
# C_mode element
ch_mode = Label(root, text="Select your Mode.", bg=lbl_bg_clr,
                fg="#006B3C", borderwidth=btn_width, font=("Arial", 20, "bold"))
enc_btn = Button(root, text="Encryption", cursor="hand2", bg=btn_bg_clr, fg=btn_fg_clr,
                 borderwidth=btn_width, font=("Arial", 12, "bold"), command=Encrypt)
dec_btn = Button(root, text="Decryption", cursor="hand2", bg=btn_bg_clr, fg=btn_fg_clr,
                 borderwidth=btn_width, font=("Arial", 12, "bold"), command=Find_sndr)


def C_mode():
    wlc_lbl.place_forget()
    gml_lbl.place_forget()
    gml_ent.place_forget()
    pswd_lbl.place_forget()
    pswd_ent.place_forget()
    submit.place_forget()
    
    # Encryption forget place
    Emsg_lbl.place_forget()
    Emsg_txt.place_forget()
    Ekey_lbl.place_forget()
    Ekey_ent.place_forget()
    rgml_lbl.place_forget()
    rgml_ent.place_forget()
    ENext_btn.place_forget()
    
    Crt_act.place_forget()
    
    update_combox()
    
    
    ch_mode.place(relx=0.3, rely=0.35)
    enc_btn.place(relx=0.3, rely=0.5)
    dec_btn.place(relx=0.6, rely=0.5)
    
    
#  login element 
wlc_lbl = Label(root, text="Welcome to \nCryptLock-Messenger", bg=lbl_bg_clr,
                fg="#F5F5F5", borderwidth=btn_width, font=("Arial", 20, "bold"))


def Fg_pass(gmail, password):
    fileR = open(f"{path}\Login_data.csv", "r+")
    
    user_pass = dict()
    
    data = list(csv.reader(fileR))
    fileR.close()
    
    file = open(f"{path}\Login_data.csv", "w+")
    for i in data:
        gml = (i[0])
        psd = (i[1])
        user_pass[gml] = psd
    cker = 0
    
    if(password_check(gmail, password)):
        for gaml, pasd in user_pass.items():
            if(gaml == gmail ):
                if(lgn_pswd_lst[lgn_user_lst.index(gmail)] != password):
                    user_pass[gmail] = password
                    lgn_pswd_lst[lgn_user_lst.index(gmail)] = password
                    cker = 1
                else:
                    messagebox.showerror("Warning", "This is old password.")
                
                
    for gaml , pasd in user_pass.items():
        user_pass[gaml] = pasd

        file.write(f"{gaml},{pasd}")
        file.write("\n")
    
        
    if(cker):
        messagebox.showwarning("Updated", "Password update successfully")
        FgPsd_gml_ent.delete(0, END)
        FgPsd_psd_ent.delete(0, END)
        login()
    
    file.close()
            

# Forget password element
FgPsd_gml_lbl = Label(root, text="Gmail", bg=lbl_bg_clr,
                      fg=lbl_fg_clr, borderwidth=btn_width, font=("Arial", 12, "bold"))
FgPsd_gml_ent = Entry(root, bg=Ent_bg_clr, fg=Ent_fg_clr, borderwidth=btn_width, font=("Arial", 12, "bold"))
FgPsd_psd_lbl = Label(root, text="Password", bg=lbl_bg_clr,
                      fg=lbl_fg_clr, borderwidth=btn_width, font=("Arial", 12, "bold"))
FgPsd_psd_ent = Entry(root, bg=Ent_bg_clr, fg=Ent_fg_clr,
                      borderwidth=btn_width, font=("Arial", 12, "bold"))
FgPsd_btn = Button(root, text="Update", cursor="hand2", bg=upd_btn_bg_clr, fg=upd_btn_fg_clr, borderwidth=btn_width, font=(
    "Arial", 12, "bold"), command=lambda: Fg_pass(FgPsd_gml_ent.get(), FgPsd_psd_ent.get()))


def Update_password():
    choice = messagebox.askokcancel("Wrong Password.", "Forget password ?")
    if(choice):
        wlc_lbl.place_forget()
        gml_lbl.place_forget()
        gml_ent.place_forget()
        pswd_lbl.place_forget()
        pswd_ent.place_forget()
        submit.place_forget()
        Crt_act.place_forget()
        
        FgPsd_gml_lbl.place(relx=0.3, rely=0.4)
        FgPsd_gml_ent.place(relx=0.5, rely=0.4)
        FgPsd_psd_lbl.place(relx=0.3, rely=0.5)
        FgPsd_psd_ent.place(relx=0.5, rely=0.5)
        FgPsd_btn.place(relx=0.7, rely=0.7)

    
def validation():
    global login_flag, curent_user
    global lgn_user_lst, lgn_pswd_lst
    
    if(gml_ent.get() in lgn_user_lst):
        indx = lgn_user_lst.index(gml_ent.get())

        if(pswd_ent.get()==lgn_pswd_lst[indx]):
            curent_user = gml_ent.get().split("@")[0]
            login_flag = 1
            C_mode()
            root.title(f"CryptLock-Messenger ({curent_user})")

            menubar.add_command(label="Sign Out",background="red",foreground="black", command=Sign_out)
            
        elif(pswd_ent.get() != lgn_pswd_lst[indx]):
            Update_password()
            FgPsd_gml_ent.insert(0,gml_ent.get())
            FgPsd_gml_ent.config(state='disabled')
            

    else:
        # Update_password()
        choice =  messagebox.askyesno("404 user", "Wrong username or password.\n\nDo you want to Create an account?")
        if(choice):
            Sign_up()
            
            
gml_lbl = Label(root, text="Gmail : ", bg=lbl_bg_clr,
                fg=lbl_fg_clr, borderwidth=btn_width, font=("Arial", 12, "bold"))
gml_ent = Entry(root, bg=Ent_bg_clr, fg=Ent_fg_clr,
                borderwidth=btn_width, font=("Arial", 12, "bold"))

pswd_lbl = Label(root, text="Password : ", bg=lbl_bg_clr,
                 fg=lbl_fg_clr, borderwidth=btn_width, font=("Arial", 12, "bold"))

pswd_ent = Entry(root, show="*", bg=Ent_bg_clr, fg=Ent_fg_clr,
                 borderwidth=btn_width, font=("Arial", 12, "bold"))

submit = Button(root, text="Login", cursor="hand2", bg=btn_bg_clr, fg=btn_fg_clr,
                borderwidth=btn_width, font=("Arial", 12, "bold"), command=validation)



wlc_SgnUp = Label(root, text="Sign Up", bg=lbl_bg_clr,fg="#006B3C",borderwidth=btn_width, font=("Arial",20, "bold"))
SgnUp_Gml_lbl = Label(root, text="Gmail : ",  bg=lbl_bg_clr,
                      fg=lbl_fg_clr, borderwidth=btn_width, font=("Arial", 12, "bold"))
SgnUp_Gml_enty = Entry(root, bg=Ent_bg_clr, fg=Ent_fg_clr,
                       borderwidth=btn_width, font=("Arial", 12, "bold"))
SgnUp_pass_lbl = Label(root, text="Password : ", bg=lbl_bg_clr,
                       fg=lbl_fg_clr, borderwidth=btn_width, font=("Arial", 12, "bold"))
SgnUp_pass_enty = Entry(root, show="*", bg=Ent_bg_clr, fg=Ent_fg_clr, borderwidth=btn_width, font=("Arial", 12, "bold") )


def password_check(gml,pwd):
    mess = """
    Invalid Gmail and password
    
    Follow the Rules:
    1) Enter valid gmail
    2) Set strong password
        a) one digit
        b) one capital latter
        c) one small latter
        d) one spical latter
        e) passwrod length min=8 , max=12
    """
    if(len(pwd) >= 8 and len(pwd) <= 12):
        lst = list(set(pwd))
        low = up = dig = sy = 0
        for i in lst:
            if(i.islower()):
                low = 1
            if(i.isupper()):
                up = 1
            if(i.isdigit()):
                dig = 1
            if(i in ("%", "$", "#", "&", "@", "_")):
                sy = 1
        if(low and up and dig and sy):
            if(gml[-4:] == ".com" and gml.find("@")>-1):
                return True
            else:
                messagebox.showerror("Invalid password.", "Invalid Gmail address")
        else:
            messagebox.showerror("Invalid password.", mess)
    else:
        messagebox.showerror("Invalid password.","Password length should be min=8 to max=12")




def SgnUp_Check():
    global lgn_user_lst, lgn_pswd_lst, curent_user,path
    
    file = open(
        f"{path}\Login_data.csv", "a")
    if(SgnUp_Gml_enty.get() == "" or SgnUp_pass_enty.get() == ""):
        messagebox.showerror("Empty Fillup", "Empty set password..")
    elif(SgnUp_Gml_enty.get() in lgn_user_lst):
        messagebox.showerror("Duplicate user", "Already have a account.")

    elif(password_check(SgnUp_Gml_enty.get(), SgnUp_pass_enty.get() ) ): 
        file.write(f"{SgnUp_Gml_enty.get()},{SgnUp_pass_enty.get()}\n")
        
        pth = os.path.join(path, "All_User")
    
        with open(f"{pth}\\{(SgnUp_Gml_enty.get()).split('@')[0]}.csv", "a"):
            pass
        
        messagebox.showinfo("Welcome", f"Welcome {SgnUp_Gml_enty.get().split('@')[0]} to \nCryptLock-Messenger!")
        lgn_user_lst.append(SgnUp_Gml_enty.get())
        lgn_pswd_lst.append(SgnUp_pass_enty.get())
        
        SgnUp_Gml_enty.delete(0, END)
        SgnUp_pass_enty.delete(0, END)
        login()
    
    file.close()
    
    
SgnUp_submit = Button(root, text="Submit", cursor="hand2", bg=btn_bg_clr, fg=btn_fg_clr,
                      borderwidth=btn_width, font=("Arial", 12, "bold"), command=SgnUp_Check)



def Sign_up():
    wlc_lbl.place_forget()
    gml_lbl.place_forget()
    gml_ent.place_forget()
    pswd_lbl.place_forget()
    pswd_ent.place_forget()
    submit.place_forget()
    Crt_act.place_forget()
    
       
    wlc_SgnUp.place(relx=0.4, rely=0.3)
    SgnUp_Gml_lbl.place(relx=0.2, rely=0.5)
    SgnUp_Gml_enty.place(relx=0.4, rely=0.5)
    SgnUp_pass_lbl.place(relx=0.2, rely=0.6)
    SgnUp_pass_enty.place(relx=0.4, rely=0.6)
    SgnUp_submit.place(relx=0.7, rely=0.8)
    


    
Crt_act = Button(root, text="Sign up", cursor="hand2",  bg=btn_bg_clr,fg=btn_fg_clr, borderwidth=btn_width, font=("Arial", 12, "bold"), command=Sign_up)

def forget_widget():
    
    SgnUp_submit.place_forget()
    
    wlc_SgnUp.place_forget()
    SgnUp_Gml_lbl.place_forget()
    SgnUp_Gml_enty.place_forget()
    SgnUp_pass_lbl.place_forget()
    SgnUp_pass_enty.place_forget()
    
    wlc_lbl.place_forget()
    gml_lbl.place_forget()
    gml_ent.place_forget()
    pswd_lbl.place_forget()
    pswd_ent.place_forget()
    submit.place_forget()
    Crt_act.place_forget()
    
    ch_mode.place_forget()
    enc_btn.place_forget()
    dec_btn.place_forget()
    
    Sgml_lbl.place_forget()
    Sgml_ent.place_forget()
    # fnd_lbl.place_forget()
    DNxt_btn.place_forget()
    
    Emsg_lbl.place_forget()
    Emsg_txt.place_forget()
    Ekey_lbl.place_forget()
    Ekey_ent.place_forget()
    rgml_lbl.place_forget()
    rgml_ent.place_forget()
    ENext_btn.place_forget()
    
    Dmsg_lbl.place_forget()
    Dmsg_txt.place_forget()
    Dkey_lbl.place_forget()
    Dkey_ent.place_forget()
    Dbtn.place_forget()
    
    
    
    global login_flag
    if(login_flag ==1):
        C_mode()
    else:
        login()
    

def login(): 
    
    FgPsd_gml_ent.delete(0, END)
    FgPsd_psd_ent.delete(0, END)    
    
    # update element forget 
    FgPsd_gml_lbl.place_forget()
    FgPsd_gml_ent.place_forget()
    FgPsd_psd_lbl.place_forget()
    FgPsd_psd_ent.place_forget()
    FgPsd_btn.place_forget()
    
    wlc_SgnUp.place_forget()
    SgnUp_Gml_lbl.place_forget()
    SgnUp_Gml_enty.place_forget()
    SgnUp_pass_lbl.place_forget()
    SgnUp_pass_enty.place_forget()
    SgnUp_submit.place_forget()
    
    wlc_lbl.place_forget()
    gml_lbl.place_forget()
    gml_ent.place_forget()
    pswd_lbl.place_forget()
    pswd_ent.place_forget()
    submit.place_forget()
    Crt_act.place_forget()
    
    # forget password element place forget
    FgPsd_gml_lbl.place_forget()
    FgPsd_gml_ent.place_forget()
    FgPsd_psd_lbl.place_forget()
    FgPsd_psd_ent.place_forget()
    FgPsd_btn.place_forget()
    
    wlc_lbl.place(relx=0.5, rely=0.15, anchor=CENTER)
    gml_lbl.place(relx=0.13, rely=0.3)
    gml_ent.place(relx=0.3, rely=0.3)
    pswd_lbl.place(relx=0.1, rely=0.4)
    pswd_ent.place(relx=0.3, rely=0.4)
    submit.place(relx=0.6, rely=.7)
    Crt_act.place(relx=0.6, rely=0.8)

         
# menubar item
def About():
    chose = messagebox.askyesno("Information", """
                        This is only for educational purposes and local 
                        message-passing applications.
                        ----------------------------------------------
                        
                        For more details, you can visit our website.
                        Do you want to visit, now?
                        """)
    
    if(chose):
        webbrowser.open_new_tab(
            "https://gmrai81.wixsite.com/golammostafarabby")


def Sign_out():
    global login_flag, curent_user
    choice = messagebox.askyesno("Sign out", "Do you want to Sign out?")
    if(choice):
        # root.destroy()
        gml_ent.delete(0, END)
        pswd_ent.delete(0, END)
        curent_user = ""
        root.title("CryptLock-Messenger")


        # -----------------------------
        SgnUp_submit.place_forget()

        wlc_SgnUp.place_forget()
        SgnUp_Gml_lbl.place_forget()
        SgnUp_Gml_enty.place_forget()
        SgnUp_pass_lbl.place_forget()
        SgnUp_pass_enty.place_forget()
        
        wlc_lbl.place_forget()
        gml_lbl.place_forget()
        gml_ent.place_forget()
        pswd_lbl.place_forget()
        pswd_ent.place_forget()
        submit.place_forget()
        Crt_act.place_forget()
        
        ch_mode.place_forget()
        enc_btn.place_forget()
        dec_btn.place_forget()
        
        Sgml_lbl.place_forget()
        Sgml_ent.place_forget()
        # fnd_lbl.place_forget()
        DNxt_btn.place_forget()
        
        Emsg_lbl.place_forget()
        Emsg_txt.place_forget()
        Ekey_lbl.place_forget()
        Ekey_ent.place_forget()
        rgml_lbl.place_forget()
        rgml_ent.place_forget()
        ENext_btn.place_forget()
        
        Dmsg_lbl.place_forget()
        Dmsg_txt.place_forget()
        Dkey_lbl.place_forget()
        Dkey_ent.place_forget()
        Dbtn.place_forget()
        # ----------------------------------

        menubar.delete(3)
        login_flag = 0
        login()
        
    

menubar = Menu(root)
root.config(menu=menubar)

# menu_inst = Menu(menubar)
# menu_main = Menu(menubar)

menubar.add_command(label="Home", command=forget_widget)
menubar.add_command(label="About", command=About)
# menubar.add_command(label="Sign Out",background="red",foreground="black", command=Sign_out)


Update_list()
login()


root.mainloop()