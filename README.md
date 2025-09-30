# QuizApp v1.2.4

A fast, keyboard-friendly quiz runner that builds questions from a PowerPoint (`.pptx`), supports images, multi‑select answers, timers & breaks, and now ships with a theme **dropdown** (Solarized, Nord, Dracula, etc.) plus a **High Contrast** theme for accessibility.

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
  - Always-visible **Show Image** button (colorized blue when image is available).
  - Click **Show Image** or Thumbnail to view image in a zoomable window.
  - Thumbnail is shown below question text when an image exists.

- **Modes**
  - **Practice Mode**: Check answers immediately, see reasons for each question.
  - **Test Mode**: No feedback until the end.
  - Visual **mode badge** in the header next to flag button/timer.

- **Quiz Options**
  - Choose number of questions (all or random subset).
  - Allow repeat questions if you want more than the bank contains.
  - Timer (set minutes, or 0 for untimed).
  - One **15-minute break** available if timer is enabled.
  - Flag questions and revisit flagged list.
  - Integrated calculator.

- **Answer Handling**
  - Submit saves answers (always neutral now).
  - Navigation with Next/Previous without reshuffling.
  - **Answer order randomized once** at quiz creation (stable during run).

- **Review Screen**
  - Accessible when clicking **Finish** (always clickable; warns if unanswered).
  - Shows:
    - Score as **X/Y (Z%)** at the top.
    - Each question with correct answer, your answer, and explanation.
    - ✅ besides questions with correct answers.
    - ❌ besides questions with incorrect answers.
  - Export review as plain text (`.txt`) with ✓/✗ markers per question.
  - Restart option that reopens the settings dialog.

---

## 📂 Project Structure

```
practice.py    # Main application
README.md        # This file
```

---

## 🚀 Usage

### Requirements
- **Python**: 3.9+ (3.10+ recommended)  
- **OS**: Windows, macOS, Linux  
- **Python packages**:
  - `PyQt6 >= 6.5.0`
  - `python-pptx >= 0.6.21`

### Run
```bash
python practice.py
```
- You’ll be prompted to select a **.pptx** file.
- The app applies your **saved theme** (via `QSettings`) at startup.  
- Use the **Theme** dropdown in the header to switch themes at any time.
  
## Themes

The app uses a **registry** of named themes (`THEMES`) and a display‑name map (`THEME_NAMES`).  
Out of the box:
- Dark
- Solarized Dark
- Nord, Gruvbox (Dark), Tokyo Night
- **High Contrast** (color‑blind friendly; black bg, white text, bright yellow focus, blue accent)
- Sapphire, Dark Rose, Crimson Ember
- Cyberpunk, and Hacker Terminal.

### Adding your own theme

1. Add an entry to `THEMES`:
   ```python
   "my_theme": {
     "bg":"#...", "surface":"#...", "surface_alt":"#...", "text":"#...",
     "muted":"#...", "border":"#...", "primary":"#...", "accent":"#...",
     "success":"#...", "warn":"#...", "error":"#..."
   }
   ```
2. Add a user‑friendly label to `THEME_NAMES`:
   ```python
   "My Theme": "my_theme"
   ```
3. Relaunch → it appears in the dropdown automatically.

### Create a standalone app
```bash\windows\macOS
pyinstaller --onefile --windowed --icon=ask.png .\practice.py
```
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

## Version checking

- On startup (and during the dependency preflight), the app fetches a **remote version** from a GitHub document and compares it with the local `VERSION` string.
- If your version is behind, you’ll see this **popup**:

> “Your version is not the latest version. For the latest version and features please download a new version from https://github.com/Comrob2018/QuizApp/tree/main”

- Remote file (default):  
  `https://raw.githubusercontent.com/Comrob2018/QuizApp/main/VERSION`  
  (Change this URL in code if you store version metadata elsewhere.)

### Offline behavior
If the version file can’t be fetched (offline / rate limited), the app continues without warning or delay.

---

## 📸 Screenshots

- File Selector:


<img width="609" height="442" alt="image" src="https://github.com/user-attachments/assets/4138d9ce-58a7-4745-88a4-003329e018bf" />


- Quiz Settings: (Will pull max number of questions from number of slides in the presentation)


<img width="518" height="286" alt="image" src="https://github.com/user-attachments/assets/bc212c17-6d93-4540-8158-73f2deb9015d" />



- Dark Mode:


<img width="974" height="733" alt="image" src="https://github.com/user-attachments/assets/a3013170-3b12-47b9-8118-f15f3e2c4295" />



- Cyberpunk:


<img width="976" height="721" alt="image" src="https://github.com/user-attachments/assets/62383662-9278-4b4c-bda6-7c39085057cf" />



- Example quiz in **STUDY Mode**


<img width="974" height="733" alt="image" src="https://github.com/user-attachments/assets/9bcd8c8c-6119-47d9-928f-6897e4f08763" />




- Example quiz in **Test Mode**


<img width="973" height="728" alt="image" src="https://github.com/user-attachments/assets/d408892e-b674-4d6c-a3cc-41f1ce504a90" />


- Unanswered questions warning


<img width="416" height="117" alt="image" src="https://github.com/user-attachments/assets/b0046c31-7dd7-4ff3-9904-013d6fc4b5ec" />


- Question with picture (blue "Show Image" button and a thumbnail beneath the question text when image is present, click either to enlarge the picture)


<img width="650" height="662" alt="image" src="https://github.com/user-attachments/assets/f5fb5750-4db1-4654-9330-ac2cb19e5578" />


- Review Screen  (✅ Correct answers,  ❌ Incorrect answers)


<img width="556" height="219" alt="image" src="https://github.com/user-attachments/assets/550834f3-e57c-4445-be90-e6cb551a7720" />


- Exported review with ✓ / ✗ next to questions.


<img width="1900" height="327" alt="image" src="https://github.com/user-attachments/assets/8d067d18-ced5-49ae-8c3d-f43be1566251" />


- Submit button answer saved


<img width="982" height="63" alt="image" src="https://github.com/user-attachments/assets/f73b7367-2e7b-4121-bd14-b42473e3277c" />


- Check answer button correct


<img width="372" height="120" alt="image" src="https://github.com/user-attachments/assets/5e77a54d-60f9-477e-a8ae-d0c2f107c8a5" />


- Check answer button not quite


<img width="362" height="118" alt="image" src="https://github.com/user-attachments/assets/b964d9c8-3a27-427e-8c9e-0cee605a2828" />


- Flagged questions popup


<img width="273" height="270" alt="image" src="https://github.com/user-attachments/assets/331b74db-a825-4bb2-a4ae-831aec43ba5d" />
