import sys

# GUI = Graphical User Interface. tkinter is the toolkit that comes with Python.
# It needs a DESKTOP DISPLAY. (On Linux install it with:  sudo apt install python3-tk)
# Without a display this file prints a message and stops.

try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    print("tkinter is not installed in this Python")
    sys.exit(0)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Converter")

        # Variables that are linked to widgets
        self.celsius = tk.StringVar()
        self.result = tk.StringVar(value="")

        # Widgets are placed in a grid (rows and columns)
        ttk.Label(self, text="Celsius:").grid(row=0, column=0, padx=8, pady=8)
        self.entry = ttk.Entry(self, textvariable=self.celsius, width=10)
        self.entry.grid(row=0, column=1, padx=8)
        self.button = ttk.Button(self, text="Convert", command=self.convert)
        self.button.grid(row=0, column=2, padx=8)
        ttk.Label(self, textvariable=self.result).grid(row=1, column=0, columnspan=3, pady=8)

        # Events: the Return key does the same as the button
        self.bind("<Return>", lambda event: self.convert())

    def convert(self):
        try:
            c = float(self.celsius.get())
        except ValueError:
            self.result.set("Enter a number")
            return
        self.result.set(f"{c * 9 / 5 + 32:.1f} F")

    def run_demo(self):
        """Drive the window from code (so this lesson prints something), then close it."""
        self.celsius.set("100")
        self.button.invoke()                    # the same as a click
        print(self.result.get())                # 212.0 F
        self.celsius.set("abc")
        self.button.invoke()
        print(self.result.get())                # Enter a number
        print(self.title(), len(self.winfo_children()))     # Converter 4
        self.destroy()


if __name__ == "__main__":
    try:
        app = App()
    except tk.TclError:
        print("No display available: the GUI demo was skipped")
        sys.exit(0)
    if "--interactive" in sys.argv:             # python 12_gui_programming.py --interactive
        app.mainloop()                          # a real window stays open until you close it
    else:
        app.after(100, app.run_demo)            # call run_demo 100 ms after the loop starts
        app.mainloop()

# THE EVENT LOOP
#   mainloop() waits for events (clicks, keys, timers) and calls your functions.
#   A long task inside a callback FREEZES the window. Do slow work in a thread and send the
#   result back with a queue that the GUI reads using after(); never touch widgets from
#   another thread.
#
# LAYOUT MANAGERS (one per container)
#   pack   stack widgets in a row or column        grid   rows and columns (best for forms)
#   place  exact positions (avoid)
#
# COMMON WIDGETS   Label, Button, Entry, Text, Checkbutton, Radiobutton, Listbox, Combobox,
#                  Frame (a container), Canvas (drawing), Scrollbar, Menu, Scale
# DIALOGS          tkinter.messagebox, tkinter.filedialog, tkinter.simpledialog
# TIMERS           root.after(ms, function)   root.after_cancel(id)
# EVENTS           widget.bind("<Button-1>", handler)   "<Key>"   "<Return>"   "<Motion>"