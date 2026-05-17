import tkinter as tk

def on_click():
    label.config(text="Hello, " + entry.get())

root = tk.Tk()
root.title("Tkinter 示例")
root.geometry("300x200")
label = tk.Label(root, text="请输入姓名：")
label.pack(pady=10)

entry = tk.Entry(root)
entry.pack(pady=5)

button = tk.Button(root, text="打招呼", command=on_click)
button.pack(pady=5)

root.mainloop()