import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

def select_source_folder():
    folder = filedialog.askdirectory()
    if folder:
        source_entry.delete(0, tk.END)
        source_entry.insert(0, folder)

def select_target_folder():
    folder = filedialog.askdirectory()
    if folder:
        target_entry.delete(0, tk.END)
        target_entry.insert(0, folder)

def one_way_sync():
    source = source_entry.get()
    target = target_entry.get()
    
    if not os.path.exists(source):
        messagebox.showerror("Error", "Source folder does not exist")
        return
    
    if not os.path.exists(target):
        messagebox.showerror("Error", "Target folder does not exist")
        return
    
    for root, dirs, files in os.walk(source):
        relative_path = os.path.relpath(root, source)
        target_path = os.path.join(target, relative_path)
        
        if not os.path.exists(target_path):
            os.makedirs(target_path)
        
        for file in files:
            src_file = os.path.join(root, file)
            target_file = os.path.join(target_path, file)
            
            if not os.path.exists(target_file):
                shutil.copy2(src_file, target_file)
                log_text.insert(tk.END, f"Copied: {src_file} to {target_file}\n")
            else:
                log_text.insert(tk.END, f"Skipped: {src_file}\n")

def two_ways_sync():
    source = source_entry.get()
    target = target_entry.get()
    
    if not os.path.exists(source):
        messagebox.showerror("Error", "Source folder does not exist")
        return
    
    if not os.path.exists(target):
        messagebox.showerror("Error", "Target folder does not exist")
        return
    
    def sync_folders(src, tgt):
        for root, dirs, files in os.walk(src):
            relative_path = os.path.relpath(root, src)
            target_path = os.path.join(tgt, relative_path)
            
            if not os.path.exists(target_path):
                os.makedirs(target_path)
            
            for file in files:
                src_file = os.path.join(root, file)
                target_file = os.path.join(target_path, file)
                
                if not os.path.exists(target_file):
                    shutil.copy2(src_file, target_file)
                    log_text.insert(tk.END, f"Copied: {src_file} to {target_file}\n")
                else:
                    log_text.insert(tk.END, f"Skipped: {src_file}\n")
    
    sync_folders(source, target)
    sync_folders(target, source)

def compare_folders():
    source = source_entry.get()
    target = target_entry.get()
    
    if not os.path.exists(source):
        messagebox.showerror("Error", "Source folder does not exist")
        return
    
    if not os.path.exists(target):
        messagebox.showerror("Error", "Target folder does not exist")
        return
    
    source_text.delete(1.0, tk.END)
    target_text.delete(1.0, tk.END)
    
    def compare(src, tgt, src_text_widget, tgt_text_widget):
        src_files = set()
        tgt_files = set()
        
        for root, dirs, files in os.walk(src):
            relative_path = os.path.relpath(root, src)
            for file in files:
                src_files.add(os.path.join(relative_path, file))
        
        for root, dirs, files in os.walk(tgt):
            relative_path = os.path.relpath(root, tgt)
            for file in files:
                tgt_files.add(os.path.join(relative_path, file))
        
        for file in sorted(src_files):
            if file not in tgt_files:
                src_text_widget.insert(tk.END, f"{file}\n", 'new')
            else:
                src_text_widget.insert(tk.END, f"{file}\n")
        
        for file in sorted(tgt_files):
            if file not in src_files:
                tgt_text_widget.insert(tk.END, f"{file}\n", 'missing')
            else:
                tgt_text_widget.insert(tk.END, f"{file}\n")
    
    compare(source, target, source_text, target_text)

app = tk.Tk()
app.title("Folder Sync")

style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", background="#ccc")
style.configure("TFrame", background="#f0f0f0")
style.configure("TLabel", background="#f0f0f0")
style.configure("TText", background="#fff")

frame = ttk.Frame(app, padding="10 10 10 10")
frame.pack(pady=10)

source_label = ttk.Label(frame, text="Source Folder:")
source_label.grid(row=0, column=0, padx=5, pady=5)
source_entry = ttk.Entry(frame, width=50)
source_entry.grid(row=0, column=1, padx=5, pady=5)
source_button = ttk.Button(frame, text="Browse", command=select_source_folder)
source_button.grid(row=0, column=2, padx=5, pady=5)

target_label = ttk.Label(frame, text="Target Folder:")
target_label.grid(row=1, column=0, padx=5, pady=5)
target_entry = ttk.Entry(frame, width=50)
target_entry.grid(row=1, column=1, padx=5, pady=5)
target_button = ttk.Button(frame, text="Browse", command=select_target_folder)
target_button.grid(row=1, column=2, padx=5, pady=5)

one_way_button = ttk.Button(app, text="One Way Sync", command=one_way_sync)
one_way_button.pack(pady=10)

two_ways_button = ttk.Button(app, text="Two Ways Sync", command=two_ways_sync)
two_ways_button.pack(pady=10)

compare_button = ttk.Button(app, text="Compare", command=compare_folders)
compare_button.pack(pady=10)

log_label = ttk.Label(app, text="Log")
log_label.pack()
log_text = tk.Text(app, height=10, width=80, bg="#fff")
log_text.pack(pady=10)

compare_frame = ttk.Frame(app, padding="10 10 10 10")
compare_frame.pack(pady=10)

source_compare_label = ttk.Label(compare_frame, text="Source Folder Details")
source_compare_label.grid(row=0, column=0, padx=5, pady=5)
target_compare_label = ttk.Label(compare_frame, text="Target Folder Details")
target_compare_label.grid(row=0, column=1, padx=5, pady=5)

source_text = tk.Text(compare_frame, height=15, width=40, bg="#fff")
source_text.grid(row=1, column=0, padx=5, pady=5)
target_text = tk.Text(compare_frame, height=15, width=40, bg="#fff")
target_text.grid(row=1, column=1, padx=5, pady=5)

source_text.tag_config('new', background='green')
target_text.tag_config('missing', background='red')

app.mainloop()