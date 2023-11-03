import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
import socket
import json
import funcClient
from tkinter import messagebox
from tkinter import filedialog, StringVar, OptionMenu
# def show_home_page():
#     flogin.pack_forget()
#     fregister.pack_forget()
#     window.geometry("650x600")
#     pageHome.pack()
#     rightListUsers.pack_forget()
#     rightListFiles.pack()
def show_frame(frame):
    # Ẩn tất cả các khung
    flogin.pack_forget()
    fregister.pack_forget()
    pageAdmin.pack_forget()
    pageHome.pack_forget()
    # Hiển thị khung được chỉ định
    frame.pack()

def switch_to_flogin():
    fregister_error_username.config(text="")
    show_frame(flogin)
def deleteFilePublish(file): 
    files = funcClient.sendDeleteFilePublish(file)
    showPublishFiles(files)

def showPublishFiles(files):
    for widget in leftpagehomeL.winfo_children():
        widget.destroy()
    for widget in leftpagehomeR.winfo_children():
        widget.destroy()
    for widget in leftpagehomeM.winfo_children():
        widget.destroy()
    tk.Label(leftpagehomeL, text="Tên file:").pack()
    tk.Label(leftpagehomeM, text="Địa chỉ:").pack()
    tk.Label(leftpagehomeR, text="Action:").pack()
    for file in files:
        tk.Label(leftpagehomeL, text=file[1], pady=5).pack()
        tk.Label(leftpagehomeM, text=file[0],  wraplength=230, padx=10, pady=5).pack()
        tk.Button(leftpagehomeR, text="Xóa", command=lambda fl=file: deleteFilePublish(fl)).pack(pady=5)
def switch_to_fregister():
    error_login.config(text="")
    show_frame(fregister)
def switch_to_home_page():
    rightListUsers.pack_forget()
    rightListFiles.pack()
    window.geometry("650x600")
    show_frame(pageHome)
def switch_to_admin_page():
    show_frame(pageAdmin)
    
    
    show_frame(pageAdmin)
def register():
    username = fregister_username_entry.get()
    password = fregister_password_entry.get()
    repassword = fregister_repassword_entry.get()
    if len(username) != 0 and len(password) != 0:
        if password == repassword:
            message = funcClient.sendRegister(username, password)
            if(message == "success"):
                show_frame(flogin)
            else:
                fregister_error_username.config(text="Tên đăng nhập đã được sử dụng")
        else: fregister_error_username.config(text="Mật khẩu nhập lại không trùng khớp")
        fregister_username_entry.delete(0, tk.END)
        fregister_password_entry.delete(0, tk.END)
        fregister_repassword_entry.delete(0, tk.END)
        fregister_username_entry.focus()
def show_admin_page(): return
def login():
    username = flogin_username_entry.get()
    password = flogin_password_entry.get()
    if len(username) != 0 and len(password) != 0:
        message = funcClient.sendLogin(username, password)
        if not message:
            error_login.config(text="Tài khoản hoặc mật khẩu không đúng", fg="red")
        else:
            role = message["role"]
            data = message["data"]
            if role == "admin":
                users = data
                for user in users:
                    tk.Label(pageAdminL, text=user[1], pady=5).pack()
                    if user[0] == True:
                        tk.Label(pageAdminM, text="online",  wraplength=230, padx=10, pady=5).pack()
                    else:
                        tk.Label(pageAdminM, text="ofline",  wraplength=230, padx=10, pady=5).pack()
                        
                    tk.Button(pageAdminR, text="Discover files", command=lambda username=user[1]: deleteFilePublish(username)).pack(pady=5)
                switch_to_admin_page()
            else:
                username = data[0]
                rightpagehome_username_label.config(text=username)
                files = data[1]
                listAvalFiles = ", ".join(data[2])
                rightpagehome_files_server.config(text=f"Các files có thể fetch bao gồm: {listAvalFiles}" ,  anchor='w', pady=10, wraplength=280)
                showPublishFiles(files)
                switch_to_home_page()
    
    flogin_username_entry.delete(0, tk.END)
    flogin_password_entry.delete(0, tk.END)
    flogin_username_entry.focus()

def select_directory():
    global directory_path 
    directory_path = filedialog.askdirectory()
    if directory_path:
        error_publish_file.config(text="")
        leftpagehome_address_label.config(text=f"Vị trí file tại: {directory_path}", wraplength=380, justify="left")
def select_directory_save():
    global directory_path_save 
    directory_path_save = filedialog.askdirectory()
    if directory_path_save:
        rightpagehome_address_save_label.config(text=f"Vị trí lưu file tại: {directory_path_save}", wraplength=280, justify="left")
     
def publishFile ():
    global directory_path
    namefile = leftpagehome_namefile_entry.get()
    if len(namefile) != 0:
        if len(directory_path) != 0:
            message = funcClient.sendPublishFile(directory_path,namefile)
            if type(message) == str:
                print("errror")
            else:
                tk.Label(leftpagehomeL, text=namefile, pady=5).pack()
                tk.Label(leftpagehomeM, text=directory_path,  wraplength=380, padx=10, pady=5).pack()
                tk.Button(leftpagehomeR, text="Xóa", command=lambda x=directory_path, y = namefile: deleteFilePublish([x, y])).pack(pady=5)
                directory_path=""
                leftpagehome_namefile_entry.delete(0, tk.END)
                leftpagehome_address_label.config(text=f"Vị trí file tại:")    
        else:
            error_publish_file.config(text="Vị trí file không được trống")
    
    
    return
def get_user_files ():
    global optionList
    namefile = rightpagehome_namefile_save_entry.get()
    if len(namefile) != 0:
        users = funcClient.sendGetUsersFile(namefile)
        rightpagehome_users_have_file.config( text=f"Danh sách người dùng hiện online và có file {namefile}")
        menuUsers['menu'].delete(0, 'end')
        for user in users:
            menuUsers['menu'].add_command(label=user,command=tk._setit(optionList, user))
        optionList.set("Chọn người lấy file")
        rightListFiles.pack_forget()
        rightListUsers.pack()
        rightpagehome_namefile_save_entry.delete(0, tk.END)
    return
def logOut(): 
    funcClient.sendLogOut()
    switch_to_flogin()
    window.geometry("400x350")

def on_closing():
    funcClient.sendLogOut()
    window.destroy()
# def OptionMenu_ChooseUser(event):
#     messagebox.showinfo("Option Menu", "You have selected the option: " + str(optionList.get()))
def fetchFile():
    funcClient.sendFetchFile(str(optionList.get()),directory_path_save, percent_download)
    
directory_path_save="./"
directory_path=""
window = tk.Tk()
window.title("Đăng ký và Đăng nhập")
window.geometry("400x350")
flogin = tk.Frame(window)
fregister = tk.Frame(window)

pageAdmin = tk.Frame(window)
pageAdminL = tk.Frame(pageAdmin)
pageAdminM = tk.Frame(pageAdmin)
pageAdminR = tk.Frame(pageAdmin)


pageHome = tk.Frame(window)
leftpagehome = tk.Frame(pageHome, width=400)
leftpagehome.pack(side="left",padx=10, anchor="n")
leftpagehomeL = tk.Frame(leftpagehome, width=50)
leftpagehomeM = tk.Frame(leftpagehome, width=300)
leftpagehomeR = tk.Frame(leftpagehome, width=50)
rightpagehome = tk.Frame(pageHome, width=300)
rightpagehome.pack(side="right", padx=10, anchor="n")
rightListUsers = tk.Frame(rightpagehome)
rightListFiles = tk.Frame(rightpagehome)
listboxPublishFile = tk.Listbox(leftpagehome)

font_style = tkFont.Font(family="Helvetica", size=16, weight="bold", slant="italic")
font_style_title = tkFont.Font(family="Helvetica", size=14, weight="bold", slant="italic")
font_style1 = tkFont.Font( size=16,  slant="italic")

flogin_username_label = tk.Label(flogin, text="File sharing with P2P",font=font_style, pady=15)
flogin_username_label.pack()
flogin_username_label = tk.Label(flogin, text="Tên đăng nhập:" )
flogin_username_label.pack()

flogin_username_entry = tk.Entry(flogin,font=15 )
flogin_username_entry.pack(pady=5)

flogin_password_label = tk.Label(flogin, text="Mật khẩu:")
flogin_password_label.pack()
flogin_password_entry = tk.Entry(flogin, show="*", font=15 )  # Sử dụng dấu '*' để ẩn mật khẩu
flogin_password_entry.pack(pady=5)
flogin_login_button = tk.Button(flogin, text="Đăng nhập", command=login, cursor="hand2", pady=10, padx=20)
flogin_login_button.pack(pady=10)
flogin_register_button = tk.Button(flogin, text="Đi tới đăng ký", command=switch_to_fregister, borderwidth=0,  cursor="hand2")
flogin_register_button.pack()

error_login = tk.Label(flogin, text="", pady=20)
error_login.pack()


fregister_username_label = tk.Label(fregister, text="File sharing with P2P",font=font_style, pady=15)
fregister_username_label.pack()
fregister_error_username = tk.Label(fregister, text="", fg="red")
fregister_error_username .pack()
fregister_username_label = tk.Label(fregister, text="Tên đăng nhập:" )
fregister_username_label.pack()
fregister_username_entry = tk.Entry(fregister,font=15 )
fregister_username_entry.pack(pady=5)
fregister_password_label = tk.Label(fregister, text="Mật khẩu:")
fregister_password_label.pack()
fregister_password_entry = tk.Entry(fregister, show="*", font=15 )  # Sử dụng dấu '*' để ẩn mật khẩu
fregister_password_entry.pack(pady=5)
fregister_repassword_label = tk.Label(fregister, text="Nhập lại mật khẩu:")
fregister_repassword_label.pack()
fregister_repassword_entry = tk.Entry(fregister, show="*", font=15 )  # Sử dụng dấu '*' để ẩn mật khẩu
fregister_repassword_entry.pack(pady=5)
fregister_login_button = tk.Button(fregister, text="Đăng ký", command=register, cursor="hand2", pady=10, padx=20)
fregister_login_button.pack(pady=10)
fregister_register_button = tk.Button(fregister, text="Đi tới đăng nhập", command=switch_to_flogin, borderwidth=0,  cursor="hand2")
fregister_register_button.pack()

fregister_username_label = tk.Label(pageAdmin, text="File sharing with P2P",font=font_style, pady=10)
fregister_username_label.pack()
tk.Label(pageAdmin, text="Các người dùng đã đăng ký trên server",font=font_style_title, anchor='w').pack(fill='both')
tk.Label(pageAdminL, text="Tên user:", padx=10).pack()
tk.Label(pageAdminM, text="Tình trạng:", padx=50).pack()
tk.Label(pageAdminR, text="Action:", padx=10).pack()
pageAdminL.pack(side="left")
pageAdminM.pack(side="left")
pageAdminR.pack(side="right")


leftpagehome_username_label = tk.Label(leftpagehome, text="File sharing with P2P",font=font_style, pady=15, padx=10)
leftpagehome_username_label.pack()



logout = tk.Frame(rightpagehome)
rightpagehome_button_logout= tk.Button(logout, text="logout", command=logOut, cursor='hand2')
rightpagehome_button_logout.pack(side="right")
rightpagehome_username_label = tk.Label(logout, text="Minhpro", pady=15, padx=10, font=font_style)
rightpagehome_username_label.pack(side="right")
logout.pack()

leftpagehome_username_label = tk.Label(leftpagehome,font=font_style_title ,text="Tải tên file có thể chia sẽ lên server", anchor='w')
leftpagehome_username_label.pack(fill='both')
error_publish_file = tk.Label(leftpagehome, text="", fg="red")
error_publish_file.pack()
leftpagehome_select_button = tk.Button(leftpagehome, text="Chọn vị trí file", command=select_directory, anchor='w')
leftpagehome_select_button.pack()
leftpagehome_address_label = tk.Label(leftpagehome, text=f"Vị trí file tại:  {directory_path}", anchor="w")
leftpagehome_address_label.pack(fill="both")
leftpagehome_namefile_label = tk.Label(leftpagehome, text="Tên file:")
leftpagehome_namefile_label.pack()
leftpagehome_namefile_entry = tk.Entry(leftpagehome,font=20 )  # Sử dụng dấu '*' để ẩn mật khẩu
leftpagehome_namefile_entry.pack()
leftpagehome_publish_button = tk.Button(leftpagehome, text="publish", padx=10, pady=10, command=publishFile,  cursor="hand2")
leftpagehome_publish_button.pack(pady=10, padx=20)

leftpagehome_username_label = tk.Label(leftpagehome, text="Các files đã publish lên server",font=font_style_title, anchor='w', pady=10)
leftpagehome_username_label.pack(fill='both')
tk.Label(leftpagehomeL, text="Tên file:").pack()
tk.Label(leftpagehomeM, text="Địa chỉ file:").pack()
tk.Label(leftpagehomeR, text="Action:").pack()
leftpagehomeL.pack(side="left")
leftpagehomeM.pack(side="left")
leftpagehomeR.pack(side="left")
# leftpagehomeM.grid(row=0, column=1)
# leftpagehomeR.grid(row=0, column=2)

tk.Label(rightpagehome, text="fetch file", font=font_style_title , anchor='w').pack(fill='both')
tk.Label(rightpagehome, text="", fg="red").pack()
rightpagehome_select_save_button = tk.Button(rightpagehome, text="Chọn vị trí lưu file", command=select_directory_save, anchor='w')
rightpagehome_select_save_button.pack()
rightpagehome_address_save_label = tk.Label(rightpagehome, text=f"Vị trí lưu file tại:  {directory_path_save}", anchor="w")
rightpagehome_address_save_label.pack(fill="both")
rightpagehome_namefile_save_label = tk.Label(rightpagehome, text="Tên file:")
rightpagehome_namefile_save_label.pack()
rightpagehome_namefile_save_entry = tk.Entry(rightpagehome, font=20 )  # Sử dụng dấu '*' để ẩn mật khẩu
rightpagehome_namefile_save_entry.pack()
rightpagehome_fetch_button = tk.Button(rightpagehome, text="fetch", command=get_user_files,  cursor="hand2", padx=10, pady=10)
rightpagehome_fetch_button.pack(pady=10)

rightpagehome_files_server = tk.Label(rightListFiles, text="Các files có thể fetch bao gồm:", anchor='w', pady=10)
rightpagehome_files_server.pack(fill='both')
rightpagehome_users_have_file =  tk.Label(rightListUsers, text="Danh sách người dùng hiện online và có file", font=font_style_title, wraplength=320, anchor='w', pady=10)
rightpagehome_users_have_file.pack(fill='both')
users = ["Name"]
optionList = StringVar()
optionList.set("Chọn người lấy file")
menuUsers = ttk.OptionMenu(rightListUsers, optionList, *users)
menuUsers.pack()
tk.Button(rightListUsers, text="Lấy file", padx=10,pady=10, command=fetchFile,  cursor="hand2").pack( padx=5)
# tk.Label(rightListUsers, text="",anchor='w', pady=10).pack()
percent_download = tk.Label(rightListUsers, text="", pady=10)
percent_download.pack()
tk.Button(rightListUsers, text="Tải lại trang", padx=10, command=switch_to_home_page,  cursor="hand2").pack( padx=5, pady=20)

 # presets the first option
# options = ["Option A", "Option B", "Option C", "Option D"]
# OptionMenu(rightListUsers, optionList, *(options), command=OptionMenu_ChooseUser).pack()
# leftpagehome_publish_button = tk.Button(leftpagehome, text="publish", padx=10, pady=10, command=publishFile,  cursor="hand2")
# leftpagehome_publish_button.pack(pady=10, padx=20)




window.protocol("WM_DELETE_WINDOW", on_closing)

show_frame(flogin)
window.mainloop()
