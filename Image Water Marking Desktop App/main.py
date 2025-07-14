from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageFont, ImageDraw

window = Tk()
window.title("Image Water Marking App")
window.config(padx=50, pady=50)

title_label = Label(text="Image Water Marking App", font=("Arial", 30, "bold"))
title_label.pack()

choose_image_button = Button(text="Choose Image", command=lambda: choose_image())
choose_image_button.pack(pady = 10)

canvas = Canvas(width=700, height=600)
canvas.pack()


display_image = None
main_image_to_save = None

def choose_image():
  global display_image, main_image_to_save
  file_path = filedialog.askopenfilename()
  if file_path:
    main = Image.open(file_path).convert("RGBA")
    main = main.resize((400, 400))

    watermark = Image.open("logo.png").convert("RGBA")
    watermark = watermark.resize((100, 100))

    position = (main.width -110, main.height -110)
    main.paste(watermark, position, mask=watermark)

    display_image = ImageTk.PhotoImage(main.convert("RGB"))
    main_image_to_save = main.convert("RGB")

    canvas.delete("all")
    canvas.create_image(350, 200, image=display_image)


def save_image():
  if main_image_to_save:
    save_path = filedialog.asksaveasfilename(
      defaultextension = ".png",
      filetypes=(("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*"))
    )
    if save_path:
      main_image_to_save.save(save_path)
      print(f"Image saved to {save_path}")
  else:
    print("No image loaded to save")


save_button = Button(window, text="Save", command=save_image)
save_button.place(y=600, x=350)
canvas.pack()
window.mainloop()