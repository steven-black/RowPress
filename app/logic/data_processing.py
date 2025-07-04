import os
import datetime
from openpyxl.styles.numbers import is_date_format

import openpyxl
import subprocess
from docx import Document
from docx2pdf import convert
from concurrent.futures import ThreadPoolExecutor, as_completed
from openpyxl.styles.numbers import BUILTIN_FORMATS

from app.state.app_state import app_state


# Function to replace placeholder in paragraphs
def replace_placeholder_in_paragraphs(doc, placeholder, replacement):
    for paragraph in doc.paragraphs:
        if placeholder in paragraph.text:
            paragraph.text = paragraph.text.replace(placeholder, replacement)


# Function to replace placeholder in tables
def replace_placeholder_in_tables(doc, placeholder, replacement):
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                if placeholder in cell.text:
                    cell.text = cell.text.replace(placeholder, replacement)


# Function to replace placeholder in headers and footers
def replace_placeholder_in_headers_footers(doc, placeholder, replacement):
    for section in doc.sections:
        header = section.header
        for paragraph in header.paragraphs:
            if placeholder in paragraph.text:
                paragraph.text = paragraph.text.replace(placeholder, replacement)

        footer = section.footer
        for paragraph in footer.paragraphs:
            if placeholder in paragraph.text:
                paragraph.text = paragraph.text.replace(placeholder, replacement)


# Function to replace placeholder in footnotes and endnotes (does not currently work)
def replace_placeholder_in_notes(doc, placeholder, replacement):
    for footnote in doc.footnotes:
        if placeholder in footnote.text:
            footnote.text = footnote.text.replace(placeholder, replacement)
    for endnote in doc.endnotes:
        if placeholder in endnote.text:
            endnote.text = endnote.text.replace(placeholder, replacement)


# Function to replace placeholder in entire document
def replace_placeholder_in_document(doc, placeholder, replacement):
    replace_placeholder_in_paragraphs(doc, placeholder, replacement)
    replace_placeholder_in_tables(doc, placeholder, replacement)
    replace_placeholder_in_headers_footers(doc, placeholder, replacement)

# Testing a function to get formatting
def format_cell_value(cell):
    """
    Return a string that looks like Excel’s displayed value
    for the most common formats (dates, currency, percent, plain text).
    Extend as needed.
    """
    cell_value   = cell.value
    fmt = cell.number_format

    if cell_value is None:
        return ""

    # --- dates / datetimes --------------------------------------------------
    if isinstance(cell_value, (datetime.datetime, datetime.date)) or is_date_format(fmt):
        try:
            # customise the display format to taste
            return cell_value.strftime("%d %B %Y")        # 04 July 2025
        except Exception:
            return str(cell_value)

    # --- percentages --------------------------------------------------------
    if "%" in fmt:
        try:
            return f"{float(cell_value) * 100:.2f}%"
        except Exception:
            return str(cell_value)

    # --- simple currency or comma number ------------------------------------
    if any(sym in fmt for sym in ("$", "€", "£", "R", "¥")) or "#" in fmt:
        currency_symbol = next((sym for sym in ("R", "$", "€", "£", "¥") if sym in fmt), "")
        try:
            return f"{currency_symbol}{float(cell_value):,.2f}".replace(",", " ")            # R 1 234.56
        except Exception:
            return str(cell_value)

    # --- fallback -----------------------------------------------------------
    return str(cell_value)


def get_data_as_list(data):
    data_list = []
    for row in data.iter_rows(values_only=False):

        data_row = [format_cell_value(cell) for cell in row]
        data_list.append(data_row)

        # data_row = []
        # for cell in row:
        #     if (cell.value is not None) and (cell.value != ""):
        #         if isinstance(cell.value, str):
        #             data_row.append(cell.value.strip())
        #         else:
        #             data_row.append(str(cell.value).strip())
        #     else:
        #         data_row.append(cell.value)
        # data_list.append(data_row)

    return data_list


def is_empty(data):
    if (data is None) or (data == "None") or (data == ""):
        return True
    else:
        return False


def convert_to_pdf(output_folder_path, output_file_name):
    convert(os.path.join(output_folder_path, output_file_name))
    os.remove(os.path.join(output_folder_path, output_file_name))


def convert_all_docx_to_pdf(output_folder_path):
    if app_state.save_as_pdf.get():
        for file in os.listdir(output_folder_path):
            if file.endswith(".docx"):
                if app_state.stop_event.is_set():
                    print(f"{output_folder_path} PDF conversion skipped due to stop request.")
                    return
                print(f"Converting {file} to PDF...")
                convert_to_pdf(output_folder_path, file)


def process_row(row, template_file_path, doc_name):
    if app_state.stop_event.is_set():
        print("Processing stopped by user.")
        return

    # Open the Word document
    doc = Document(template_file_path)

    date = datetime.datetime.today()

    placeholder = "[DATE]"
    replacement = date.strftime("%d %B %Y")

    replace_placeholder_in_document(doc, placeholder, replacement)

    personalized_name_list = [row[i] for i in app_state.get_naming_columns()]
    personalized_name = ""

    for i, word in enumerate(personalized_name_list):
        if is_empty(word):
            word = "N/A"
        
        personalized_name += word
        if i < len(personalized_name_list) - 1:
            personalized_name += " "

    print(f"Processing document: {personalized_name}")

    for placeholder_and_replacement_column in app_state.get_placeholders_and_replacement_columns():

        placeholder = placeholder_and_replacement_column[0]
        replacement_column = placeholder_and_replacement_column[1]
        replacement = row[replacement_column]

        if is_empty(replacement):
            replacement = "N/A"
        
        print(f"Replacing placeholder '{placeholder}' with '{replacement}' in document: {personalized_name}")
        replace_placeholder_in_document(doc, placeholder, replacement)

        # Save the modified document
        print(f"Saving document: {personalized_name}")
        os.makedirs(app_state.output_folder_path, exist_ok=True)

    doc.save(f"{app_state.output_folder_path}\\{personalized_name}_{doc_name}_{date.year}.docx")


def toggle_processing_state():
    app_state.is_processing = not app_state.is_processing
    if app_state.is_processing:
        app_state.propogate_template_button.configure(state="disabled")
        app_state.stop_processing_button.configure(state="normal")
    elif not app_state.is_processing:
        app_state.propogate_template_button.configure(state="normal")
        app_state.stop_processing_button.configure(state="disabled")


def propogate_template(excel_file_path, template_file_path):
    app_state.stop_event.clear()
    toggle_processing_state()

    wb = openpyxl.load_workbook(excel_file_path, data_only=True, read_only=True)
    
    excel_sheet_name = app_state.get_sheet_name()
    excel_sheet = get_data_as_list(wb[excel_sheet_name])
    doc_name = app_state.get_document_name()

    # Implemnent multithreading for processing rows
    max_workers = max(1, os.cpu_count() - 1)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for row in excel_sheet:
            futures.append(executor.submit(process_row, row, template_file_path, doc_name))
        
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error processing row: {e}")

    # for row in excel_sheet:
    #     try:
    #         process_row(row, template_file_path, doc_name)
    #     except Exception as e:
    #         print(f"Error processing row {row}: {e}")
    
    if not app_state.stop_event.is_set():
        convert_all_docx_to_pdf(app_state.output_folder_path)
    else:
        print("PDF conversion skipped due to stop request.")


    toggle_processing_state()
    print("Template propagation completed.")