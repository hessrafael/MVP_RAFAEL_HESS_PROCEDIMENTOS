from sqlalchemy import Column, String, DateTime, Boolean, Integer, UniqueConstraint, ForeignKey
from datetime import datetime
import uuid
import enum

from models import Base

class Prescricao(Base):
    __tablename__ = 'prescription'

    prescription_id = Column(String(36), primary_key =True)
    quantity = Column(Integer, nullable=False)
    #FK para o procedimento associado a prescrição
    proceeding_id = Column(String(36), ForeignKey("proceeding.proceeding_id"), nullable=False )
    #id do medicamento prescrito
    medicament_id = Column(String(36), nullable=False)

    created_at = Column(DateTime, default=datetime.now())
    is_active = Column(Boolean, default=True)

    def __init__(self,quantity:int,proceeding_id:str(36),medicament_id:str(36)):
        self.prescription_id = uuid.uuid4().__str__()
        self.quantity = quantity
        self.proceeding_id = proceeding_id
        self.medicament_id = medicament_id
        