import math


def make_pagination_range(page_range, qty_pages, current_page):
    middle_page = math.ceil(qty_pages / 2)
    start_range = current_page - middle_page
    stop_range = current_page + middle_page
    total_pages = len(page_range)

    start_range_offset = abs(start_range) if start_range < 0 else 0

    if stop_range >= total_pages:
        start_range = start_range - abs(stop_range - total_pages)

    if start_range < 0:
        start_range = 0
        stop_range += start_range_offset

    pagination = page_range[start_range:stop_range]

    return {
        'pagination': pagination,
        'start_range': start_range,
        'stop_range': stop_range,
        'page_range': page_range,
        'current_page': current_page,
        'qty_pages': qty_pages,
        'total_pages': total_pages,
        'first_page_out_of_range': current_page > middle_page,
        'last_page_out_of_range': stop_range < total_pages,
    }
