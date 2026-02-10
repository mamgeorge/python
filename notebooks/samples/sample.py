# https://www.youtube.com/watch?v=VmCbkSEyMM0
# python C:/workspace/github/python/notebooks/samples/sample.py
# pip install tcl tk
import tkinter as tk
import marspermit

# tk._test()

def check_login():
	username = varUser.get()
	password = varPass.get()
	print(f'USER: {username}')
	print(f'PASS: {'*' * len(password)}')

def return_user(event):
	entryPass.focus()

def return_pass(event):
		check_login()

root = tk.Tk()
root.title("MLG")
root.geometry("600x500")

varUser = tk.StringVar()
varPass = tk.StringVar()

# username
labelUser = tk.Label( root, text="User:" )
labelUser.grid(row=0, column=0, padx=5, pady=5 ) # label.pack()

entryUser = tk.Entry(root, textvariable=varUser)
entryUser.grid(row=0, column=1, padx=5, pady=5 ) # username.pack()
entryUser.bind('<Return>', return_user)

# password
labelPass = tk.Label( root, text="Pass: " )
labelPass.grid(row=1, column=0, padx=5, pady=5 ) # label.pack()

entryPass = tk.Entry(root, textvariable=varPass, show="*")
entryPass.grid(row=1, column=1, padx=5, pady=5 ) # username.pack()
entryPass.bind('<Return>', return_pass)

# button
buttonLogin = tk.Button( root, text="Login", command=check_login )
buttonLogin.grid(row=2, column=0, columnspan=2, padx=5, pady=5 ) # button.pack()

labelMirror = tk.Label(root, textvariable=varUser)
labelMirror.grid(row=3, column=0, padx=5, pady=5 )

root.mainloop()
