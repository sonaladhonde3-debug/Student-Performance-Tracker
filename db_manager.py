import sqlite3
import pandas as pd
from typing import List, Tuple, Optional

class DatabaseManager:
    def __init__(self, db_name: str = "student_performance.db"):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                roll_number TEXT UNIQUE NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                math_score REAL NOT NULL,
                logic_score REAL NOT NULL,
                coding_score REAL NOT NULL,
                communication_score REAL NOT NULL,
                final_exam_score REAL,
                FOREIGN KEY (student_id) REFERENCES students(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_student_score(self, name: str, roll_number: str, math_score: float,
                         logic_score: float, coding_score: float, 
                         communication_score: float, final_exam_score: Optional[float] = None) -> bool:
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('SELECT id FROM students WHERE roll_number = ?', (roll_number,))
            result = cursor.fetchone()
            
            if result:
                student_id = result[0]
            else:
                cursor.execute('INSERT INTO students (name, roll_number) VALUES (?, ?)', 
                             (name, roll_number))
                student_id = cursor.lastrowid
            
            cursor.execute('''
                INSERT INTO scores (student_id, math_score, logic_score, coding_score, 
                                  communication_score, final_exam_score)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (student_id, math_score, logic_score, coding_score, 
                  communication_score, final_exam_score))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error adding student score: {e}")
            return False
    
    def fetch_all_data(self) -> pd.DataFrame:
        try:
            conn = sqlite3.connect(self.db_name)
            query = '''
                SELECT s.id, s.name, s.roll_number, 
                       sc.math_score, sc.logic_score, sc.coding_score, 
                       sc.communication_score, sc.final_exam_score
                FROM students s
                JOIN scores sc ON s.id = sc.student_id
            '''
            df = pd.read_sql_query(query, conn)
            conn.close()
            return df
        except Exception as e:
            print(f"Error fetching data: {e}")
            return pd.DataFrame()
    
    def get_students_list(self) -> List[Tuple[int, str, str]]:
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('SELECT id, name, roll_number FROM students')
            students = cursor.fetchall()
            conn.close()
            return students
        except Exception as e:
            print(f"Error fetching students list: {e}")
            return []
    
    def get_student_scores(self, student_id: int) -> Optional[dict]:
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT math_score, logic_score, coding_score, communication_score, final_exam_score
                FROM scores
                WHERE student_id = ?
                ORDER BY id DESC
                LIMIT 1
            ''', (student_id,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {
                    'math_score': result[0],
                    'logic_score': result[1],
                    'coding_score': result[2],
                    'communication_score': result[3],
                    'final_exam_score': result[4]
                }
            return None
        except Exception as e:
            print(f"Error fetching student scores: {e}")
            return None
    
    def clear_database(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM scores')
            cursor.execute('DELETE FROM students')
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error clearing database: {e}")
            return False