from fastapi import FastAPI
import uvicorn
# from fas.routers import user, product, sale
from routers import user, product, sale
import models
from database import engine
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# Include routers
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(product.router, prefix="/products", tags=["products"])
app.include_router(sale.router, prefix="/sales", tags=["sales"])


if __name__ == "__main__":
    uvicorn.run(app=app, host='192.168.18.117', port=9000)
