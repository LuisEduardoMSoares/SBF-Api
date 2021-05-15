# Typing imports
from pydantic import BaseModel



class PaginationLinksSchema(BaseModel):
    current: str
    first: str
    previous: str
    next: str
    last: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "current": "3?per_page=20&name=test",
                "first": "1?per_page=20&name=test",
                "previous": "2?per_page=20&name=test",
                "next": "4?per_page=20&name=test",
                "last": "5?per_page=20&name=test"
            }
        }

class PaginationMetadataSchema(BaseModel):
    page: int
    per_page: int
    page_count: int
    total_count: int
    links: PaginationLinksSchema

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "page": 3,
                "per_page": 20,
                "page_count": 5,
                "total_count": 100,
                "links": {
                    "current": "3?per_page=20&name=test",
                    "first": "1?per_page=20&name=test",
                    "previous": "2?per_page=20&name=test",
                    "next": "4?per_page=20&name=test",
                    "last": "5?per_page=20&name=test"
                }
            }
        }


def _make_url_args(url_args: dict):
    """
    Make url parameters

    Args:
        url_args (Dict): Dict of url parametes

    Returns:
        str: The url parameters
    
    Example:
        input: {'test1': 1, 'test2': 2, 'test3': 3}
        output: "&test1=1&test2=2&test3=3"
    """
    url = ''
    for key, value in url_args.items():
        if key != '' and value != '' and value != None:
            url = f'{url}&{key}={value}'
    return url

def _make_links(page: int, per_page: int, url_args: dict = {}):
    """
    Make pagination link parameters.

    Args:
        page (int): Page to fetch.
        per_page (int): Quantity of items per page.
        url_args (dict): Dict of url parametes.
    """
    link = f"{page}?per_page={per_page}"
    url_params = _make_url_args(url_args)
    # filtro de nome input: {'name': name_filter}
    link = f"{link}{url_params}"
        
    return link

def make_pagination_metadata(current_page: int, total_pages: int, per_page: int,
    total_items: int, url_args: dict) -> PaginationMetadataSchema:
    """
    Make pagination metadata.

    Args:
        current_page (int): Current page.
        total_pages (int): Total of pages.
        per_page (int): Quantity of items per page.
        total_items (int): Total of items per page.
        url_args (dict): Dict of url parametes.
    """
    # set previous page
    if current_page == 1:
        previous_page = 1
    elif current_page > 1:
        previous_page = current_page - 1

    # set next page
    if current_page == total_pages:
        next_page = current_page
    elif current_page < total_pages:
        next_page = current_page + 1

    links = PaginationLinksSchema(
        current = _make_links(current_page, per_page, url_args),
        first = _make_links(1, per_page, url_args),
        previous = _make_links(previous_page, per_page, url_args),
        next = _make_links(next_page, per_page, url_args),
        last = _make_links(total_pages, per_page, url_args),
    )

    metadata = PaginationMetadataSchema(
        page = current_page,
        per_page = per_page,
        page_count = total_pages,
        total_count = total_items,
        links = links
    )

    return metadata