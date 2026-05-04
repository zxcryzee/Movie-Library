import json
import os
from tkinter import *
from tkinter import ttk, messagebox

def main():
    root = Tk()
    root.title("Movie Library - Личная кинотека")
    root.geometry("900x500")
    root.resizable(True, True)

    movies = []
    filtered_movies = []
    data_file = "movies.json"

    if os.path.exists(data_file):
        try:
            with open(data_file, "r", encoding="utf-8") as f:
                movies = json.load(f)
        except:
            movies = []
    else:
        movies = []

    input_frame = LabelFrame(root, text="Добавление фильма", padx=10, pady=10)
    input_frame.pack(fill="x", padx=10, pady=5)

    entries = {}

    labels = ["Название:", "Жанр:", "Год выпуска:", "Рейтинг (0-10):"]
    for i, text in enumerate(labels):
        Label(input_frame, text=text).grid(row=i, column=0, sticky="e", padx=5, pady=5)
        entry = Entry(input_frame, width=30)
        entry.grid(row=i, column=1, padx=5, pady=5)
        entries[text[:-1]] = entry

    filter_frame = LabelFrame(root, text="Фильтрация", padx=10, pady=10)
    filter_frame.pack(fill="x", padx=10, pady=5)

    Label(filter_frame, text="Фильтр по жанру:").grid(row=0, column=0, padx=5)
    genre_filter_entry = Entry(filter_frame, width=20)
    genre_filter_entry.grid(row=0, column=1, padx=5)

    Label(filter_frame, text="Фильтр по году:").grid(row=0, column=2, padx=5)
    year_filter_entry = Entry(filter_frame, width=10)
    year_filter_entry.grid(row=0, column=3, padx=5)

    table_frame = Frame(root)
    table_frame.pack(fill="both", expand=True, padx=10, pady=5)

    columns = ("ID", "Название", "Жанр", "Год", "Рейтинг")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150 if col != "ID" else 40)

    scrollbar = Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    info_label = Label(root, text=f"Всего фильмов: {len(movies)}", fg="blue")
    info_label.pack(pady=5)

    def save_data():
        try:
            with open(data_file, "w", encoding="utf-8") as f:
                json.dump(movies, f, ensure_ascii=False, indent=4)
        except:
            pass

    def update_table(movies_list):
        for row in tree.get_children():
            tree.delete(row)
        for movie in movies_list:
            tree.insert("", END, values=(
                movie["id"],
                movie["title"],
                movie["genre"],
                movie["year"],
                movie["rating"]
            ))

    def refresh_table():
        update_table(movies)
        info_label.config(text=f"Всего фильмов: {len(movies)}")

    def clear_entries():
        for entry in entries.values():
            entry.delete(0, END)

    def validate_and_add():
        title = entries["Название"].get().strip()
        genre = entries["Жанр"].get().strip()
        year_str = entries["Год выпуска"].get().strip()
        rating_str = entries["Рейтинг (0-10)"].get().strip()

        if not title or not genre:
            messagebox.showerror("Ошибка", "Название и жанр не могут быть пустыми")
            return

        try:
            year_int = int(year_str)
            if year_int < 1888 or year_int > 2030:
                messagebox.showerror("Ошибка", "Год должен быть между 1888 и 2030")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть числом")
            return

        try:
            rating_float = float(rating_str)
            if rating_float < 0 or rating_float > 10:
                messagebox.showerror("Ошибка", "Рейтинг должен быть от 0 до 10")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом")
            return

        movie = {
            "id": len(movies) + 1,
            "title": title,
            "genre": genre,
            "year": year_int,
            "rating": rating_float
        }
        movies.append(movie)
        save_data()
        clear_entries()
        refresh_table()
        messagebox.showinfo("Успех", f"Фильм '{title}' добавлен!")

    def apply_filter():
        genre_filter = genre_filter_entry.get().strip().lower()
        year_filter = year_filter_entry.get().strip()
        filtered = movies.copy()

        if genre_filter:
            filtered = [m for m in filtered if genre_filter in m["genre"].lower()]

        if year_filter:
            try:
                year_int = int(year_filter)
                filtered = [m for m in filtered if m["year"] == year_int]
            except ValueError:
                messagebox.showerror("Ошибка", "Год фильтрации должен быть числом")
                return

        update_table(filtered)
        info_label.config(text=f"Показано: {len(filtered)} из {len(movies)} фильмов")

    def reset_filter():
        genre_filter_entry.delete(0, END)
        year_filter_entry.delete(0, END)
        update_table(movies)
        info_label.config(text=f"Всего фильмов: {len(movies)}")

    add_btn = Button(input_frame, text="Добавить фильм", command=validate_and_add, bg="lightgreen")
    add_btn.grid(row=4, column=0, columnspan=2, pady=10)

    filter_btn = Button(filter_frame, text="Применить фильтр", command=apply_filter, bg="lightblue")
    filter_btn.grid(row=0, column=4, padx=10)

    reset_btn = Button(filter_frame, text="Сбросить фильтр", command=reset_filter)
    reset_btn.grid(row=0, column=5, padx=5)

    refresh_table()
    root.mainloop()

if __name__ == "__main__":
    main()
