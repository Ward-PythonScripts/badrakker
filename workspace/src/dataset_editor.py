#python module that lets you edit datasets
#e.g. There is a PlayerMale and PlayerFemale label that should be trained as player by the detection model -> make both of them Player
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog,messagebox
from PIL import Image,ImageTk
import os
from shutil import copyfile,rmtree
import json


FONT_TEXT = ("Helvetica",12)
FONT_SUBTITLE = ("Helvetica",14)
FONT_TITLE = ("Helvetica",30)


class DatasetEditorGUI:
    def __init__(self) -> None:
        self.window = self.create_main_window()
        #inits
        self.init_images()
        self.init_merge_lists()
        self.files_in_set = False
        self.files_out_set = False
        self.from_dir = None
        self.to_dir = None

    
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
        right_textbox = tk.Entry(right_frame)
        right_textbox.pack(pady=10)
        self.merge_into_tf.append(right_textbox)

    def create_add_merge_button(self,window):
        merge_button = tk.Button(window,image=self.add_img,command=lambda:self.add_merge_option())
        merge_button.pack(pady=10)

    def craete_edit_button(self,window):
        edit_button = tk.Button(window, text="Edit Dataset", font=FONT_SUBTITLE, command=lambda:self.edit_dataset())
        edit_button.pack(pady=10)
    
    def add_merge_option(self):
        self.create_merges(self.all_merge_frame)
        
    
    def edit_dataset(self):
        merge_into = []
        for tv in self.merge_into_tf:
            text = tv.get()
            text.replace(" ","_")
            text.replace("\t","_")
            merge_into.append(text)
        merge_from = []
        for tv in self.to_merge_tf:
            text = tv.get(1.0,tk.END)
            merge_from.append(input_text_to_list(text))

        ERROR_TITLE = "Can't start the conversion"
        
        if self.from_dir:
            if self.to_dir:
                if len(merge_into) > 0:
                    if len(merge_from) > 0:
                        start_conversion(from_dir=self.from_dir,to_dir=self.to_dir,to_merge=merge_from,merge_into=merge_into)
                    else:
                        messagebox.showerror(ERROR_TITLE,"Merge from was empty")
                else:
                    messagebox.showerror(ERROR_TITLE,"Merge into was empty")
            else:
                messagebox.showerror(ERROR_TITLE,"To directory was empty")
        else:
            messagebox.showerror(ERROR_TITLE,"From directory was empty")

        

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
                if self.check_if_folder_contains_all(old_database_location,to_check):
                    self.input_database_received(True)
                    self.from_dir = old_database_location  
            else:
                self.input_database_received(False)
    
        else:
            #need to create a new folder at requested location
            storage_location = filedialog.askdirectory(title="Where to save the new dataset?",initialdir="workspace/datasets")
            if storage_location:
                if not os.path.exists(storage_location):
                    self.output_dataset_reveiced(True)
                    self.to_dir = storage_location   
            else:   
                self.output_dataset_reveiced(False)


def start_conversion(from_dir,to_dir,to_merge,merge_into):
    os.mkdir(to_dir)

    image_path_new = os.path.join(to_dir,"images")
    os.mkdir(image_path_new)
    label_path_new = os.path.join(to_dir,"labels")
    os.mkdir(label_path_new)

    image_path_old = os.path.join(from_dir,"images")
    images = [f for f in os.listdir(image_path_old) if os.path.isfile(os.path.join(image_path_old, f))]
    labels_path_old = os.path.join(from_dir,"labels")
    labels = [f for f in os.listdir(labels_path_old) if os.path.isfile(os.path.join(labels_path_old, f))]

    #get id map
    with open(os.path.join(from_dir,'notes.json')) as json_f:
        data = json.load(json_f)
        categories = (data['categories'])
        cat_list = []
        id_map = {
            'categories':[],
            'remapping':[]
        }
        current_id = 0

        for cat in categories:
            if get_1d_index_in_2d(to_merge,cat['name']) != -1:
                #this is one that we need to merge-> write down in map what key it should get
                #first get to merge index
                merge_into_value = merge_into[get_1d_index_in_2d(to_merge,cat['name'])]
                was_id = current_id
                target_index = index_of_value_for_key_in_list(id_map["categories"],merge_into_value,'name')
                if target_index  == -1:
                    id_map["categories"].append({
                        'id':current_id,
                        'name':merge_into_value
                    })
                    current_id += 1
                else:
                    was_id = id_map["categories"][target_index]['id']
                    
                #then tell it the new position
                id_map['remapping'].append({
                    'from':cat['id'],
                    'to':was_id
                })
                        

            else:
                id_map['categories'].append({
                    'id':current_id,
                    'name':cat['name']
                })
                id_map["remapping"].append({
                    'from':cat['id'],
                    'to':current_id
                })
                current_id += 1


    #check if the same amount of images as labels
    if len(images) != len(labels):
        messagebox.showerror("Bad original dataset","Couldn't make a new dataset because there aren't the same amount of images and labels in the old datset")
        return
    for image in images:
        identifier = os.path.splitext(image)[0]
        label_file = identifier + ".txt"
        copyfile(os.path.join(image_path_old,image),os.path.join(image_path_new,image))

        #write to label file
        file_write = open(os.path.join(label_path_new,label_file),"w+")
        with open(os.path.join(labels_path_old,label_file),"r") as file_read:
            for line in file_read:
                line_lst = line.split(" ",1)
                id_orig = line_lst[0]
                id_new = get_to_from_id_map(id_map,id_orig)
                if id_new == -1:
                    raise Exception("new id returned -1, shouldn't")
                new_line = str(id_new) + " " + line_lst[1]

                file_write.write(new_line)
        file_write.close()
        file_read.close()

    #create classes.txt, just the classes from high id to low id
    categories = id_map["categories"]
    names = [None] * len(categories)
    for cat in categories:
        names[cat['id']] = cat['name']
    classes_write = open(os.path.join(to_dir,"classes.txt"),"w+")
    for i in range(0,len(names)):
        classes_write.write(names[i]+"\n")
    classes_write.close()

    #create notes.json
    with open(os.path.join(to_dir,"notes.json"),"w+") as json_write:
        json.dump({
            "categories":id_map["categories"],
            "info":data["info"]
        },json_write)
    json_write.close()


            


def index_of_value_for_key_in_list(lst,value,key):
    for i in range(0,len(lst)):
        if lst[i][key] == value:
            return i
    return -1


def get_1d_index_in_2d(lst,search_term):
    for i in range(0,len(lst)):
        if search_term in lst[i]:
            return i
    return -1


def get_to_from_id_map(id_map,from_id):
    remaps = id_map['remapping']
    for remap in remaps:
        if remap['from'] == int(from_id):
            return remap['to']
    return -1

    



def input_text_to_list(txt):
    li = []
    l = txt.split('\n')
    for item in l:
        item = item.replace(" ","_")
        item = item.replace("\t","_")
        if item != '':
            li.append(item)
    return li
    

if __name__ == "__main__":
    #DatasetEditorGUI().start_gui()
    try:
        rmtree("/home/markel/gitrepos/badrakker/workspace/datasets/markel")
    except Exception:
        pass
    start_conversion("/home/markel/gitrepos/badrakker/workspace/datasets/badrakker_1","/home/markel/gitrepos/badrakker/workspace/datasets/markel",[['PlayerMale','PlayerFemale']],['Player'])
