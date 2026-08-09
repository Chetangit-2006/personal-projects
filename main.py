import tkinter as tk
from tkinter import ttk, messagebox, filedialog


# =====================================================
# STUDENT GRADE CALCULATOR
# =====================================================

# Create main window
window = tk.Tk()

window.title("Student Grade Calculator")
window.geometry("650x750")
window.resizable(False, False)

# Colors
LIGHT_BG = "#F4F7FB"
DARK_BG = "#1E1E2E"

window.configure(bg=LIGHT_BG)


# =====================================================
# VARIABLES
# =====================================================

subjects = [
    "English",
    "Mathematics",
    "Python",
    "DBMS",
    "DAA"
]

entries = {}

dark_mode = False


# =====================================================
# TITLE
# =====================================================

title = tk.Label(
    window,
    text="🎓 Student Grade Calculator",
    font=("Arial", 24, "bold"),
    bg=LIGHT_BG,
    fg="#222222"
)

title.pack(pady=(20, 5))


subtitle = tk.Label(
    window,
    text="Enter student details and marks",
    font=("Arial", 11),
    bg=LIGHT_BG,
    fg="#666666"
)

subtitle.pack(pady=(0, 15))


# =====================================================
# STUDENT NAME
# =====================================================

name_label = tk.Label(
    window,
    text="Student Name",
    font=("Arial", 11, "bold"),
    bg=LIGHT_BG,
    fg="#222222"
)

name_label.pack()

name_entry = ttk.Entry(
    window,
    width=40
)

name_entry.pack(pady=(5, 15))


# =====================================================
# SUBJECT MARKS
# =====================================================

for subject in subjects:

    label = tk.Label(
        window,
        text=subject + " Marks",
        font=("Arial", 11),
        bg=LIGHT_BG,
        fg="#222222"
    )

    label.pack()

    entry = ttk.Entry(
        window,
        width=40
    )

    entry.pack(pady=4)

    entries[subject] = entry


# =====================================================
# RESULT VARIABLES
# =====================================================

total_value = tk.StringVar(value="Total Marks: --")
percentage_value = tk.StringVar(value="Percentage: --")
grade_value = tk.StringVar(value="Grade: --")
result_value = tk.StringVar(value="Result: --")


# =====================================================
# CALCULATE RESULT
# =====================================================

def calculate_result():

    # Check student name
    name = name_entry.get().strip()

    if name == "":
        messagebox.showerror(
            "Missing Name",
            "Please enter the student name."
        )
        return

    marks = []

    # Validate each subject
    for subject in subjects:

        value = entries[subject].get().strip()

        if value == "":
            messagebox.showerror(
                "Missing Marks",
                f"Please enter marks for {subject}."
            )
            return

        try:
            mark = float(value)

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                f"Please enter a valid number for {subject}."
            )
            return

        if mark < 0 or mark > 100:
            messagebox.showerror(
                "Invalid Marks",
                f"{subject} marks must be between 0 and 100."
            )
            return

        marks.append(mark)

    # Calculate total
    total = sum(marks)

    # Calculate percentage
    percentage = total / 5

    # Calculate grade
    if percentage >= 90:
        grade = "A+"

    elif percentage >= 80:
        grade = "A"

    elif percentage >= 70:
        grade = "B"

    elif percentage >= 60:
        grade = "C"

    elif percentage >= 50:
        grade = "D"

    else:
        grade = "F"

    # Pass / Fail
    if percentage >= 40:
        result = "PASS"

    else:
        result = "FAIL"

    # Display result
    total_value.set(
        f"Total Marks: {total:.0f} / 500"
    )

    percentage_value.set(
        f"Percentage: {percentage:.2f}%"
    )

    grade_value.set(
        f"Grade: {grade}"
    )

    result_value.set(
        f"Result: {result}"
    )

    # Update progress bar
    progress_bar["value"] = percentage

    # Update grade badge
    grade_badge.config(
        text=f"Grade {grade}"
    )


# =====================================================
# RESET FUNCTION
# =====================================================

def reset_form():

    name_entry.delete(0, tk.END)

    for subject in subjects:
        entries[subject].delete(0, tk.END)

    total_value.set("Total Marks: --")
    percentage_value.set("Percentage: --")
    grade_value.set("Grade: --")
    result_value.set("Result: --")

    progress_bar["value"] = 0

    grade_badge.config(
        text="Grade --"
    )


# =====================================================
# SAVE RESULT
# =====================================================

def save_result():

    name = name_entry.get().strip()

    if name == "":
        messagebox.showerror(
            "Error",
            "Please enter student name."
        )
        return

    # Check whether marks are entered
    for subject in subjects:

        if entries[subject].get().strip() == "":
            messagebox.showerror(
                "Error",
                "Please calculate the result first."
            )
            return

    # Get current values
    total_text = total_value.get()
    percentage_text = percentage_value.get()
    grade_text = grade_value.get()
    result_text = result_value.get()

    if "--" in total_text:
        messagebox.showerror(
            "Error",
            "Please calculate the result first."
        )
        return

    # Create report
    report = f"""
========================================
        STUDENT GRADE REPORT
========================================

Student Name: {name}

----------------------------------------
SUBJECT MARKS
----------------------------------------

English       : {entries["English"].get()}
Mathematics   : {entries["Mathematics"].get()}
Python        : {entries["Python"].get()}
DBMS          : {entries["DBMS"].get()}
DAA           : {entries["DAA"].get()}

----------------------------------------
RESULT
----------------------------------------

{total_text}
{percentage_text}
{grade_text}
{result_text}

========================================
        END OF REPORT
========================================
"""

    # Ask user where to save
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[
            ("Text Files", "*.txt"),
            ("All Files", "*.*")
        ],
        title="Save Student Result"
    )

    if file_path:

        with open(file_path, "w") as file:
            file.write(report)

        messagebox.showinfo(
            "Success",
            "Result saved successfully!"
        )


# =====================================================
# DARK / LIGHT MODE
# =====================================================

def toggle_theme():

    global dark_mode

    if dark_mode is False:

        dark_mode = True

        window.configure(bg=DARK_BG)

        title.config(
            bg=DARK_BG,
            fg="white"
        )

        subtitle.config(
            bg=DARK_BG,
            fg="#CCCCCC"
        )

        name_label.config(
            bg=DARK_BG,
            fg="white"
        )

        for widget in window.winfo_children():

            if isinstance(widget, tk.Label):

                widget.config(
                    bg=DARK_BG
                )

        theme_button.config(
            text="☀ Light Mode"
        )

    else:

        dark_mode = False

        window.configure(bg=LIGHT_BG)

        title.config(
            bg=LIGHT_BG,
            fg="#222222"
        )

        subtitle.config(
            bg=LIGHT_BG,
            fg="#666666"
        )

        name_label.config(
            bg=LIGHT_BG,
            fg="#222222"
        )

        for widget in window.winfo_children():

            if isinstance(widget, tk.Label):

                widget.config(
                    bg=LIGHT_BG
                )

        theme_button.config(
            text="🌙 Dark Mode"
        )


# =====================================================
# BUTTON FRAME
# =====================================================

button_frame = tk.Frame(
    window,
    bg=LIGHT_BG
)

button_frame.pack(pady=15)


# Calculate button

calculate_button = ttk.Button(
    button_frame,
    text="📊 Calculate",
    command=calculate_result
)

calculate_button.grid(
    row=0,
    column=0,
    padx=5
)


# Reset button

reset_button = ttk.Button(
    button_frame,
    text="🔄 Reset",
    command=reset_form
)

reset_button.grid(
    row=0,
    column=1,
    padx=5
)


# Save button

save_button = ttk.Button(
    button_frame,
    text="💾 Save Result",
    command=save_result
)

save_button.grid(
    row=0,
    column=2,
    padx=5
)


# =====================================================
# THEME BUTTON
# =====================================================

theme_button = ttk.Button(
    window,
    text="🌙 Dark Mode",
    command=toggle_theme
)

theme_button.pack(pady=5)


# =====================================================
# RESULT SECTION
# =====================================================

result_title = tk.Label(
    window,
    text="📋 Result Summary",
    font=("Arial", 16, "bold"),
    bg=LIGHT_BG,
    fg="#222222"
)

result_title.pack(pady=(10, 5))


total_label = tk.Label(
    window,
    textvariable=total_value,
    font=("Arial", 11, "bold"),
    bg=LIGHT_BG,
    fg="#222222"
)

total_label.pack(pady=2)


percentage_label = tk.Label(
    window,
    textvariable=percentage_value,
    font=("Arial", 11, "bold"),
    bg=LIGHT_BG,
    fg="#222222"
)

percentage_label.pack(pady=2)


grade_label = tk.Label(
    window,
    textvariable=grade_value,
    font=("Arial", 11, "bold"),
    bg=LIGHT_BG,
    fg="#222222"
)

grade_label.pack(pady=2)


result_label = tk.Label(
    window,
    textvariable=result_value,
    font=("Arial", 11, "bold"),
    bg=LIGHT_BG,
    fg="#222222"
)

result_label.pack(pady=2)


# =====================================================
# PROGRESS BAR
# =====================================================

progress_bar = ttk.Progressbar(
    window,
    length=400,
    maximum=100,
    mode="determinate"
)

progress_bar.pack(pady=10)


# =====================================================
# GRADE BADGE
# =====================================================

grade_badge = tk.Label(
    window,
    text="Grade --",
    font=("Arial", 15, "bold"),
    bg="#E8EAF6",
    fg="#303F9F",
    padx=20,
    pady=5
)

grade_badge.pack(pady=5)


# =====================================================
# START APPLICATION
# =====================================================

window.mainloop()