#Get x amount of images from a video file
import cv2
import random
import tkinter as tk
from tkinter import filedialog, simpledialog
import os

def get_x_images(filename,amount_of_images,storage_location,image_names):
    vidcap = cv2.VideoCapture(filename)
    #create directory to store the images
    new_file_store_path = os.path.join(storage_location,image_names)
    if not os.path.exists(new_file_store_path):
        os.makedirs(new_file_store_path)
    else:
        #shouldn't happen
        print("wanted to store images in path", new_file_store_path,"but path already exists")
        exit()
    # get total number of frames
    totalFrames = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)

    usedFrames = []
    for index in range(0,amount_of_images):
        
        randomFrameNumber=random.randint(0, totalFrames)
        #don't want to get two the same frames
        while randomFrameNumber in usedFrames:
            randomFrameNumber = random.randint(0,totalFrames)
        # set frame position
        usedFrames.append(randomFrameNumber)
        vidcap.set(cv2.CAP_PROP_POS_FRAMES,randomFrameNumber)
        success, image = vidcap.read()
        file_path = os.path.join(new_file_store_path,image_names+"_"+str(index)+".jpg")
        if success:
            cv2.imwrite(file_path, image)
    vidcap.release()


def exit_if_no_file(result):
    if result is None or result == "":
        print("User didn't give answer so we don't continue work")
        exit()

def main():
    root = tk.Tk()
    root.withdraw()

    source_video = filedialog.askopenfile(defaultextension='.mp4',initialdir='footage',title="Which video do you want to get images from?")
    exit_if_no_file(source_video)
    amount_of_images = simpledialog.askinteger("How many images do you want?", "amount of images:\t\t\t\t\t\t")
    exit_if_no_file(amount_of_images)
    image_name = simpledialog.askstring("What should the images be named?",'image name: \t\t\t\t\t\t\t')
    exit_if_no_file(image_name)
    storage_location = filedialog.askdirectory(title="Where to save directory with images?",initialdir="collected_images")
    exit_if_no_file(storage_location)
    get_x_images(source_video.name,amount_of_images,storage_location,image_name)


if __name__ == "__main__":
    main()