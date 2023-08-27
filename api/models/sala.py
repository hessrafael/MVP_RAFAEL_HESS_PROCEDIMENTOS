from sqlalchemy import Column, String, DateTime, Boolean, Integer, UniqueConstraint, ForeignKey
from datetime import datetime
import uuid
import enum

from models import Base

class Sala(Base):
    __tablename__='room'

    room_id = Column(String(36), primary_key =True)
    room_number = Column(Integer,nullable=False)

    created_at = Column(DateTime, default=datetime.now())
    is_active = Column(Boolean, default=True)

    #adicionando a restrição de que não podem ter salas com numero repetidos
    __table_args__ = (UniqueConstraint('room_number', name='uq_room'),
                      )
    
    def __init__(self,room_number:int):
        self.room_id = uuid.uuid4().__str__()
        self.room_number = room_number