import customtkinter as ctk
from tkinter import filedialog, messagebox
from app.state.app_state import app_state


def add_frame(master, pady=5, padx=5):
    frame = ctk.CTkFrame(master=master)
    frame.pack(pady=pady, padx=padx)
    return frame

def add_label(master, text, pady=5, padx=5):
    label = ctk.CTkLabel(master=master, text=text)
    label.pack(pady=pady, padx=padx)
    return label

def add_entry(master, width=100, pady=5, padx=5):
    entry = ctk.CTkEntry(master=master, width=width)
    entry.pack(pady=pady, padx=padx)
    return entry


def remove_placeholder_and_replacement_group(group):
    group.destroy()
    app_state.placeholders_and_replacements_groups.remove(group)
    
    # if app_state.current_column > 0:
    #     app_state.current_column -= 1

    # if app_state.current_column == 0:
    #     app_state.current_column = app_state.get_max_columns()
    #     app_state.current_row -= 1
    
    # for placeholder_and_replacement_group in app_state.placeholders_and_replacements_groups:
    #     placeholder_and_replacement_group.grid(row=app_state.current_row, column=app_state.current_column, sticky="nesw")
    #     app_state.current_column += 1
    #     if app_state.current_column >= app_state.get_max_columns():
    #         app_state.current_column = 0
    #         app_state.current_row += 1


def add_placeholder_and_replacement(master):
        placeholder_and_replacement_group = ctk.CTkFrame(master=master)
        placeholder_and_replacement_group.grid(pady=2, padx=2, row=app_state.current_row, column=app_state.current_column, sticky="nesw")
        app_state.current_column += 1
        if app_state.current_column >= app_state.get_max_columns():
            app_state.current_column = 0
            app_state.current_row += 1
        

        placeholder_label = ctk.CTkLabel(master=placeholder_and_replacement_group, text="Placeholder:")
        placeholder_label.grid(row=0, column=0)
        placeholder_entry = ctk.CTkEntry(master=placeholder_and_replacement_group, width=100)
        placeholder_entry.grid(row=1, column=0)

        replacement_label = ctk.CTkLabel(master=placeholder_and_replacement_group, text="Replacement Column:")
        replacement_label.grid(row=2, column=0)
        replacement_entry = ctk.CTkEntry(master=placeholder_and_replacement_group, width=100)
        replacement_entry.grid(row=3, column=0)

        remove_button = ctk.CTkButton(master=placeholder_and_replacement_group, text="Remove", command=lambda: remove_placeholder_and_replacement_group(placeholder_and_replacement_group))
        remove_button.grid(row=4, column=0)

        placeholder_and_replacement = []
        placeholder_and_replacement.append(placeholder_entry)
        placeholder_and_replacement.append(replacement_entry)

        app_state.placeholders_and_replacements_groups.append(placeholder_and_replacement)

        app_state.root.update_idletasks()