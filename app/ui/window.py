import customtkinter as ctk
import threading
from tkinter import filedialog, messagebox
from app.state.app_state import app_state
from app.logic.data_processing import *
from app.logic.ui_logic import *


def open_excel_file():
    file_path = filedialog.askopenfilename(
        title="Select Excel File",
        filetypes=[("Excel files", "*.xlsx *.xls")]
    )
    if file_path:
        print(f"Excel file selected: {file_path}")
        app_state.excel_file_path = file_path


def open_word_file():
    file_path = filedialog.askopenfilename(
        title="Select Word Template Document",
        filetypes=[("Word files", "*.docx *.doc")]
    )
    if file_path:
        print(f"Word document selected: {file_path}")
        app_state.word_template_path = file_path


def call_propogate_template():
    propogate_template(app_state.excel_file_path, app_state.excel_sheet_name, app_state.word_template_path)


def launch_ui():

    app_state.root = ctk.CTk()
    app_state.root.title("Xemplate")
    app_state.root.protocol("WM_DELETE_WINDOW", app_state.root.quit)
    screen_height = app_state.root.winfo_screenheight()
    screen_width = app_state.root.winfo_screenwidth()
    app_state.root.geometry(f"{screen_height}x{int(screen_width/2)}+0+0")

    # Groups
    app_state.left_group = ctk.CTkFrame(master=app_state.root)
    app_state.left_group.grid(pady=5, column=0, row=0, sticky="nsew")
    app_state.right_group = ctk.CTkFrame(master=app_state.root)
    app_state.right_group.grid(pady=5, column=1, row=0, sticky="nsew")

    # Left Group Elements
    excel_upload_button = ctk.CTkButton(master=app_state.left_group, text="Upload Excel Data", command=open_excel_file)
    excel_upload_button.grid(pady=5, column=0, row=0, sticky="nsew")

    document_name_label = ctk.CTkLabel(master=app_state.left_group, text="Document Name:")
    document_name_label.grid(pady=5, column=0, row=1, sticky="nsew")
    app_state.document_name_entry = ctk.CTkEntry(master=app_state.left_group, width=100)
    app_state.document_name_entry.grid(pady=5, column=0, row=2, sticky="nsew")

    sheet_name_label = ctk.CTkLabel(master=app_state.left_group, text="Name of Sheet to use:")
    sheet_name_label.grid(pady=5, column=0, row=3, sticky="nsew")
    app_state.sheet_name_entry = ctk.CTkEntry(master=app_state.left_group, width=100)
    app_state.sheet_name_entry.grid(pady=5, column=0, row=4, sticky="nsew")

    word_upload_button = ctk.CTkButton(master=app_state.left_group, text="Upload Word Template", command=open_word_file)
    word_upload_button.grid(pady=5, column=0, row=5, sticky="nsew")

    output_file_name_label = ctk.CTkLabel(master=app_state.left_group, text="Columns to use for naming: (A; B; AA; AB)")
    output_file_name_label.grid(pady=5, column=0, row=6, sticky="nsew")
    app_state.naming_columns_entry = ctk.CTkEntry(master=app_state.left_group, width=100)
    app_state.naming_columns_entry.grid(pady=5, column=0, row=7, sticky="nsew")

    add_placeholder_and_replacement_button = ctk.CTkButton(master=app_state.left_group, text="Add Placeholder and Replacement", command=lambda: add_placeholder_and_replacement(app_state.right_group))
    add_placeholder_and_replacement_button.grid(pady=5, column=0, row=8, sticky="nsew")

    app_state.save_as_pdf = ctk.BooleanVar(value=True)
    save_as_pdf_checkbox = ctk.CTkCheckBox(master=app_state.left_group, text="Save as PDF", variable=app_state.save_as_pdf)
    save_as_pdf_checkbox.grid(pady=5, column=0, row=9, sticky="nsew")

    app_state.propogate_template_button = ctk.CTkButton(master=app_state.left_group, text="Propogate Template", command=lambda: threading.Thread(target=propogate_template, args=(app_state.excel_file_path, app_state.word_template_path), daemon=True).start())
    app_state.propogate_template_button.grid(pady=5, column=0, row=10, sticky="nsew")

    app_state.stop_processing_button = ctk.CTkButton(master=app_state.left_group, text="Stop", command=app_state.stop_event.set)
    app_state.stop_processing_button.grid(pady=5, column=0, row=11, sticky="nsew")
    app_state.stop_processing_button.configure(state="disabled")

    # test_button = ctk.CTkButton(master=app_state.left_group, text="Test", command=app_state.get_placeholders_and_replacement_columns)
    # test_button.grid(pady=5, column=0, row=12, sticky="nsew")

    app_state.root.mainloop()
