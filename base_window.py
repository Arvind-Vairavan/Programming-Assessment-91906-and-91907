"""
So this is version one where I have just created a simple window, with no styling in particular just adding base feature, 
I will be using the as a gui template for my other classes

This version works, the window look plain and default
"""


from tkinter import Tk, ttk


class BaseWindow:
    def __init__(self, title, width=400, height=300):
        self.win = Tk()
        self.win.title(title)

        x = (self.win.winfo_screenwidth() - width) // 2
        y = (self.win.winfo_screenheight() - height) // 2
        self.win.geometry(f"{width}x{height}+{x}+{y}")

    def add_title(self, text):
        ttk.Label(
            self.win,
            text=text,
            font=("Arial", 20, "bold")
        ).pack(pady=15)

    def card(self, content_func):
        frame = ttk.Frame(self.win, padding=10)
        frame.pack(fill="x", padx=15, pady=10)
        content_func(frame)

    def add_close(self):
        ttk.Button(
            self.win,
            text="Close",
            command=self.win.destroy
        ).pack(pady=15)

    def run(self):
        self.win.mainloop()


def main():
    win = BaseWindow("Version 1")

    win.add_title("VERSION 1")

    def card(frame):
        ttk.Label(frame, text="No dark theme").pack(anchor="w")
        ttk.Label(frame, text="No card styling").pack(anchor="w")
        ttk.Label(frame, text="Just default Tkinter").pack(anchor="w")

    win.card(card)
    win.add_close()

    win.run()


if __name__ == "__main__":
    main()