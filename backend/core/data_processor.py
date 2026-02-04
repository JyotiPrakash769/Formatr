import os
import pandas as pd
import json

class DataProcessor:
    @staticmethod
    def csv_to_json(input_path: str, output_dir: str) -> str:
        """Convert CSV to JSON"""
        filename = os.path.basename(input_path)
        name, _ = os.path.splitext(filename)
        output_path = os.path.join(output_dir, f"{name}.json")
        
        df = pd.read_csv(input_path)
        df.to_json(output_path, orient='records', indent=2)
        
        return output_path
    
    @staticmethod
    def json_to_csv(input_path: str, output_dir: str) -> str:
        """Convert JSON to CSV"""
        filename = os.path.basename(input_path)
        name, _ = os.path.splitext(filename)
        output_path = os.path.join(output_dir, f"{name}.csv")
        
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        df = pd.DataFrame(data)
        df.to_csv(output_path, index=False)
        
        return output_path
    
    @staticmethod
    def csv_to_excel(input_path: str, output_dir: str) -> str:
        """Convert CSV to Excel (XLSX)"""
        filename = os.path.basename(input_path)
        name, _ = os.path.splitext(filename)
        output_path = os.path.join(output_dir, f"{name}.xlsx")
        
        df = pd.read_csv(input_path)
        df.to_excel(output_path, index=False, engine='openpyxl')
        
        return output_path
    
    @staticmethod
    def excel_to_csv(input_path: str, output_dir: str) -> str:
        """Convert Excel (XLSX) to CSV"""
        filename = os.path.basename(input_path)
        name, _ = os.path.splitext(filename)
        output_path = os.path.join(output_dir, f"{name}.csv")
        
        df = pd.read_excel(input_path, engine='openpyxl')
        df.to_csv(output_path, index=False)
        
        return output_path
    
    @staticmethod
    def excel_to_json(input_path: str, output_dir: str) -> str:
        """Convert Excel (XLSX/XLS) to JSON"""
        filename = os.path.basename(input_path)
        name, ext = os.path.splitext(filename)
        output_path = os.path.join(output_dir, f"{name}.json")
        
        # Detect engine based on extension
        engine = 'xlrd' if ext.lower() == '.xls' else 'openpyxl'
        
        df = pd.read_excel(input_path, engine=engine)
        df.to_json(output_path, orient='records', indent=2)
        
        return output_path
    
    @staticmethod
    def xls_to_xlsx(input_path: str, output_dir: str) -> str:
        """Convert legacy Excel (XLS) to modern Excel (XLSX)"""
        filename = os.path.basename(input_path)
        name, _ = os.path.splitext(filename)
        output_path = os.path.join(output_dir, f"{name}.xlsx")
        
        # Read with xlrd, write with openpyxl
        df = pd.read_excel(input_path, engine='xlrd')
        df.to_excel(output_path, index=False, engine='openpyxl')
        
        return output_path
