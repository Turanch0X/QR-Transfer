import qrcode, tkinter, io, win32clipboard
from tkinter import filedialog
from PIL import ImageTk

window = tkinter.Tk()
window_size = (520,550)
text_font = ('Georgia', 14)
enter_font = ('Georgia', 20)
enter_hint = "Paste URL here:"

window.geometry(f'{window_size[0]}x{window_size[1]}+750+100')
window.title("QR-Transfer")
window.config(background='grey')
window.iconbitmap("logo.ico")

canvas_up = tkinter.Canvas(window, bg='white', width=window_size[0], height=60)
canvas_up.pack()

canvas_down = tkinter.Canvas(window, bg='grey', highlightthickness=0, relief="flat")
canvas_down.pack()

qr = qrcode.QRCode(version = 2.5, error_correction = qrcode.ERROR_CORRECT_L, box_size = 10, border = 3)

def show_hint(event):
    if entry.get()==enter_hint:
        entry.delete(0, tkinter.END)
        entry.config(fg='black')

def hide_hint(event):
    if entry.get()=='':
        entry.insert(0, enter_hint)
        entry.config(fg='grey')

def input_delete():
    if not entry.get():
        tkinter.messagebox.showwarning("Input Error.", "Please enter correct URL.")
    else:
        entry.delete(0, tkinter.END)

def transfer_url_to_image():
    if not entry.get() or 'https' not in entry.get():
        tkinter.messagebox.showwarning("Input Error.", "Please enter correct URL.")
        return
    else:
        qr.clear()
        qr.add_data(entry.get())
        qr.make(fit = True)
        image = qr.make_image(fill='black', back_color = 'white')
        if image:
            qr_photo = ImageTk.PhotoImage(image)
            image_labl.config(image = qr_photo)
            image_labl.image = qr_photo
            image_labl.grid(row=0, column=0, columnspan=2)
            save_btn.grid(row=1, column=0, sticky='NSEW')
            copy_btn.grid(row=1, column=1, sticky='NSEW')
            save_btn.config(command=lambda: save_image(image))
            copy_btn.config(command=lambda: copy_image(image))

def save_image(qr_image_obj):
    file_path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[("Image Files", "*.png")])
    if file_path:
        qr_image_obj.save(file_path)

        tkinter.messagebox.showinfo("Success", f"QR code image has been saved as {file_path}")

def copy_image(qr_image_obj):
    qr_image_obj = qr_image_obj.convert("RGB")
    output = io.BytesIO()
    qr_image_obj.save(output, format="BMP")
    data = output.getvalue()[14:]  # Skip BMP header
    output.close()
    
    win32clipboard.OpenClipboard()
    try:
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    finally:
        win32clipboard.CloseClipboard()

    tkinter.messagebox.showinfo("Success", "QR code image copied to clipboard!")
    
entry = tkinter.Entry(window, background='grey', font=enter_font, border=5, relief='ridge')
entry.insert(0, enter_hint)
run_btn = tkinter.Button(window, text="Run", bg='orange', font=text_font, border=5, relief='ridge', command=transfer_url_to_image)
delete_btn = tkinter.Button(window, text="Delete", bg='orange', font=text_font, border=5, relief='ridge', command=input_delete)

image_labl = tkinter.Label(canvas_down, bg='grey', justify='center', border=5, relief='ridge')
save_btn = tkinter.Button(canvas_down, text="Save", bg='orange', border=5, relief='ridge', font=text_font)
copy_btn = tkinter.Button(canvas_down, text="Copy", bg='orange', border=5, relief='ridge', font=text_font)

entry.bind('<FocusIn>', show_hint)
entry.bind('<FocusOut>', hide_hint)
save_btn.config(command=lambda: save_image(image_labl))

canvas_up.create_window(180, 30, window=entry)
canvas_up.create_window(480, 30, window=delete_btn)
canvas_up.create_window(400, 30, window=run_btn)

window.mainloop()