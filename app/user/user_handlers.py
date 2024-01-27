import random

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from app.user.user_keyboard import *
import data.database.db as db
import data.config as config

router = Router()


class UserStates(StatesGroup):
    set_book_name = State()
    set_genre_name = State()
    set_author_name = State()
    set_book_description = State()
    set_search_name = State()


@router.message(Command("start"))
async def start(message: Message):
    if not await db.get_user_exists(message.from_user.id):
        await db.add_user(message.from_user.id)
        config.logger.info(f"User {message.from_user.id} added to database")
    await message.answer(f"Привет, {message.from_user.first_name}, добро пожаловать в бота {config.bot_name}!",
                         reply_markup=await main_keyboard())


@router.message(F.text == "📚 Все книги")
async def all_books(message: Message):
    await message.delete()
    books = await db.get_all_books()
    await message.answer("📚 Все книги, которые доступны в библиотеке",
                         reply_markup=await show_books_keyboard(books, "all_books"))


@router.callback_query(F.data.startswith("all_books"))
async def all_books_callback(call: CallbackQuery):
    page = int(call.data.split(":")[1])
    books = await db.get_all_books()
    await call.message.edit_reply_markup(reply_markup=await show_books_keyboard(books, "all_books", page))


@router.callback_query(F.data.startswith("open_book"))
async def open_book(call: CallbackQuery):
    book_id = int(call.data.split(":")[1])
    book = await db.get_book_by_id(book_id)
    if book:
        await call.answer()
        emoji_list = ["📕", "📗", "📘", "📙"]
        await call.message.answer(
            f"{random.choice(emoji_list)} <b>Полная информация о книге</b>\n\n📖 <b>Название:</b> {book[1]}\n📚 <b>Автор:</b> {book[2]}\n🎭 <b>Жанр:</b> {book[3]}\n📃 <b>Описание:</b> {book[4]}",
            reply_markup=await edit_book_keyboard(book_id))
    else:
        await call.answer("😢 Книга не найдена")


@router.callback_query(F.data.startswith("delete_book"))
async def delete_book(call: CallbackQuery):
    book_id = int(call.data.split(":")[1])
    try:
        await db.delete_book(book_id)
        await call.answer("✅ Книга удалена")
        await call.message.delete()
        config.logger.info(f"Book {book_id} deleted by {call.from_user.id}")
    except:
        await call.answer("❌ Ошибка, книгу не удалось удалить")


@router.message(F.text == "📝 Добавить книгу")
async def add_book(message: Message, state: FSMContext):
    await message.delete()
    m = await message.answer("📝 <b>Добавление книги</b>\n\nВведите название книги",
                             reply_markup=await cancel_keyboard())
    await state.set_state(UserStates.set_book_name)
    await state.update_data(m_id=m.message_id)


@router.message(F.text, UserStates.set_book_name)
async def set_book_name(message: Message, state: FSMContext):
    book_name = message.text
    data = await state.get_data()
    m_id = data["m_id"]
    await state.update_data(book_name=book_name)
    try:
        await message.delete()
    except:
        pass
    await message.bot.edit_message_text(chat_id=message.chat.id, message_id=m_id,
                                        text=f"📝 <b>Добавление книги</b>\n\n<b>Название:</b> {book_name}\n\nВыберите жанр книги",
                                        reply_markup=await genres_keyboard())


@router.callback_query(F.data == "add_genre")
async def add_genre(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    try:
        m_id = data["m_id"]
        book_name = data["book_name"]
        await call.bot.edit_message_text(chat_id=call.message.chat.id, message_id=m_id,
                                         text=f"📝 <b>Добавление книги</b>\n\n<b>Название:</b> {book_name}\n\nВведите название жанра",
                                         reply_markup=None)
        await state.set_state(UserStates.set_genre_name)
    except:
        await call.message.delete()


@router.message(F.text, UserStates.set_genre_name)
async def set_genre_name(message: Message, state: FSMContext):
    genre_name = message.text
    try:
        await message.delete()
    except:
        pass
    genre_id = await db.add_genre(genre_name)
    data = await state.get_data()
    m_id = data["m_id"]
    book_name = data["book_name"]
    await state.update_data(genre_name=genre_name, genre_id=genre_id)
    await message.bot.edit_message_text(chat_id=message.chat.id, message_id=m_id,
                                        text=f"📝 <b>Добавление книги</b>\n\n<b>Название:</b> {book_name}\n<b>Жанр:</b> {genre_name}\n\nВыберите автора книги",
                                        reply_markup=await authors_keyboard())


@router.callback_query(F.data.startswith("choose_genre"))
async def choose_genre(call: CallbackQuery, state: FSMContext):
    try:
        genre_id = int(call.data.split(":")[1])
        genre = await db.get_genre_by_id(genre_id)
        data = await state.get_data()
        m_id = data["m_id"]
        book_name = data["book_name"]
        await state.update_data(genre_name=genre[1], genre_id=genre[0])
        await call.message.bot.edit_message_text(chat_id=call.message.chat.id, message_id=m_id,
                                                 text=f"📝 <b>Добавление книги</b>\n\n<b>Название:</b> {book_name}\n<b>Жанр:</b> {genre[1]}\n\nВыберите автора книги",
                                                 reply_markup=await authors_keyboard())
    except:
        await call.answer("❌ Ошибка, попробуйте еще раз")
        await call.message.delete()


@router.callback_query(F.data == "add_author")
async def add_author(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    try:
        m_id = data["m_id"]
        book_name = data["book_name"]
        genre_name = data["genre_name"]
        await call.bot.edit_message_text(chat_id=call.message.chat.id, message_id=m_id,
                                         text=f"📝 <b>Добавление книги</b>\n\n<b>Название:</b> {book_name}\n<b>Жанр:</b> {genre_name}\n\nВведите имя автора",
                                         reply_markup=None)
        await state.set_state(UserStates.set_author_name)
    except:
        await call.message.delete()


@router.message(F.text, UserStates.set_author_name)
async def set_author_name(message: Message, state: FSMContext):
    author_name = message.text
    try:
        await message.delete()
    except:
        pass
    author_id = await db.add_author(author_name)
    data = await state.get_data()
    m_id = data["m_id"]
    book_name = data["book_name"]
    genre_name = data["genre_name"]
    await state.update_data(author_name=author_name, author_id=author_id)
    await message.bot.edit_message_text(chat_id=message.chat.id, message_id=m_id,
                                        text=f"📝 <b>Добавление книги</b>\n\n<b>Название:</b> {book_name}\n<b>Жанр:</b> {genre_name}\n<b>Автор:</b> {author_name}\n\nВведите описание книги",
                                        reply_markup=await cancel_keyboard())
    await state.set_state(UserStates.set_book_description)


@router.callback_query(F.data.startswith("choose_author"))
async def choose_author(call: CallbackQuery, state: FSMContext):
    try:
        author_id = int(call.data.split(":")[1])
        author = await db.get_author_by_id(author_id)
        data = await state.get_data()
        m_id = data["m_id"]
        book_name = data["book_name"]
        genre_name = data["genre_name"]
        await state.update_data(author_name=author[1], author_id=author[0])
        await call.message.bot.edit_message_text(chat_id=call.message.chat.id, message_id=m_id,
                                                 text=f"📝 <b>Добавление книги</b>\n\n<b>Название:</b> {book_name}\n<b>Жанр:</b> {genre_name}\n<b>Автор:</b> {author[1]}\n\nВведите описание книги",
                                                 reply_markup=await cancel_keyboard())
        await state.set_state(UserStates.set_book_description)
    except:
        await call.answer("❌ Ошибка, попробуйте еще раз")
        await call.message.delete()


@router.message(F.text, UserStates.set_book_description)
async def set_book_description(message: Message, state: FSMContext):
    try:
        book_description = message.text
        data = await state.get_data()
        book_name = data["book_name"]
        author_id = data["author_id"]
        genre_id = data["genre_id"]
        m_id = data["m_id"]
        try:
            await message.delete()
            await message.bot.delete_message(chat_id=message.chat.id, message_id=m_id)
        except:
            pass
        await db.add_book(book_name, author_id, genre_id, book_description)
        await message.answer(f"✅ Книга <b>{book_name}</b> успешно добавлена в библиотеку!")
        await state.clear()
        config.logger.info(f"Book {book_name} added by {message.from_user.id}")
    except:
        await message.answer("❌ Ошибка, попробуйте еще раз")
        await state.clear()


@router.message(F.text == "🔍 Найти книгу")
async def find_book(message: Message):
    await message.delete()
    await message.answer("🔎 Выберите тип поиска", reply_markup=await choose_search_type_keyboard())


@router.callback_query(F.data.startswith("search_by_name"))
async def search_by_name(call: CallbackQuery, state: FSMContext):
    await call.answer()
    try:
        query = call.data.split(":")[1]
        page = int(call.data.split(":")[2])
        books = await db.get_books_by_query(query)
        await call.message.edit_text(f"🔎 Результаты поиска по запросу <b>{query}</b>",
                                     reply_markup=await show_books_keyboard(books, f"search_by_name:{query}", page))
    except:
        m = await call.message.answer("Введите ключевое слово или фразу для поиска книг")
        await state.set_state(UserStates.set_search_name)
        await state.update_data(m_id=m.message_id)


@router.message(F.text, UserStates.set_search_name)
async def set_search_name(message: Message, state: FSMContext):
    query = message.text
    data = await state.get_data()
    m_id = data["m_id"]
    books = await db.get_books_by_query(query)
    try:
        await message.delete()
        await message.bot.delete_message(chat_id=message.chat.id, message_id=m_id)
    except:
        pass
    await message.answer(f"🔎 Результаты поиска по запросу <b>{query}</b>",
                         reply_markup=await show_books_keyboard(books, f"search_by_name:{query}"))
    await state.clear()
    config.logger.info(f"User {message.from_user.id} searched by {query}")


@router.callback_query(F.data == "search_by_genre")
async def search_by_genre(call: CallbackQuery):
    await call.answer()
    await call.message.answer("🎭 Выберите жанр для поиска",
                              reply_markup=await search_by_genre_keyboard())


@router.callback_query(F.data.startswith("get_books_by_genre"))
async def get_books_by_genre(call: CallbackQuery):
    genre_id = int(call.data.split(":")[1])
    genre = await db.get_genre_by_id(genre_id)
    page = int(call.data.split(":")[2])
    books = await db.get_books_by_genre_id(genre_id)
    await call.answer()
    await call.message.edit_text(f"🔎 Результаты поиска по жанру <b>{genre[1]}</b>",
                                 reply_markup=await show_books_keyboard(books, f"get_books_by_genre:{genre_id}", page))
    config.logger.info(f"User {call.from_user.id} searched by genre {genre_id}")


@router.callback_query(F.data == "close")
async def close(call: CallbackQuery):
    await call.message.delete()


@router.callback_query(F.data == "cancel")
async def cancel(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.clear()
    try:
        await call.message.delete()
    except:
        pass
