import PySimpleGUI as sg
import os.path
from PIL import Image, ImageTk
import io

sg.theme('LightBrown6')

from main import classify

#---Needed to use Pillow becuase jpeg wasn't supported by PySimpleGui---

def get_img_data(f, maxsize=(1200, 850), first=False):
 
    img = Image.open(f)
    img.thumbnail(maxsize)
    if first:                     # tkinter is inactive the first time
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()
    return ImageTk.PhotoImage(img)

#---Columns for Layout---
file_list_column = [
    [
        sg.Text("Image Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
        )
    ],
]


image_viewer_column = [
    [sg.Text("Choose an image from list on left:")],
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-")],
]

result_column = [
    [sg.Button("Test that sucker!", key="-TEST-")],
    #[sg.Text("Result:")],
    [sg.Text(size=(30,1), key="-ROUT-")]
]

# ----- Full layout -----
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
        sg.VSeparator(),
        sg.Column(result_column)
    ]
]

# Compile layout and add it to window
window = sg.Window("Image Viewer", layout)


# ------ Event ------
filename = ''
while True:

    event, values = window.read()

    # Handle event of a folder being selected
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            # Get list of images in folder
            file_list = os.listdir(folder)
        except:
            file_list = []

        # Handle file directory
        fnames = [ f for f in file_list if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith((".png", ".gif", ".jpeg")) ]
        
        window["-FILE LIST-"].update(fnames)
    
    # File List
    elif event == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            window["-TOUT-"].update(filename)
            window["-IMAGE-"].update(data=get_img_data(filename, first=True))
            
        except:
            pass

    # Test button
    elif event == "-TEST-": 

        # Refactor image path
        abs_path_len = os.path.abspath(os.getcwd())
        path = '.'+ filename[len(abs_path_len):] 

        # Classify single image
        class_and_score = classify(path)

        # In the simple case when picture is assigned to only one class
        if len(class_and_score) == 1:   
            class_type, confidence = class_and_score[0]['class'], class_and_score[0]['score'] 
        
            if class_type == "masks_off": window['-ROUT-'].update("NO MASK!", text_color='red')
            else: window['-ROUT-'].update("MASK PRESENT!", text_color='green')
        
            print("Class: {}\nConfidence: {}\n".format(class_type, confidence))
        
        # Else, just print out the dictonary(?)
        else:
            window['-ROUT-'].update(str(class_and_score), text_color='white')

    if event == "Exit" or event == sg.WIN_CLOSED:
        break

