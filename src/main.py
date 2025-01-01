from tkinter import Tk
from gui.fitness import Fitness
from backend.database import Database

def main():
    # Initialize the database
    user = Database()

    # Create the main application window
    root = Tk()
    root.title("Everything Fitness")
    root.geometry("800x800")

    # Create the main application
    fitness_app = Fitness(root, user)
    fitness_app.pack(fill='both', expand=True)

    root.resizable(False, False)

    # Start the Tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    main()