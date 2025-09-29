| Shorthand  | Longhand meaning                                                                 |
| ---------- | -------------------------------------------------------------------------------- |
| `q`        | The current **question dict** (or question text in review/export loops).         |
| `opts`     | List of **answer option strings** for a question.                                |
| `cb`       | A **QCheckBox** representing one multi-select option.                            |
| `btn`      | Generic **button** object (QPushButton/QRadioButton) used in helpers and rows.   |
| `dlg`      | A **dialog** instance (e.g., `BreakDialog`, flag list `QDialog`).                |
| `v`        | A **QVBoxLayout** (vertical layout) placeholder var.                             |
| `row`      | A **QHBoxLayout** (or row container) placeholder var for footer/action rows.     |
| `hl`       | A **horizontal layout** used inside an answer row.                               |
| `lst`      | The **QListWidget** that lists flagged questions.                                |
| `it`       | The **currently selected item** (`QListWidgetItem`) in the flag dialog.          |
| `idx`      | The **current question index** (int).                                            |
| `mm`, `ss` | **Minutes** / **seconds** when formatting timers.                                |
| `img`      | The **image path** for the current question.                                     |
| `pix`      | A **QPixmap** loaded from `img`.                                                 |
| `scaled`   | The **scaled pixmap** used for the thumbnail label.                              |
| `ms`       | **Milliseconds** for flash/revert timers on buttons.                             |
| `t`        | The in-flight **QTimer** used to revert a flashed button.                        |
| `n`        | **Requested question count** from Settings.                                      |
| `r`        | One **review/export row dict** while writing the .txt.                           |
| `i`        | **Loop index** (1-based in export).                                              |
| `w`        | Generic **widget** variable in “add this widget” loops.                          |
| `cw`       | The **central widget** (`QWidget`) for the main window.                          |
| `root`     | The main window’s **root layout** (`QVBoxLayout`).                               |
| `head`     | The **header row** layout (timer, theme, mode, flags).                           |
| `actions`  | The **actions row** (Show Image, Why, Check, Break…).                            |
| `nav`      | The **navigation row** (Prev/Next/Submit/Finish).                                |
| `_e`       | Throwaway **event object** in mouse handlers.                                    |
