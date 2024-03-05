import cv2
import customtkinter
import tkinter as tk
from tkinter import Text, Scrollbar
from PIL import Image, ImageTk

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class FaceBlurApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        self.video = cv2.VideoCapture(0)
        self.is_camera_enabled = False
        self.is_debug_enabled = False
        self.is_gesture_enabled = False

        self.image_label = tk.Label(window)
        self.image_label.pack()

        self.button_frame = tk.Frame(window)
        self.button_frame.pack()

        self.toggle_gesture_button = tk.Button(self.button_frame, text="Toggle Gesture Recognition", command=self.toggle_gesture_recognition, padx=10)
        self.toggle_gesture_button.pack(side=tk.LEFT)

        self.toggle_camera_button = tk.Button(self.button_frame, text="Toggle Camera", command=self.toggle_camera, padx=10)
        self.toggle_camera_button.pack(side=tk.LEFT)

        self.debug_button = tk.Button(self.button_frame, text="Debug", command=self.toggle_debug_console, padx=10)
        self.debug_button.pack(side=tk.RIGHT)

        self.gray_image = Image.new("RGB", (640, 480), "gray")  # Создаем серый прямоугольник
        self.gray_photo = ImageTk.PhotoImage(self.gray_image)
        self.image_label.config(image=self.gray_photo)  # Устанавливаем серый прямоугольник по умолчанию

        self.debug_console = None

        self.timer = None

    def toggle_camera(self):
        self.is_camera_enabled = not self.is_camera_enabled
        if self.is_camera_enabled:
            self.start_camera()
        else:
            self.stop_camera()

        if self.is_debug_enabled:
                if self.is_camera_enabled:
                    self.send_debug_message("camera enabled")
                else:
                    self.send_debug_message("camera disabled")

    def start_camera(self):
        self.timer = self.window.after(10, self.update_frame)

    def stop_camera(self):
        if self.timer:
            self.window.after_cancel(self.timer)
        self.image_label.config(image=self.gray_photo)  # При отключении камеры отображаем серый прямоугольник

    def update_frame(self):
        ret, frame = self.video.read()
        if ret:
            # Зеркально отразить кадр по горизонтали
            frame = cv2.flip(frame, 1)

            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb_image)
            img = ImageTk.PhotoImage(image=img)

            self.image_label.img = img
            self.image_label.config(image=img)

        if self.is_camera_enabled:
            self.timer = self.window.after(10, self.update_frame)

    def toggle_debug_console(self):
        self.is_debug_enabled = not self.is_debug_enabled
        if self.is_debug_enabled:
            self.open_debug_console()
        else:
            self.close_debug_console()

    def open_debug_console(self):
        if not self.debug_console:
            self.debug_console = tk.Toplevel(self.window)
            self.debug_console.title("Debug Console")
            self.debug_console.resizable(False, False)  # Запрещаем изменение размеров окна

            self.debug_text = Text(self.debug_console)
            self.debug_text.pack(expand=True, fill=tk.BOTH)

            scrollbar = Scrollbar(self.debug_console, command=self.debug_text.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self.debug_text.config(yscrollcommand=scrollbar.set)

            self.window.bind("<Key>", self.on_key_pressed)

    def close_debug_console(self):
        if self.debug_console:
            self.debug_console.destroy()
            self.debug_console = None

    def on_key_pressed(self, event):
        self.debug_text.insert(tk.END, event.char)
        self.debug_text.see(tk.END)

    def toggle_gesture_recognition(self):
        self.is_gesture_enabled = not self.is_gesture_enabled
        if self.is_debug_enabled:
                if self.is_gesture_enabled:
                    self.send_debug_message("gesture recognition enabled")
                else:
                    self.send_debug_message("gesture recognition disabled")



    def send_debug_message(self, message):
        if self.is_debug_enabled and self.debug_text:
            self.debug_text.insert(tk.END, message + "\n")
            self.debug_text.see(tk.END)

if __name__ == "__main__":
    window = tk.Tk()
    app = FaceBlurApp(window, "Face Blur App")
    window.mainloop()
