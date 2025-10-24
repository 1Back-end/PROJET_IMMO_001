from fastapi import APIRouter
from .migration_controller import router as migration
from .authentification_controller import router as authentication
from .user_controller import router as user
from .storage_controller import router as storage
from .address_controller import router as address
from .reservation_controller import router as reservation
from .products_controller import router as products
from .payments_controller import router as payments
from .customers_controller import router as customers
from .contrats_controller import router as contrats

from .country_with_city_controller import router as country_with_citys
api_router = APIRouter()

api_router.include_router(migration)
api_router.include_router(authentication)
api_router.include_router(user)
api_router.include_router(storage)
api_router.include_router(country_with_citys)
api_router.include_router(reservation)
api_router.include_router(products)
api_router.include_router(payments)
api_router.include_router(customers)
api_router.include_router(contrats)
