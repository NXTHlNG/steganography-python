from tkinter import filedialog, messagebox
from tkinter import *
from PIL import Image, ImageTk
import os
import steno
import util
from customtkinter import *


IMAGE_WIDTH = 300
IMAGE_HEIGHT = 300


class App(CTk):
    def __init__(self):
        super().__init__()
        self.img = None
        self.data = None
        self.img_with_data = None
        self.extracted_data = None

        with Image.open('resources/no_image.png') as img:
            self.no_img = ImageTk.PhotoImage(img)

        self.title('Steganography')

        self.tabControl = CTkTabview(master=self)

        self.hide_data_tab = CTkFrame(self.tabControl)
        self.hide_data_tab = self.tabControl.add("Hide data")

        self.extract_data_tab = CTkFrame(self.tabControl)
        self.extract_data_tab = self.tabControl.add("Extract data")

        self.tabControl.pack()

        # Input image label and button
        self.input_image_label = CTkLabel(self.hide_data_tab, text='')
        self.input_image_label.configure(image=self.no_img)
        self.input_image_label.image = self.no_img
        self.input_image_label.pack()

        self.select_img_button = CTkButton(self.hide_data_tab, text='Select Image', command=self.select_img)
        self.select_img_button.pack(pady=10)

        # Data file label and button

        self.data_info_label = CTkLabel(self.hide_data_tab, text='Data size: 0 bytes\nData path empty')
        self.data_info_label.pack()

        self.select_data_button = CTkButton(self.hide_data_tab, text='Select Data', command=self.select_data)
        self.select_data_button.pack(pady=10)

        # Password entry
        # self.password_label = Label(root, text='Password (optional):')
        # self.password_label.pack()

        # self.password_entry = Entry(root, show='*')
        # self.password_entry.pack()

        # Output image label and button
        self.modded_image_label = CTkLabel(self.hide_data_tab, text='')
        self.modded_image_label.configure(image=self.no_img)
        self.modded_image_label.image = self.no_img
        self.modded_image_label.pack()

        self.modded_image_path_label = CTkLabel(self.hide_data_tab, text='Modified image path:')
        self.modded_image_path_label.pack()

        self.hide_data_button = CTkButton(self.hide_data_tab, text='Hide Data', command=self.hide_data)
        self.hide_data_button.pack()

        # Input image label and button
        self.input_modded_image = CTkLabel(self.extract_data_tab, text='')
        self.input_modded_image.configure(image=self.no_img)
        self.input_modded_image.image = self.no_img
        self.input_modded_image.pack()

        self.select_modded_image = CTkButton(self.extract_data_tab, text='Select Image', command=self.select_img_with_data)
        self.select_modded_image.pack()

        self.extracted_message_info_label = CTkLabel(self.extract_data_tab, text='Extracted data path:')
        self.extracted_message_info_label.pack()

        extract_data_button = CTkButton(self.extract_data_tab, text='Extract Data', command=self.extract_data)
        extract_data_button.pack()

    def select_img(self):
        img_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.jpg *.jpeg *.png")])

        if img_path:
            with Image.open(img_path) as img:
                self.img = img.convert("RGB")
                img_tk = ImageTk.PhotoImage(util.resize_image(self.img, IMAGE_WIDTH, IMAGE_HEIGHT))
                self.input_image_label.configure(image=img_tk)
                self.input_image_label.image = img_tk

    def select_img_with_data(self):
        img_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.jpg *.jpeg *.png")])

        if img_path:
            with Image.open(img_path) as img:
                self.img_with_data = img.convert("RGB")
                img_tk = ImageTk.PhotoImage(util.resize_image(self.img_with_data, IMAGE_WIDTH, IMAGE_HEIGHT))
                self.input_modded_image.configure(image=img_tk)
                self.input_modded_image.image = img_tk

    def select_data(self):
        data_path = filedialog.askopenfilename(title="Select data to hide", defaultextension="txt", filetypes=[("Text files", "*.txt")])

        if data_path:
            with open(data_path, "rb") as f:
                self.data = f.read()

            data_size = os.path.getsize(data_path)
            self.data_info_label.configure(text=f'Data size: {data_size} bytes\n{data_path}')

    def hide_data(self):
        if (self.img and self.data):
            modif_img_path = filedialog.asksaveasfilename(defaultextension="png", initialfile="modded_image")
            self.modded_image_path_label.configure(text=modif_img_path)
            img_with_msg = steno.hide_message(self.img, self.data)
            img_with_msg.save(modif_img_path)
            img_tk = ImageTk.PhotoImage(util.resize_image(img_with_msg, IMAGE_WIDTH, IMAGE_HEIGHT))
            self.modded_image_label.configure(image=img_tk)
            self.modded_image_label.image = img_tk
        else:
            messagebox.showerror("Error", "Select image and data")

    def extract_data(self):
        if (self.img_with_data):
            extracted_message_path = filedialog.asksaveasfilename(defaultextension="txt", initialfile="extracted_message")
            extracted_message = steno.extract_message(self.img_with_data)
            self.extracted_message_info_label.configure(text=f'Extracted message path: {extracted_message_path}\nMessage: {extracted_message}')
            with open(extracted_message_path, "w") as f:
                f.write(extracted_message)
        else:
            messagebox.showerror("Error", "Select image")


app = App()
app.mainloop()
