from sqlalchemy import Table, Column, Integer, ForeignKey
from database import Base

lecturer_division_table = Table(
    "lecturer_divisions",
    Base.metadata,
    Column("lecturer_id", Integer, ForeignKey("lecturers.id"), primary_key=True),
    Column("division_id", Integer, ForeignKey("divisions.id"), primary_key=True)
)
