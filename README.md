# QuizApp v4.2

A feature-rich quiz application built with **Python 3.13** and **PyQt6**, designed to run practice or test-style quizzes using PowerPoint slide decks (`.pptx`) as the question bank.

---
- **Question Bank from PowerPoint**
  - Extracts questions, multiple choice/multi-select answers, explanations, and images from slide decks.
  - Notes section in slides must contain the line:  
    `Answer is: option1 | option2 ; option3`  
    followed optionally by a line explaining the reason.

- **Answer Types**
  - Single choice (radio buttons).
  - Multi-select (checkboxes) when multiple answers are correct.

- **Images**
  - Slide images automatically imported.
  - Always-visible **Show Image** button (colorized when image is available).
  - Click or press **`I`** to view image in a zoomable window.
  - 📷 emoji shown in question text when an image exists.

- **Modes**
  - **Practice Mode**: Check answers immediately, see reasons.
  - **Test Mode**: No feedback until the end.
  - Visual **mode badge** in the header and window title.

- **Quiz Options**
  - Choose number of questions (all or random subset).
  - Allow repeat questions if you want more than the bank contains.
  - Timer (set minutes, or 0 for untimed).
  - One **15-minute break** available if timer is enabled.
  - Flag questions and revisit flagged list.
  - Integrated calculator.

- **Answer Handling**
  - Submit saves answers (neutral in Test Mode).
  - Navigation with Next/Previous without reshuffling.
  - **Answer order randomized once** at quiz creation (stable during run).

- **Review Screen**
  - Accessible when clicking **Finish** (always clickable; warns if unanswered).
  - Shows:
    - Score as **X/Y (Z%)** at the top.
    - Each question with correct answer, your answer, and explanation.
    - ✅ Correct answers highlighted in green.
    - ❌ Incorrect answers highlighted in red.
    - [FLAGGED] marker if flagged during the test.
  - Export review as plain text (`.txt`) with ✓/✗ markers per question.
  - Restart option that reopens the settings dialog.

---

## 📂 Project Structure

```
practiceqt.py    # Main application
README.md        # This file
```

---

## 🚀 Usage

### Requirements
- Python **3.13+**
- Install dependencies:
  ```bash
  pip install PyQt6 python-pptx
  ```

### Run
```bash
python quiz_pyqt6.py
```

### Starting a Quiz
1. Choose a `.pptx` file containing your question bank.
2. Configure quiz settings (mode, timer, question count, repeats, etc.).
3. Begin quiz.

---

## 📝 Creating Questions in PowerPoint

1. **Slides**:  
   - First text box → Question text.  
   - Subsequent text boxes or lines → Answer options.

2. **Notes**:  
   - First line must contain the correct answers:  
     `Answer is: A | C`  
     or  
     `Answer is: AWS Shield ; AWS Shield Advanced`
   - Next line (optional) → Explanation or reason.

3. **Images**:  
   - First image on a slide is imported and linked to the question.

---

## 📸 Screenshots

- File Selector:


<img width="609" height="442" alt="image" src="https://github.com/user-attachments/assets/4138d9ce-58a7-4745-88a4-003329e018bf" />


- Quiz Settings:


<img width="514" height="277" alt="image" src="https://github.com/user-attachments/assets/56cd86c1-0dd3-4822-b0d5-d99b1a4a54fd" />


- Example quiz in **Practice Mode**

  
<img width="976" height="729" alt="image" src="https://github.com/user-attachments/assets/ac1af6bb-da9f-452d-a245-0039fc5443e9" />


- Example quiz in **Test Mode**


<img width="972" height="694" alt="image" src="https://github.com/user-attachments/assets/d89c2c68-aa33-4213-b9c9-ff3921dc3210" />


- Question with picture (blue "Show Image" button and camera icon besides question text)


<img width="622" height="668" alt="image" src="https://github.com/user-attachments/assets/c30ddc25-0dcd-4a83-9e3a-2284413147f8" />


- Review screen with ✓ / ✗ 


<img width="1900" height="327" alt="image" src="https://github.com/user-attachments/assets/8d067d18-ced5-49ae-8c3d-f43be1566251" />

