import tkinter as tk
from tkinter import ttk, messagebox
import json
import uuid
import os

DATA_FILE = "books.json"


class BookForm(tk.Toplevel):
    """Fereastră de formular pentru adăugarea sau editarea unei cărți."""

    def __init__(self, parent, book_data=None, on_save_callback=None):
        super().__init__(parent)
        self.transient(parent)  # Se afișează peste fereastra părinte
        self.grab_set()  # Modal: blochează interacțiunea cu fereastra părinte

        self.book_data = book_data
        self.on_save_callback = on_save_callback

        if self.book_data:
            self.title("Editare Carte")
            self.book_id = book_data.get("id")
        else:
            self.title("Adăugare Carte Nouă")
            self.book_id = str(uuid.uuid4())  # Generează un ID unic pentru cărțile noi

        self.geometry("400x250")
        self.resizable(False, False)

        self._setup_widgets()
        if self.book_data:
            self._load_book_data()

    def _setup_widgets(self):
        """Configurează widget-urile din formular."""
        form_frame = ttk.Frame(self, padding="10 10 10 10")
        form_frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(form_frame, text="Titlu:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.title_entry = ttk.Entry(form_frame, width=40)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Autor:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.author_entry = ttk.Entry(form_frame, width=40)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text="An publicație:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.year_entry = ttk.Entry(form_frame, width=40)
        self.year_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text="ISBN (Opțional):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.isbn_entry = ttk.Entry(form_frame, width=40)
        self.isbn_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=15, sticky="e")

        save_button = ttk.Button(button_frame, text="Salvează", command=self._on_save)
        save_button.pack(side=tk.LEFT, padx=5)

        cancel_button = ttk.Button(button_frame, text="Anulează", command=self.destroy)
        cancel_button.pack(side=tk.LEFT)

        form_frame.columnconfigure(1, weight=1)  # Permite câmpurilor de intrare să se extindă

    def _load_book_data(self):
        """Încarcă datele cărții în câmpurile formularului pentru editare."""
        self.title_entry.insert(0, self.book_data.get("title", ""))
        self.author_entry.insert(0, self.book_data.get("author", ""))
        self.year_entry.insert(0, str(self.book_data.get("year", "")))
        self.isbn_entry.insert(0, self.book_data.get("isbn", ""))

    def _on_save(self):
        """Validează și salvează datele cărții."""
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        year_str = self.year_entry.get().strip()
        isbn = self.isbn_entry.get().strip()

        if not title or not author or not year_str:
            messagebox.showerror("Eroare Validare", "Titlul, autorul și anul sunt obligatorii.", parent=self)
            return

        try:
            year = int(year_str)
            if year < 0 or year > 9999:  # Validare simplă pentru an
                raise ValueError("Anul trebuie să fie un număr valid.")
        except ValueError as e:
            messagebox.showerror("Eroare Validare", f"Anul publicației este invalid: {e}", parent=self)
            return

        new_book_data = {
            "id": self.book_id,
            "title": title,
            "author": author,
            "year": year,
            "isbn": isbn
        }

        if self.on_save_callback:
            self.on_save_callback(new_book_data)
        self.destroy()


class BookManagerApp:
    """Clasa principală a aplicației de gestionare a cărților."""

    def __init__(self, root_window):
        self.root = root_window
        self.root.title("📚 Catalog Cărți")
        self.root.geometry("800x500")
        self.root.minsize(600, 400)

        self.books_data = self._load_books()

        self._setup_main_ui()  # Aici este corecția relevantă
        self._refresh_book_list()

    def _load_books(self):
        """Încarcă cărțile din fișierul JSON."""
        if not os.path.exists(DATA_FILE):
            return []
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                else:
                    messagebox.showwarning("Atenție",
                                           "Formatul fișierului de date este incorect. Se va crea un fișier nou.",
                                           parent=self.root)
                    return []
        except (json.JSONDecodeError, FileNotFoundError):
            messagebox.showwarning("Atenție Date", "Fișierul de date este gol sau corupt. Se începe cu o listă goală.",
                                   parent=self.root)
            return []

    def _save_books(self):
        """Salvează lista curentă de cărți în fișierul JSON."""
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.books_data, f, indent=4, ensure_ascii=False)
        except IOError:
            messagebox.showerror("Eroare Salvare", "Nu s-au putut salva datele în fișier.", parent=self.root)

    def _setup_main_ui(self):
        """Configurează interfața grafică principală."""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        style.configure("TButton", padding=6, relief="flat", font=('Helvetica', 9))
        style.configure("Treeview", rowheight=25, font=('Helvetica', 9))

        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(expand=True, fill=tk.BOTH)

        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(pady=10, fill=tk.X)

        self.add_button = ttk.Button(controls_frame, text="➕ Adaugă Carte", command=self._add_book)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.edit_button = ttk.Button(controls_frame, text="✏️ Editează Selectat", command=self._edit_book,
                                      state=tk.DISABLED)
        self.edit_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = ttk.Button(controls_frame, text="❌ Șterge Selectat", command=self._delete_book,
                                        state=tk.DISABLED)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        list_frame = ttk.Frame(main_frame)
        list_frame.pack(expand=True, fill=tk.BOTH)

        # --- ÎNCEPUT CORECȚIE ---
        # Definește TOATE coloanele pe care le vor conține datele (inclusiv cele interne)
        self.all_data_columns = ("id", "title", "author", "year", "isbn")
        # Definește coloanele care vor fi VIZIBILE pentru utilizator
        self.display_columns_for_user = ("title", "author", "year", "isbn")

        self.book_tree = ttk.Treeview(
            list_frame,
            columns=self.all_data_columns,  # Folosește toate coloanele definite pentru date
            displaycolumns=self.display_columns_for_user,  # Specifică ce coloane sunt efectiv afișate
            show="headings",
            selectmode="browse"
        )

        # Setează antetele pentru TOATE coloanele (chiar dacă 'id' nu e vizibil, e bine să fie definit)
        self.book_tree.heading("id", text="ID Intern")
        self.book_tree.heading("title", text="Titlu")
        self.book_tree.heading("author", text="Autor")
        self.book_tree.heading("year", text="An")
        self.book_tree.heading("isbn", text="ISBN")

        # Configurează proprietățile coloanelor (lățime, aliniere etc.)
        self.book_tree.column("id", width=180, stretch=tk.NO, anchor="w")
        self.book_tree.column("title", width=250, anchor="w")
        self.book_tree.column("author", width=200, anchor="w")
        self.book_tree.column("year", width=80, anchor="center")
        self.book_tree.column("isbn", width=150, anchor="w")
        # Linia "self.book_tree.column("id", display=tk.FALSE)" a fost eliminată.
        # --- SFÂRȘIT CORECȚIE ---

        scrollbar_y = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.book_tree.yview)
        scrollbar_x = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.book_tree.xview)
        self.book_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.book_tree.pack(expand=True, fill=tk.BOTH)

        self.book_tree.bind("<<TreeviewSelect>>", self._on_book_select)
        self.book_tree.bind("<Double-1>", lambda event: self._edit_book() if self.book_tree.selection() else None)

    def _refresh_book_list(self):
        """Șterge și repopulează lista de cărți în Treeview."""
        self.edit_button.config(state=tk.DISABLED)
        self.delete_button.config(state=tk.DISABLED)

        for item in self.book_tree.get_children():
            self.book_tree.delete(item)
        for book in self.books_data:
            # Valorile trebuie să corespundă cu ordinea și numărul din self.all_data_columns
            self.book_tree.insert("", tk.END, iid=book["id"], values=(
                book["id"],
                book.get("title", "N/A"),
                book.get("author", "N/A"),
                book.get("year", "N/A"),
                book.get("isbn", "N/A")
            ))

    def _on_book_select(self, event=None):
        """Activează/dezactivează butoanele Edit/Delete la selectarea unei cărți."""
        selected_items = self.book_tree.selection()
        if selected_items:
            self.edit_button.config(state=tk.NORMAL)
            self.delete_button.config(state=tk.NORMAL)
        else:
            self.edit_button.config(state=tk.DISABLED)
            self.delete_button.config(state=tk.DISABLED)

    def _get_selected_book_data(self):
        """Returnează datele cărții selectate din Treeview."""
        selected_items = self.book_tree.selection()
        if not selected_items:
            return None

        selected_item_id = selected_items[0]

        for book in self.books_data:
            if book["id"] == selected_item_id:
                return book
        return None

    def _add_book(self):
        """Deschide fereastra de formular pentru adăugarea unei cărți noi."""
        BookForm(self.root, on_save_callback=self._save_new_book)

    def _save_new_book(self, book_data):
        """Adaugă o carte nouă în listă și salvează."""
        self.books_data.append(book_data)
        self._save_books()
        self._refresh_book_list()
        messagebox.showinfo("Succes", f"Cartea '{book_data['title']}' a fost adăugată.", parent=self.root)

    def _edit_book(self):
        """Deschide fereastra de formular pentru editarea cărții selectate."""
        selected_book = self._get_selected_book_data()
        if not selected_book:
            messagebox.showwarning("Nicio selecție", "Vă rugăm selectați o carte pentru a o edita.", parent=self.root)
            return
        BookForm(self.root, book_data=selected_book, on_save_callback=self._save_edited_book)

    def _save_edited_book(self, updated_book_data):
        """Actualizează o carte existentă în listă și salvează."""
        book_id_to_update = updated_book_data["id"]
        for i, book in enumerate(self.books_data):
            if book["id"] == book_id_to_update:
                self.books_data[i] = updated_book_data
                break
        self._save_books()
        self._refresh_book_list()
        messagebox.showinfo("Succes", f"Cartea '{updated_book_data['title']}' a fost actualizată.", parent=self.root)

    def _delete_book(self):
        """Șterge cartea selectată după confirmare."""
        selected_book = self._get_selected_book_data()
        if not selected_book:
            messagebox.showwarning("Nicio selecție", "Vă rugăm selectați o carte pentru a o șterge.", parent=self.root)
            return

        confirm = messagebox.askyesno(
            "Confirmare Ștergere",
            f"Sunteți sigur că doriți să ștergeți cartea '{selected_book['title']}'?",
            parent=self.root
        )
        if confirm:
            book_id_to_delete = selected_book["id"]
            self.books_data = [book for book in self.books_data if book["id"] != book_id_to_delete]
            self._save_books()
            self._refresh_book_list()
            messagebox.showinfo("Succes", f"Cartea '{selected_book['title']}' a fost ștearsă.", parent=self.root)


def main():
    """Funcția principală pentru a porni aplicația."""
    root = tk.Tk()
    app = BookManagerApp(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (app._save_books(), root.destroy()))
    root.mainloop()


if __name__ == "__main__":
    main()