import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime, timedelta
import os

class TaskPrioritization:
    """Class to evaluate the score of a task based on priority, time needed, and due date."""

    def __init__(self, current_time):
        self.current_time = current_time

    def evaluate_task_score(self, task):
        """Evaluate score based on priority, time needed, and proximity to due date."""
        task_name, deadline, priority, time_needed = task

        # Calculate time difference in hours between current time and deadline
        time_until_deadline = (deadline - self.current_time).total_seconds() / 3600

        # Convert time_needed to hours
        time_needed_hours, time_needed_minutes = map(int, time_needed.split(":"))
        total_time_needed = time_needed_hours + (time_needed_minutes / 60)

        # Priority scoring (mapping to numeric values)
        priority_score = {"High": 3, "Medium": 2, "Low": 1}[priority]

        # Weights adjustment based on the previous recommendation
        w1 = 5   # Weight for priority score
        w2 = 10  # Weight for time ratio
        w3 = 100  # Weight for deadline proximity

        # Small constant to avoid division by zero
        epsilon = 0.1

        # Calculate urgency score using the adjusted weights
        urgency_score = (
            w1 * priority_score +
            w2 * (1 - time_until_deadline / (total_time_needed + time_until_deadline + epsilon)) +
            w3 / (time_until_deadline + epsilon)
        )

        return urgency_score

    def get_ordered_tasks(self, tasks):
        """Return tasks ordered by evaluated score, in descending order (higher score = higher priority)."""
        # Evaluate score for each task
        scored_tasks = [(task, self.evaluate_task_score(task)) for task in tasks]
        # Sort tasks by score in descending order
        ordered_tasks = sorted(scored_tasks, key=lambda x: x[1], reverse=True)
        return [task for task, score in ordered_tasks]


class TaskList(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Define colors for the UI elements
        self.bg_color = "light gray"
        self.text_color = "black"

        # Initialize tasks list and other instance variables
        self.tasks = []

        # Define filter constants for clarity
        self.FILTER_BY_DUE_DATE = 0
        self.FILTER_BY_IMPORTANCE = 1
        self.FILTER_TO_DO_ORDER = 2

        # Set the initial filter
        self.current_filter = self.FILTER_BY_DUE_DATE  # Default filter set to "sort by due date"

        # Create a canvas and a scrollbar to make the UI scrollable
        self.canvas = tk.Canvas(self, bg=self.bg_color)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.bg_color)

        # Configure the canvas and scrollbar
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self._configure_scroll_region()
        )

        # Create a window inside the canvas for the scrollable frame
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Grid layout for canvas and scrollbar
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # Configure the main frame and scrollable frame to expand and fill
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)  # Allow column 0 to expand horizontally

        # Bind the canvas to resize based on the containing frame
        self.canvas.bind("<Configure>", self._resize_canvas)

        # Bind the mouse scroll event to the canvas
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Task Input Section (Expands horizontally)
        task_label = tk.Label(self.scrollable_frame, text="Task Name:", font=("Helvetica", 12), bg=self.bg_color, fg=self.text_color)
        task_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.task_entry = tk.Entry(self.scrollable_frame, bg=self.bg_color, fg=self.text_color)
        self.task_entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Calendar widget for selecting deadlines (Expands horizontally)
        deadline_label = tk.Label(self.scrollable_frame, text="Select Deadline:", font=("Helvetica", 12), bg=self.bg_color, fg=self.text_color)
        deadline_label.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        self.calendar = Calendar(self.scrollable_frame, selectmode="day", showweeknumbers=False)
        self.calendar.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        # Time selection dropdowns for deadline (Expands horizontally)
        time_label = tk.Label(self.scrollable_frame, text="Select Deadline Time (HH:MM):", font=("Helvetica", 12), bg=self.bg_color, fg=self.text_color)
        time_label.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

        # Frame to hold hour and minute dropdowns for deadline
        deadline_time_frame = tk.Frame(self.scrollable_frame, bg=self.bg_color)
        deadline_time_frame.grid(row=5, column=0, padx=10, pady=5, sticky="ew")
        deadline_time_frame.grid_columnconfigure(0, weight=1)  # Allow dropdown to expand horizontally
        deadline_time_frame.grid_columnconfigure(1, weight=1)

        # Hour dropdown for deadline (Expands horizontally)
        self.hour_var = tk.StringVar(self)
        self.hour_var.set("12")
        hours = [f"{i:02d}" for i in range(24)]
        self.hour_dropdown = tk.OptionMenu(deadline_time_frame, self.hour_var, *hours)
        self.hour_dropdown.grid(row=0, column=0, padx=2, pady=5, sticky="ew")

        # Minute dropdown for deadline (Expands horizontally)
        self.minute_var = tk.StringVar(self)
        self.minute_var.set("00")
        minutes = [f"{i:02d}" for i in range(0, 60, 5)]
        self.minute_dropdown = tk.OptionMenu(deadline_time_frame, self.minute_var, *minutes)
        self.minute_dropdown.grid(row=0, column=1, padx=2, pady=5, sticky="ew")

        # Time Needed dropdowns (Expands horizontally)
        time_needed_label = tk.Label(self.scrollable_frame, text="Amount of Time Needed (HH:MM):", font=("Helvetica", 12), bg=self.bg_color, fg=self.text_color)
        time_needed_label.grid(row=6, column=0, padx=10, pady=5, sticky="ew")

        # Frame to hold hour and minute dropdowns for time needed (Expands horizontally)
        time_needed_frame = tk.Frame(self.scrollable_frame, bg=self.bg_color)
        time_needed_frame.grid(row=7, column=0, padx=10, pady=5, sticky="ew")
        time_needed_frame.grid_columnconfigure(0, weight=1)
        time_needed_frame.grid_columnconfigure(1, weight=1)

        # Hour dropdown for time needed
        self.time_needed_hour_var = tk.StringVar(self)
        self.time_needed_hour_var.set("01")
        self.time_needed_hour_dropdown = tk.OptionMenu(time_needed_frame, self.time_needed_hour_var, *hours)
        self.time_needed_hour_dropdown.grid(row=0, column=0, padx=2, pady=5, sticky="ew")

        # Minute dropdown for time needed
        self.time_needed_minute_var = tk.StringVar(self)
        self.time_needed_minute_var.set("00")
        self.time_needed_minute_dropdown = tk.OptionMenu(time_needed_frame, self.time_needed_minute_var, *minutes)
        self.time_needed_minute_dropdown.grid(row=0, column=1, padx=2, pady=5, sticky="ew")

        # Priority dropdown for tasks (Expands horizontally)
        priority_label = tk.Label(self.scrollable_frame, text="Priority:", font=("Helvetica", 12), bg=self.bg_color, fg=self.text_color)
        priority_label.grid(row=8, column=0, padx=10, pady=5, sticky="ew")

        self.priority_var = tk.StringVar(self)
        self.priority_var.set("Medium")

        self.priority_dropdown = tk.OptionMenu(self.scrollable_frame, self.priority_var, "Low", "Medium", "High")
        self.priority_dropdown.grid(row=9, column=0, padx=10, pady=5, sticky="ew")

        # Add Task Button (Expands horizontally)
        add_button = tk.Button(self.scrollable_frame, text="Add Task", command=self.add_task, bg="#4CAF50", fg="black", font=("Helvetica", 12))
        add_button.grid(row=10, column=0, padx=10, pady=10, sticky="ew")

        # Task List Box (Expands horizontally)
        self.task_listbox = tk.Listbox(self.scrollable_frame, height=10, bg=self.bg_color, fg=self.text_color)
        self.task_listbox.grid(row=11, column=0, padx=10, pady=10, sticky="ew")

        # Sort by due date button (Expands horizontally)
        sort_due_button = tk.Button(self.scrollable_frame, text="Sort by Due Date", command=self.sort_by_due_date, bg="#2196F3", fg="black", font=("Helvetica", 12))
        sort_due_button.grid(row=12, column=0, padx=10, pady=10, sticky="ew")

        # Sort by importance button (Expands horizontally)
        sort_importance_button = tk.Button(self.scrollable_frame, text="Sort by Importance", command=self.sort_by_importance, bg="#FF5722", fg="black", font=("Helvetica", 12))
        sort_importance_button.grid(row=13, column=0, padx=10, pady=10, sticky="ew")

        # Replace Refresh Tasks Button with "To Do" Button (Expands horizontally)
        to_do_button = tk.Button(self.scrollable_frame, text="To Do", command=self.show_to_do_order, bg="#FFDD57", fg="black", font=("Helvetica", 12))
        to_do_button.grid(row=14, column=0, padx=10, pady=10, sticky="ew")

        # New button to view passed tasks
        view_passed_tasks_button = tk.Button(self.scrollable_frame, text="View Passed Tasks", command=self.view_passed_tasks, bg="#FF0000", fg="white", font=("Helvetica", 12))
        view_passed_tasks_button.grid(row=15, column=0, padx=10, pady=10, sticky="ew")

        # Load existing tasks from file
        self.load_tasks()

        # Start the observer function to check passed tasks periodically
        self.check_passed_tasks()

    def show_to_do_order(self):
        """Sort tasks based on the evaluation algorithm and display in the listbox."""
        prioritization = TaskPrioritization(datetime.now())
        ordered_tasks = prioritization.get_ordered_tasks(self.tasks)
        self.tasks = ordered_tasks  # Update the main task list to reflect the new order
        self.current_filter = self.FILTER_TO_DO_ORDER  # Set the current filter to "To Do"
        self.update_task_listbox()

    def view_passed_tasks(self):
        """Open a new window to view passed tasks."""
        # Create a larger window for displaying passed tasks
        passed_tasks_window = tk.Toplevel(self)
        passed_tasks_window.title("Passed Tasks")
        passed_tasks_window.geometry("600x400")  # Increase size to 600x400 for better readability

        # Create a text box to display passed tasks
        passed_tasks_text = tk.Text(passed_tasks_window, wrap="word", bg="light gray", fg="black", font=("Helvetica", 12))
        passed_tasks_text.pack(expand=True, fill="both")

        # Load and display passed tasks from the file
        if os.path.exists("logs/passed_tasks_log.txt"):
            with open("logs/passed_tasks_log.txt", "r") as file:
                passed_tasks = file.read()
                passed_tasks_text.insert("1.0", passed_tasks)
        else:
            passed_tasks_text.insert("1.0", "No passed tasks found.")

    def _on_mousewheel(self, event):
        """Handle mouse scroll for the canvas."""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _configure_scroll_region(self):
        """Update scrollregion to include all elements in the scrollable frame."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _resize_canvas(self, event):
        """Adjust canvas width to match the frame width."""
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw"), width=canvas_width)

    def add_task(self):
        task_name = self.task_entry.get()
        deadline = self.calendar.get_date()
        priority = self.priority_var.get()
        hour = self.hour_var.get()
        minute = self.minute_var.get()
        time_needed_hours = self.time_needed_hour_var.get()
        time_needed_minutes = self.time_needed_minute_var.get()

        if task_name == "":
            messagebox.showwarning("Input Error", "Task name cannot be empty.")
            return

        # Convert the selected deadline and time to a datetime object
        try:
            deadline_date = datetime.strptime(deadline, "%m/%d/%y")
            deadline_date = deadline_date.replace(hour=int(hour), minute=int(minute), second=0)
        except ValueError:
            messagebox.showwarning("Invalid Time", "Please enter a valid time.")
            return

        # Format the time needed as HH:MM
        try:
            time_needed_hours = int(time_needed_hours)
            time_needed_minutes = int(time_needed_minutes)
            if time_needed_hours < 0 or time_needed_minutes < 0:
                raise ValueError
            time_needed_formatted = f"{time_needed_hours:02d}:{time_needed_minutes:02d}"
        except ValueError:
            messagebox.showwarning("Invalid Time Needed", "Please enter a valid amount of time needed.")
            return

        current_datetime = datetime.now()

        # Check if the selected date is today
        if deadline_date.date() == current_datetime.date():
            # Check if the selected time (hour and minute) has already passed for today
            if deadline_date.time() <= current_datetime.time():
                messagebox.showwarning("Invalid Time", "The selected time has already passed. Please choose a future time.")
                return

        # Check if the selected deadline date and time is in the past
        if deadline_date < current_datetime:
            messagebox.showwarning("Invalid Deadline", "The selected deadline has already passed. Please choose a future date and time.")
            return

        # Add task to internal list as a tuple if the deadline is valid
        task_info = (task_name, deadline_date, priority, time_needed_formatted)
        self.tasks.append(task_info)

        # Update the task listbox based on the current filter (sort by due date)
        self.sort_by_due_date()

        # Save tasks to file
        self.save_tasks()

        # Clear the task entry fields
        self.task_entry.delete(0, tk.END)

    def save_tasks(self):
        """Write tasks to a text file."""
        with open("logs/task_log.txt", "w") as file:
            for task in self.tasks:
                task_string = f"{task[0]} - Deadline: {task[1].strftime('%m/%d/%y %H:%M:%S')}, Priority: {task[2]}, Time Needed: {task[3]}"
                file.write(f"{task_string}\n")

    def load_tasks(self):
        """Load tasks from the text file."""
        self.tasks.clear()  # Clear the current task list

        try:
            with open("logs/task_log.txt", "r") as file:
                tasks = file.readlines()
                for task in tasks:
                    task_name, rest = task.split(" - Deadline: ")
                    deadline_str, priority_and_time = rest.split(", Priority: ")
                    priority, time_needed = priority_and_time.split(", Time Needed: ")

                    # Try to parse deadline with the most complete format first
                    deadline_str = deadline_str.strip()
                    parsed_successfully = False

                    # List of possible formats
                    formats = [
                        "%m/%d/%y %H:%M:%S",  # Format with date, hour, minute, and second
                        "%m/%d/%y %H:%M",     # Format with date, hour, and minute
                        "%m/%d/%y"            # Format with only date
                    ]

                    # Try each format in the list until one succeeds
                    for date_format in formats:
                        try:
                            deadline_date = datetime.strptime(deadline_str, date_format)
                            parsed_successfully = True
                            break
                        except ValueError:
                            continue

                    # If no format matches, raise an error
                    if not parsed_successfully:
                        raise ValueError(f"Unable to parse date: {deadline_str}")

                    # Append the task as a tuple, using the formatted "Time Needed" field
                    self.tasks.append((task_name, deadline_date, priority.strip(), time_needed.strip()))

                # Update the task listbox after loading tasks
                self.sort_by_due_date()
        except FileNotFoundError:
            pass

    def update_task_listbox(self):
        """Update the task listbox to display tasks."""
        # Clear the listbox
        self.task_listbox.delete(0, tk.END)

        # Display the tasks in the listbox
        for task in self.tasks:
            task_string = f"{task[0]} - Deadline: {task[1].strftime('%m/%d/%y %H:%M')}, Priority: {task[2]}, Time Needed: {task[3]}"
            self.task_listbox.insert(tk.END, task_string)

    def sort_by_due_date(self):
        """Sort tasks by deadline."""
        self.tasks.sort(key=lambda task: task[1])
        self.current_filter = self.FILTER_BY_DUE_DATE  # Set the current filter to "sort by due date"
        self.update_task_listbox()

    def sort_by_importance(self):
        """Sort tasks by importance."""
        priority_map = {"High": 1, "Medium": 2, "Low": 3}
        self.tasks.sort(key=lambda task: priority_map[task[2]])
        self.current_filter = self.FILTER_BY_IMPORTANCE  # Set the current filter to "sort by importance"
        self.update_task_listbox()

    def refresh_tasks(self):
        """Move passed tasks to a separate file and remove them from the main list."""
        current_datetime = datetime.now()  # Get the current date and time
        remaining_tasks = []
        passed_tasks = []

        for task in self.tasks:
            # If the task deadline has passed (date and time), consider it as passed
            if task[1] < current_datetime:
                passed_tasks.append(task)
            else:
                remaining_tasks.append(task)

        # Update the remaining tasks in the main list
        self.tasks = remaining_tasks

        # Save passed tasks to the new file
        with open("logs/passed_tasks_log.txt", "a") as file:
            for task in passed_tasks:
                task_string = f"{task[0]} - Deadline: {task[1].strftime('%m/%d/%y %H:%M')}, Priority: {task[2]}, Time Needed: {task[3]}"
                file.write(f"{task_string}\n")

        # Reapply the current filter after refreshing tasks
        self.apply_current_filter()

    def apply_current_filter(self):
        """Apply the currently active filter to the tasks."""
        if self.current_filter == self.FILTER_BY_DUE_DATE:  # Sort by due date
            self.sort_by_due_date()
        elif self.current_filter == self.FILTER_BY_IMPORTANCE:  # Sort by importance
            self.sort_by_importance()
        elif self.current_filter == self.FILTER_TO_DO_ORDER:  # Show 'To Do' order
            self.show_to_do_order()
            
    def check_passed_tasks(self):
        """Periodically check for passed tasks and move them to the passed task log."""
        self.refresh_tasks()
        self.after(60000, self.check_passed_tasks)  # Check every 60 seconds
