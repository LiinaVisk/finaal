import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
from datetime import datetime

class View(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Failiotsing")
        self.geometry("800x500")
        self.configure(bg="lime")
        self.selected_file_label = tk.Label(self, text="", bg="yellow")
        self.selected_file_label.pack(pady=5)
        self.btn_open_file = tk.Button(self, text="Ava fail", command=self.open_file_dialog, bg="yellow")
        self.btn_open_file.pack(pady=5)
        self.entry_search = tk.Entry(self, width=50)
        self.entry_search.pack(pady=10)
        self.entry_search.insert(0, "Sisestage otsingusõna (min 3 tähemärki)")
        self.entry_search.config(fg="black")
        self.entry_search.bind("<FocusIn>", self.on_entry_click)
        self.entry_search.bind("<FocusOut>", self.on_focus_out)
        self.btn_search = tk.Button(self, text="Otsi", command=self.search, bg="yellow")
        self.btn_search.pack(pady=5)
        self.tree = ttk.Treeview(self, columns=("Nr", "Eesnimi", "Perenimi", "Sugu", "Sünniaeg", "Surnud", "Asula", "TÄ%Ä%p", "Maakond"))
        self.tree.heading("#0", text="Nr")
        self.tree.heading("#1", text="Eesnimi")
        self.tree.heading("#2", text="Perenimi")
        self.tree.heading("#3", text="Sugu")
        self.tree.heading("#4", text="Sünniaeg")
        self.tree.heading("#5", text="Surnud")
        self.tree.heading("#6", text="Asula")
        self.tree.heading("#7", text="TÄ%Ä%p")
        self.tree.heading("#8", text="Maakond")
        self.tree.pack(fill="both", expand=True)
        self.status_label = tk.Label(self, text="", bg="yellow")
        self.status_label.pack(pady=5)
        # Peidame Treeview alguses
        self.tree.pack_forget()

    def on_entry_click(self, event):
        """Kui sisenetakse otsingu välja, kustutatakse märge."""
        if self.entry_search.get() == "Sisestage otsingusõna (min 3 tähemärki)":
            self.entry_search.delete(0, "end")
            self.entry_search.config(fg="black")

    def on_focus_out(self, event):
        """Kui fookus lahkub otsingu väljalt ja pole sisestatud midagi, lisatakse märge tagasi."""
        if not self.entry_search.get():
            self.entry_search.insert(0, "Sisestage otsingusõna (min 3 tähemärki)")
            self.entry_search.config(fg="grey")

    def open_file_dialog(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])
        if file_path:
            print("Valitud fail:", file_path)
            self.selected_file_label.config(text="Valitud fail: " + file_path)
            self.controller.open_file_dialog(file_path)

    def search(self):
        search_text = self.entry_search.get().strip()
        if len(search_text) < 3:
            messagebox.showwarning("Hoiatus", "Otsingutulemused puuduvad. Otsing peab olema vähemalt 3 tähemärki pikk.")
        else:
            results, column_names = self.controller.search(search_text)
            self.show_results(results, column_names)

    def show_results(self, results, column_names):
        # Kustutame kõik eelnevalt kuvatud andmed
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Kuvame uued andmed
        for i, row in enumerate(results, start=1):
            self.tree.insert("", "end", values=row, text=str(i))

        # Kuvame veeru nimed
        for i, col_name in enumerate(column_names):
            self.tree.heading(f"#{i}", text=col_name)

        # Kuvame päise teksti ainult siis, kui leiti otsingutulemused
        if results:
            self.status_label.config(text="Otsingutulemused:")
            # Näitame Treeview, kui otsingutulemused on olemas
            self.tree.pack(fill="both", expand=True)
        else:
            messagebox.showinfo("Teade", "Otsingutulemusi ei leitud.")
            # Peidame Treeview, kui otsingutulemusi ei leitud
            self.tree.pack_forget()
