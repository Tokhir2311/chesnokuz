from fastapi import FastAPI

from app.routers import posts_router , category_router, user_router, tags_router


app = FastAPI(
    title="Chesnokdek achchiq yangiliklar",
    description="Chesnokuz - news website inspired from Qalampir.uz, built in FastAPI",
)

app.include_router(posts_router)
app.include_router(category_router)
app.include_router(user_router)
app.include_router(tags_router)