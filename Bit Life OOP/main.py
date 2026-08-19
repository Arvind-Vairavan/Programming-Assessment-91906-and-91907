from tkinter import Tk
from gui.main_gui import BitLifeGUI


def main():
    root = Tk()
    app = BitLifeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()