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
