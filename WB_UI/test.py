import cv2
import PIL.Image
import PIL.ImageTk
import tkinter as tk


def update_image(image_label, cv_capture):
    cv_image = cv_capture.read()[1]
    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
    pil_image = PIL.Image.fromarray(cv_image)
    tk_image = PIL.ImageTk.PhotoImage(image=pil_image)
    image_label.configure(image=tk_image)
    image_label._image_cache = tk_image  # avoid garbage collection
    root.update()


def update_all(root, image_label, cv_capture):
    if root.quit_flag:
        root.destroy()  # this avoids the update event being in limbo
    else:
        update_image(image_label, cv_capture)
        root.after(10, func=lambda: update_all(root, image_label, cv_capture))


if __name__ == '__main__':
    cv_capture = cv2.VideoCapture()
    cv_capture.open(0)  # have to use whatever your camera id actually is
    root = tk.Tk()
    setattr(root, 'quit_flag', False)
    def set_quit_flag():
        root.quit_flag = True
    root.protocol('WM_DELETE_WINDOW', set_quit_flag)  # avoid errors on exit
    image_label = tk.Label(master=root)  # the video will go here
    image_label.pack()
    root.after(0, func=lambda: update_all(root, image_label, cv_capture))
    root.mainloop()
