from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import List
from pydantic import BaseModel

class FoodItem(BaseModel):
    id: int
    name: str
    description: str
    calories: int
    is_vegan: bool
    image_url: str

food_catalog = [
    FoodItem(id=1, name="Quinoa Salad", description="Fresh quinoa with veggies", calories=320, is_vegan=True, image_url="https://example.com/images/quinoa_salad.jpg"),
    FoodItem(id=2, name="Grilled Chicken", description="Lean grilled chicken breast", calories=250, is_vegan=False, image_url="https://example.com/images/grilled_chicken.jpg"),
    FoodItem(id=3, name="Fruit Bowl", description="Seasonal fruits", calories=180, is_vegan=True, image_url="https://example.com/images/fruit_bowl.jpg"),
    FoodItem(id=4, name="Veggie Wrap", description="Whole wheat wrap with mixed veggies", calories=290, is_vegan=True, image_url="https://example.com/images/veggie_wrap.jpg"),
    FoodItem(id=5, name="Salmon Fillet", description="Grilled salmon with herbs", calories=350, is_vegan=False, image_url="https://example.com/images/salmon_fillet.jpg"),
    FoodItem(id=6, name="Tofu Stir Fry", description="Stir fried tofu with vegetables", calories=270, is_vegan=True, image_url="https://example.com/images/tofu_stir_fry.jpg"),
    FoodItem(id=7, name="Chicken Caesar Salad", description="Classic Caesar salad with grilled chicken", calories=310, is_vegan=False, image_url="https://example.com/images/chicken_caesar_salad.jpg"),
    FoodItem(id=8, name="Lentil Soup", description="Hearty lentil soup", calories=220, is_vegan=True, image_url="https://example.com/images/lentil_soup.jpg"),
    FoodItem(id=9, name="Egg White Omelette", description="Omelette made with egg whites and veggies", calories=200, is_vegan=False, image_url="https://example.com/images/egg_white_omelette.jpg"),
    FoodItem(id=10, name="Avocado Toast", description="Whole grain toast with smashed avocado", calories=240, is_vegan=True, image_url="https://example.com/images/avocado_toast.jpg"),
]

app = FastAPI(title="LLM4Rec API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint that returns a welcome message."""
    return {"message": "Welcome to LLM4Rec API"}

@app.get("/catalog", response_model=List[FoodItem])
async def get_catalog():
    """Endpoint that returns a catalog of food items with details."""
    return food_catalog

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
