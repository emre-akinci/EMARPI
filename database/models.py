# database/models.py

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class Part(Base):
    __tablename__ = "parts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    part_number = Column(String, unique=True, nullable=False)
    part_type = Column(String, nullable=True)
    manufacturer = Column(String, nullable=True)
    manufacturer_part_number = Column(String, nullable=True)
    description = Column(String, nullable=True)
    comment = Column(String, nullable=True)
    value = Column(String, nullable=True)
    use_as_units = Column(String, nullable=True)
    attrition = Column(Float, nullable=True, default=0.0)
    manufactured_here = Column(Boolean, nullable=True, default=False)
    rohs_compliant = Column(Boolean, nullable=True, default=False)

    def __repr__(self):
        return f"<Part(id={self.id}, part_number='{self.part_number}')>"

class BOMItem(Base):
    __tablename__ = "bom_items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    parent_part_id = Column(Integer, ForeignKey("parts.id"), nullable=False)
    child_part_id = Column(Integer, ForeignKey("parts.id"), nullable=False)
    quantity = Column(Float, default=1.0)
    reference_designator = Column(String, nullable=True)

    def __repr__(self):
        return f"<BOMItem(id={self.id}, parent={self.parent_part_id}, child={self.child_part_id})>"
