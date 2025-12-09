import openpyxl

class ExcelReader:
    @staticmethod
    def get_data(file_path, sheet_name):
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook[sheet_name]
        data = []
        
        # Assuming first row is header
        for row in sheet.iter_rows(min_row=2, values_only=True):
            data.append(row)
            
        return data
