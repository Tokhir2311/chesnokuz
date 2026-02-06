from fastapi import FastAPI , HTTPException, Query 

from app.routers import posts_router , category_router, user_router, tags_router, prof_router, comment_router, weather_router, auth_router




app = FastAPI(
    title="Chesnokdek achchiq yangiliklar",
    description="Chesnokuz - news website inspired from Qalampir.uz, built in FastAPI",
)

app.include_router(posts_router)
app.include_router(category_router)
app.include_router(user_router)
app.include_router(tags_router)
app.include_router(prof_router)
app.include_router(comment_router)
app.include_router(weather_router)
app.include_router(auth_router)