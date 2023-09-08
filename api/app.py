from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, url_for
from urllib.parse import unquote
import requests
import json

from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, or_

from models import Session, Sala, Prescricao, Procedimento
#from logger import logger
from schemas import *
from flask_cors import CORS
import datetime

info = Info(title="API gestão Procedimentos", version="1.0.0")
app = OpenAPI(__name__, info=info)
app.config["DEBUG"] = True
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
procedimento_tag = Tag(name="Procedimentos", description="Adição, visualização e remoção de Procedimentos à base")
prescricao_tag = Tag(name="Prescrições", description="Adição, visualização e remoção de Prescrições à base")
sala_tag = Tag(name="Salas", description="Adição, visualização e remoção de Salas à base")

#### SALAS ####----

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi') 

@app.post('/sala', tags=[sala_tag],
          responses={"200":SalaViewSchema,"400":ErrorSchema, "409":ErrorSchema})
def add_sala(form: SalaSchema):
    """Adiciona uma nova sala no banco de dados
    """
    try:
        sala = Sala(room_number=form.numero)
    except:
        error_msg = "Valores inválidos de parametros para nova instância de Sala"
        return {"message": error_msg}, 400
    
    try:
        # criando conexão com a base
        session = Session()
        # adicionando instancia
        session.add(sala)
        # efetivando o camando de adição de instancia
        session.commit()
        return apresenta_sala(sala), 200

    except IntegrityError as e:
        error_msg = "Sala com mesmo id já salvo na base :/"
        return {"message": error_msg}, 409   
    
    
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar nova Sala :/"
        return {"message": error_msg}, 400

@app.get('/sala', tags=[sala_tag],
         responses={"200":SalaViewSchema,"400":ErrorSchema, "404":ErrorSchema})
def get_sala(query: SalaBuscaIDSchema):
    """Retorna dados da sala com base no ID
    """
    try:
        # criando conexão com o banco
        session = Session()
        # buscando todas as instâncias ativas
        sala = session.query(Sala).filter(Sala.is_active == True, Sala.room_id == query.id).first()
        if not sala:
            error_msg = 'Nenhuma sala encontrado com o id'
            return {"message": error_msg},404
        else:
            #retorna a sala
            return apresenta_sala(sala), 200
    except Exception as e:
        error_msg = "Não foi possível realizar a consulta de sala"
        return {"message": error_msg}, 400

@app.get('/all_salas',tags=[sala_tag],
         responses={"200":SalaListViewSchema,"400":ErrorSchema, "404":ErrorSchema})
def get_all_salas():
    """Retorna todos as salas cadastrados no banco
    """
    try:
        # criando conexão com o banco
        session = Session()
        # buscando todas as instâncias ativas
        salas = session.query(Sala).filter(Sala.is_active == True).all()

        if not salas:
            error_msg = 'Nenhuma sala encontrada'
            return {"message": error_msg},404
        else:
            #retorna as salas
            return apresenta_salas(salas), 200
    except Exception as e:
        error_msg = "Não foi possível realizar a consulta de salas"
        return {"message": error_msg}, 400

#### PROCEDIMENTOS ####----

@app.post('/procedimento',tags=[procedimento_tag],
          responses={"200":ProcedimentoViewSchema,"400":ErrorSchema, "409":ErrorSchema})
def add_procedimento(form: ProcedimentoSchema):
    """Cadastra um novo procedimento na base de dados
    """
    try:
        parsed_start = datetime.datetime.strptime(form.start_time, '%d/%m/%Y %H:%M')
        parsed_end = datetime.datetime.strptime(form.end_time,'%d/%m/%Y %H:%M')        
    except:
        error_msg = "Valores inválidos de horários de início e fim. Deve ser no formato dd/mm/aaaa hh:mm"
        return {"message": error_msg}, 400

    try:
        procedimento = Procedimento(start_time=parsed_start,end_time=parsed_end,description=form.description,room_id=form.room_id,paciente_id=form.paciente_id)
    except:
        error_msg = "Valores inválidos de parametros para nova instância de Procedimento"
        return {"message": error_msg}, 400
      
    
    try:
        # criando conexão com a base
        session = Session()

        #consultando se há alguma sobreposição de procedimentos para uma mesma sala
        session = Session()
        procedimentos = session.query(Procedimento).filter(
            Procedimento.is_active == True,Procedimento.room_id == form.room_id,
            or_(
                and_(
                    Procedimento.start_time < parsed_end,
                    Procedimento.end_time > parsed_start
                ),
                and_(
                    Procedimento.start_time < parsed_end,
                    Procedimento.end_time > parsed_start
                ),
                and_(
                    Procedimento.start_time >= parsed_start,
                    Procedimento.end_time <= parsed_end
                )
                )).all()

        if procedimentos:
            error_msg = "Conflito de horários no agendamento de procedimentos"
            return {"message": error_msg}, 400
        else:
            # adicionando instancia
            session.add(procedimento)
            # efetivando o camando de adição de instancia
            session.commit()
            return apresenta_procedimento(procedimento), 200

    except IntegrityError as e:
        error_msg = "Procedimento com mesmo id já salvo na base :/"
        return {"message": error_msg}, 409   
    
    
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo Procedimento :/"
        return {"message": error_msg}, 400

@app.get('/procedimento',tags=[procedimento_tag],
         responses={"200":ProcedimentoViewSchema,"400":ErrorSchema, "404":ErrorSchema})
def get_procedimento(query: ProcedimentoBuscaIDSchema):
    """Retorna procedimento com base no seu ID
    """
    try:
        # criando conexão com o banco
        session = Session()
        # buscando todas as instâncias ativas
        procedimento = session.query(Procedimento).filter(Procedimento.is_active == True, Procedimento.proceeding_id == query.id).first()
        if not procedimento:
            error_msg = 'Nenhuma procedimento encontrado com o id'
            return {"message": error_msg},404
        else:
            #retorna os procedimentos
            return apresenta_procedimento(procedimento), 200
    except Exception as e:
        error_msg = "Não foi possível realizar a consulta de procedimento"
        return {"message": error_msg}, 400

@app.get('/procedimentos_paciente',tags=[procedimento_tag],
         responses={"200":ProcedimentoListViewSchema,"400":ErrorSchema, "404":ErrorSchema})
def get_procedimentos_paciente(query: ProcedimentoBuscaIDSchema):
    """Retorna procedimento com base no ID do paciente
    """
    try:
        # criando conexão com o banco
        session = Session()
        # buscando todas as instâncias ativas
        procedimentos = session.query(Procedimento).filter(Procedimento.is_active == True, Procedimento.paciente_id == query.id).all()
        if not procedimentos:
            error_msg = 'Nenhum procedimento encontrado para o paciente'
            return {"message": error_msg},404
        else:
            #retorna os procedimentos
            return apresenta_procedimentos(procedimentos), 200
    except Exception as e:
        error_msg = "Não foi possível realizar a consulta de procedimento"
        return {"message": error_msg}, 400

@app.get('/all_procedimentos',tags=[procedimento_tag],
         responses={"200":ProcedimentoListViewSchema,"400":ErrorSchema, "404":ErrorSchema})
def get_all_procedimentos():
    """Retorna todos os procedimentos ativos
    """
    try:
        # criando conexão com o banco
        session = Session()
        # buscando todas as instâncias ativas
        procedimentos = session.query(Procedimento).filter(Procedimento.is_active == True).all()

        if not procedimentos:
            error_msg = 'Nenhum procedimento encontrado'
            return {"message": error_msg},404
        else:
            #retorna os procedimentos
            return apresenta_procedimentos(procedimentos), 200
    except Exception as e:
        error_msg = "Não foi possível realizar a consulta de procedimentos"
        return {"message": error_msg}, 400


@app.put('/altera_descricao_procedimento', tags=[procedimento_tag],
         responses={"200":ProcedimentoViewSchema,"400":ErrorSchema, "404":ErrorSchema})
def altera_descricao_procedimento(form: ProcedimentoAlteraDescSchema):
    """Permite alterar a descrição de um procedimento já criado
    """
    try:
        
        #cria a session
        session = Session()
        #busca o procedimento
        procedimento = session.query(Procedimento).filter(Procedimento.is_active == True, Procedimento.proceeding_id == form.id).first()
        
        #verifica se o procedimento existe
        if not procedimento:
            error_msg = 'Procedimento não encontrado no banco'
            return {"message": error_msg}, 404
        else:
            procedimento.description = form.description
            session.commit()
            return apresenta_procedimento(procedimento), 200
    
    except Exception as e:
        error_msg = "Não foi possível realizar a alteração da descrição do procedimento"
        return {"message": error_msg}, 400

@app.delete('/delete_procedimentos', tags=[procedimento_tag],
            responses={"200":ProcedimentoListViewSchema,"400":ErrorSchema, "404":ErrorSchema})
def delete_procedimentos(body: ProcedimentoListBuscaIDSchema):
    """Deleta um ou mais procedimentos 
    """
    try:
        #pegando todos os ids
        list_ids = [obj.id for obj in body.ids]
        # criando conexão com o banco
        session = Session()
        # buscando todas a instância ativas de procedimentos que ainda não ocorreram
        procedimentos = session.query(Procedimento).filter(Procedimento.is_active == True, Procedimento.proceeding_id.in_(list_ids), Procedimento.start_time > datetime.datetime.now()).all()
        if not procedimentos:
            return apresenta_procedimentos(procedimentos), 200
        else:
            proceeding_ids = [procedimento.proceeding_id for procedimento in procedimentos]
            #busca todas as prescricoes ativas relacionadas ao procedimento
            prescricoes = session.query(Prescricao).filter(Prescricao.is_active == True, Prescricao.proceeding_id.in_(proceeding_ids)).all()
            prescription_ids = [PrescricaoBuscaIDSchema(id=prescricao.prescription_id) for prescricao in prescricoes]
            
            #deleta prescrições            
            response, status = delete_multi_prescricoes(PrescricaoListBuscaIDSchema(ids=prescription_ids))

            if status != 200:
                #se deu erro, retorna erro
                error_msg = "Não foi possível realizar a deleção dos procedimentos por causa das prescricoes associadas"
                return {"message": error_msg}, 400
            else:
                #se deu certo, deleta os procedimentos
                for procedimento in procedimentos:
                    # Deletando
                    procedimento.is_active = False  
                session.commit()
                return apresenta_procedimentos(procedimentos), 200            
    
    except Exception as e:
        error_msg = "Não foi possível realizar a deleção dos procedimentos"
        return {"message": error_msg}, 400

    
#### PRESCRIÇÕES ####----
@app.post('/prescricao',tags=[prescricao_tag],
          responses={"200":PrescricaoViewSchema,"400":ErrorSchema, "404":ErrorSchema})
def add_prescricao(form: PrescricaoSchema):
    """Adiciona uma prescrição de um medicamento para um procedimento
    """    
    
    
    try:
        #verifica se o procedimento existe
        session = Session()
        #busca o procedimento
        procedimento = session.query(Procedimento).filter(Procedimento.is_active == True, Procedimento.proceeding_id == form.proceeding_id).first()

        if not procedimento:
            error_msg = 'Procedimento não encontrado no banco'
            return {"message": error_msg}, 404
        else:
            try:
                #verifica o estoque do medicamento prescrito junto ao servico de medicamentos
                response =  requests.get(f'http://127.0.0.1:5001/medicamento?id={form.medicament_id}')
                if response.status_code == 200:
                    data = response.json()
                    estoque_med = data.get('quantidade')
                    if estoque_med < form.quantity:
                        error_msg = 'Valor prescrito maior que o estoque'
                        return {"message": error_msg}, 400
                    else:
                        # Monta o payload de consumo dos medicamentos a serem consumidos com base na estrutura esperada
                        payload = {
                            "medicamentos": [
                                {
                                    "consumed_refilled_quantity": form.quantity,
                                    "id": form.medicament_id
                                }                        
                            ]
                        }
                        
                        #decrementa o medicamento
                        headers = {'Content-Type': 'application/json'}
                        response = requests.put('http://127.0.0.1:5001/consome_medicamentos',data=json.dumps(payload),headers=headers)
                        
                        if response.status_code != 200:
                            error_msg = response.json().get('message')
                            return {"message": error_msg}, response.status_code

                else:
                    error_msg = response.json().get('message')
                    return {"message": error_msg}, response.status_code
            
            except Exception as e:
                error_msg = 'Não foi possível consumir os medicamentos'
                return {"message": error_msg}, 400
            
            prescricao = Prescricao(quantity=form.quantity, proceeding_id=form.proceeding_id,medicament_id=form.medicament_id)
            session.add(prescricao)
            session.commit()
            return apresenta_prescricao(prescricao), 200
    
    except Exception as e:
        error_msg = "Não foi possível cadastrar a prescrição"
        return {"message": error_msg}, 400

@app.get('/prescricao',tags=[prescricao_tag],
         responses={"200":PrescricaoViewSchema,"400":ErrorSchema, "404":ErrorSchema})
def get_prescricao(query: PrescricaoBuscaIDSchema):
    """Retorna prescricao com base no ID da prescricao
    """
    try:
        # criando conexão com o banco
        session = Session()
        # buscando todas as instâncias ativas
        prescricao = session.query(Prescricao).filter(Prescricao.is_active == True, Prescricao.prescription_id == query.id).first()
        if not prescricao:
            error_msg = 'Nenhuma prescricao encontrada com o ID'
            return {"message": error_msg},404
        else:
            #retorna as prescricoes
            return apresenta_prescricao(prescricao), 200
    except Exception as e:
        error_msg = "Não foi possível realizar a consulta de prescricao"
        return {"message": error_msg}, 400

@app.get('/prescricao_procedimento',tags=[prescricao_tag],
         responses={"200":PrescricaoListViewSchema,"400":ErrorSchema, "404":ErrorSchema})
def get_prescricao_procedimento(query: ProcedimentoBuscaIDSchema):
    """Retorna todas prescricoes associadas a um procedimento
    """
    try:
        # criando conexão com o banco
        session = Session()
        # buscando todas as instâncias ativas
        prescricoes = session.query(Prescricao).filter(Prescricao.is_active == True, Prescricao.proceeding_id == query.id).all()
        if not prescricoes:
            error_msg = 'Nenhuma prescricao encontrada para o procedimento'
            return {"message": error_msg},404
        else:
            #retorna as prescricoes
            return apresenta_prescricoes(prescricoes), 200
    except Exception as e:
        error_msg = "Não foi possível realizar a consulta de prescricao"
        return {"message": error_msg}, 400

@app.get('/prescricao_medicamento',tags=[prescricao_tag],
         responses={"200":PrescricaoListViewSchema,"400":ErrorSchema, "404":ErrorSchema})
def get_prescricao_medicamento(query: PrescricaoBuscaIDSchema):
    """Retorna todas prescricoes associadas a um medicamento
    """
    try:
        # criando conexão com o banco
        session = Session()
        # buscando todas as instâncias ativas
        prescricoes = session.query(Prescricao).filter(Prescricao.is_active == True, Prescricao.medicament_id == query.id).all()
        if not prescricoes:
            error_msg = 'Nenhuma prescricao encontrada para o medicamento'
            return {"message": error_msg},404
        else:
            #retorna as prescricoes
            return apresenta_prescricoes(prescricoes), 200
    except Exception as e:
        error_msg = "Não foi possível realizar a consulta de prescricao"
        return {"message": error_msg}, 400

    
@app.delete('/delete_prescricoes',tags=[prescricao_tag],
            responses={"200":PrescricaoListViewSchema,"400":ErrorSchema, "404":ErrorSchema})
def delete_prescricoes(body: PrescricaoListBuscaIDSchema):
    """Deleta uma ou mais prescrição com base no ID e repoe o estoque de medicamento
    """
    return delete_multi_prescricoes(body)


def delete_multi_prescricoes(body: PrescricaoListBuscaIDSchema):
    try:
        #pegando todos os ids
        list_ids = [obj.id for obj in body.ids]
        # criando conexão com o banco
        session = Session()
        # buscando todas a instância ativas
        prescricoes = session.query(Prescricao).filter(Prescricao.is_active == True, Prescricao.prescription_id.in_(list_ids)).all()

        if not prescricoes:
            # Se não há prescricores deletaveis, retorna nenhuma prescricao
            return apresenta_prescricoes(prescricoes), 200
        else:
           
            prescription_e_medicament_e_quantity_e_proceeding = [(prescricao.prescription_id, prescricao.medicament_id, prescricao.quantity, prescricao.proceeding_id) for prescricao in prescricoes]
            # Filtrando apenas as prescrições cujos procedimentos ainda não aconteceram
            prescription_e_medicament_e_quantity_e_proceeding_deletaveis = []
            for prescription_id, medicament_id, quantity, proceeding_id in prescription_e_medicament_e_quantity_e_proceeding:
                procedimento = session.query(Procedimento).filter(Procedimento.is_active == True, Procedimento.proceeding_id == proceeding_id, Procedimento.start_time > datetime.datetime.now()).first()
                if not procedimento:
                    pass
                else:
                    prescription_e_medicament_e_quantity_e_proceeding_deletaveis.append((prescription_id,medicament_id, quantity, proceeding_id))

            if not prescription_e_medicament_e_quantity_e_proceeding_deletaveis:
                # Se não há prescricores deletaveis, retorna nenhuma prescricao
                return apresenta_prescricoes(prescription_e_medicament_e_quantity_e_proceeding_deletaveis), 200
            
            else:
                # Filtra apenas as prescrições que iremos deletar
                prescricoes_deletar = []
                prescricoes_id_deletar = [el[0] for el in prescription_e_medicament_e_quantity_e_proceeding_deletaveis]                
                for prescricao in prescricoes:
                    if prescricao.prescription_id in prescricoes_id_deletar:
                        prescricoes_deletar.append(prescricao)

                # Monta o payload de retorno dos medicamentos a serem retornado com base na estrutura esperada
                payload = {
                    "medicamentos": [
                        {
                            "consumed_refilled_quantity": qty,
                            "id": med_id
                        }
                        for presc_id, med_id, qty, proc_id in prescription_e_medicament_e_quantity_e_proceeding_deletaveis
                    ]
                }
                
                # Repoe todos os medicamentos associados a prescricao
                headers = {'Content-Type': 'application/json'}
                try:
                    response = requests.put('http://127.0.0.1:5001/repoe_medicamentos',data=json.dumps(payload),headers=headers)
                except Exception as e:
                    error_msg = 'Não foi possível prosseguir com a reposição de medicamentos'
                    return {"message": error_msg}, 400
                if response.status_code != 200:
                    error_msg = response.json().get('message')
                    return {"message": error_msg}, response.status_code 
                else:
                    #se deu certo, deleta as prescricoes que são deletáveis
                    for prescricao in prescricoes_deletar:
                        prescricao.is_active = False  
                    session.commit()
                    return apresenta_prescricoes(prescricoes_deletar), 200            
    
    except Exception as e:
        error_msg = "Não foi possível realizar a deleção das prescricoes"
        return {"message": error_msg}, 400
