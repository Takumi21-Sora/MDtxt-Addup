import os
import glob
import re
import tkinter as tk
from tkinter import filedialog, messagebox

def extract_title(content):
    lines = content.split('\n')
    if lines and lines[0].startswith('#'):
        return lines[0].strip('# ')
    return None

def replace_japanese_dot(text):
    return text.replace('・', '·')

def merge_md_files(input_dir, output_file):
    md_files = glob.glob(os.path.join(input_dir, '*.md'))
    md_files.sort()
    
    chapter_index = 1
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for md_file in md_files:
            with open(md_file, 'r', encoding='utf-8') as infile:
                content = infile.read()
            
            chapter_title = extract_title(content)
            if chapter_title:
                content = '\n'.join(content.split('\n')[2:])
            else:
                chapter_title = os.path.splitext(os.path.basename(md_file))[0]
            
            chapter_title = replace_japanese_dot(chapter_title)
            
            # Add chapter marker
            outfile.write(f"\n\nChapter {chapter_index} {chapter_title}\n\n")
            chapter_index += 1
        
            content = replace_japanese_dot(content)
            
            outfile.write(content.strip())
            outfile.write("\n\n")
    
    return f"Merge completed, output file: {output_file}"

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Markdown File Merger")
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.input_label = tk.Label(self, text="Input directory:")
        self.input_label.pack()

        self.input_entry = tk.Entry(self, width=50)
        self.input_entry.pack()

        self.input_button = tk.Button(self, text="Choose directory", command=self.select_input_dir)
        self.input_button.pack()

        self.output_label = tk.Label(self, text="Output file:")
        self.output_label.pack()

        self.output_entry = tk.Entry(self, width=50)
        self.output_entry.pack()

        self.output_button = tk.Button(self, text="Choose file", command=self.select_output_file)
        self.output_button.pack()

        self.merge_button = tk.Button(self, text="Merge files", command=self.merge_files)
        self.merge_button.pack()

    def select_input_dir(self):
        self.input_dir = filedialog.askdirectory()
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, self.input_dir)

    def select_output_file(self):
        self.output_file = filedialog.asksaveasfilename(defaultextension=".txt")
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, self.output_file)

    def merge_files(self):
        input_dir = self.input_entry.get()
        output_file = self.output_entry.get()
        
        if not input_dir or not output_file:
            messagebox.showerror("Error", "Please select input directory and output file")
            return
        
        try:
            result = merge_md_files(input_dir, output_file)
            messagebox.showinfo("Success", result)
        except Exception as e:
            messagebox.showerror("Error", str(e))

root = tk.Tk()
app = Application(master=root)
app.mainloop()