import controller_cart, controller_item, controller_user, controller_pay, controller_db
from fastapi import FastAPI

app = FastAPI()

app.include_router(controller_cart.app)
app.include_router(controller_item.app)
app.include_router(controller_user.app)
app.include_router(controller_pay.app)
app.include_router(controller_db.app)

@app.get("/")
async def root():
    return {'hello', 'root'}