from os import lseek
from typing import List
from pydantic import BaseModel


class IncomingProductsData(BaseModel):
    product_id: int
    quantity: int

payload: List[IncomingProductsData] = [
    {
        "product_id": 1,
        "quantity": 8
    },{
        "product_id": 3,
        "quantity": 15
    },{
        "product_id": 1,
        "quantity": 2
    },{
        "product_id": 5,
        "quantity": 22
    }
]

print(payload)


# Check and Sum duplicates
def check_and_sum_duplicates(payload: List[IncomingProductsData]):
    already_added = []
    checked_payload = []

    sorted_payload = sorted(payload, key=lambda v: v['product_id']) 
    for value in sorted_payload:
        if value['product_id'] not in already_added:
            already_added.append(value['product_id'])
            checked_payload.append(value)

        else:
            checked_payload[-1]['quantity'] += value['quantity']
    
    return checked_payload


print('\n')
print(check_and_sum_duplicates(payload))
