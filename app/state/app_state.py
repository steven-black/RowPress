import threading
from openpyxl.utils import column_index_from_string

class AppState:
    def __init__(self):
        self.document_name_entry = None # Entry for document name in the UI
        self.sheet_name_entry = None # Entry for sheet name in the UI

        self.naming_columns_entry = None # Entry for naming columns in the UI
        self.naming_columns = [] # List of rows to be used for naming the documents
        self.excel_file_path = ""
        self.word_template_path = ""

        self.replacement = ""
        self.placeholder = ""

        self.output_folder_path = "output-docs"
        self.output_file_name = "" # Main name of the output file

        self.personalization_name = ""

        self.save_as_pdf = None # Boolean to save the output as PDF or not
        self.is_processing = False # Boolean to indicate if the app is processing data
        self.stop_event = threading.Event() # Event to stop the processing thread

        # UI Elements
        self.root = None
        self.left_group = None
        self.right_group = None
        self.propogate_template_button = None # Button to propogate the template
        self.stop_processing_button = None # Button to stop the processing
        self.placeholders_and_replacements_groups = [] # List of UI elements for placeholders and replacements
        self.placeholders_and_replacement_columns = [] # List to hold placeholder and replacement entries

        # UI Variables
        self.current_row = 0
        self.current_column = 0

    def get_max_columns(self):
            self.root.update_idletasks()
            
            max_columns = int((self.root.winfo_width() - self.left_group.winfo_width()) / 50)
            print(f"Max columns: {max_columns}")
            return max_columns
            
    
    def get_document_name(self):
        if self.document_name_entry:
            return self.document_name_entry.get()
        return ""
    
    def get_sheet_name(self):
        if self.sheet_name_entry:
            return self.sheet_name_entry.get()
        return ""
    
    def get_naming_columns(self):
        if self.naming_columns_entry:
            naming_columns = self.naming_columns_entry.get()
            if naming_columns:
                self.naming_columns = [col.strip() for col in naming_columns.split(";")]
                naming_columns_index = []
                for col in self.naming_columns:
                    if col == '': # Check for empty columns
                        continue
                    naming_columns_index.append(column_index_from_string(col)-1)
                    self.naming_columns = naming_columns_index
                return self.naming_columns
        return []
    
    def get_placeholders_and_replacement_columns(self):
        self.placeholder_and_replacement_columns = []
        for placeholder_and_replacement_column in self.placeholders_and_replacements_groups:
            placeholder_entry = placeholder_and_replacement_column[0].get()
            replacement_column_entry = placeholder_and_replacement_column[1].get()
            if placeholder_entry and replacement_column_entry:
                self.placeholders_and_replacement_columns.append((placeholder_entry, column_index_from_string(replacement_column_entry)-1))
        return self.placeholders_and_replacement_columns


app_state = AppState()
