from tkinter import Tk
from gui import StudentProfilerApp


def main():
    root = Tk()
    app = StudentProfilerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
