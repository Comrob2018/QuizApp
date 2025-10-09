# QuizApp v2.0.0

A fast, keyboard-friendly quiz runner that builds questions from a question bank(now supports: .txt, .md, .docx, and .pptx), supports images, multi-select answers, timers & breaks. Includes a **theme dropdown** (Solarized, Nord, Dracula, etc.) and a **High Contrast** theme for accessibility.

---

## 🧠 Question Bank Formats

Your quiz app can now load question banks from multiple file types.

### ✅ Supported File Types

| Format | Description | Recommended Use |
|---------|--------------|-----------------|
| `.pptx` | PowerPoint slides | Visual question decks and training imports |
| `.txt`  | Plain text | Quick editing and scripting |
| `.md`   | Markdown | GitHub-friendly quizzes with clean syntax |
| `.docx` | Word document | Authoring by non-technical users |

---

### 🧾 Plain Text Example (`.txt`)
```
Q: What does the acronym "IDS" stand for?
- Intrusion Detection System
- Internal Data Service
- Internet Delivery Software
- Integrated Defense Strategy
Answer: Intrusion Detection System
Reason: IDS tools monitor network traffic for suspicious activities.
```

---

### 📝 Markdown Example (`.md`)
```markdown
# Sample Cybersecurity Practice Test

## What does the acronym "IDS" stand for?
- Intrusion Detection System
- Internal Data Service
- Internet Delivery Software
- Integrated Defense Strategy
**Answer:** Intrusion Detection System  
**Reason:** IDS tools monitor network traffic for suspicious activities.
```

Multiple correct answers can be written as:
```markdown
**Answer:** A | C
```

---

### 🧮 Word Document Example (`.docx`)
Each question uses a **Heading** for the prompt, bullet points for answers, and labeled lines for answer and reason.

Example:
```
[Heading] What does the acronym "IDS" stand for?
• Intrusion Detection System  
• Internal Data Service  
• Internet Delivery Software  
• Integrated Defense Strategy  
Answer: Intrusion Detection System  
Reason: IDS tools monitor network traffic for suspicious activities.
```

---

### 🖼 PowerPoint Example (`.pptx`)
- Each **slide** = one question  
- **Title** = question text  
- **Bullets** = answer options  
- **Notes section** may contain:
  ```
  Answer: A | C
  Reason: Explanation or context.
  ```
- First slide image is automatically imported as the question image.

---

### ⚙️ How to Load
When prompted to open a question bank file:
1. Click **“Select Question Bank”**
2. Choose any supported format (`.pptx`, `.txt`, `.md`, `.docx`)
3. The app automatically detects and parses the file.

---

### 🧩 Tips for Authors
- `.md`: Great for GitHub versioning and readability  
- `.docx`: Ideal for collaborators without coding experience  
- `.txt`: Best for quick drafts or command-line users  
- `.pptx`: Perfect for training slides with visuals  

---

## 📂 Project Structure
```
practice.py      # Main application
README.md        # This file
```

### Requirements
```bash
pip install -r requirements.txt
```

### Run
```bash
python practice.py
```
- You’ll be prompted to select a `.pptx`, `.txt`, `.md`, or `.docx` file.
- The app applies your **saved theme** (via `QSettings`) at startup.  
- Use the **Theme** dropdown in the header to switch themes.

---

## Themes
The app uses a **registry** of named themes (`THEMES`) and a display‑name map (`THEME_NAMES`).  
Out of the box: 
  Solarized, Hoth, Tokyo Night, High Contrast, Cyberpunk, Superman, Dark Rose,
  H@(k3r_term!n41, Dathomir, Tatooine, Kashyyyk, Cloud City, Sith, Jedi, Crimson Dawn

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


- Quiz Settings: (Set # of Questions, Timer length, Test mode, Allow for breaks, repeated questions, and calculator)


<img width="514" height="284" alt="image" src="https://github.com/user-attachments/assets/b3178ad6-7e4a-4ae5-aadb-0d399280e367" />



- Dark Mode:


<img width="975" height="728" alt="image" src="https://github.com/user-attachments/assets/a3dc7f26-fcba-4a1f-b3d3-d148aaabcbcc" />



- Cyberpunk:


<img width="973" height="730" alt="image" src="https://github.com/user-attachments/assets/5788bfbb-b702-4ba4-82c7-05916d8a0e51" />



- Example quiz in **STUDY MODE**


<img width="976" height="729" alt="image" src="https://github.com/user-attachments/assets/e211e0bb-3770-495f-9610-94744420b71f" />



- Example quiz in **TEST MODE**


<img width="975" height="728" alt="image" src="https://github.com/user-attachments/assets/30371731-5ae6-417e-b650-96f26ad29813" />




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


- Flagged questions popup (click on the question and then click goto to go to that question)


<img width="273" height="270" alt="image" src="https://github.com/user-attachments/assets/331b74db-a825-4bb2-a4ae-831aec43ba5d" />
