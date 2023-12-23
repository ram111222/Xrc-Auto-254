import tkinter as tk
from Auto254 import moveRobot
global targetList
targetList = [0,0,90]
global target_location
target_location = [631/2,300/2]

def map_values(x, y):
    # Mapping x from (0, 300) to (-10, 10)
    mapped_x = ((x - 0) * (4 - (-4)) / (300 - 0)) + (-4)
    
    # Mapping y from (0, 611) to (-5, 5)
    mapped_y = ((y - 0) * (10 - (-10)) / (550 - 0)) + (-10)
    return [-mapped_x, mapped_y]


def on_click(event):
    global target_location
    target_location = [event.x, event.y, 0]
    print(f"Target Position set to: {target_location}")


def main_loop():
    #print('loop')
    global target_location
    global targetList
    mappedTarget = map_values(target_location[0],target_location[1])
    targetList = [-mappedTarget[0],-mappedTarget[1],270]
    print(targetList)
    #print('run')
    moveRobot(targetList)
    root.after(100,main_loop)
    
    



if __name__ == "__main__":
    # Create a simple GUI window using tkinter
    print('GUI')
    root = tk.Tk()
    root.title("Click to Set Target Position")
    root.geometry("300x611")

    label = tk.Label(root, text="Click anywhere on the canvas to set the target position.")
    label.pack(pady=20)

    canvas = tk.Canvas(root, width=300, height=631, bg="white")
    canvas.pack()

    canvas.bind("<Button-1>", on_click)

    root.after(30,main_loop)

    root.mainloop()

    # After closing the GUI, start the main loop
    print('here')
    main_loop()

