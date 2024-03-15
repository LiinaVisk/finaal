import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
from datetime import datetime

class Controller:
    def __init__(self):
        self.current_file = None
        self.file_content = []  # Salvestame faili sisu muutujasse
        self.column_widths = []  # Salvestame tulba laiused

    def open_file_dialog(self, file_path):
        if file_path:
            print("Valitud fail:", file_path)
            self.read_csv_file(file_path)
            self.current_file = file_path

    def read_csv_file(self, file_path):
        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=';')
                self.file_content = list(reader)  # Salvestame faili sisu muutujasse
                column_names = next(reader)
                return self.file_content, column_names
        except Exception as e:
            print("Viga faili lugemisel:", e)

    def search(self, search_text):
        # Otsimismeetod vastavalt kasutaja sisestatud otsingule
        results = []
        column_names = []
        for row in self.file_content:
            formatted_row = [self.format_entry(entry) for entry in row]
            for item in formatted_row:
                if search_text.lower() in item.lower():
                    results.append(formatted_row)
                    break
        # Tagastame nii otsingutulemused kui ka veergude nimed
        return results, column_names

    def format_entry(self, entry):
        # Vormindab sissekande vastavalt vajadustele
        try:
            # Kui see on kuupäev, vorminda kuupäev
            date_format = "%d.%m.%Y"
            return datetime.strptime(entry, date_format).strftime(date_format)
        except ValueError:
            pass

        try:
            # Kui see on kellaaeg, vorminda kellaaeg
            time_format = "%H:%M"
            return datetime.strptime(entry, time_format).strftime(time_format)
        except ValueError:
            pass

        # Asendab semikoolonid tühikutega
        return entry.replace(';', ' ')