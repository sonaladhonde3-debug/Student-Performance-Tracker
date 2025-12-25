import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from db_manager import DatabaseManager
from ml_engine import MLEngine


class StudentProfilerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Student Skills & Performance Profiler")
        self.root.geometry("1100x720")

        # Color palette
        self.bg = '#f4f6fb'
        self.panel = '#ffffff'
        self.accent = '#3b82f6'
        self.muted = '#6b7280'

        # Modern ttk styling
        style = ttk.Style()
        try:
            style.theme_use('clam')
        except Exception:
            pass

        style.configure('TFrame', background=self.bg)
        style.configure('Card.TFrame', background=self.panel, relief='flat')
        style.configure('TLabel', background=self.bg, font=('Segoe UI', 10))
        style.configure('Header.TLabel', background=self.bg, font=('Segoe UI', 13, 'bold'))
        style.configure('Accent.TButton', foreground='white', background=self.accent, font=('Segoe UI', 10, 'bold'))
        style.map('Accent.TButton', background=[('active', '#2b6fd6')])
        style.configure('TEntry', padding=6)
        style.configure('TCombobox', padding=6)
        style.configure('TLabelFrame', background=self.bg)
        style.configure('TNotebook', background=self.bg, padding=0)
        style.configure('TNotebook.Tab', padding=[0, 0])
        # Hide tab headers completely
        style.layout('TNotebook.Tab', [])

        self.root.configure(background=self.bg)

        self.db_manager = DatabaseManager()
        self.ml_engine = MLEngine(self.db_manager)

        container = ttk.Frame(self.root, style='TFrame')
        container.pack(fill=tk.BOTH, expand=True)

        # Left sidebar for navigation
        sidebar = ttk.Frame(container, width=220, style='TFrame')
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(12, 6), pady=12)

        logo = ttk.Label(sidebar, text="StudentProfiler", font=('Segoe UI', 12, 'bold'), background=self.panel, anchor='center')
        logo.pack(fill=tk.X, pady=(0, 12))

        nav_frame = ttk.Frame(sidebar, style='TFrame')
        nav_frame.pack(fill=tk.X)

        self.btn_data = tk.Button(nav_frame, text='Data Entry', command=self._on_tab_select_0, bg=self.accent, fg='white', font=('Segoe UI', 10, 'bold'), relief=tk.FLAT, padx=8, pady=6, cursor='hand2')
        self.btn_data.pack(fill=tk.X, pady=6)
        self.btn_analysis = tk.Button(nav_frame, text='Class Analysis', command=self._on_tab_select_1, bg=self.muted, fg='white', font=('Segoe UI', 10), relief=tk.FLAT, padx=8, pady=6, cursor='hand2')
        self.btn_analysis.pack(fill=tk.X, pady=6)
        self.btn_predict = tk.Button(nav_frame, text='Prediction', command=self._on_tab_select_2, bg=self.muted, fg='white', font=('Segoe UI', 10), relief=tk.FLAT, padx=8, pady=6, cursor='hand2')
        self.btn_predict.pack(fill=tk.X, pady=6)
        
        self.nav_buttons = [self.btn_data, self.btn_analysis, self.btn_predict]

        # Main content area
        content = ttk.Frame(container, style='TFrame')
        content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(6, 12), pady=12)

        self.notebook = ttk.Notebook(content)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.create_data_entry_tab()
        self.create_analysis_tab()
        self.create_prediction_tab()

        self.ml_engine.train_models()

    def _on_tab_select_0(self):
        self.notebook.select(0)
        self._update_nav_buttons(0)
    
    def _on_tab_select_1(self):
        self.notebook.select(1)
        self._update_nav_buttons(1)
    
    def _on_tab_select_2(self):
        self.notebook.select(2)
        self._update_nav_buttons(2)
    
    def _update_nav_buttons(self, active_index):
        for i, btn in enumerate(self.nav_buttons):
            if i == active_index:
                btn.config(bg=self.accent, font=('Segoe UI', 10, 'bold'))
            else:
                btn.config(bg=self.muted, font=('Segoe UI', 10))

    def create_data_entry_tab(self):
        tab1 = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(tab1, text="")

        card = ttk.Frame(tab1, style='Card.TFrame', padding=14)
        card.place(relx=0.03, rely=0.03, relwidth=0.94, relheight=0.92)

        heading = ttk.Label(card, text="Add Student Record", style='Header.TLabel')
        heading.grid(row=0, column=0, columnspan=2, sticky='w')

        ttk.Label(card, text="Name:").grid(row=1, column=0, sticky=tk.W, pady=8)
        self.name_entry = ttk.Entry(card, width=40)
        self.name_entry.grid(row=1, column=1, pady=8, sticky='w')

        ttk.Label(card, text="Roll Number:").grid(row=2, column=0, sticky=tk.W, pady=8)
        self.roll_entry = ttk.Entry(card, width=40)
        self.roll_entry.grid(row=2, column=1, pady=8, sticky='w')

        ttk.Label(card, text="Math Score:").grid(row=3, column=0, sticky=tk.W, pady=6)
        self.math_entry = ttk.Entry(card, width=20)
        self.math_entry.grid(row=3, column=1, sticky='w')

        ttk.Label(card, text="Logic Score:").grid(row=4, column=0, sticky=tk.W, pady=6)
        self.logic_entry = ttk.Entry(card, width=20)
        self.logic_entry.grid(row=4, column=1, sticky='w')

        ttk.Label(card, text="Coding Score:").grid(row=5, column=0, sticky=tk.W, pady=6)
        self.coding_entry = ttk.Entry(card, width=20)
        self.coding_entry.grid(row=5, column=1, sticky='w')

        ttk.Label(card, text="Communication Score:").grid(row=6, column=0, sticky=tk.W, pady=6)
        self.comm_entry = ttk.Entry(card, width=20)
        self.comm_entry.grid(row=6, column=1, sticky='w')

        ttk.Label(card, text="Final Exam Score (Optional):").grid(row=7, column=0, sticky=tk.W, pady=6)
        self.final_entry = ttk.Entry(card, width=20)
        self.final_entry.grid(row=7, column=1, sticky='w')

        button_frame = ttk.Frame(card, style='Card.TFrame')
        button_frame.grid(row=8, column=0, columnspan=2, pady=(12, 0), sticky='w')

        ttk.Button(button_frame, text="Save to DB", command=self.save_student, style='Accent.TButton').pack(side=tk.LEFT, padx=6)
        ttk.Button(button_frame, text="Import CSV", command=self.import_csv).pack(side=tk.LEFT, padx=6)
        ttk.Button(button_frame, text="Clear Database", command=self.clear_db).pack(side=tk.LEFT, padx=6)

        self.status_label = ttk.Label(card, text="", foreground='green')
        self.status_label.grid(row=9, column=0, columnspan=2, pady=10, sticky='w')

    def create_analysis_tab(self):
        tab2 = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(tab2, text="")

        panel = ttk.Frame(tab2, style='Card.TFrame', padding=12)
        panel.place(relx=0.03, rely=0.03, relwidth=0.94, relheight=0.92)

        header = ttk.Label(panel, text='Class Visualizations', style='Header.TLabel')
        header.pack(anchor='w')

        ttk.Button(panel, text="Refresh Visualizations", command=self.update_visualizations).pack(anchor='w', pady=8)

        self.fig = Figure(figsize=(10, 6), facecolor=self.panel)
        self.canvas = FigureCanvasTkAgg(self.fig, panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.update_visualizations()

    def create_prediction_tab(self):
        tab3 = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(tab3, text="")

        panel = ttk.Frame(tab3, style='Card.TFrame', padding=12)
        panel.place(relx=0.03, rely=0.03, relwidth=0.94, relheight=0.92)

        header = ttk.Label(panel, text='Predict Student Performance', style='Header.TLabel')
        header.grid(row=0, column=0, sticky='w')

        ttk.Label(panel, text="Select Student:").grid(row=1, column=0, sticky='w', pady=8)
        self.student_var = tk.StringVar()
        self.student_combo = ttk.Combobox(panel, textvariable=self.student_var, width=48, state="readonly")
        self.student_combo.grid(row=1, column=1, pady=8, padx=6, sticky='w')
        self.student_combo.bind("<<ComboboxSelected>>", self.load_student_scores)

        ttk.Button(panel, text="Refresh Students", command=self.refresh_students).grid(row=1, column=2, padx=6)

        self.scores_frame = ttk.LabelFrame(panel, text="Current Scores", padding=10)
        self.scores_frame.grid(row=2, column=0, columnspan=3, sticky='we', pady=10)

        self.math_label = ttk.Label(self.scores_frame, text="Math: -")
        self.math_label.grid(row=0, column=0, padx=8, pady=4)
        self.logic_label = ttk.Label(self.scores_frame, text="Logic: -")
        self.logic_label.grid(row=0, column=1, padx=8, pady=4)
        self.coding_label = ttk.Label(self.scores_frame, text="Coding: -")
        self.coding_label.grid(row=0, column=2, padx=8, pady=4)
        self.comm_label = ttk.Label(self.scores_frame, text="Communication: -")
        self.comm_label.grid(row=0, column=3, padx=8, pady=4)

        ttk.Button(panel, text="Predict Performance", command=self.predict_performance, style='Accent.TButton').grid(row=3, column=0, columnspan=3, pady=12)

        # Prediction card
        self.prediction_frame = ttk.Frame(panel, style='Card.TFrame', padding=12)
        self.prediction_frame.grid(row=4, column=0, columnspan=3, sticky='we')

        self.predicted_score_label = ttk.Label(self.prediction_frame, text="Predicted Final Score: -", font=("Segoe UI", 11, 'bold'))
        self.predicted_score_label.pack(anchor='w')

        # Progress bar for predicted score
        self.score_progress = ttk.Progressbar(self.prediction_frame, orient='horizontal', length=400, mode='determinate')
        self.score_progress.pack(pady=6)

        self.cluster_label = ttk.Label(self.prediction_frame, text="Category: -", font=("Segoe UI", 11))
        self.cluster_label.pack(anchor='w', pady=4)

        self.recommendation_label = ttk.Label(self.prediction_frame, text="Recommendation: -", font=("Segoe UI", 10), wraplength=700)
        self.recommendation_label.pack(anchor='w', pady=4)

        self.refresh_students()

    # The rest of the methods are kept same behavior as before but scoped to this class
    def save_student(self):
        try:
            name = self.name_entry.get().strip()
            roll = self.roll_entry.get().strip()
            math = float(self.math_entry.get())
            logic = float(self.logic_entry.get())
            coding = float(self.coding_entry.get())
            comm = float(self.comm_entry.get())
            final = self.final_entry.get().strip()

            if not name or not roll:
                messagebox.showerror("Error", "Name and Roll Number are required")
                return

            final_score = float(final) if final else None

            if self.db_manager.add_student_score(name, roll, math, logic, coding, comm, final_score):
                self.status_label.config(text="Student Added Successfully!", foreground="green")
                self.clear_entries()
                self.ml_engine.train_models()
                self.refresh_students()
            else:
                self.status_label.config(text="Error adding student", foreground="red")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric scores")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.roll_entry.delete(0, tk.END)
        self.math_entry.delete(0, tk.END)
        self.logic_entry.delete(0, tk.END)
        self.coding_entry.delete(0, tk.END)
        self.comm_entry.delete(0, tk.END)
        self.final_entry.delete(0, tk.END)

    def import_csv(self):
        try:
            file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
            if not file_path:
                return

            df = pd.read_csv(file_path)
            required_cols = ['name', 'roll_number', 'math_score', 'logic_score', 'coding_score', 'communication_score']

            if not all(col in df.columns for col in required_cols):
                messagebox.showerror("Error", "CSV must contain: name, roll_number, math_score, logic_score, coding_score, communication_score")
                return

            count = 0
            for _, row in df.iterrows():
                final_score = row.get('final_exam_score', None)
                if pd.isna(final_score):
                    final_score = None

                if self.db_manager.add_student_score(
                    str(row['name']), str(row['roll_number']),
                    float(row['math_score']), float(row['logic_score']),
                    float(row['coding_score']), float(row['communication_score']),
                    float(final_score) if final_score is not None else None
                ):
                    count += 1

            self.status_label.config(text=f"Imported {count} records successfully!", foreground="green")
            self.ml_engine.train_models()
            self.refresh_students()
        except Exception as e:
            messagebox.showerror("Error", f"Error importing CSV: {str(e)}")

    def clear_db(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all data?"):
            if self.db_manager.clear_database():
                self.status_label.config(text="Database cleared successfully", foreground="green")
                self.ml_engine.train_models()
                self.refresh_students()
            else:
                self.status_label.config(text="Error clearing database", foreground="red")

    def update_visualizations(self):
        try:
            df = self.db_manager.fetch_all_data()

            if df.empty:
                self.fig.clear()
                ax = self.fig.add_subplot(111)
                ax.text(0.5, 0.5, "No data available", ha='center', va='center', fontsize=14)
                self.canvas.draw()
                return

            self.fig.clear()

            ax1 = self.fig.add_subplot(2, 1, 1)
            score_cols = ['math_score', 'logic_score', 'coding_score', 'communication_score']
            corr_matrix = df[score_cols].corr()
            sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', ax=ax1,
                        xticklabels=['Math', 'Logic', 'Coding', 'Communication'],
                        yticklabels=['Math', 'Logic', 'Coding', 'Communication'])
            ax1.set_title('Correlation Heatmap of Skills', fontsize=12, fontweight='bold')

            ax2 = self.fig.add_subplot(2, 1, 2)
            averages = df[score_cols].mean()
            ax2.bar(['Math', 'Logic', 'Coding', 'Communication'], averages.values, color=['#3498db', '#2ecc71', '#e74c3c', '#f39c12'])
            ax2.set_title('Class Average by Subject', fontsize=12, fontweight='bold')
            ax2.set_ylabel('Average Score')
            ax2.set_ylim(0, 100)

            for i, v in enumerate(averages.values):
                ax2.text(i, v + 2, f'{v:.1f}', ha='center', va='bottom')

            self.fig.tight_layout()
            self.canvas.draw()
        except Exception as e:
            messagebox.showerror("Error", f"Error updating visualizations: {str(e)}")

    def refresh_students(self):
        students = self.db_manager.get_students_list()
        student_names = [f"{name} ({roll})" for _, name, roll in students]
        self.student_combo['values'] = student_names
        if students:
            self.student_combo.current(0)
            self.load_student_scores()

    def load_student_scores(self, event=None):
        try:
            selected = self.student_var.get()
            if not selected:
                return

            students = self.db_manager.get_students_list()
            student_names = [f"{name} ({roll})" for _, name, roll in students]

            if selected in student_names:
                idx = student_names.index(selected)
                student_id = students[idx][0]
                scores = self.db_manager.get_student_scores(student_id)

                if scores:
                    self.math_label.config(text=f"Math: {scores['math_score']:.1f}")
                    self.logic_label.config(text=f"Logic: {scores['logic_score']:.1f}")
                    self.coding_label.config(text=f"Coding: {scores['coding_score']:.1f}")
                    self.comm_label.config(text=f"Communication: {scores['communication_score']:.1f}")
                    self.current_scores = scores
                    self.current_student_id = student_id
        except Exception as e:
            print(f"Error loading student scores: {e}")

    def predict_performance(self):
        try:
            if not hasattr(self, 'current_scores'):
                messagebox.showwarning("Warning", "Please select a student first")
                return

            scores = self.current_scores
            predicted = self.ml_engine.predict_final_score(
                scores['math_score'], scores['logic_score'],
                scores['coding_score'], scores['communication_score']
            )

            _, cluster_name = self.ml_engine.get_student_cluster(
                scores['math_score'], scores['logic_score'],
                scores['coding_score'], scores['communication_score']
            )

            recommendation = self.ml_engine.get_recommendation(
                scores['math_score'], scores['logic_score'],
                scores['coding_score'], scores['communication_score'],
                predicted
            )

            self.predicted_score_label.config(text=f"Predicted Final Score: {predicted:.2f}")
            self.cluster_label.config(text=f"Category: {cluster_name}")
            self.recommendation_label.config(text=f"Recommendation: {recommendation}")
        except Exception as e:
            messagebox.showerror("Error", f"Error predicting performance: {str(e)}")
