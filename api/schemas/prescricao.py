from pydantic import BaseModel
from typing import List
from models.prescricao import Prescricao

class PrescricaoSchema(BaseModel):
    """ Define como uma Prescricao nova deve ser adicionado
    """
    quantity : int = 10
    proceeding_id : str = '206b887e-5465-4e47-b239-17ccc6ebcefa'
    medicament_id : str = '206b887e-5465-4e47-b239-17ccc6ebcefa'

class PrescricaoViewSchema(BaseModel):
    """ Define como uma Prescricao deve ser retornada
    """
    prescription_id : str = '206b887e-5465-4e47-b239-17ccc6ebcefa'
    quantity : int = 10
    proceeding_id : str = '206b887e-5465-4e47-b239-17ccc6ebcefa'
    medicament_id : str = '206b887e-5465-4e47-b239-17ccc6ebcefa'

class PrescricaoListViewSchema(BaseModel):
    """Define como uma Lista de Prescricoes deve ser retornada
    """
    prescricoes: List[PrescricaoViewSchema]

class PrescricaoBuscaIDSchema(BaseModel):
    """Define como deve ser feita a busca pela prescricao
    """
    id: str = '206b887e-5465-4e47-b239-17ccc6ebcefa'

class PrescricaoListBuscaIDSchema(BaseModel):
    """Define como deve ser feita a busca por vários procedimentos
    """
    ids: List[PrescricaoBuscaIDSchema] = [PrescricaoBuscaIDSchema(),PrescricaoBuscaIDSchema()]

def apresenta_prescricao(prescricao: Prescricao):
    """Retorna uma visualização da prescricao conforme definido em PrescricaoViewSchema
    """
    return{
        "id": prescricao.prescription_id,
        "quantidade": prescricao.quantity,
        "proceeding_id": prescricao.proceeding_id,
        "medicament_id": prescricao.medicament_id
    }

def apresenta_prescricoes(prescricoes: List[Prescricao]):
    """Retorna uma visualização em lista conforme definido em PrescricaoListViewSchema
    """
    prescricao_lista = []
    for prescricao in prescricoes:
        prescricao_lista.append(apresenta_prescricao(prescricao))
    return {"prescricoes": prescricao_lista}