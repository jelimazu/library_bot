from sqlite3 import Row
from typing import Iterable

from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram import types

import data.database.db as db
from units import navigation_buttons, list_page


async def main_keyboard() -> ReplyKeyboardMarkup:
    """
    Возвращает клавиатуру с основными кнопками

    Returns:
        ReplyKeyboardMarkup: клавиатура с основными кнопками
    """

    buttons = [
        [
            types.KeyboardButton(text="📝 Добавить книгу"),
        ],
        [
            types.KeyboardButton(text="📚 Все книги"),
            types.KeyboardButton(text="🔍 Найти книгу"),
        ],
    ]
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)
    return keyboard


async def show_books_keyboard(books: Iterable[Row] | None, callback_data: str, page: int = 0) -> InlineKeyboardMarkup:
    """
    Возвращает клавиатуру с книгами

    Args:
        books (Iterable[Row]): список книг
        callback_data (str): callback_data для кнопок
        page (int, optional): страница. Defaults to 0.

    Returns:
        InlineKeyboardMarkup: клавиатура с книгами
    """

    buttons = []
    if books:
        page_items, has_next_page = list_page.get_page_from_list(books, page)
        for book in page_items:
            buttons.append([types.InlineKeyboardButton(text=f"{book[1]} | {book[2]}", callback_data=f"open_book:{book[0]}")])
        navigation_buttons_ = navigation_buttons.get_navigation_buttons(page, has_next_page, callback_data)
        buttons.append(navigation_buttons_)
    else:
        buttons.append([types.InlineKeyboardButton(text="😢 Книг не найдено", callback_data="nothing")])
    buttons.append([types.InlineKeyboardButton(text="❌", callback_data="close")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def edit_book_keyboard(book_id: int) -> InlineKeyboardMarkup:
    """
    Возвращает клавиатуру для редактирования книги

    Args:
        book_id (int): id книги

    Returns:
        InlineKeyboardMarkup: клавиатура для редактирования книги
    """

    buttons = [
        [
            types.InlineKeyboardButton(text="🗑 Удалить книгу", callback_data=f"delete_book:{book_id}"),
        ],
        [
            types.InlineKeyboardButton(text="❌", callback_data="close")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def genres_keyboard() -> InlineKeyboardMarkup:
    """
    Возвращает клавиатуру с жанрами

    Returns:
        InlineKeyboardMarkup: клавиатура с жанрами
    """

    buttons = []
    genres = await db.get_all_genres()
    for genre in genres:
        buttons.append([types.InlineKeyboardButton(text=f"{genre[1]}", callback_data=f"choose_genre:{genre[0]}")])
    buttons.append([types.InlineKeyboardButton(text="📝 Добавить жанр", callback_data="add_genre")])
    buttons.append([types.InlineKeyboardButton(text="❌", callback_data="cancel")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def authors_keyboard() -> InlineKeyboardMarkup:
    """
    Возвращает клавиатуру с авторами

    Returns:
        InlineKeyboardMarkup: клавиатура с авторами
    """

    buttons = []
    authors = await db.get_all_authors()
    for author in authors:
        buttons.append([types.InlineKeyboardButton(text=f"{author[1]}", callback_data=f"choose_author:{author[0]}")])
    buttons.append([types.InlineKeyboardButton(text="📝 Добавить автора", callback_data="add_author")])
    buttons.append([types.InlineKeyboardButton(text="❌", callback_data="cancel")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def choose_search_type_keyboard() -> InlineKeyboardMarkup:
    """
    Возвращает клавиатуру с выбором типа поиска

    Returns:
        InlineKeyboardMarkup: клавиатура с выбором типа поиска
    """

    buttons = [
        [
            types.InlineKeyboardButton(text="🔍 Поиск по названию/автору", callback_data="search_by_name"),
        ],
        [
            types.InlineKeyboardButton(text="🔍 Поиск по жанру", callback_data="search_by_genre"),
        ],
        [
            types.InlineKeyboardButton(text="❌", callback_data="close")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def search_by_genre_keyboard(page: int = 0) -> InlineKeyboardMarkup:
    """
    Возвращает клавиатуру с жанрами для поиска

    Args:
        page (int, optional): страница. Defaults to 0.

    Returns:
        InlineKeyboardMarkup: клавиатура с жанрами для поиска
    """

    buttons = []
    genres = await db.get_all_genres()
    for genre in genres:
        buttons.append([types.InlineKeyboardButton(text=f"{genre[1]}", callback_data=f"get_books_by_genre:{genre[0]}:{page}")])
    buttons.append([types.InlineKeyboardButton(text="❌", callback_data="close")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def cancel_keyboard() -> InlineKeyboardMarkup:
    """
    Возвращает клавиатуру для отмены действия

    Returns:
        InlineKeyboardMarkup: клавиатура для отмены действия
    """

    buttons = [
        [
            types.InlineKeyboardButton(text="❌", callback_data="cancel")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def close_keyboard() -> InlineKeyboardMarkup:
    """
    Возвращает клавиатуру для закрытия меню

    Returns:
        InlineKeyboardMarkup: клавиатура для закрытия меню
    """

    buttons = [
        [
            types.InlineKeyboardButton(text="❌", callback_data="close")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard