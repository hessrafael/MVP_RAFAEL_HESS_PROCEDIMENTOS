from pydantic import BaseModel
from typing import List
from models.procedimento import Procedimento

class ProcedimentoSchema(BaseModel):
    """ Define como um Procedimento novo deve ser adicionado
    """
    start_time : str = "dd/mm/aaaa hh:mm"
    end_time : str = "dd/mm/aaaa hh:mm"
    description : str = 'Descrição do procedimento'
    room_id : str = '206b887e-5465-4e47-b239-17ccc6ebcefa'
    paciente_id : str = '206b887e-5465-4e47-b239-17ccc6ebcefa'

class ProcedimentoViewSchema(BaseModel):
    """ Define como um Procedimento deve ser retornado
    """
    id: str = '206b887e-5465-4e47-b239-17ccc6ebcefa'
    start_time : str = "dd/mm/aaaa hh:mm"
    end_time : str = "dd/mm/aaaa hh:mm"
    description : str = 'Descrição do procedimento'
    room_id : str = '206b887e-5465-4e47-b239-17ccc6ebcefa'
    paciente_id : str = '206b887e-5465-4e47-b239-17ccc6ebcefa'

class ProcedimentoListViewSchema(BaseModel):
    """Define como uma Lista de Procedimentos deve ser retornada
    """
    procedimentos: List[ProcedimentoViewSchema]

class ProcedimentoAlteraDescSchema(BaseModel):
    id: str = '206b887e-5465-4e47-b239-17ccc6ebcefa'
    description : str = 'Nova descrição do procedimento'

class ProcedimentoBuscaIDSchema(BaseModel):
    """Define como deve ser feita a busca pelo procedimento
    """
    id: str = '206b887e-5465-4e47-b239-17ccc6ebcefa'

class ProcedimentoListBuscaIDSchema(BaseModel):
    """Define como deve ser feita a busca por vários procedimentos
    """
    ids: List[ProcedimentoBuscaIDSchema] = [ProcedimentoBuscaIDSchema(),ProcedimentoBuscaIDSchema()]

def apresenta_procedimento(procedimento: Procedimento):
    """Retorna uma visualização do procedimento conforme definido em ProcedimentoViewSchema
    """
    return{
        "id": procedimento.proceeding_id,
        "start": procedimento.start_time,
        "end": procedimento.end_time,
        "description": procedimento.description,
        "room_id": procedimento.room_id,
        "paciente_id": procedimento.paciente_id
    }

def apresenta_procedimentos(procedimentos: List[Procedimento]):
    """Retorna uma visualização em lista conforme definido em ProcedimentoListViewSchema
    """
    procedimento_lista = []
    for procedimento in procedimentos:
        procedimento_lista.append(apresenta_procedimento(procedimento))
    return {"procedimentos": procedimento_lista}