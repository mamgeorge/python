# https://www.youtube.com/watch?v=VmCbkSEyMM0
# python C:/workspace/github/python/notebooks/samples/marspermit.py
# pip install tcl tk
import tkinter as tk
from tkinter import ttk



def submit_landing_request():

	experienced = experience_text.get('1.0', 'end-1c')
	if experienced == '': experienced = 'STANDARD'

	print(f'Landing Site Selected: {site_var.get() }')
	print(f'Visting Purpose:     { purpose_var.get() }')
	print(f'Experience:          { experienced }')
	print(f'Rover Protection:    { rover_var.get() }')
	print(f'Mars Time Accepted:  { time_var.get() }')
	root.destroy()

root = tk.Tk()
root.title('Mars Surface Control: Landing Permit Application')
root.geometry('600x500')

# variables
site_var = tk.StringVar()
purpose_var = tk.IntVar()
rover_var = tk.BooleanVar()
time_var = tk.BooleanVar()
fontMain = ("Verdana", 12, "bold")

# landing site selection
site_label = ttk.Label(root, font=(fontMain), text='Intended Landing Site')
site_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

landing_sites = [

	"Olympus Mons, Base Alpha",
	"Valles Marineris, Research Station",
	"Rover Battle Stadium",
	"Hellas Impact Basin, Resort"
]

site_combo = ttk.Combobox(root, textvariable=site_var, values=landing_sites, width=30)
site_combo.grid(row=1, column=0, padx=5, pady=5, sticky='w')
site_combo.set('Select Landing Site')

# visit purpose
purpose_label = ttk.Label(root, font=(fontMain), text='Purpose of Visit: ')
purpose_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')

purposes = [

	("Terraforming Work Permit", 1),
	("Red Planet Tourism", 2),
	("Martian University Studies", 3),
	("Definitely Not Earth Invasion", 4)
]

for ictr, (text, value) in enumerate(purposes):
	rb = ttk.Radiobutton(root, text=text, variable=purpose_var, value=value)
	rb.grid(row=ictr+3, column=0, padx=20, pady=2, sticky='w')

# experience text area / textvariable=experience_var
experience_label = ttk.Label(root, font=(fontMain), text='Please explain your experience with low gravity environments: ')
experience_label.grid(row=8, column=0, padx=5, pady=5, sticky='w')

experience_text = tk.Text(root, height=4, width=50)
experience_text.grid(row=9, column=0, padx=5, pady=5, sticky='w')

# required declarations
declaration_label = ttk.Label(root, font=(fontMain), text='Required Declarations: ')
declaration_label.grid(row=10, column=0, padx=5, pady=10, sticky='w')

rover_check = ttk.Checkbutton(root, variable=rover_var, text='I am not allergic to iron oxide')
rover_check.grid(row=13, column=0, padx=5, pady=2, sticky='w')

time_check = ttk.Checkbutton(root, variable=time_var, text='I accept that a Mars day is 24 hours and 37 minutes')
time_check.grid(row=14, column=0, padx=5, pady=2, sticky='w')

# Submit Button
submit_button = tk.Button(root, text='Submit Landing Request',
	bg="#FFBF00", fg="white", font=(fontMain),
	command=submit_landing_request )
submit_button.grid(row=15, column=0, padx=5, pady=40, sticky='w')

root.mainloop()

