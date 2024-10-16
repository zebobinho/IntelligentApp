import tkinter as tk
from components.task_list import TaskList


class StressManagementApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set fixed window size and center the window on the screen
        self.title("Stress Management App")
        self.geometry("525x900+300+100")  # Fixed window size, centered on screen

        # Configure the grid layout for the main window
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create frames for Mood Tracker and Task List
        self.task_list_frame = TaskList(self)

        # Create the button in the center of the screen
        self.create_centered_button()

    def create_centered_button(self):
        # Button to switch to Task List
        self.task_button = tk.Button(self, text="Task List", command=self.show_task_list)

        # Center the button using grid
        self.task_button.grid(row=0, column=0)

        # Expand row and column to take up all available space, centering the button
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def show_task_list(self):
        # Hide the button by removing it from the grid
        self.task_button.grid_remove()

        # Show the task list frame
        self.task_list_frame.grid(row=0, column=0, sticky="nsew")


if __name__ == "__main__":
    app = StressManagementApp()
    app.mainloop()
