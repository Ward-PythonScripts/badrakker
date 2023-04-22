#python module that lets you edit datasets
#e.g. There is a PlayerMale and PlayerFemale label that should be trained as player by the detection model -> make both of them Player
import tkinter as tk
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
        self.start_gui()
    
    def start_gui(self):
        self.create_files_in_out(window=self.window)
        self.create_merges(self.window)
        self.craete_edit_button(self.window)
        self.window.mainloop()

    def init_images(self):
        self.search_img = ImageTk.PhotoImage(Image.open("workspace/src/img/search.png"),master=self.window)
        self.done_img = ImageTk.PhotoImage(Image.open("workspace/src/img/done.png"),master=self.window)
        self.warning_img = ImageTk.PhotoImage(Image.open("workspace/src/img/warning.png"),master=self.window)
    
    def create_main_window(self):
        # Create the main window
        window = tk.Tk()
        window.title("Dataset Editor")

        # Create a title label
        title_label = tk.Label(window, text="Dataset Editor", font=FONT_TITLE)
        title_label.pack(pady=10)
        return window
    
    def create_files_in_out(self,window):
        ##in
        files_in_frame = tk.Frame(window)
        files_in_frame.pack(pady=10)
        files_label = tk.Label(files_in_frame,text="Folder of old dataset",font=FONT_SUBTITLE)
        files_label.pack(side=tk.LEFT,padx=10)
        files_in_button = tk.Button(files_in_frame,image=self.search_img,command=self.get_file(True))
        files_in_button.pack(side=tk.LEFT,padx=10)
        ##out
        files_out_frame = tk.Frame(window)
        files_out_frame.pack(pady=10)
        files_out_labe = tk.Label(files_out_frame,text="Folder of new dataset",font=FONT_SUBTITLE)
        files_out_labe.pack(side=tk.LEFT,padx=10)
        files_out_button = tk.Button(files_out_frame,image=self.search_img,command=self.get_file(False))
        files_out_button.pack(side=tk.LEFT,padx=10)


    def create_merges(self,window):
        #create frame for merges
        merge_frame = tk.Frame(window)
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

    def craete_edit_button(self,window):

        # Create an "Edit Dataset" button
        edit_button = tk.Button(window, text="Edit Dataset", font=FONT_SUBTITLE, command=self.edit_dataset)
        edit_button.pack(pady=10)
    
    
    def edit_dataset(self):
        # Function to handle the "Edit Dataset" button click event
        pass  # Add your implementation here

    def get_file(self,folder_is_in):
        print("getfile called")
        return None
        if folder_is_in:
            #just need to load this folder
            old_database_location = filedialog.askdirectory(title="Old dataset",initialdir="workspace/datasets")

            
        else:
            #need to create a new folder at requested location
            storage_location = filedialog.askdirectory(title="Where to save the new dataset?",initialdir="workspace/datasets")

        



if __name__ == "__main__":
    DatasetEditorGUI()
