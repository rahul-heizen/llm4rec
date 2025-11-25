from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from typing import List
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
load_dotenv()

class FoodItem(BaseModel):
    id: int
    name: str
    description: str
    calories: int
    is_vegan: bool
    image_url: str

food_catalog = [
    FoodItem(
        id=1,
        name="Quinoa Power Salad",
        description="A vibrant salad featuring protein-rich quinoa, crisp bell peppers, cherry tomatoes, cucumber, and a zesty lemon-tahini dressing. Perfect for a light, energizing meal.",
        calories=320,
        is_vegan=True,
        image_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ12p-bErtTQXhAasJDrQHAp1qT8G1w-2lxsA&s"
    ),
    FoodItem(
        id=2,
        name="Herb-Grilled Chicken Breast",
        description="Tender chicken breast marinated in fresh herbs and garlic, grilled to perfection and served with a side of roasted seasonal vegetables.",
        calories=250,
        is_vegan=False,
        image_url="https://www.feastingathome.com/wp-content/uploads/2021/06/Grilled-lemon-Herb-Chicken-17.jpg"
    ),
    FoodItem(
        id=3,
        name="Seasonal Fruit Medley",
        description="A refreshing bowl of handpicked seasonal fruits including berries, melon, and citrus, topped with a sprinkle of toasted coconut.",
        calories=180,
        is_vegan=True,
        image_url="https://gooddinnermom.com/wp-content/uploads/1a7.jpg"
    ),
    FoodItem(
        id=4,
        name="Garden Veggie Wrap",
        description="Whole wheat wrap filled with grilled zucchini, bell peppers, spinach, and hummus, offering a nutritious and satisfying vegan option.",
        calories=290,
        is_vegan=True,
        image_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQcDkLOru31_OpYAPLRJqlBVUEk4JWGGFIJ9A&s"
    ),
    FoodItem(
        id=5,
        name="Lemon-Dill Salmon Fillet",
        description="Wild-caught salmon fillet seasoned with lemon and dill, oven-roasted and served with a side of garlic sautéed green beans.",
        calories=350,
        is_vegan=False,
        image_url="https://vikalinka.com/wp-content/uploads/2023/10/Salmon-with-Creamy-Salmon-Dill-Sauce-5-Edit.jpg"
    ),
    FoodItem(
        id=6,
        name="Tofu & Broccoli Stir Fry",
        description="Crispy tofu cubes stir-fried with broccoli, carrots, and snap peas in a savory ginger-soy sauce, served over brown rice.",
        calories=270,
        is_vegan=True,
        image_url="https://omnivorescookbook.com/wp-content/uploads/2025/01/241217_Tofu-And-Broccoli_550.jpg"
    ),
    FoodItem(
        id=7,
        name="Classic Chicken Caesar Salad",
        description="Grilled chicken breast atop crisp romaine lettuce, tossed with creamy Caesar dressing, parmesan cheese, and crunchy whole grain croutons.",
        calories=310,
        is_vegan=False,
        image_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSh1AJXXSvA_O9yB1PacKxgeJAqEqAqTLNQfA&s"
    ),
    FoodItem(
        id=8,
        name="Hearty Lentil & Vegetable Soup",
        description="A warming soup made with green lentils, carrots, celery, tomatoes, and aromatic spices, simmered to perfection for a filling vegan meal.",
        calories=220,
        is_vegan=True,
        image_url="https://www.therusticfoodie.com/wp-content/uploads/2023/01/Hearty-Lentil-Soup-featured.jpg"
    ),
    FoodItem(
        id=9,
        name="Veggie-Packed Egg White Omelette",
        description="Fluffy egg white omelette loaded with spinach, mushrooms, tomatoes, and feta cheese, served with a slice of whole grain toast.",
        calories=200,
        is_vegan=False,
        image_url="https://beautifuleatsandthings.com/wp-content/uploads/2018/05/Veggie-Stuffed-Egg-White-Omelet.jpg"
    ),
    FoodItem(
        id=10,
        name="Avocado Smash Toast",
        description="Toasted whole grain bread topped with creamy smashed avocado, cherry tomatoes, radish slices, and a sprinkle of chili flakes.",
        calories=240,
        is_vegan=True,
        image_url="https://images.immediate.co.uk/production/volatile/sites/30/2020/08/avocado-on-toast-96e3158.jpg"
    ),
]

class RecommendRequest(BaseModel):
    user_background: str

class RecommendResponse(BaseModel):
    recommended_ids: List[int] = Field(description="List of recommended food item IDs")

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

@app.post("/recommend", response_model=List[FoodItem])
async def recommend_food(request: RecommendRequest):
    catalog_context = "\n".join([
        f"ID: {item.id}, Name: {item.name}, Desc: {item.description}, Calories: {item.calories}, Vegan: {item.is_vegan}"
        for item in food_catalog
    ])
    prompt = (
        "Given the following food catalog:\n"
        f"{catalog_context}\n\n"
        f"User background: {request.user_background}\n"
        "Recommend a list of food item IDs (as a Python list) that best match the user's background. "
        "Only output the list of IDs in the 'recommended_ids' field."
    )

    openai_api_key = os.getenv("OPENAI_KEY")
    llm = ChatOpenAI(openai_api_key=openai_api_key, model="gpt-4o", temperature=0.2)
    llm_structured = llm.with_structured_output(RecommendResponse)
    response = llm_structured.invoke(prompt)
    catalog = [
        FoodItem(
            id=item.id,
            name=item.name,
            description=item.description,
            calories=item.calories,
            is_vegan=item.is_vegan,
            image_url=item.image_url
        )
        for item in food_catalog
        if item.id in response.recommended_ids
    ]
    return catalog

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
