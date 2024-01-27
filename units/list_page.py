def get_page_from_list(list_: list, page: int) -> tuple[list, bool]:
    """
    Возвращает элементы списка для страницы

    Args:
        list_ (list): список
        page (int): страница

    Returns:
        tuple[list, bool]: элементы списка для страницы, есть ли следующая страница
    """

    items_per_page = 10
    start_index = page * items_per_page
    end_index = page * items_per_page + items_per_page
    page_items = list_[start_index:end_index]
    has_next_page = end_index < len(list_)
    return page_items, has_next_page
