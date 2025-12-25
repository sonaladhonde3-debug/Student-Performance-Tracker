**Project**: Student Skills & Performance Profiler

**Overview:**
- GUI app using `tkinter` to enter student scores, visualize class data, and predict final exam scores.
- Uses an SQLite DB (`student_performance.db`) created automatically in the project folder.

**Requirements:**
- Python 3.8+ (Windows recommended installer that includes Tk/Tcl)
- The Python packages in `requirements.txt`.

**How to run (PowerShell):**
```powershell
# 1) (Optional) Create a virtual environment in the project root
python -m venv .venv

# 2) Activate the venv
& ".\.venv\Scripts\Activate.ps1"

# 3) Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4) Run the app
python main.py
```

**Notes:**
- `tkinter` is included with the standard Python installer on Windows. If you see Tk errors, reinstall Python with Tcl/Tk support.
- Use the "Import CSV" button in the GUI to bulk add student records. CSV must contain: `name`, `roll_number`, `math_score`, `logic_score`, `coding_score`, `communication_score`. `final_exam_score` is optional.
- To reset data, either delete `student_performance.db` or use the "Clear Database" button.

If you want, I can install the requirements and launch the GUI now.
