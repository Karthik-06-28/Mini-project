from tkinter import *
from tkinter import filedialog
from tkinter import messagebox,ttk
# from PIL import ImageTk,Image
import matplotlib.pyplot as plt

total_retirement=0
monthly_retirement=0

def present_vs_future():
    monthly_income=float(income.get())
    monthly_contribution=float(monthly_saving_entry.get())
    categories=['Monthly Expenses','Projected Monthly Retirement Income','Monthly Contributions']
    values=[monthly_income-monthly_contribution,monthly_retirement,monthly_contribution]
    colors=['#66b3ff','#99ff99','#ffcc99']
    plt.figure(figsize=(8,6))
    bars=plt.bar(categories,values,color=colors,edgecolor='black')
    for bar in bars:
        plt.text(bar.get_x()+bar.get_width()/2,bar.get_height(),f"₹{bar.get_height():,.2f}",ha='center',va='bottom',fontsize=10)
    plt.title('Financial Overview: Income and Retirement Comparison',fontsize=14,fontweight='bold')
    plt.ylabel('Amount (₹)',fontsize=12)
    plt.tight_layout() #for padding 
    plt.show()

def calculate_future_income(current_age,retirement_age,monthly_contribution,annual_return):
    years_to_invest=retirement_age-current_age
    months_to_invest=years_to_invest*12
    future_value_of_contributions=monthly_contribution*(((1+annual_return/12)**months_to_invest-1)/(annual_return / 12))
    total_amount=future_value_of_contributions
    return total_amount,total_amount/(20*12) #after retirement the amount is being used for 20 years....

def calculate_and_show():
    global total_retirement, monthly_retirement
    try:
        current_age=int(current_age_entry.get())
        retirement_age=int(retirement_age_entry.get())
        monthly_contribution=float(monthly_saving_entry.get())
        annual_return=investment_options[investment_type.get()]  # Use selected investment's return rate
        if retirement_age <= current_age:
            raise ValueError("Retirement age must be greater than current age.")   
        total_retirement,monthly_retirement=calculate_future_income(current_age,retirement_age,monthly_contribution,annual_return)
        messagebox.showinfo("Expected Income at Retirement",
                            f"Total retirement amount: ₹{total_retirement:,.2f}\n"
                            f"Expected monthly retirement income(For 20 Years): ₹{monthly_retirement:,.2f}")
        present_vs_future() # Show financial overview graph after calculation
    except ValueError as ve:
        messagebox.showerror("Input Error", str(ve))

def show_additional_contribution():
    try:
        current_age=int(current_age_entry.get())
        retirement_age=int(retirement_age_entry.get())
        monthly_contribution=float(monthly_saving_entry.get())
        annual_return=investment_options[investment_type.get()]
        if retirement_age <= current_age:
            raise ValueError("Retirement age must be greater than current age.")
        increments=[0,5,10,15,20]  # Percent increments
        future_values=[]
        labels=[]
        for percent in increments:
            additional_contribution=monthly_contribution*(1+percent/100)
            future_value,_=calculate_future_income(current_age, retirement_age, additional_contribution, annual_return)
            future_values.append(future_value)
            labels.append(f"₹{additional_contribution:,.2f}")
        plt.figure(figsize=(10,6))
        colors=['#66b3ff','#99ff99','#ffcc99','#ff9999','#c2c2f0']
        bars=plt.bar(labels,future_values,color=colors,edgecolor='black')
        for bar in bars:
            plt.text(bar.get_x()+bar.get_width()/2, bar.get_height(),f"₹{bar.get_height():,.2f}",ha='center',va='bottom',fontsize=10)
        plt.title("Impact of Additional Contributions on Retirement Savings",fontsize=14,fontweight='bold')
        plt.xlabel("Monthly Contribution Amount (₹)",fontsize=12)
        plt.ylabel("Total Retirement Corpus (₹)",fontsize=12)
        plt.tight_layout()
        plt.show()
    except ValueError as ve:
        messagebox.showerror("Input Error",str(ve))

#for setting the help in the menu bar 
def show_help():
    help_text = (
        "1.Enter your monthly income.\n"
        "2.Provide your current age and planned retirement age.\n"
        "3.Select an investment type from the dropdown menu.\n"
        "4.Enter your monthly contribution amount.\n"
        "5.Click 'Calculate and Show Financial Graph' to see the financial overview.\n"
        "6.Use 'Show Additional Contributions Graph' to view the impact of increased contributions."
    )
    messagebox.showinfo("Help", help_text)

#for setting the about in menu bar
def show_about():
    about_text = (
        "Financial Overview and Retirement Calculation Tool\n"
        "This tool helps you plan your financial future by calculating\n"
        "1.Projected retirement savings\n"
        "2.Expected monthly retirement income\n"
        "3.The impact of additional contributions\n\n"
    )
    messagebox.showinfo("About", about_text)

def save_to_file():
    try:
        file_path=filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files","*.txt"),("All files","*.*")],
            title="Save Data"
        )
        if not file_path:
            return
        current_age=current_age_entry.get()
        retirement_age=retirement_age_entry.get()
        monthly_income=income.get()
        monthly_contribution=monthly_saving_entry.get()
        investment=investment_type.get()
        if not (current_age and retirement_age and monthly_income and monthly_contribution and investment):
            raise ValueError("All fields must be filled before saving.")
        with open(file_path,"w") as file:
            file.write("Financial Overview Data\n")
            file.write(f"Monthly Income: {monthly_income}\n")
            file.write(f"Current Age: {current_age}\n")
            file.write(f"Retirement Age: {retirement_age}\n")
            file.write(f"Investment Type: {investment}\n")
            file.write(f"Monthly Contribution: {monthly_contribution}\n")
        messagebox.showinfo("Save Successful","Data has been saved successfully!")
    except ValueError as ve:
        messagebox.showerror("Save Error", str(ve))

def open_file():
    try:
        file_path=filedialog.askopenfilename(
            filetypes=[("Text files","*.txt"),("All files", "*.*")],
            title="Open File"
        )
        if not file_path:
            return
        with open(file_path, "r") as file:
            lines=file.readlines()
        if len(lines)<5:
            raise ValueError("Invalid file format.")
        income.delete(0,END)
        current_age_entry.delete(0,END)
        retirement_age_entry.delete(0,END)
        monthly_saving_entry.delete(0,END)
        income.insert(0,lines[1].split(":")[1].strip())
        current_age_entry.insert(0,lines[2].split(":")[1].strip())
        retirement_age_entry.insert(0,lines[3].split(":")[1].strip())
        investment_type.set(lines[4].split(":")[1].strip())
        monthly_saving_entry.insert(0,lines[5].split(":")[1].strip())
        messagebox.showinfo("Open Successful","Data has been loaded successfully!")
    except Exception as e:
        messagebox.showerror("Open Error",f"Failed to open file: {e}")

#configuring the interface
root=Tk()
root.title("Financial Overview")
root.geometry('580x450')
root.configure(bg='#f0f8ff')
label_font=('Helvetica',12,'bold')
bg_color='#e6f2ff'
fg_color='#003366'
# bg_image=ImageTk.PhotoImage(Image.open("C:\\Users\\karthik\\OneDrive\\Desktop\\MINI-PROJECT\\BG.jpeg"))
# bg_label=Label(root,image=bg_image)
# bg_label.place(relwidth=1,relheight=1)
label_0=Label(root,text="Financial Overview and Retirement Calculation",font=("Helvetica", 14, "bold"), bg="#f0f0f0")
label_1=Label(root,text="Monthly Income",font=label_font,bg=bg_color,fg=fg_color)
label_2=Label(root,text="Current Age:",font=label_font,bg=bg_color,fg=fg_color)
label_3=Label(root,text="Retirement Age:",font=label_font,bg=bg_color,fg=fg_color)
label_4=Label(root,text="Investment Type:",font=label_font,bg=bg_color,fg=fg_color)
label_5=Label(root,text="Monthly Contribution:",font=label_font,bg=bg_color,fg=fg_color)
label_0.grid(row=0,columnspan=3,pady=10)
label_1.grid(row=1,column=1,padx=15,pady=10)
label_2.grid(row=2,column=1,padx=15,pady=10)
label_3.grid(row=3,column=1,padx=15,pady=10)
label_4.grid(row=4,column=1,padx=15,pady=10)
label_5.grid(row=5,column=1,padx=15,pady=10)
entry_font=('Helvetica',12)
income=Entry(root,font=entry_font)
current_age_entry=Entry(root,font=entry_font)
retirement_age_entry=Entry(root,font=entry_font)
# annual_return_entry=Entry(root,font=entry_font)
monthly_saving_entry=Entry(root,font=entry_font)
income.grid(row=1,column=2,padx=15,pady=10)
current_age_entry.grid(row=2,column=2,padx=15,pady=10)
retirement_age_entry.grid(row=3,column=2,padx=15,pady=10)
# annual_return_entry.grid(row=4,column=2,padx=15,pady=10)
monthly_saving_entry.grid(row=5,column=2,padx=15,pady=10)
# e1=income.get()
# e2=current_age.get()
# e3=retirement_age.get()
# e4=annual_return.get()
# e5=monthly_saving.get()
button_font=('Helvetica',12,'bold')
#investements options 
investment_options={
    "Fixed Deposits (FD)": 0.07,
    "Public Provident Fund (PPF)": 0.071,
    "Mutual Funds": 0.11,
    "Gold": 0.13,
    "National Pension System (NPS)": 0.1,
    "Post Office Monthly Income Scheme (POMIS)": 0.074,
    "Real Estate": 0.10,
    "Corporate Bonds": 0.08,
    "Government Bonds": 0.065
}
investment_type=StringVar()
investment_dropdown=ttk.Combobox(root,textvariable=investment_type,font=entry_font,values=list(investment_options.keys()), state="readonly")
investment_dropdown.grid(row=4, column=2, padx=15, pady=10)
investment_dropdown.set("Select Investment Type")
button_font=('Helvetica', 12, 'bold')
calculate_button=Button(root,text="Calculate and Show Financial Graph",command=calculate_and_show,font=button_font,bg="red",fg="white")
calculate_button.grid(row=7, columnspan=4, pady=10)
additional_graph_button=Button(root,text="Show Additional Contributions Graph",command=show_additional_contribution,font=button_font,bg="blue",fg="white")
additional_graph_button.grid(row=8,columnspan=4,pady=10)
menu_bar=Menu(root)
root.config(menu=menu_bar)
file_menu=Menu(menu_bar,tearoff=0)
file_menu.add_command(label="Save",command=save_to_file)
file_menu.add_command(label="Open",command=open_file)
file_menu.add_command(label="Exit",command=root.quit)
menu_bar.add_cascade(label="Menu",menu=file_menu)
help_menu=Menu(menu_bar, tearoff=0)
help_menu.add_command(label="How to Use",command=show_help)
menu_bar.add_cascade(label="Help",menu=help_menu)
about_menu=Menu(menu_bar,tearoff=0)
about_menu.add_command(label="About",command=show_about)
menu_bar.add_cascade(label="About",menu=about_menu)
# exit=Button(root,text="EXIT",command=root.quit,fg="Black",font=button_font) #will add in MENU 
# exit.grid(row=5,column=1,columnspan=2,padx=10,pady=5)
root.mainloop()