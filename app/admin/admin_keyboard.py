from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def admin_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура админ панели

    Returns:
        InlineKeyboardMarkup: клавиатура админ панели
    """

    buttons = [
        [
            InlineKeyboardButton(text="📊 Статистика", callback_data=f"statistic"),
        ],
        [
            InlineKeyboardButton(text="📨 Рассылка", callback_data=f"send_mailing"),
        ],
        [
            InlineKeyboardButton(text="❌", callback_data=f"cancel")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def mailing_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура рассылки

    Returns:
        InlineKeyboardMarkup: клавиатура рассылки
    """

    buttons = [
        [
            InlineKeyboardButton(text="📨 Отправить", callback_data=f"count_send_mailing"),
            InlineKeyboardButton(text="🔄 Заново", callback_data=f"send_mailing")
        ],
        [
            InlineKeyboardButton(text="❌", callback_data=f"cancel")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def ask_mailing_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура рассылки

    Returns:
        InlineKeyboardMarkup: клавиатура рассылки
    """

    buttons = [
        [
            InlineKeyboardButton(text="📨 Отправить", callback_data=f"start_send_mailing")
        ],
        [
            InlineKeyboardButton(text="❌", callback_data=f"cancel")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def admin_cancel_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура отмены действия

    Returns:
        InlineKeyboardMarkup: клавиатура отмены действия
    """

    buttons = [
        [
            InlineKeyboardButton(text="❌", callback_data=f"cancel")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
