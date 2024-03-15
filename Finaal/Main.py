from Controller import Controller
from View import View

def main():
    controller = Controller()
    view = View(controller)
    view.mainloop()

if __name__ == "__main__":
    main()
