#python module that lets you edit datasets
#e.g. There is a PlayerMale and PlayerFemale label that should be trained as player by the detection model -> make both of them Player
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image,ImageTk
import os


FONT_TEXT = ("Helvetica",12)
FONT_SUBTITLE = ("Helvetica",14)
FONT_TITLE = ("Helvetica",30)


class DatasetEditorGUI:
    def __init__(self) -> None:
        self.window = self.create_main_window()
        #inits
        self.init_images()
        self.init_merge_lists()

    
    def start_gui(self):
        self.create_files_in_out(window=self.window)
        self.create_all_merges_frame(self.window)
        self.create_merges(self.window)
        self.create_add_merge_button(self.window)
        self.craete_edit_button(self.window)
        self.window.mainloop()

    def init_merge_lists(self):
        self.to_merge_tf = []
        self.merge_into_tf = []

    def init_images(self):
        self.search_img = ImageTk.PhotoImage(Image.open("workspace/src/img/search.png"),master=self.window)
        self.done_img = ImageTk.PhotoImage(Image.open("workspace/src/img/done.png"),master=self.window)
        self.warning_img = ImageTk.PhotoImage(Image.open("workspace/src/img/warning.png"),master=self.window)
        self.add_img = ImageTk.PhotoImage(Image.open("workspace/src/img/add.png"),master=self.window)
    
    def create_main_window(self):
        # Create the main window
        root = tk.Tk()
        root.geometry("400x800")
        root.title("Dataset Editor")

        # Create a Canvas widget
        canvas = tk.Canvas(root)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a Scrollbar widget
        scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the Canvas widget to use the Scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        # Create a Frame inside the Canvas to hold the content
        frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor='nw')

        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        return frame
    
    def create_files_in_out(self,window):
        ##in
        files_in_frame = tk.Frame(window)
        files_in_frame.pack(pady=10)
        files_label = tk.Label(files_in_frame,text="Folder of old dataset",font=FONT_SUBTITLE)
        files_label.pack(side=tk.LEFT,padx=10)
        files_in_button = tk.Button(files_in_frame,image=self.search_img,command=lambda:self.get_file(True))
        files_in_button.pack(side=tk.LEFT,padx=10)
        self.files_in_button = files_in_button
        ##out
        files_out_frame = tk.Frame(window)
        files_out_frame.pack(pady=10)
        files_out_labe = tk.Label(files_out_frame,text="Folder of new dataset",font=FONT_SUBTITLE)
        files_out_labe.pack(side=tk.LEFT,padx=10)
        files_out_button = tk.Button(files_out_frame,image=self.search_img,command=lambda:self.get_file(False))
        files_out_button.pack(side=tk.LEFT,padx=10)
        self.files_out_button = files_out_button
    
    def create_all_merges_frame(self,window):
        all_merge_frame = tk.Frame(window)
        all_merge_frame.pack(pady=10)
        self.all_merge_frame = all_merge_frame

    def create_merges(self,all_merge_frame):
        #create frame for merges
        merge_frame = tk.Frame(all_merge_frame)
        merge_frame.pack(pady=10)

        # Create a subtitle label
        subtitle_label = tk.Label(merge_frame, text="Merge Labels into One", font=FONT_SUBTITLE)
        subtitle_label.pack(pady=10)

        # Create a frame to hold the left zone
        left_frame = tk.Frame(merge_frame)
        left_frame.pack(side=tk.LEFT, padx=10)

        # Create a label for the left zone
        left_label = tk.Label(left_frame, text="Labels", font=FONT_TEXT)
        left_label.pack()

        # Create a text box for the left zone
        left_textbox = tk.Text(left_frame, height=10, width=20)
        left_textbox.pack(pady=10)
        self.to_merge_tf.append(left_textbox)

        # Create a frame to hold the middle zone
        middle_frame = tk.Frame(merge_frame)
        middle_frame.pack(side=tk.LEFT)

        # Create a label for the middle zone
        middle_label = tk.Label(middle_frame, text="Merge", font=FONT_TEXT)
        middle_label.pack()

        # Create a label for the arrow sign in the middle zone
        arrow_label = tk.Label(middle_frame, text=">", font=("Helvetica", 48))
        arrow_label.pack(pady=10)

        # Create a frame to hold the right zone
        right_frame = tk.Frame(merge_frame)
        right_frame.pack(side=tk.LEFT, padx=10)

        # Create a label for the right zone
        right_label = tk.Label(right_frame, text="Merged Label", font=FONT_TEXT)
        right_label.pack()

        # Create a text box for the right zone
        right_textbox = tk.Text(right_frame, height=10, width=20)
        right_textbox.pack(pady=10)
        self.merge_into_tf.append(right_textbox)

    def create_add_merge_button(self,window):
        merge_button = tk.Button(window,image=self.add_img,command=lambda:self.add_merge_option())
        merge_button.pack(pady=10)

    def craete_edit_button(self,window):

        # Create an "Edit Dataset" button
        edit_button = tk.Button(window, text="Edit Dataset", font=FONT_SUBTITLE, command=lambda:self.edit_dataset)
        edit_button.pack(pady=10)
    
    def add_merge_option(self):
        self.create_merges(self.all_merge_frame)
        
    
    def edit_dataset(self):
        # Function to handle the "Edit Dataset" button click event
        pass  # Add your implementation here

    def input_database_received(self,was_correctly):
        if was_correctly:
            self.files_in_button.config(image=self.done_img)
        else:
            self.files_in_button.config(image=self.warning_img)
    def output_dataset_reveiced(self,was_correctly):
        if was_correctly:
            self.files_out_button.config(image=self.done_img)
        else:
            self.files_out_button.config(image=self.warning_img)


    def check_if_folder_contains_all(self,parent_dir,to_check):
        for check in to_check:
            if not os.path.exists(os.path.join(parent_dir,check)):
                return False
        return True


    def get_file(self,folder_is_in):
        if folder_is_in:
            #just need to load this folder
            old_database_location = filedialog.askdirectory(title="Old dataset",initialdir="workspace/datasets")
            if old_database_location:
                to_check = ["images","labels","classes.txt"]
                self.input_database_received(self.check_if_folder_contains_all(old_database_location,to_check))  
            else:
                self.input_database_received(False)
    
        else:
            #need to create a new folder at requested location
            storage_location = filedialog.askdirectory(title="Where to save the new dataset?",initialdir="workspace/datasets")
            if storage_location:
                self.output_dataset_reveiced(not os.path.exists(storage_location))   
            else:   
                self.output_dataset_reveiced(False)

if __name__ == "__main__":
    DatasetEditorGUI().start_gui()
