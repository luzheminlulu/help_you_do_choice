# coding:utf-8
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
import random

application_window = tk.Tk()
my_path = ""
my_filetypes = []
search_mode=1
result = []

def initial_window():
	global application_window,comboxlist,my_filetypes,get_filetypes_text,button1_text,button2_text
	
	application_window.geometry('600x300')#界面大小
	application_window.title("帮你做选择")
	
	title_label = tk.Label(application_window, text="帮你做选择",font=("黑体",30))
	title_label.place(x=200,y=20)
	
	combox_label = tk.Label(application_window, text="搜索方式:")
	combox_label.place(x=30,y=85)
	comboxlist=ttk.Combobox(application_window) #初始化	 
	comboxlist["values"]=("递归搜索","当前文件夹搜索")	
	comboxlist.bind("<<ComboboxSelected>>",change_search_mode)
	comboxlist.current(1)  #选择第2个	
	comboxlist.place(x=100,y=85)
	
	f=open("./HelpYouDoChoice.ini","r")
	file_type = f.read()
	f.close()
	my_filetypes=file_type.split(",")
	my_filetypes_show=''
	for i in my_filetypes:
		my_filetypes_show += i
		my_filetypes_show += ','
	
	get_filetypes_label = tk.Label(application_window, text='文件格式:')
	get_filetypes_label.place(x=30,y=120)
	get_filetypes_text = tk.Text(application_window, height=1, width=23)
	get_filetypes_text.insert('0.0', my_filetypes_show[:-1])
	get_filetypes_button = tk.Button(application_window, text='修改', command=get_filetypes)
	get_filetypes_text.place(x=100,y=125)
	get_filetypes_button.place(x=280,y=120)
	
	button1_text = tk.Text(application_window, height=1, width=60)
	button1 = tk.Button(application_window, text='选择文件夹', width=12, height=1, command=get_path)
	button1_text.place(x=30,y=185)
	button1.place(x=480,y=180)
	
	button2_text = tk.Text(application_window, height=1, width=60)
	button2 = tk.Button(application_window, text='选一个', width=12, height=1, command=get_file)
	button2_text.place(x=30,y=245)
	button2.place(x=480,y=240)

def get_filetypes():
	global my_filetypes
	new_filetype = get_filetypes_text.get('0.0', 'end')[:-1]
	f=open("./HelpYouDoChoice.ini","w")
	f.write(new_filetype)
	f.close()
	my_filetypes=new_filetype.split(",")

def change_search_mode(*args):	 #处理事件，*args表示可变参数	
	global comboxlist,search_mode
	if (comboxlist.get()=="递归搜索"):
		search_mode=0
	elif (comboxlist.get()=="当前文件夹搜索"):
		search_mode=1

def get_path():
	global my_path
	# 设置文件对话框会显示的文件类型
	# my_filetypes = [('all files', '.*'), ('text files', '.txt')]
	
	# 请求选择文件夹/目录
	my_path = filedialog.askdirectory(parent=application_window,
									initialdir=os.getcwd(),
									title="Please select a folder:")
	button1_text.delete('0.0', 'end')
	button1_text.insert('0.0', my_path)
	## 请求选择文件
	#answer = filedialog.askopenfilename(parent=application_window,initialdir=os.getcwd(),title="Please select a file:",filetypes=my_filetypes)
	## 请求选择一个或多个文件
	#answer = filedialog.askopenfilenames(parent=application_window,initialdir=os.getcwd(),title="Please select one or more files:",filetypes=my_filetypes)
	## 请求选择一个用以保存的文件
	#answer = filedialog.asksaveasfilename(parent=application_window,initialdir=os.getcwd(),title="Please select a file name for saving:",filetypes=my_filetypes)

def get_file():
	global my_path,my_filetypes,result

	try:
		result = []
		result = get_list(my_path,my_filetypes)
		movie = random.sample(result,1)[0]
	except:
		movie = "我也做不出选择呢！！！"
		
	button2_text.delete('0.0', 'end')
	button2_text.insert('0.0', movie)

def get_list(path,type):
	global result
	dir_list = os.listdir(path)
	
	if(search_mode==0):
		for file in dir_list:
			sub_dir = os.path.join(path,file)
			if os.path.isdir(sub_dir):
				get_list(sub_dir,type)
			else:
				filename,typename=os.path.splitext(file)
				for i in type:
					if typename==i:
						result.append(file)
						break
	elif(search_mode==1):
		for file in dir_list:
			filename,typename=os.path.splitext(file)
			for i in type:
				if typename==i:
					result.append(file)
					break
	return result
	

if __name__ == '__main__':
	initial_window()
	application_window.mainloop()
	
	


