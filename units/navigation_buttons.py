from aiogram import types


def get_navigation_buttons(page: int, has_next_page: bool, callback_data: str) -> list[types.InlineKeyboardButton]:
    """
    Возвращает кнопки навигации

    Args:
        page (int): страница
        has_next_page (bool): есть ли следующая страница
        callback_data (str): callback_data для кнопок

    Returns:
        list[types.InlineKeyboardButton]: кнопки навигации
    """

    navigation_buttons = []
    if page != 0 and has_next_page:
        navigation_buttons.append(
            types.InlineKeyboardButton(text="⬅️", callback_data=f"{callback_data}:{page - 1}"))
        navigation_buttons.append(
            types.InlineKeyboardButton(text="➡️", callback_data=f"{callback_data}:{page + 1}"))
    elif page != 0:
        navigation_buttons.append(
            types.InlineKeyboardButton(text="⬅️", callback_data=f"{callback_data}:{page - 1}"))
    elif has_next_page:
        navigation_buttons.append(
            types.InlineKeyboardButton(text="➡️", callback_data=f"{callback_data}:{page + 1}"))
    return navigation_buttons
