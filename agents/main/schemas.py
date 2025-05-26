from pydantic import BaseModel, Field
from typing import Dict

class GroceryItem(BaseModel):
    quantity: float = Field(..., gt=0, description="Quantity must be greater than 0")
    price: float = Field(..., ge=0, description="Price must be 0 or greater")

class GroceriesInput(BaseModel):
    groceries: Dict[str, GroceryItem] = Field(
        ...,
        description=(
            "This contains multiple grocery items. "
            "Each item must include a 'quantity' > 0 and a 'price' >= 0."
        )
    )
