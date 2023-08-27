from sqlalchemy import Column, String, DateTime, Boolean, Integer, UniqueConstraint, ForeignKey, CheckConstraint
from datetime import datetime
import uuid
import enum

from models import Base

class Procedimento(Base):
    __tablename__ = 'proceeding'

    proceeding_id = Column(String(36), primary_key =True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    description = Column(String, nullable=False)
    #FK para tabela de salas
    room_id = Column(String(36), ForeignKey("room.room_id"), nullable=False )
    #relação com paciente
    paciente_id = Column(String(36), nullable=False)

    created_at = Column(DateTime, default=datetime.now())
    is_active = Column(Boolean, default=True)

    __table_args__ = (CheckConstraint('start_time < end_time'),
                      )

    def __init__(self,start_time:datetime,end_time:datetime,description:str,room_id:str(36),paciente_id:str(36)):
        self.proceeding_id = uuid.uuid4().__str__()
        self.start_time = start_time
        self.end_time = end_time
        self.description = description
        self.room_id = room_id
        self.paciente_id = paciente_id

        