# Stress Management App

This application is designed to help users track and manage tasks efficiently, helping the user manage their stress. The app features an intelligent implementation of a **Task List** which aims to provide the user with the optimal order of completion of their tasks.

## Project Structure

The project directory is structured as follows:


/stress_management_app<br>
│<br>
├── app.py                 # Main file that runs the application<br>
├── components <br>
│   └── task_list.py        # File for task list UI and logic (handled by the other student)<br>
├── logs                    # Directory for storing logs (new)<br>
│   └── task_log.txt        # Text file to store tasks and deadlines<br>
└── assets                  # Any images, icons, or other assets if needed<br>


### Key Components

- **`app.py`**: This is the main entry point for the application. In this version it simply has the button to go to task_list.py.
  
- **Task List (`task_list.py`)**: 
  - Allows users to create and manage tasks, set deadlines, and keep track of task progress.
  - Task entries are saved in the `logs/task_log.txt` file.

### Logs

- **task_log.txt**: Stores all tasks with details such as task name, task due date and time, importance and time to completion.
- **passed_tasks_log.txt**: Stores all tasks that have already passed.

### Assets

- A folder where any images, icons, or other assets can be placed.

### Feature Removal

- The **`mood_tracker.py`** was removed from this version as the intelligent version of it contained my group mates OpenAI key, which must be kept private. This version solely contains the part I worked on which is **`task_list.py`**.

## Installation and Setup

1. Clone the repository to your local machine:
   git clone https://github.com/zebobinho/IntelligentApp
2. Install any necessary dependencies:
   pip install -r requirements.txt
3. Run the application:
   python App.py

## Usage
### Overview 
The task list is used to organize your tasks and stay on top of your deadlines to reduce stress and provide assistance on how to approach your tasks.<br>

### Components

#### Task Creation 
Task list is made up the **`Task Name`**, **`Calendar`**, **`Deadline Time`**, **`Amount of Time needed`**, **`Importance`** and **`Add Task`** which are all used for the user to create their tasks. <br>

#### Filters
The box in the middle of the screen is where the tasks will be displayed, to enhance the display of tasks, there are 3 filters that can be used to see your tasks in different ways:<br>
- **`Sort by Due Data`** to see tasks from the closest due date to the furthest due date.
- **`Sort by Importance`** to see tasks from High importance to Low importance.
- **`To Do`** which is the intelligent feature, this invokes an algorithm that computes weights to tasks and organizes them based on the order the user should work on.

#### Quality of Life additions
- **`View Passed Tasks`** button which allows the user to see passed tasks. 
- The task list has an observer which every minute checks whether any tasks have passed and if they have, sends them to "passed_tasks_log.txt".

### Manual
#### Using the Calendar
To use the calendar:
- Top left: Use arrows to go through the months
- Top right: User arrows to go through the years
- When you have found the day of your task, simply click on it on the calendar
#### Adding task
In order to add a task:
1. Write down the name of the task under **`Task Name`**
2. Select the due date in the **`Calendar`** and due time in **`Deadline time`** (The time is in the format of HH:MM)
3. Select an estimated **`Amount of Time needed`** (The time is in the format of HH:MM)
4. Select an **`Importance`** in the dropdown menu
5. Press **`Add Task`**
6. The task will appear in the box below

#### Modifying Filters
The initial applied filter is the **`Due Date`** filter. If you wish to change the way the current tasks are displayed, simply click one of the filter buttons:
- **`Sort by Due Date`**
- **`Sort by Importance`**
- **`To Do`**

#### Looking at Passed Tasks
To look at tasks that have already passed, simply scroll to the bottom of the page, and click the **`View Passed Tasks`** button.