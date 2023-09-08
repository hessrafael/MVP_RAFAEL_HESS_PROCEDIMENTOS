from pydantic import BaseModel
from typing import List
from models.sala import Sala

class SalaSchema(BaseModel):
    """ Define como uma Sala nova deve ser adicionada
    """
    numero : int = 10

class SalaViewSchema(BaseModel):
    """ Define como uma Sala deve ser retornado
    """
    id: str = '206b887e-5465-4e47-b239-17ccc6ebcefa'
    numero : int = 10

class SalaListViewSchema(BaseModel):
    """Define como uma Lista de Salas deve ser retornada
    """
    medicamentos: List[SalaViewSchema]

class SalaBuscaIDSchema(BaseModel):
    """Define como deve ser feita a busca pela Sala
    """
    id: str = '206b887e-5465-4e47-b239-17ccc6ebcefa'

def apresenta_sala(sala: Sala):
    """Retorna uma visualização do Sala conforme definido em SalaViewSchema
    """
    return{
        "id": sala.room_id,
        "numero": sala.room_number
    }

def apresenta_salas(salas: List[Sala]):
    """Retorna uma visualização em lista conforme definido em SalaListViewSchema
    """
    sala_lista = []
    for sala in salas:
        sala_lista.append(apresenta_sala(sala))
    return {"salas": sala_lista}