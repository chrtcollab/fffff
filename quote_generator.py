
import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime

# Предопределённые цитаты
PREDEFINED_QUOTES = [
    {"text": "Будь изменением, которое ты хочешь увидеть в мире.", "author": "Махатма Ганди", "topic": "Мотивация"},
    {"text": "Жизнь — это то, что с тобой происходит, пока ты строишь планы.", "author": "Джон Леннон", "topic": "Жизнь"},
    {"text": "Воображение важнее знания.", "author": "Альберт Эйнштейн", "topic": "Наука"},
    {"text": "Сложнее всего начать действовать, остальное зависит от упорства.", "author": "Пауло Коэльо", "topic": "Мотивация"},
    {"text": "Кто не рискует, тот не пьёт шампанское.", "author": "Народная мудрость", "topic": "Риск"},
    {"text": "Всё, что нас не убивает, делает нас сильнее.", "author": "Фридрих Ницше", "topic": "Жизнь"},
]

HISTORY_FILE = "quotes.json"

class QuoteGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Quote Generator")
        self.root.geometry("700x500")

        self.history = self.load_history()
        self.filtered_history = self.history[:]

        # --- Виджеты ---
        # Текущая цитата
        self.quote_label = tk.Label(root, text="Нажмите кнопку для генерации", wraplength=600, font=("Arial", 12, "italic"))
        self.quote_label.pack(pady=20)

        self.author_label = tk.Label(root, text="", font=("Arial", 10))
        self.author_label.pack()

        # Кнопка генерации
        self.generate_btn = tk.Button(root, text="Сгенерировать цитату", command=self.generate_quote)
        self.generate_btn.pack(pady=10)

        # --- Фильтры ---
        filter_frame = tk.Frame(root)
        filter_frame.pack(pady=10)

        tk.Label(filter_frame, text="Фильтр по автору:").grid(row=0, column=0, padx=5)
        self.author_filter_entry = tk.Entry(filter_frame, width=20)
        self.author_filter_entry.grid(row=0, column=1, padx=5)
        self.author_filter_entry.bind("<KeyRelease>", self.apply_filters)

        tk.Label(filter_frame, text="Фильтр по теме:").grid(row=0, column=2, padx=5)
        self.topic_filter_entry = tk.Entry(filter_frame, width=20)
        self.topic_filter_entry.grid(row=0, column=3, padx=5)
        self.topic_filter_entry.bind("<KeyRelease>", self.apply_filters)

        # --- Таблица истории ---
        self.tree = ttk.Treeview(root, columns=("text", "author", "topic", "date"), show="headings")
        self.tree.heading("text", text="Цитата")
        self.tree.heading("author", text="Автор")
        self.tree.heading("topic", text="Тема")
        self.tree.heading("date", text="Дата")
        self.tree.column("text", width=300)
        self.tree.column("author", width=120)
        self.tree.column("topic", width=100)
        self.tree.column("date", width=150)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- Кнопка добавления новой цитаты ---
        add_frame = tk.Frame(root)
        add_frame.pack(pady=5)
        tk.Label(add_frame, text="Новая цитата:").grid(row=0, column=0)
        self.new_quote_entry = tk.Entry(add_frame, width=40)
        self.new_quote_entry.grid(row=0, column=1)
        tk.Label(add_frame, text="Автор:").grid(row=1, column=0)
        self.new_author_entry = tk.Entry(add_frame, width=40)
        self.new_author_entry.grid(row=1, column=1)
        tk.Label(add_frame, text="Тема:").grid(row=2, column=0)
        self.new_topic_entry = tk.Entry(add_frame, width=40)
        self.new_topic_entry.grid(row=2, column=1)

        self.add_btn = tk.Button(root, text="Добавить цитату", command=self.add_new_quote)
        self.add_btn.pack(pady=5)

        self.refresh_history_display()

    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_history(self):
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:

    json.dump(self.history, f, ensure_ascii=False, indent=2)

    def generate_quote(self):
        # Выбираем случайную цитату из предопределённых
        chosen = random.choice(PREDEFINED_QUOTES)
        quote_entry = {
            "text": chosen["text"],
            "author": chosen["author"],
            "topic": chosen["topic"],
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.history.append(quote_entry)
        self.save_history()
        self.apply_filters()  # обновляем фильтры и отображение

        self.quote_label.config(text=f"“{chosen['text']}”")
        self.author_label.config(text=f"— {chosen['author']} (Тема: {chosen['topic']})")

    def add_new_quote(self):
        text = self.new_quote_entry.get().strip()
        author = self.new_author_entry.get().strip()
        topic = self.new_topic_entry.get().strip()

        # Проверка корректности ввода
        if not text or not author or not topic:
            messagebox.showwarning("Ошибка ввода", "Все поля (цитата, автор, тема) должны быть заполнены!")
            return

        new_quote = {
            "text": text,
            "author": author,
            "topic": topic,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.history.append(new_quote)
        self.save_history()
        self.apply_filters()

        # Очистка полей
        self.new_quote_entry.delete(0, tk.END)
        self.new_author_entry.delete(0, tk.END)
        self.new_topic_entry.delete(0, tk.END)

        messagebox.showinfo("Успех", "Цитата добавлена в историю!")

    def apply_filters(self, event=None):
        author_filter = self.author_filter_entry.get().strip().lower()
        topic_filter = self.topic_filter_entry.get().strip().lower()

        filtered = []
        for q in self.history:
            if author_filter and author_filter not in q["author"].lower():
                continue
            if topic_filter and topic_filter not in q["topic"].lower():
                continue
            filtered.append(q)

        self.filtered_history = filtered
        self.refresh_history_display()

    def refresh_history_display(self):
        # Очистка таблицы
        for row in self.tree.get_children():
            self.tree.delete(row)

        for q in self.filtered_history:
            self.tree.insert("", tk.END, values=(q["text"], q["author"], q["topic"], q["date"]))

    if __name__ == "__main__":
        root = tk.Tk()
        app = QuoteGeneratorApp(root)
        root.mainloop()