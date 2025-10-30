from fastapi import APIRouter
from .migration_controller import router as migration
from .authentification_controller import router as authentication
from .user_controller import router as user
from .storage_controller import router as storage
from .address_controller import router as address
from .customers_controller import router as customers
from .country_with_city_controller import router as country_with_citys
from .product_controller import router as products
from .reservation_controller import router as reservations
from .contrats_controller import router as contrats
from .payments_controller import router as payments
api_router = APIRouter()

api_router.include_router(migration)
api_router.include_router(authentication)
api_router.include_router(user)
api_router.include_router(storage)
api_router.include_router(country_with_citys)
api_router.include_router(customers)
api_router.include_router(products)
api_router.include_router(reservations)
api_router.include_router(contrats)
api_router.include_router(payments)
