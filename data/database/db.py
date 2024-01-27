from sqlite3 import Row
from typing import Iterable
import aiosqlite
import datetime
from os import system
import pytz

from units.register_changes import make_lower

path = "data/database/database.db"


async def check_db():
    """
    Проверяет существует ли база данных и создает ее, если она не существует
    """

    system("cls")
    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        try:
            await cursor.execute("SELECT * FROM users")
            print("----\tDatabase was found\t----")
        except aiosqlite.OperationalError:
            print("----\tDatabase not found\t----")
            print("----\tCreating database\t----")
            await cursor.execute("""CREATE TABLE "users" (
"user_id"	INTEGER,
"reg_date"	TEXT)""")
            await cursor.execute("""CREATE TABLE "authors" (
"id"	INTEGER UNIQUE,
"author"	TEXT NOT NULL,
PRIMARY KEY("id" AUTOINCREMENT))""")
            await cursor.execute("""CREATE TABLE "genres" (
"id"	INTEGER UNIQUE,
"genre"	TEXT NOT NULL,
PRIMARY KEY("id" AUTOINCREMENT)
)""")
            await cursor.execute("""CREATE TABLE "books" (
"id"	INTEGER UNIQUE,
"name"	TEXT NOT NULL,
"author_id"	INTEGER NOT NULL,
"genre_id"	INTEGER NOT NULL,
"description"	TEXT,
FOREIGN KEY("genre_id") REFERENCES "genres"("id"),
FOREIGN KEY("author_id") REFERENCES "authors"("id"),
PRIMARY KEY("id" AUTOINCREMENT)
)""")
            await db.commit()
            print("----\tDatabase created\t----")
        print(f"----\t{get_now_time()}\t----")


def get_now_date() -> str:
    """
    Возвращает текущую дату

    Returns:
        str: текущая дата в формате dd.mm.yyyy
    """

    dt = datetime.datetime.now()
    tz = pytz.timezone("Europe/Kiev")
    mess_date = tz.normalize(dt.astimezone(tz))
    format_date = mess_date.strftime("%d.%m.%Y")
    return format_date


def get_now_time() -> str:
    """
    Возвращает текущее время

    Returns:
        str: текущее время в формате dd.mm.yyyy HH:MM
    """

    dt = datetime.datetime.now()
    tz = pytz.timezone("Europe/Kiev")
    mess_date = tz.normalize(dt.astimezone(tz))
    format_date = mess_date.strftime("%d.%m.%Y %H:%M")
    return format_date


async def get_user_exists(user_id) -> bool:
    """
    Проверяет существует ли пользователь в базе данных

    Args:
        user_id (int): id пользователя

    Returns:
        bool: True - пользователь существует в базе данных, False - пользователь не существует в базе данных
    """

    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute(f"SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = await cursor.fetchone()
        if user is None:
            return False
        else:
            return True


async def add_user(user_id):
    """
    Добавляет пользователя в базу данных

    Args:
        user_id (int): id пользователя
    """

    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute(f"INSERT INTO users (user_id, reg_date) VALUES (?, ?)", (user_id, get_now_date(),))
        await db.commit()


async def get_all_reg_date() -> Iterable[Row] | None:
    """
    Возвращает список дат регистрации пользователей

    Returns:
        Iterable[Row]: список дат регистрации пользователей
    """

    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute(f"SELECT reg_date FROM users")
        dates = await cursor.fetchall()
        return dates


async def get_all_users_id() -> Iterable[Row] | None:
    """
    Возвращает список id пользователей

    Returns:
        Iterable[Row]: список id пользователей
    """

    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute(f"SELECT user_id FROM users")
        users = await cursor.fetchall()
        return users


async def get_all_genres() -> Iterable[Row] | None:
    """
    Возвращает список жанров

    Returns:
        Iterable[Row]: список жанров
    """

    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute("SELECT * FROM genres")
        genres = await cursor.fetchall()
        return genres


async def add_genre(genre: str) -> int:
    """
    Добавляет жанр в базу данных

    Args:
        genre (str): жанр

    Returns:
        int: id жанра
    """

    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute("INSERT INTO genres (genre) VALUES (?)", (genre,))
        await db.commit()
        await cursor.execute("SELECT * FROM genres WHERE genre = ?", (genre,))
        genre = await cursor.fetchone()
        return genre[0]


async def get_genre_by_id(genre_id: int) -> Row | None:
    """
    Возвращает жанр по id

    Args:
        genre_id (int): id жанра

    Returns:
        Row: жанр
    """

    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute("SELECT * FROM genres WHERE id = ?", (genre_id,))
        genre = await cursor.fetchone()
        return genre


async def get_all_authors() -> Iterable[Row] | None:
    """
    Возвращает список авторов

    Returns:
        Iterable[Row]: список авторов
    """

    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute("SELECT * FROM authors")
        authors = await cursor.fetchall()
        return authors


async def add_author(author: str) -> int:
    """
    Добавляет автора в базу данных

    Args:
        author (str): автор

    Returns:
        int: id автора
    """

    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute("INSERT INTO authors (author) VALUES (?)", (author,))
        await db.commit()
        await cursor.execute("SELECT * FROM authors WHERE author = ?", (author,))
        author = await cursor.fetchone()
        return author[0]


async def get_author_by_id(author_id: int) -> Row | None:
    """
    Возвращает автора по id

    Args:
        author_id (int): id автора

    Returns:
        Row: автор
    """

    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute("SELECT * FROM authors WHERE id = ?", (author_id,))
        author = await cursor.fetchone()
        return author


async def get_all_books() -> Iterable[Row] | None:
    """
    Возвращает список книг

    Returns:
        Iterable[Row]: список книг
    """

    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute("""SELECT books.id, books.name, authors.author, genres.genre, books.description
FROM ((books
INNER JOIN authors ON books.author_id = authors.id)
INNER JOIN genres ON books.genre_id = genres.id)
""")
        books = await cursor.fetchall()
        return books


async def get_book_by_id(book_id: int) -> Row | None:
    """
    Возвращает книгу по id

    Args:
        book_id (int): id книги

    Returns:
        Row: книга
    """

    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute("""SELECT books.id, books.name, authors.author, genres.genre, books.description
FROM ((books
INNER JOIN authors ON books.author_id = authors.id)
INNER JOIN genres ON books.genre_id = genres.id)
WHERE books.id = ?
""", (book_id,))
        book = await cursor.fetchone()
        return book


async def delete_book(book_id: int):
    """
    Удаляет книгу из базы данных

    Args:
        book_id (int): id книги
    """

    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
        await db.commit()


async def add_book(name: str, author_id: int, genre_id: int, description: str):
    """
    Добавляет книгу в базу данных

    Args:
        name (str): название книги
        author_id (int): id автора
        genre_id (int): id жанра
        description (str): описание книги
    """

    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute("INSERT INTO books (name, author_id, genre_id, description) VALUES (?, ?, ?, ?)",
                             (name, author_id, genre_id, description,))
        await db.commit()


async def get_books_by_query(name: str) -> Iterable[Row] | None:
    """
    Возвращает список книг по запросу

    Args:
        name (str): запрос

    Returns:
        Iterable[Row]: список книг
    """

    async with aiosqlite.connect(path) as db:
        await db.create_function("mylower", 1, make_lower)
        cursor = await db.cursor()
        await cursor.execute("""SELECT books.id, books.name, authors.author, genres.genre, books.description
FROM ((books
INNER JOIN authors ON books.author_id = authors.id)
INNER JOIN genres ON books.genre_id = genres.id)
WHERE mylower(books.name) LIKE ? OR mylower(authors.author) LIKE ?
""", (f"%{name.lower()}%", f"%{name.lower()}%",))
        books = await cursor.fetchall()
        return books


async def get_books_by_genre_id(genre_id: int) -> Iterable[Row] | None:
    """
    Возвращает список книг по id жанра

    Args:
        genre_id (int): id жанра

    Returns:
        Iterable[Row]: список книг
    """

    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute("""SELECT books.id, books.name, authors.author, genres.genre, books.description
FROM ((books
INNER JOIN authors ON books.author_id = authors.id)
INNER JOIN genres ON books.genre_id = genres.id)
WHERE books.genre_id = ?
""", (genre_id,))
        books = await cursor.fetchall()
        return books
