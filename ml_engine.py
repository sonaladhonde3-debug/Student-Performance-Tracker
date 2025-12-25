import pandas as pd
import numpy as np
from typing import Tuple
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from db_manager import DatabaseManager

class MLEngine:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.regression_model = LinearRegression()
        self.clustering_model = KMeans(n_clusters=3, random_state=42, n_init=10)
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def generate_synthetic_data(self, n_samples: int = 20) -> pd.DataFrame:
        np.random.seed(42)
        data = []
        
        for i in range(n_samples):
            math = np.random.uniform(50, 100)
            logic = np.random.uniform(50, 100)
            coding = np.random.uniform(50, 100)
            comm = np.random.uniform(50, 100)
            
            final_score = (math * 0.25 + logic * 0.25 + coding * 0.30 + comm * 0.20) + np.random.uniform(-10, 10)
            final_score = np.clip(final_score, 0, 100)
            
            data.append({
                'math_score': round(math, 2),
                'logic_score': round(logic, 2),
                'coding_score': round(coding, 2),
                'communication_score': round(comm, 2),
                'final_exam_score': round(final_score, 2)
            })
        
        return pd.DataFrame(data)
    
    def prepare_training_data(self) -> pd.DataFrame:
        df = self.db_manager.fetch_all_data()
        
        if df.empty or len(df) < 10:
            synthetic_df = self.generate_synthetic_data(20)
            if not df.empty:
                synthetic_df = pd.concat([df[['math_score', 'logic_score', 'coding_score', 
                                             'communication_score', 'final_exam_score']], 
                                         synthetic_df], ignore_index=True)
            return synthetic_df
        
        return df[['math_score', 'logic_score', 'coding_score', 
                   'communication_score', 'final_exam_score']].copy()
    
    def train_models(self):
        try:
            df = self.prepare_training_data()
            
            if df.empty:
                return False
            
            X = df[['math_score', 'logic_score', 'coding_score', 'communication_score']].values
            y = df['final_exam_score'].values
            
            X_scaled = self.scaler.fit_transform(X)
            
            self.regression_model.fit(X_scaled, y)
            self.clustering_model.fit(X_scaled)
            
            self.is_trained = True
            return True
        except Exception as e:
            print(f"Error training models: {e}")
            return False
    
    def predict_final_score(self, math_score: float, logic_score: float, 
                           coding_score: float, communication_score: float) -> float:
        if not self.is_trained:
            self.train_models()
        
        try:
            X = np.array([[math_score, logic_score, coding_score, communication_score]])
            X_scaled = self.scaler.transform(X)
            prediction = self.regression_model.predict(X_scaled)[0]
            return max(0, min(100, round(prediction, 2)))
        except Exception as e:
            print(f"Error predicting score: {e}")
            return 0.0
    
    def get_student_cluster(self, math_score: float, logic_score: float,
                           coding_score: float, communication_score: float) -> Tuple[int, str]:
        if not self.is_trained:
            self.train_models()
        
        try:
            X = np.array([[math_score, logic_score, coding_score, communication_score]])
            X_scaled = self.scaler.transform(X)
            cluster = self.clustering_model.predict(X_scaled)[0]
            
            cluster_names = {
                0: "High Performers",
                1: "Average",
                2: "At Risk"
            }
            
            return cluster, cluster_names.get(cluster, "Unknown")
        except Exception as e:
            print(f"Error getting cluster: {e}")
            return -1, "Unknown"
    
    def get_recommendation(self, math_score: float, logic_score: float,
                          coding_score: float, communication_score: float,
                          predicted_score: float) -> str:
        scores = {
            'Math': math_score,
            'Logic': logic_score,
            'Coding': coding_score,
            'Communication': communication_score
        }
        
        min_skill = min(scores, key=scores.get)
        min_score = scores[min_skill]
        
        if predicted_score < 60:
            return f"Needs significant improvement. Focus on {min_skill} (current: {min_score:.1f})"
        elif predicted_score < 75:
            return f"Needs help in {min_skill} (current: {min_score:.1f})"
        elif predicted_score < 85:
            return f"Good performance. Consider strengthening {min_skill} for better results"
        else:
            return "Excellent performance! Maintain current study habits"

