# database/models.py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship

Base = declarative_base()

class Part(Base):
    """
    A basic 'Part' table to mirror some of the Aligni fields:
      - part_number (internal SKU)
      - part_type
      - manufacturer
      - manufacturer_part_number
      - description
      - comment
      - value (as string or float)
      - use_as_units (e.g. 'each', 'cm', 'ml')
      - attrition (percentage override)
      - manufactured_here (boolean)
      - rohs_compliant (boolean)
    """
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
