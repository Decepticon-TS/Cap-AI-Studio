
import sqlite3
import pandas as pd
import threading
import uuid
from typing import Dict, Optional, List
import os

class SessionManager:
    """Manages session data and database operations for the image captioning system."""
    
    def __init__(self, db_path: str = "sessions.db"):
        """Initialize the SessionManager with database connection and table setup."""
        self.db_path = db_path
        self.lock = threading.Lock()
        self._init_database()
    
    def _init_database(self):
        """Initialize the SQLite database and create necessary tables if they don't exist."""
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS sessions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        original_order TEXT NOT NULL,
                        content_id TEXT UNIQUE NOT NULL,
                        stock_url TEXT NOT NULL,
                        caption_summary TEXT,
                        subject_people_objects TEXT,
                        subject_environment TEXT,
                        creative_technical_elements TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                conn.commit()
    
    def add_session_data(self, 
                        original_order: str,
                        stock_url: str,
                        analysis_components: Dict[str, str]) -> str:
        """
        Add new session data to the database.
        
        Args:
            original_order: Original order number provided by user
            stock_url: URL of the processed image
            analysis_components: Dictionary containing analysis results
            
        Returns:
            content_id: Unique identifier for the session
        """
        content_id = str(uuid.uuid4())
        
        # Map the analysis components to database fields
        mapped_data = {
            'caption_summary': analysis_components.get('base_description', ''),
            'subject_people_objects': '',  # Will be parsed from detailed_analysis
            'subject_environment': '',     # Will be parsed from detailed_analysis
            'creative_technical_elements': ''  # Will be parsed from detailed_analysis
        }
        
        # Parse the detailed analysis to separate sections
        if 'detailed_analysis' in analysis_components:
            detailed = analysis_components['detailed_analysis']
            sections = detailed.split('\n\n')
            for section in sections:
                if 'Subject Analysis' in section:
                    mapped_data['subject_people_objects'] = section
                elif 'Environment and Setting' in section:
                    mapped_data['subject_environment'] = section
                elif 'Technical Aspects' in section:
                    mapped_data['creative_technical_elements'] = section
        
        with self.lock:
            try:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute('''
                        INSERT INTO sessions (
                            original_order,
                            content_id,
                            stock_url,
                            caption_summary,
                            subject_people_objects,
                            subject_environment,
                            creative_technical_elements
                        ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        original_order,
                        content_id,
                        stock_url,
                        mapped_data['caption_summary'],
                        mapped_data['subject_people_objects'],
                        mapped_data['subject_environment'],
                        mapped_data['creative_technical_elements']
                    ))
                    conn.commit()
                return content_id
            except sqlite3.Error as e:
                raise Exception(f"Failed to add session data: {str(e)}")
    
    def get_session_data(self, content_id: str) -> Optional[Dict]:
        """Retrieve session data for a specific content ID."""
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM sessions WHERE content_id = ?
                ''', (content_id,))
                result = cursor.fetchone()
                
                if result:
                    columns = [description[0] for description in cursor.description]
                    return dict(zip(columns, result))
                return None
    
    def export_to_excel(self, output_path: str = "session_data.xlsx"):
        """Export the database contents to an Excel file."""
        with self.lock:
            try:
                with sqlite3.connect(self.db_path) as conn:
                    query = "SELECT * FROM sessions ORDER BY created_at"
                    df = pd.read_sql_query(query, conn)
                    
                    # Rename columns to match client template
                    df = df.rename(columns={
                        'original_order': 'Original Order',
                        'content_id': 'Content ID',
                        'stock_url': 'Stock URL',
                        'caption_summary': 'Caption Summary',
                        'subject_people_objects': 'Subject - People & Objects',
                        'subject_environment': 'Subject - Environment',
                        'creative_technical_elements': 'Creative & Technical Elements'
                    })
                    
                    # Remove internal columns not needed in export
                    df = df.drop(['id', 'created_at'], axis=1, errors='ignore')
                    
                    # Export to Excel
                    df.to_excel(output_path, index=False, engine='openpyxl')
                    return output_path
            except Exception as e:
                raise Exception(f"Failed to export to Excel: {str(e)}")
    
    def reset_database(self):
        """Clear all session data and reinitialize the database."""
        with self.lock:
            try:
                # Close any existing connections
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute("DROP TABLE IF EXISTS sessions")
                    conn.commit()
                
                # Reinitialize the database
                self._init_database()
            except sqlite3.Error as e:
                raise Exception(f"Failed to reset database: {str(e)}")
    
    def get_database_path(self) -> str:
        """Return the path to the SQLite database file."""
        return os.path.abspath(self.db_path)
    
    def get_all_sessions(self) -> List[Dict]:
        """Retrieve all session data ordered by creation date."""
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM sessions ORDER BY created_at")
                columns = [description[0] for description in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
