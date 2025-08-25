import os
import tkinter as tk
from tkinter import filedialog, messagebox
import textwrap
import random
import re
import time
from PIL import Image, ImageTk # type: ignore, must install PIL package
from pptx import Presentation # type: ignore, must install python-pptx

"""
For this to work you must place it in the directory with the practice_test.pptx
or change the file to the full file path of the that you wish to use.
Additionally, you must install the PIL and pptx packages with PIP
pip install PIL
pip install python-pptx <-This is the pptx library
"""
# Directory where extracted images will be saved
output_dir = "extracted_images"
os.makedirs(output_dir, exist_ok=True)

# Function to extract images from the PowerPoint file and prepare quiz data
def extract_images_and_prepare_quiz(pptx_file):
    presentation = Presentation(pptx_file)
    quiz_data = []

    for slide_number, slide in enumerate(presentation.slides):
        # Extract text and images from each slide
        question_text = []
        image_paths = []
        options = []

        # Loop through shapes in the slide to get both text and images
        for shape_number, shape in enumerate(slide.shapes):
            # Extract text from shapes (if available)
            if hasattr(shape, "text"):
                text = shape.text
                question_text.append(text)
            # Extract the answer and the explanation from the slides
            if slide.has_notes_slide:
                notes_slide = slide.notes_slide
                notes_text = notes_slide.notes_text_frame.text
                answer = notes_text.split("is:")[1].split("\n")[0]
                try:
                    reason = notes_text.split("\n")[1]
                except IndexError:
                    reason = "No Reason Given"
            # Extract images (if available)
            if shape.shape_type == 13:  # Shape type 13 is for pictures
                image = shape.image
                image_filename = f"slide_{slide_number + 1}_image_{shape_number + 1}.{image.ext}"
                image_path = os.path.join(output_dir, image_filename)
                with open(image_path, "wb") as image_file:
                    image_file.write(image.blob)
                image_paths.append(image_path)
       
        # Combine the text content to form a question
        if question_text:
            options = [] # These are the answer choices
            question = question_text[0] # This is the title block for each slide
            # Next we extract the remaining contents as answer choices
            items = question_text[1:]
            for option in items:
                options.append(option)
            options = " ".join(options)
            # append all information to quiz_data object for use when building questions
            quiz_data.append({
                "question": question,
                "options": options,
                "answer": answer,  
                "image_paths": image_paths,
                "reason" : reason
            })
    return quiz_data

def prompt_for_pptx_path() -> str | None:
    """Open a file browser to pick a PPTX file, starting at the user's home directory."""
    root = tk.Tk()
    root.withdraw()  # hide the root window while browsing
    start_dir = os.getcwd()
    path = filedialog.askopenfilename(
        parent=root,
        title="Select PowerPoint Quiz File",
        initialdir=start_dir,
        filetypes=[("PowerPoint files", "*.pptx"), ("All files", "*.*")]
    )
    root.destroy()  # cleanup hidden root
    if not path:
        messagebox.showinfo("No file selected", "You must pick a PPTX file to start.")
        return None
    return path

def _parse_correct_set(answer_str: str, options: list[str]) -> set[str]:
    """
    Turn the notes 'answer' string into a set of option texts that are correct.
    Works if answers are separated by newline, comma, semicolon, slash, or pipe,
    and matches either exact text or a contains/contained-in match.
    """
    if not isinstance(answer_str, str):
        return set()

    tokens = [t.strip() for t in re.split(r"[\n;/|]+", answer_str) if t.strip()]
    # If the notes only contain one big blob, keep it as-is so single-answer still works
    if len(tokens) <= 1:
        # try to map that blob to exactly one option
        blob = tokens[0].lower() if tokens else answer_str.lower()
        for opt in options:
            if opt.lower() == blob or blob in opt.lower() or opt.lower() in blob:
                return {opt}
        return set()

    matched = set()
    for t in tokens:
        t_low = t.lower()
        for opt in options:
            o_low = opt.lower()
            if t_low == o_low or t_low in o_low or o_low in t_low:
                matched.add(opt)
    return matched


# Function to display images in tkinter
def show_images(self, image_paths):
    for image_path in image_paths:
        # Open and display each image
        img = Image.open(image_path)
        img_tk = ImageTk.PhotoImage(img)
        image_label = tk.Label(self.image_frame, image=img_tk)
        image_label.image = img_tk  # Keep reference to avoid garbage collection
        image_label.pack(pady=10)
        # Bind a click event to the image to open it in a popup window
        image_label.bind("<Button-1>", lambda e, img_path=image_path: open_image_popup(img_path))

def open_image_popup(image_path, scale_factor=2):
    # Create a new popup window
    popup = tk.Toplevel()
    popup.title("Enlarged Image")

    # Load the image and resize it proportionally
    img = Image.open(image_path)
    img_width, img_height = img.size
    new_width = int(img_width * scale_factor)
    new_height = int(img_height * scale_factor)
    resized_img = img.resize((new_width, new_height), Image.LANCZOS)

    # Convert the resized image to a format suitable for Tkinter
    img_tk = ImageTk.PhotoImage(resized_img)

    # Create a label to hold the enlarged image
    image_label = tk.Label(popup, image=img_tk)
    image_label.image = img_tk  # Keep reference to avoid garbage collection
    image_label.pack(padx=5, pady=5)

    # Optionally, you can set a fixed size or let the window adjust to the image size
    popup.geometry(f"{(img_width * scale_factor) + 20}x{(img_height * scale_factor) + 20}")

# Custom class to get the number of questions for the quiz
class QuestionPopup:
    def __init__(self, master, max_questions: int):
        """Create a popup for the number of questions"""
        self.max_questions = max_questions

        self.popup = tk.Toplevel(master)
        self.popup.title("Settings")

        # Make the popup Modal (Disables the main window until popup closes)
        self.popup.grab_set()

        # initialize the result variable
        self.result = None

        label_text = (
            f"""How many questions do you want?
Enter a number between 1 - {self.max_questions}
a - (all questions)
r - (random number of questions)"""
        )
        self.label = tk.Label(self.popup, text=label_text, justify="left")
        self.label.pack(padx=10, pady=(10, 0), anchor="w")

        # Number input
        self.entry = tk.Entry(self.popup)
        self.entry.pack(padx=10, pady=(2, 10), fill="x")

        # Timer input
        self.timer_label = tk.Label(self.popup, text="""Timer (optional) 
Enter mm:ss or mm or 0 (no timer):""")
        self.timer_label.pack(padx=10, anchor="w")
        self.timer_entry = tk.Entry(self.popup)
        self.timer_entry.pack(padx=10, pady=(2, 10), fill="x")

        # Repeat checkbox
        self.repeat = tk.BooleanVar(value=True)
        self.repeat_checkbox = tk.Checkbutton(self.popup, text="Allow repeated questions", variable=self.repeat)
        self.repeat_checkbox.pack(padx=10, pady=(0, 10), anchor="w")

        # Buttons
        btn_frame = tk.Frame(self.popup)
        btn_frame.pack(fill="x", padx=10, pady=10)

        self.ok_button = tk.Button(btn_frame, text="OK", command=self.on_ok, width=8)
        self.ok_button.pack(side="left", padx=5)

        self.entry.bind("<Return>", self.on_ok)  # Main keyboard enter key press

        self.cancel_button = tk.Button(btn_frame, text="Cancel", command=self.on_cancel, width=8)
        self.cancel_button.pack(side="right", padx=5)

    def on_ok(self, event=None):
        """Handle the OK button click."""
        user_input = self.entry.get().strip().lower()

        if user_input.isdigit():
            self.result = max(1, min(int(user_input), self.max_questions))

        elif user_input == "a":
            self.result = self.max_questions

        elif user_input == "r":
            self.result = random.randint(1, self.max_questions)

        else:
            # Fallback: default to max if input is unexpected
            self.result = self.max_questions

        # Parse timer
        raw_timer = self.timer_entry.get().strip()
        try:
            if ":" in raw_timer:
                minutes_str, seconds_str = raw_timer.split(":")
                minutes = int(minutes_str or 0)
                seconds = int(seconds_str or 0)
            else:
                minutes = int(raw_timer or 0)
                seconds = 0
        except ValueError:
            minutes, seconds = 0, 0

        self.time_left = minutes * 60 + seconds
        self.popup.destroy()

    def on_cancel(self):
        """Cancel -> default to 'all questions' and no timer."""
        self.result = self.max_questions
        self.time_left = 0
        self.popup.destroy()

    def get_result(self):
        """Return (num_questions, repeat_checkbox, time_left_seconds)."""
        self.popup.wait_window()  # Wait for the popup to close
        return self.result, self.repeat, self.time_left


class ReviewPopup:
    def __init__(self, root, incorrect_questions):
        # Define the maximum width for wrapping only the answer and reason text
        wrap_width = 80

        # Create the popup window
        self.popup = tk.Toplevel(root)
        self.popup.title("Review Incorrect Answers")

        # Set up a scrollable text area
        text_area = tk.Text(self.popup, wrap="word", font=("Arial", 12), bg="gray")
        text_area.pack(padx=10, pady=10, fill="both", expand=True)

        if not incorrect_questions:
            text_area.insert("1.0", "No incorrect questions to review.")
        else:
            for idx, question_info in enumerate(incorrect_questions, start=1):
                # Wrap the correct answer and reason fields to 80 characters
                question_text = textwrap.fill(f'Q{idx}: {question_info.get("question", "Question not found")}\n', wrap_width)
                correct_answer_text = textwrap.fill(f'\nCorrect Answer: {question_info.get("correct_answer", "Answer not found")}\n', wrap_width)
                reason_text = textwrap.fill(f'\nExplanation: {question_info.get("reason", "Reason not found")}', wrap_width)
                #reasoner = reason_text.strip("The correct answer is: ")[1:]
                # Insert each section with tags for styling
                text_area.insert("end", f"{question_text}\n", "question")
                text_area.insert("end", f"{correct_answer_text}\n", "answer")
                text_area.insert("end", f"{reason_text}\n\n", "reason")
               
            # Tag configurations for optional styling
            text_area.tag_config("question", font=("Arial", 12, "bold"), foreground="black")
            text_area.tag_config("answer", font=("Arial", 12, "bold"), foreground="black")
            text_area.tag_config("reason", font=("Arial", 12, "bold"), foreground="black")

        # Make the text area read-only
        text_area.config(state="disabled")
       

# Custom popup class for popups during the quiz
class CustomPopup:
    ''' This will create the popup messages for the check, and score buttons'''
    def __init__(self, master, title, message, size):
        self.top = tk.Toplevel(master)
        self.top.title(title)
        self.top.configure(bg='gray')
        self.top.geometry(size)
       
        # Create label for the message
        self.label = tk.Label(self.top, text=message, bg='gray', fg='black', wraplength=300)
        self.label.pack(pady=20)

        # Create button to close the popup
        self.ok_button = tk.Button(self.top, text="Close", command=self.top.destroy)
        self.ok_button.pack(pady=10)

class CalculatorPopup:
    def __init__(self, parent):
        """Initialize the calculator popup window."""
        self.parent = parent
        self.expression = ""  # Holds the mathematical expression
        self.input_text = tk.StringVar()  # Holds the display text
       
        # Create a new Toplevel window for the calculator
        self.calc_window = tk.Toplevel(self.parent)
        self.calc_window.title("Calculator")
        self.calc_window.geometry("320x450")
       
        # Set up the display for the calculator
        self.create_display()
       
        # Set up the buttons
        self.create_buttons()

    def create_display(self):
        """Create the display for the calculator."""
        input_frame = tk.Frame(self.calc_window)
        input_frame.pack()

        input_field = tk.Entry(input_frame, textvariable=self.input_text, font=('Arial', 18), bd=10, insertwidth=4, width=14, borderwidth=4)
        input_field.grid(row=0, column=0)
        input_field.pack()

    def create_buttons(self):
        """Create the calculator buttons and lay them out."""
        btns_frame = tk.Frame(self.calc_window)
        btns_frame.pack(pady=(2,5))

        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            'C', '0', '=', '+'
        ]

        row_val = 0
        col_val = 0
        for button in buttons:
            if button == "=":
                btn = tk.Button(btns_frame, text=button, width=5, height=5, command=self.evaluate)
            elif button == "C":
                btn = tk.Button(btns_frame, text=button, width=5, height=5, command=self.clear_display)
            else:
                btn = tk.Button(btns_frame, text=button, width=5, height=5, command=lambda x=button: self.click_button(x))
           
            btn.grid(row=row_val, column=col_val, padx=5, pady=5)
           
            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1

    def click_button(self, item):
        """Handle button click and update the expression."""
        self.expression += str(item)
        self.input_text.set(self.expression)

    def clear_display(self):
        """Clear the calculator display and reset the expression."""
        self.expression = ""
        self.input_text.set("")

    def evaluate(self):
        """Evaluate the current expression and display the result."""
        try:
            result = str(eval(self.expression))  # Evaluate the expression
            self.input_text.set(result)  # Update the display with the result
            self.expression = result  # Use the result as the new expression
        except:
            self.input_text.set("Error")
            self.expression = ""

class ReasonPopup:
    ''' This will create the popup messages for the reason button'''
    def __init__(self, master, title, message):
        self.top = tk.Toplevel(master)
        self.top.title(title)
        self.top.configure(bg='gray')
        # Create a text widget to display the reason text
        reason_label = tk.Text(self.top, wrap=tk.WORD, bg="gray", fg="black",
                               font=("Arial", 14), borderwidth=0, highlightthickness=0)
        reason_label.insert(tk.END, message)
        reason_label.config(state=tk.DISABLED)  # Make the text read-only
        reason_label.pack(padx=5, pady=5)

        # Automatically resize the window based on the content
        self.top.update_idletasks()  # Update the geometry manager before resizing
        text_width = reason_label.winfo_reqwidth()
        text_height = reason_label.winfo_reqheight()
        self.top.geometry(f"{text_width}x{text_height}")

        # Close button
        close_button = tk.Button(self.top, text="Close", command=self.top.destroy)
        close_button.pack(pady=10)


# Main QuizApp class
class QuizApp:
    def __init__(self, root, quiz_data):
        self.root = root
        self.master = root
        self.root.title("Quiz App")
        self.root.configure(bg='gray')
        self.question_index = 0
        self.score = 0
        self.quiz_data = quiz_data
        self.button_width = 8
        self.max_attempts = 2  # Max attempts allowed before moving on
        self.attempts_made = 0  # Track how many times the user checks the answer
        self.running = False
        self.incorrect_questions = []
        self.checkbox_vars = []   # [(option_text, tk.BooleanVar), ...] for multi-answer screens
        self.is_multi_current = False  
        self.correct_set_current = set()
        self.flagged_questions = set()    # set of question indexes (ints)
        self.flag_button = None           # created below in the button bar
        self.next_flagged_button = None
        self.pause_used = False           # already took the 15-min break?
        self.pause_active = False         # currently paused?
        self.pause_end_epoch = None       # epoch time when pause ends
        self.saved_answers = {}

        # Ask for number of questions
        self.num_questions, self.repeat, self.time_left = self.ask_number_of_questions(max_questions=len(self.quiz_data))
       
        if self.repeat.get() == True:
            # If the repeat question checkbox is checked leave alone
            selected_questions = self.quiz_data
        elif self.repeat.get() == False:
            # If repeat question checkbox is unchecked duplicates be removed
            seen_questions = set()
            unique_questions = []
            for item in self.quiz_data:
                question = item["question"]
                if question not in seen_questions:
                    unique_questions.append(item)
                    seen_questions.add(question)
            selected_questions = unique_questions

        # Shuffle the questions
        random.shuffle(selected_questions)
       
        # use the number of questions to set the length
        self.new_quiz_data = selected_questions[0:self.num_questions]    

        # Create a frame for the question number, timer and question
        self.question_frame = tk.Frame(root, bg="gray")
        self.question_frame.pack(pady=2)

        # Label for question count
        self.question_count_label = tk.Label(self.question_frame, text="", font=("Arial", 18, "bold"), fg='black', bg='gray')
        self.question_count_label.pack(pady=5,anchor='nw')

        # Question label
        self.question_label = tk.Label(self.question_frame, text="", font=("Arial", 18, "bold"), fg='black', bg='gray')
        self.question_label.pack(pady=(10,5), anchor="w")

        # Create an image frame for any images
        self.image_frame = tk.Frame(root, bg="gray")
        self.image_frame.pack(pady=2, anchor="center")

        # Create radio button container for options
        self.radio_button_frame = tk.Frame(root, bg='gray')
        self.radio_button_frame.pack(pady=5, padx=(2,10), anchor='w')

        # StringVar for holding the selected answer
        self.selected_answer = tk.StringVar()

        # Create a button container for the other buttons
        self.button_frame = tk.Frame(root, bg='gray')
        self.button_frame.pack(pady=5)

        # Previous button to move to the previous question
        self.previous_button = tk.Button(self.button_frame, text="Prev.", command=self.previous_question, width=self.button_width)
        self.previous_button.pack(side="left", padx=1, pady=2)

        # Next button to move to the next question
        self.next_button = tk.Button(self.button_frame, text="Next", command=self.next_question, width=self.button_width)
        self.next_button.pack(side="left", padx=1, pady=2)
        
        # Toggle flag for review
        self.flag_button = tk.Button(self.button_frame, text="Flag", command=self.toggle_flag, width=self.button_width)
        self.flag_button.pack(side="left", padx=1, pady=2)

        # Jump to next flagged question
        self.next_flagged_button = tk.Button(self.button_frame, text="Next Flagged", command=self.go_to_next_flagged, width=10)
        self.next_flagged_button.pack(side="left", padx=1, pady=2)

        # Button to show the reason for the correct answer
        self.reason_button = tk.Button(self.button_frame, text="Reason", command=self.show_reason, width=self.button_width)
        self.reason_button.pack(side="left", padx=1, pady=2)

        # Button for calculator
        self.open_calc = tk.Button(self.button_frame, text="Calc.", command=self.calculator, width=self.button_width)
        self.open_calc.pack(side="left", padx=1, pady=2)
       
        # Create a show score button
        self.show_score_button = tk.Button(self.button_frame, text="Score", command=self.show_score, width=self.button_width)
        self.show_score_button.pack(side="left", padx=1, pady=2)
        
        # One-time break button
        self.break_button = tk.Button(self.button_frame, text="Take Break",command=self.start_break, width=10)
        self.break_button.pack(side="left", padx=1, pady=2)

        # Only shown (or enabled) during a pause
        self.resume_button = tk.Button(self.button_frame, text="End Break", command=self.resume_after_break, state=tk.DISABLED, width=10)
        self.resume_button.pack(side="left", padx=1, pady=2)
        # Button to check the answer
        self.check_button = tk.Button(self.button_frame, text="Check", command=self.check_answer, width=self.button_width)
        self.check_button.pack(side="left", padx=1, pady=2)
       
        # Button to Finish and score the quiz
        self.finish_button = tk.Button(self.button_frame, text="Finish", command=self.finish_quiz, width=self.button_width)
        self.finish_button.pack(side="left", padx=1, pady=2)

        # Close button to close the window
        self.close_button = tk.Button(self.button_frame, text="Close", command=self.root.destroy, width=self.button_width)
        self.close_button.pack(side="left", padx=1, pady=2)
       
        # Timer label
        self.timer_label = tk.Label(self.button_frame, font=("Arial", 20), text="", fg="black", bg='gray')
        self.timer_label.pack(side="left", padx=15, pady=2)

        if self.time_left > 0:  # Start timer only if input is greater than zero
            self.running = True
            self.update_timer()

        # Load the first question
        self.load_question()

    # Function to display images in tkinter
    def show_images(self, image_paths):
        for image_path in image_paths:
            # Open and display each image
            img = Image.open(image_path)
            img_tk = ImageTk.PhotoImage(img)
            image_label = tk.Label(self.image_frame, image=img_tk)
            image_label.image = img_tk  # Keep reference to avoid garbage collection
            image_label.pack(pady=20)
            # Bind a click event to the image to open it in a popup window
            image_label.bind("<Button-1>", lambda e, img_path=image_path: open_image_popup(img_path))

    def ask_number_of_questions(self, max_questions: int):
        """Open the question popup"""
        popup = QuestionPopup(self.root, max_questions=max_questions)
        return popup.get_result()

    def load_question(self):
        # Clear previous images
        for widget in self.image_frame.winfo_children():
            widget.destroy()
        self.image_frame.config()

        current_question = self.new_quiz_data[self.question_index]

        # Wrap the question text
        wrapped_question = textwrap.fill(current_question["question"], width=90)
        self.question_label.config(text=wrapped_question)

        # Display any associated images
        if "image_paths" in current_question and current_question["image_paths"]:
            show_images(self, current_question["image_paths"])
        else:
            self.image_frame.config(width=0, height=0)
            default_label = tk.Label(self.image_frame, bg='gray')
            default_label.pack()

        # Reset option area
        for widget in self.radio_button_frame.winfo_children():
            widget.destroy()
        self.selected_answer.set(None)
        self.checkbox_vars = []
        self.is_multi_current = False
        self.correct_set_current = set()

        # Prepare options (existing behavior)
        options = current_question["options"].split("\n")
        random.shuffle(options)

        # Detect whether this is multi-answer by parsing the notes 'answer'
        correct_set = _parse_correct_set(current_question.get("answer", ""), options)
        self.correct_set_current = correct_set
        self.is_multi_current = len(correct_set) > 1

        if self.is_multi_current:
            # Show a hint
            hint = tk.Label(self.radio_button_frame, text="(Select all that apply)", font=("Arial", 12, "bold"),
                            fg="black", bg="gray")
            hint.pack(anchor='w', pady=(0, 6))

            # Render checkboxes
            for opt in options:
                var = tk.BooleanVar(value=False)
                wrapped_option = textwrap.fill(opt, width=90)
                cb = tk.Checkbutton(self.radio_button_frame, text=wrapped_option, variable=var,command=self._persist_multi_selection,
                                    font=("Arial", 16, "bold"), fg='black', bg='gray', onvalue=True, offvalue=False)
                cb.pack(anchor='w')
                self.checkbox_vars.append((opt, var))
        else:
            # Single-answer (existing radio behavior)
            for opt in options:
                wrapped_option = textwrap.fill(opt, width=90)
                rb = tk.Radiobutton(self.radio_button_frame, text=wrapped_option, variable=self.selected_answer, command=self._on_single_change,
                                    value=opt, font=("Arial", 16, "bold"), fg='black', bg='gray')
                rb.pack(anchor='w')
        saved = self.saved_answers.get(self.question_index)
        if saved:
            if saved["mode"] == "single":
                self.selected_answer.set(saved.get("selected", ""))
            elif saved["mode"] == "multi":
                selset = set(saved.get("selected", []))
                for opt, var in self.checkbox_vars:
                    var.set(opt in selset)
                # Reset buttons
                self.check_button.config(state=tk.NORMAL)

        # Enable/Disable the Previous and Next buttons
        self.previous_button.config(state=tk.NORMAL if self.question_index > 0 else tk.DISABLED)
        self.next_button.config(state=tk.NORMAL if self.question_index < len(self.new_quiz_data) - 1 else tk.DISABLED)
        self.selected_answer.set(None)

         # --- Flag indicator on the question counter (step 3) ---
        if self.question_index in self.flagged_questions:
            self.flag_button.config(text="Unflag")
            self.question_count_label.config(
                text=f"⚑ Question {self.question_index + 1} of {len(self.new_quiz_data)}"
            )
        else:
            self.flag_button.config(text="Flag")
            self.question_count_label.config(
                text=f"Question {self.question_index + 1} of {len(self.new_quiz_data)}"
            )

    def _on_single_change(self):
        """Persist single-answer selection immediately."""
        self.saved_answers[self.question_index] = {
            "mode": "single",
            "selected": self.selected_answer.get() or ""
        }

    def _persist_multi_selection(self):
        """Persist multi-answer selection immediately."""
        selected_list = [opt for opt, var in self.checkbox_vars if var.get()]
        self.saved_answers[self.question_index] = {
            "mode": "multi",
            "selected": selected_list
        }

    def toggle_flag(self):
        """Flag or unflag the current question index for review."""
        idx = self.question_index
        if idx in self.flagged_questions:
            self.flagged_questions.remove(idx)
            self.flag_button.config(text="Flag")
            # remove glyph
            self.question_count_label.config(
                text=f"Question {self.question_index + 1} of {len(self.new_quiz_data)}"
            )
        else:
            self.flagged_questions.add(idx)
            self.flag_button.config(text="Unflag")
            # show glyph
            self.question_count_label.config(
                text=f"⚑ Question {self.question_index + 1} of {len(self.new_quiz_data)}"
            )

    def go_to_next_flagged(self):
        """Jump to the next flagged question after the current one (wraps around)."""
        if not self.flagged_questions:
            CustomPopup(self.root, "No flagged questions", "You haven't flagged any questions yet.", '260x120')
            return

        total = len(self.new_quiz_data)
        current = self.question_index
        # ordered list starting after current, wrapping around
        order = list(range(current + 1, total)) + list(range(0, current + 1))
        for i in order:
            if i in self.flagged_questions:
                self.question_index = i
                self.load_question()
                return

        # Shouldn't reach here, but just in case
        CustomPopup(self.root, "Not Found", "No next flagged question found.", '260x120')

    def set_interaction_enabled(self, enabled: bool):
        state = tk.NORMAL if enabled else tk.DISABLED

        # Nav & action buttons
        for b in [self.previous_button, self.next_button, self.check_button,
                self.reason_button, self.open_calc, self.finish_button,
                self.break_button, self.flag_button, self.next_flagged_button]:
            if b is not None:
                # During a pause, allow Resume button only; block Break button
                if not enabled and b is self.break_button:
                    b.config(state=tk.DISABLED)
                else:
                    b.config(state=state)

        # Options (radios / checkboxes) inside radio_button_frame
        for child in self.radio_button_frame.winfo_children():
            try:
                child.config(state=state)
            except Exception:
                pass

        # Special: while paused, enable resume button
        if not enabled:
            self.resume_button.config(state=tk.NORMAL)


    def start_break(self):
        if self.pause_used:
            CustomPopup(self.root, "Break already used", "You can only take one 15-minute break.", '260x120')
            return
        if self.pause_active:
            return

        self.pause_active = True
        self.pause_used = True
        self.pause_end_epoch = time.time() + 15 * 60  # 15 minutes
        self.set_interaction_enabled(False)
        self.break_button.config(text="Break (in progress)", state=tk.DISABLED)
        # Optional: show a banner
        self.question_label.config(text=f"⏸ Break in progress (15 minutes). Timer is paused.\n"
                                        f"You can click 'Resume Now' to return early.")

    def resume_after_break(self):
        if not self.pause_active:
            return
        # Force end of pause
        self.pause_end_epoch = time.time()

    def check_answer(self):
        current_question = self.new_quiz_data[self.question_index]

        if self.is_multi_current:
            selected_list = [opt for opt, var in self.checkbox_vars if var.get()]
            if not selected_list:
                CustomPopup(self.root, "No Selection", "Please select at least one option before checking.", '260x120')
                return

            if set(selected_list) == self.correct_set_current:
                CustomPopup(self.root, "Correct!", "Your answer is correct.", '200x100')
            else:
                # Build a friendly display of the correct set
                correct_display = "\n".join(self.correct_set_current) if self.correct_set_current else current_question.get("answer", "See notes")
                CustomPopup(self.root, "Incorrect", f"Incorrect! The correct answers were:\n\n{correct_display}", '500x260')
        else:
            if not self.selected_answer.get():
                CustomPopup(self.root, "No Selection", "Please select an option before checking.", '200x100')
                return

            if self.selected_answer.get() in current_question["answer"] or current_question["answer"] in self.selected_answer.get():
                CustomPopup(self.root, "Correct!", "Your answer is correct.", '200x100')
            else:
                CustomPopup(self.root, "Incorrect", f"Incorrect! The correct answer was: {current_question['answer']}.", '400x200')

        # Enable progressing after check
        self.check_button.config(state=tk.NORMAL)
        self.next_button.config(state=tk.NORMAL)
        self.answer_checked = True

   

    def calculator(self):
        CalculatorPopup(self.root)
   

    # Create the review button function
    def review_incorrect_questions(self):
        ReviewPopup(self.root, self.incorrect_questions)


    def next_question(self):
        current_question = self.new_quiz_data[self.question_index]

        if self.is_multi_current:
            selected_list = [opt for opt, var in self.checkbox_vars if var.get()]
            if set(selected_list) == self.correct_set_current:
                self.score += 1
            else:
                self.incorrect_questions.append({
                    "question": current_question["question"],
                    "correct_answer": "\n".join(self.correct_set_current) if self.correct_set_current else current_question.get("answer", "See notes"),
                    "reason": current_question.get("reason", "No explanation provided.")
                })
        else:
            if self.selected_answer.get() in current_question["answer"] or current_question["answer"] in self.selected_answer.get():
                self.score += 1
            else:
                self.incorrect_questions.append({
                    "question": current_question["question"],
                    "correct_answer": current_question["answer"],
                    "reason": current_question.get("reason", "No explanation provided.")
                })
        # Move to the next question or finish the quiz
        self.question_index += 1
        if self.question_index < len(self.new_quiz_data):
            self.load_question()
        else:
            self.show_result()


    def previous_question(self):
        # This will load the previous question
        if self.question_index > 0:
            self.question_index -= 1
            self.load_question()


    def show_reason(self):
        current_question = self.new_quiz_data[self.question_index]
        reason = current_question.get("reason", "No reason provided.")
        ReasonPopup(self.root, "Reason", reason)


    def show_result(self):
        """Display the final result with the score."""
        self.root.geometry("500x150")
        # Clear the window by removing existing widgets
        for widget in self.root.pack_slaves():
            widget.destroy()
        # Get the total number of questions and the percentage score
        total_questions = len(self.new_quiz_data)
        try:
            percentage_score = (self.score/total_questions)*100
            # Create a label to display the final score
            score_label = tk.Label(self.root, text=f"Quiz Completed!\nYour score is {percentage_score:.2f}%",
                                font=("Arial", 20), fg="black", bg="gray")
            score_label.pack(padx=10,pady=10)
        except ZeroDivisionError:
            score_label = tk.Label(self.root, text=f"Quiz Completed!\nYou didn't answer any questions.",
                                font=("Arial", 20), fg="black", bg="gray")
            score_label.pack(padx=10,pady=10)
       
        # Create a button container for the other buttons
        button_frame = tk.Frame(root, bg='gray')
        button_frame.pack(pady=5)

        # Button to review incorrect questions
        review_button = tk.Button(button_frame, text="Review", command=self.review_incorrect_questions, font=("Arial", 18))
        review_button.pack(side="left",pady=5,padx=5)

        # Button to review flagged questions
        flagged_button = tk.Button(button_frame, text="Flagged", command=self.review_flagged_questions, font=("Arial", 18))
        flagged_button.pack(side="left", pady=5, padx=5)

        # Create a restart quiz button
        restart_button = tk.Button(button_frame, text="Restart", command=self.restart_quiz, font=("Arial", 18), width=self.button_width)
        restart_button.pack(side="left",pady=5,padx=5)

        # Create an Exit button to close the quiz
        exit_button = tk.Button(button_frame, text="Close", command=self.root.quit, font=("Arial", 18), width=self.button_width)
        exit_button.pack(side="left",padx=5,pady=5)
    
    def review_flagged_questions(self):
        """Open a simple picker of flagged questions and jump to the selected one."""
        if not self.flagged_questions:
            CustomPopup(self.root, "No flagged questions", "You didn't flag any questions.", '260x120')
            return

        win = tk.Toplevel(self.root)
        win.title("Flagged Questions")
        win.configure(bg='gray')
        win.geometry("700x420")

        tk.Label(win, text="Select a flagged question:", bg='gray', fg='black', font=("Arial", 14, "bold")).pack(pady=6)

        # Listbox with preview of the question text
        lb = tk.Listbox(win, width=100, height=12)
        items = []
        for idx in sorted(self.flagged_questions):
            qtext = self.new_quiz_data[idx]["question"]
            # compact preview
            preview = textwrap.shorten(qtext.replace("\n", " "), width=95, placeholder="…")
            items.append((idx, preview))
            lb.insert(tk.END, f"{idx+1:>3}. {preview}")
        lb.pack(padx=10, pady=8, fill="both", expand=True)

        def _go_to_selected():
            sel = lb.curselection()
            if not sel:
                return
            target_idx = items[sel[0]][0]
            # Restore main quiz view
            for widget in self.root.pack_slaves():
                widget.destroy()
            # Rebuild main layout by restarting the quiz view statefully
            # (Simpler: just set index and call load_question if your layout persists)
            self.question_index = target_idx
            self.build_main_ui_again = getattr(self, "build_main_ui_again", None)
            if callable(self.build_main_ui_again):
                self.build_main_ui_again()
            else:
                # If you don't have a separate builder, just call load_question and re-create the button bar
                # assuming the main layout still exists. If not, restart the app state as needed.
                pass
            self.load_question()
            win.destroy()

        tk.Button(win, text="Go", command=_go_to_selected, width=8).pack(pady=6)


    def show_score(self):
        # This button will show the current number of correct answers
        CustomPopup(self.root, "Current Score:", f"You have answered {self.score} questions correctly!", '300x100')
   

    def finish_quiz(self):
        """Display the final result with the score."""
        self.root.geometry("500x150")
        # Clear the window by removing existing widgets
        for widget in self.root.pack_slaves():
            widget.destroy()
        # Get the total number of questions and the percentage score
        questions_answered = self.question_index
        try:
            percentage_score = (self.score/questions_answered)*100
            # Create a label to display the final score
            score_label = tk.Label(self.root, text=f"Quiz Completed!\nYour score is {percentage_score:.2f}%",
                                font=("Arial", 18), fg="black", bg="gray")
            score_label.pack(padx=10,pady=10)
        except ZeroDivisionError:
            score_label = tk.Label(self.root, text=f"Quiz Completed!\nYou didn't answer any questions.",
                                font=("Arial", 18), fg="black", bg="gray")
            score_label.pack(padx=10,pady=10)
       
        # Create a button container for the other buttons
        button_frame = tk.Frame(root, bg='gray')
        button_frame.pack(pady=5)

        # Button to review incorrect questions
        review_button = tk.Button(button_frame, text="Review", command=self.review_incorrect_questions, font=("Arial", 18))
        review_button.pack(side="left",pady=5,padx=5)        
       
        # Create a restart quiz button
        restart_button = tk.Button(button_frame, text="Restart", command=self.restart_quiz, font=("Arial", 18), width=self.button_width)
        restart_button.pack(side="left",pady=5,padx=5)

        # Create an Exit button to close the quiz
        exit_button = tk.Button(button_frame, text="Close", command=self.root.quit, font=("Arial", 18), width=self.button_width)
        exit_button.pack(side="left",padx=5,pady=5)


    def update_timer(self):
        # If no timer was set (e.g., 0 or None), just don't run the loop.
        if getattr(self, "time_left", None) in (None, 0):
            # Optionally hide/clear the timer label if you want:
            # self.timer_label.config(text="")
            return

        # -------------------- BREAK HANDLING --------------------
        if self.pause_active:
            # Freeze the exam timer; show remaining break time
            now = time.time()
            remaining_pause = int(max(0, (self.pause_end_epoch or now) - now))

            mins, secs = divmod(remaining_pause, 60)
            # Show a distinct break countdown
            self.timer_label.config(text=f"Break: {mins:02d}:{secs:02d} remaining")

            # While paused, keep everything disabled except Resume
            self.set_interaction_enabled(False)
            self.resume_button.config(state=tk.NORMAL)

            if remaining_pause <= 0:
                # Break is over -> resume normal operation
                self.pause_active = False
                self.pause_end_epoch = None
                self.set_interaction_enabled(True)
                # Lock the break button after use
                if getattr(self, "break_button", None):
                    self.break_button.config(text="Break used", state=tk.DISABLED)
                # Resume normal timer display on next tick
            # Schedule next tick and exit (do NOT decrement test timer during break)
            self.root.after(1000, self.update_timer)
            return

        # -------------------- NORMAL TIMER TICK --------------------
        # Re-enable UI if not paused
        self.set_interaction_enabled(True)
        if getattr(self, "pause_used", False):
            # User already consumed the break; disable its button
            if getattr(self, "break_button", None):
                self.break_button.config(text="Break used", state=tk.DISABLED)
            if getattr(self, "resume_button", None):
                self.resume_button.config(state=tk.DISABLED)

        # Decrement remaining test time
        self.time_left = max(0, int(self.time_left) - 1)

        mins, secs = divmod(int(self.time_left), 60)
        self.timer_label.config(text=f"Time Left: {mins:02d}:{secs:02d}")

        if self.time_left <= 0:
            # Time's up -> finalize once
            try:
                self.show_result()
            finally:
                return

        # Keep ticking
        self.root.after(1000, self.update_timer)

    def restart_quiz(self):
        self.root.destroy()
        self.root = tk.Tk()
        self.root.withdraw()
        # Destroy all the widgets before restarting.
        for widget in self.root.winfo_children():
            widget.destroy()
        # Call the QuizApp class again
        QuizApp(self.root, self.quiz_data)
        self.root.deiconify()

# Get the filepath for the powerpoint, replace with correct file name or full file
# path, additionally, you can change this to a input() function to take user input
pptx_file = prompt_for_pptx_path()
if not pptx_file:
    print("No file selected, exiting.")  

# Initialize tkinter window
root = tk.Tk()

# Hide the main window while getting the number of questions
root.withdraw()

# Extract images and prepare quiz data from PowerPoint
quiz_data = extract_images_and_prepare_quiz(pptx_file)

# Create the quiz app
quiz_app = QuizApp(root, quiz_data)

# Show the main window
root.deiconify()

# Start the tkinter main loop
root.mainloop()