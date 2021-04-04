# Typing imports
from pydantic import BaseModel

# Exception Imports
from sqlalchemy_filters.exceptions import InvalidPage



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
                "current": "?page=3&per_page=20&name=test",
                "first": "?page=1&per_page=20&name=test",
                "previous": "?page=2&per_page=20&name=test",
                "next": "?page=4&per_page=20&name=test",
                "last": "?page=5&per_page=20&name=test"
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
                    "current": "?page=3&per_page=20&name=test",
                    "first": "?page=1&per_page=20&name=test",
                    "previous": "?page=2&per_page=20&name=test",
                    "next": "?page=4&per_page=20&name=test",
                    "last": "?page=5&per_page=20&name=test"
                }
            }
        }


def _make_links(page: int, per_page: int, name_filter: str = ''):
    """
    Make pagination link parameters.

    Args:
        page (int): Page to fetch.
        per_page (int): Quantity of items per page.
        name_filter (str): Parameter to filtering by name.
    """
    if name_filter != '' and name_filter != None:
        return f"?page={page}&per_page={per_page}&name={name_filter}"
    else:
        return f"?page={page}&per_page={per_page}"

def make_pagination_metadata(current_page: int, total_pages: int, per_page: int,
    total_items: int, name_filter: str = '') -> PaginationMetadataSchema:
    """
    Make pagination metadata.

    Args:
        current_page (int): Current page.
        total_pages (int): Total of pages.
        per_page (int): Quantity of items per page.
        total_items (int): Total of items per page.
        name_filter (str): Parameter to filtering by name.
    """
    if current_page == 0:
        raise InvalidPage(f"Page number should be positive: {current_page}")
    elif current_page > total_pages:
        raise InvalidPage(f"Page number invalid, the total of pages is {total_pages}: {current_page}")

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
        current = _make_links(current_page, per_page, name_filter),
        first = _make_links(1, per_page, name_filter),
        previous = _make_links(previous_page, per_page, name_filter),
        next = _make_links(next_page, per_page, name_filter),
        last = _make_links(total_pages, per_page, name_filter),
    )

    metadata = PaginationMetadataSchema(
        page = current_page,
        per_page = per_page,
        page_count = total_pages,
        total_count = total_items,
        links = links
    )

    return metadata