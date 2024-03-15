import csv
from tkinter import filedialog
from datetime import datetime
from View import View


class Controller:
    def __init__(self):
        self.view = View(self)
        self.current_file = None  # Salvestab praeguse valitud faili tee
        self.file_content = []  # Salvestab avatud faili sisu

    def run(self):
        self.view.mainloop()

    def open_file_dialog(self):
        # Dialoogiaken faili avamiseks
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])
        if file_path:
            print("Valitud fail:", file_path)
            self.read_csv_file(file_path)
            self.current_file = file_path  # Salvestab praeguse valitud faili tee
            self.view.update_status(file_path)  # Uuendab faili nime kuvamist

    def read_csv_file(self, file_path):
        # Loeme avatud CSV-faili ja salvestame selle sisu muutujasse
        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                self.file_content = list(reader)
        except Exception as e:
            print("Viga faili lugemisel:", e)

    def search(self):
        # Otsingu teostamine
        search_text = self.view.entry_search.get().lower()  # Saame otsingu teksti ja muudame selle väiketähtedeks
        self.view.text_results.delete("1.0", "end")  # Tühjendame tekstiakna

        # Kui otsing on tühi, tagastame
        if not search_text.strip():
            return

        # Otsime faili sisust otsingusõna ja kuvame need tulemused
        for row in self.file_content:
            formatted_row = [self.format_entry(entry) for entry in row]
            for item in formatted_row:
                if search_text in item.lower():
                    self.view.text_results.insert("end", ', '.join(formatted_row) + '\n')
                    break

    def format_entry(self, entry):
        # Vormindab sissekande vastavalt vajadustele
        try:
            # Kui see on kuupäev, vorminda kuupäev
            date_format = "%d.%m.%Y"
            datetime.strptime(entry, date_format)
            return datetime.strftime(datetime.strptime(entry, date_format), date_format)
        except ValueError:
            pass

        try:
            # Kui see on kellaaeg, vorminda kellaaeg
            time_format = "%H:%M"
            datetime.strptime(entry, time_format)
            return datetime.strftime(datetime.strptime(entry, time_format), time_format)
        except ValueError:
            pass

        # Asendab semikoolonid tühikutega
        return entry.replace(';', ' ')



