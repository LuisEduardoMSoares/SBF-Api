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


def _make_links(page: int, per_page: int, name_filter: str = ''):
    """
    Make pagination link parameters.

    Args:
        page (int): Page to fetch.
        per_page (int): Quantity of items per page.
        name_filter (str): Parameter to filtering by name.
    """
    link = f"{page}?per_page={per_page}"

    if name_filter != '' and name_filter != None:
        link = f"{link}&name={name_filter}"
        
    return link

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