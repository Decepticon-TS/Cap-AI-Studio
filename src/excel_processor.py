import pandas as pd
from typing import Dict, List
from datetime import datetime

class ExcelProcessor:
    def __init__(self):
        self.columns = [
            'original order', 'content_id', 'URL', 'Base_Description',
            'Subject Analysis (People, Objects, Actions)', 
            'Environment and Setting', 'Technical Aspects', 'Final_Summary'
        ]
        
    def load_excel(self, file) -> pd.DataFrame:
        """Load the input Excel file and validate its structure"""
        try:
            df = pd.read_excel(file)
            # Validate required columns
            required_cols = ['URL', 'content_id']
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                raise ValueError(f"Missing required columns: {missing_cols}")
            return df
        except Exception as e:
            raise Exception(f"Failed to load Excel file: {str(e)}")

    def save_results(self, input_df: pd.DataFrame, results: List[Dict], output_path: str):
        """Save the results to a new Excel file"""
        try:
            # Create a copy of input DataFrame
            output_df = input_df.copy()
            
            # Update with results
            for result in results:
                idx = output_df[output_df['content_id'] == result['content_id']].index[0]
                output_df.loc[idx, 'Base_Description'] = result.get('base_description', '')
                output_df.loc[idx, 'Subject Analysis (People, Objects, Actions)'] = result.get('detailed_analysis', '')
                output_df.loc[idx, 'Environment and Setting'] = result.get('environment_setting', '')
                output_df.loc[idx, 'Technical Aspects'] = result.get('technical_aspects', '')
                output_df.loc[idx, 'Final_Summary'] = result.get('final_summary', '')
            
            # Save to new file
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"{output_path}_processed_{timestamp}.xlsx"
            output_df.to_excel(output_file, index=False)
            return output_file
        except Exception as e:
            raise Exception(f"Failed to save results: {str(e)}")
