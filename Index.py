import time
import json
import tkinter as tk

# Initialize target_location
target_location = [0, 0, 0]

def main_loop():
    global target_location

    # PID constants
    kp = 0.5
    ki = 0.01
    kd = 0.1

    integral = 0
    previous_error = 0

    while True:
        try:
            # Read current global position from myrobot.txt
            with open('myrobot.txt', 'r') as file:
                data = json.load(file)
                current_location = data['myrobot'][1]['global pos']

            # Calculate error
            error = target_location[0] - current_location[0]

            # Update integral and derivative terms
            integral = integral + error
            derivative = error - previous_error

            # Calculate control variable (output)
            control = kp * error + ki * integral + kd * derivative

            # Apply control to movement (YMov in this case)
            YMov = control

            # Update previous error for next iteration
            previous_error = error

            # Read existing data from Controls.txt
            with open('Controls.txt', 'r') as control_file:
                lines = control_file.readlines()

            # Update the 'left_y' value with YMov
            for i, line in enumerate(lines):
                if line.startswith('left_y='):
                    lines[i] = f"left_y={YMov}\n"
                    break

            # Write the updated data back to Controls.txt
            with open('Controls.txt', 'w') as control_file:
                control_file.writelines(lines)

            if abs(error) < 0.1:
                YMov = 0
                break

            time.sleep(0.1)

        except KeyError:
            print("Error: Key not found in JSON data.")
            time.sleep(1)

    time.sleep(0.2)

# Function to handle mouse clicks on the canvas
def on_click(event):
    global target_location
    target_location = [event.x, event.y, 0]
    print(f"Target Position set to: {target_location}")

if __name__ == "__main__":
    # Create a simple GUI window using tkinter
    root = tk.Tk()
    root.title("Click to Set Target Position")
    root.geometry("400x300")

    label = tk.Label(root, text="Click anywhere on the canvas to set the target position.")
    label.pack(pady=20)

    canvas = tk.Canvas(root, width=400, height=300, bg="white")
    canvas.pack()

    canvas.bind("<Button-1>", on_click)

    root.mainloop()

    # After closing the GUI, start the main loop
    main_loop()

