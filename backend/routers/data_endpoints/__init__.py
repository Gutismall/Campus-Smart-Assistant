from fastapi import APIRouter
from .users import router as users_router
from .campuses import router as campuses_router
from .divisions import router as divisions_router
from .buildings import router as buildings_router
from .rooms import router as rooms_router
from .students import router as students_router
from .lecturers import router as lecturers_router
from .tests import router as tests_router

# Core router spanning all models mapped to /api/data
router = APIRouter(
    prefix="/api/data",
    tags=["system admin data handling"],
)

router.include_router(users_router)
router.include_router(campuses_router)
router.include_router(divisions_router)
router.include_router(buildings_router)
router.include_router(rooms_router)
router.include_router(students_router)
router.include_router(lecturers_router)
router.include_router(tests_router)
