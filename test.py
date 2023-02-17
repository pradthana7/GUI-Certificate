import tkinter as tk


class App:
    def __init__(self, master):
        self.master = master
        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(self.master, textvariable=self.entry_var,
                              validate="key", validatecommand=self.validate_input)
        self.entry.pack()

    def validate_input(self):
        value = self.entry_var.get()

        if value == "":
            return True

        try:
            number = int(value)
            if number < 60 or number > 100:
                return False
            else:
                return True
        except ValueError:
            return False


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
