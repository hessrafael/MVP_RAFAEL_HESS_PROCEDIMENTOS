import json
from conftest import SalaValue1, SalaValue2, ProcValue1, ProcValue2

"""Testing Salas
"""


def test_home_page(test_client):  
    response = test_client.get('/')
    assert response.status_code == 302

def test_add_sala(test_client):
    response = test_client.post('/sala',data={
        "numero":15
    })
    assert response.status_code == 200
    response_data = json.loads(response.data.decode('utf-8'))
    assert response_data["numero"] == 15
    SalaValue1.id = response_data["id"]

def test_get_sala(test_client):
    response = test_client.get(f'/sala?id={SalaValue1.id}')
    assert response.status_code == 200
    response_data = json.loads(response.data.decode('utf-8'))
    assert response_data["numero"] == 15

def test_add_same_sala(test_client):
    response = test_client.post('/sala',data={
        "numero":15
    })
    assert response.status_code == 409
    response_data = json.loads(response.data.decode('utf-8'))
    assert response_data["message"] == "Sala com mesmo id já salvo na base :/"

def test_add_second_sala(test_client):
    response = test_client.post('/sala',data={
        "numero":18
    })
    assert response.status_code == 200
    response_data = json.loads(response.data.decode('utf-8'))
    assert response_data["numero"] == 18
    SalaValue2.id = response_data["id"]

def test_get_all_salas(test_client):
    response = test_client.get('/all_salas')
    assert response.status_code == 200
    response_data = json.loads(response.data.decode('utf-8'))
    assert len(response_data["salas"]) == 2
    assert response_data["salas"][0]["id"] == SalaValue1.id
    assert response_data["salas"][0]["numero"] == 15
    assert response_data["salas"][1]["id"] == SalaValue2.id
    assert response_data["salas"][1]["numero"] == 18

"""Testing Procedimentos
"""
def test_add_proc_paciente_1(test_client):
    response = test_client.post('/procedimento',data={
        "description":"Amputação da perna",
        "start_time":"15/05/3000 10:00",
        "end_time":"15/05/3000 10:30",
        "paciente_id":"1",
        "room_id": SalaValue1.id
    })
    assert response.status_code == 200
    response_data = json.loads(response.data.decode('utf-8'))
    print(response_data)
    assert response_data["description"] == "Amputação da perna"
    assert response_data["room_id"] == SalaValue1.id
    assert response_data["start_time"] == "Thu, 15 May 3000 10:00:00 GMT"
    assert response_data["end_time"] == "Thu, 15 May 3000 10:30:00 GMT"
    assert response_data["paciente_id"] == "1"
    ProcValue1.id = response_data["id"]

def test_get_proc(test_client):
    response = test_client.get(f'/procedimento?id={ProcValue1.id}')
    assert response.status_code == 200
    response_data = json.loads(response.data.decode('utf-8'))
    assert response_data["description"] == "Amputação da perna"
    assert response_data["room_id"] == SalaValue1.id
    assert response_data["start_time"] == "Thu, 15 May 3000 10:00:00 GMT"
    assert response_data["end_time"] == "Thu, 15 May 3000 10:30:00 GMT"
    assert response_data["paciente_id"] == "1"

def test_alter_description_proc(test_client):
    response = test_client.put('/altera_descricao_procedimento',data={
            "description": "Nova Desc",
            "id": ProcValue1.id                 
    })
    print(response)
    assert response.status_code == 200
    response_data = json.loads(response.data.decode('utf-8'))
    assert response_data["description"] == "Nova Desc"
    assert response_data["room_id"] == SalaValue1.id
    assert response_data["start_time"] == "Thu, 15 May 3000 10:00:00 GMT"
    assert response_data["end_time"] == "Thu, 15 May 3000 10:30:00 GMT"
    assert response_data["paciente_id"] == "1"

def test_add_proc_paciente_1_same_time_ends_within(test_client):
    response = test_client.post('/procedimento',data={
        "description":"Amputação da perna",
        "start_time":"15/05/3000 09:00",
        "end_time":"15/05/3000 10:05",
        "paciente_id":"1",
        "room_id": SalaValue1.id
    })
    assert response.status_code == 400
    response_data = json.loads(response.data.decode('utf-8'))
    print(response_data)
    assert response_data["message"] == "Conflito de horários no agendamento de procedimentos"

def test_add_proc_paciente_1_same_time_begins_within(test_client):
    response = test_client.post('/procedimento',data={
        "description":"Amputação da perna",
        "start_time":"15/05/3000 10:05",
        "end_time":"15/05/3000 10:31",
        "paciente_id":"1",
        "room_id": SalaValue1.id
    })
    assert response.status_code == 400
    response_data = json.loads(response.data.decode('utf-8'))
    print(response_data)
    assert response_data["message"] == "Conflito de horários no agendamento de procedimentos"

def test_add_proc_paciente_1_same_time_all_within(test_client):
    response = test_client.post('/procedimento',data={
        "description":"Amputação da perna",
        "start_time":"15/05/3000 10:05",
        "end_time":"15/05/3000 10:25",
        "paciente_id":"1",
        "room_id": SalaValue1.id
    })
    assert response.status_code == 400
    response_data = json.loads(response.data.decode('utf-8'))
    print(response_data)
    assert response_data["message"] == "Conflito de horários no agendamento de procedimentos"

def test_add_proc_paciente_2(test_client):
    response = test_client.post('/procedimento',data={
        "description":"Transplante de Coração",
        "start_time":"15/05/1900 10:00",
        "end_time":"15/05/1900 10:30",
        "paciente_id":"2",
        "room_id": SalaValue2.id
    })
    assert response.status_code == 200
    response_data = json.loads(response.data.decode('utf-8'))
    print(response_data)
    assert response_data["description"] == "Transplante de Coração"
    assert response_data["room_id"] == SalaValue2.id
    assert response_data["start_time"] == "Tue, 15 May 1900 10:00:00 GMT"
    assert response_data["end_time"] == "Tue, 15 May 1900 10:30:00 GMT"
    assert response_data["paciente_id"] == "2"
    ProcValue2.id = response_data["id"]

def test_get_all_procs(test_client):
    response = test_client.get(f'/all_procedimentos')
    assert response.status_code == 200
    response_data = json.loads(response.data.decode('utf-8'))    
    assert len(response_data["procedimentos"]) == 2
    assert response_data["procedimentos"][0]["id"] == ProcValue1.id
    assert response_data["procedimentos"][0]["description"] == "Nova Desc"
    assert response_data["procedimentos"][0]["room_id"] == SalaValue1.id
    assert response_data["procedimentos"][0]["start_time"] == "Thu, 15 May 3000 10:00:00 GMT"
    assert response_data["procedimentos"][0]["end_time"] == "Thu, 15 May 3000 10:30:00 GMT"
    assert response_data["procedimentos"][0]["paciente_id"] == "1"
    assert response_data["procedimentos"][1]["id"] == ProcValue2.id
    assert response_data["procedimentos"][1]["description"] == "Transplante de Coração"
    assert response_data["procedimentos"][1]["room_id"] == SalaValue2.id
    assert response_data["procedimentos"][1]["start_time"] == "Tue, 15 May 1900 10:00:00 GMT"
    assert response_data["procedimentos"][1]["end_time"] == "Tue, 15 May 1900 10:30:00 GMT"
    assert response_data["procedimentos"][1]["paciente_id"] == "2"

def test_get_proc_paciente_1(test_client):
    response = test_client.get(f'/procedimentos_paciente?id=1')
    assert response.status_code == 200
    response_data = json.loads(response.data.decode('utf-8'))
    assert len(response_data["procedimentos"]) == 1
    assert response_data["procedimentos"][0]["id"] == ProcValue1.id
    assert response_data["procedimentos"][0]["description"] == "Nova Desc"
    assert response_data["procedimentos"][0]["room_id"] == SalaValue1.id
    assert response_data["procedimentos"][0]["start_time"] == "Thu, 15 May 3000 10:00:00 GMT"
    assert response_data["procedimentos"][0]["end_time"] == "Thu, 15 May 3000 10:30:00 GMT"
    assert response_data["procedimentos"][0]["paciente_id"] == "1"

def test_delete_proc_from_past(test_client):
    response = test_client.delete(f'/delete_procedimentos',json={
        "ids": [
            {
                "id": ProcValue2.id
            }
        ]
    })
    assert response.status_code == 200
    response_data = json.loads(response.data.decode('utf-8'))
    assert len(response_data["procedimentos"]) == 0

def test_delete_proc_with_no_presc(test_client):
    response = test_client.delete(f'/delete_procedimentos',json={
        "ids": [
            {
                "id": ProcValue1.id
            }
        ]
    })
    assert response.status_code == 200
    response_data = json.loads(response.data.decode('utf-8'))
    assert len(response_data["procedimentos"]) == 1
    assert response_data["procedimentos"][0]["id"] == ProcValue1.id
    assert response_data["procedimentos"][0]["description"] == "Nova Desc"
    assert response_data["procedimentos"][0]["room_id"] == SalaValue1.id
    assert response_data["procedimentos"][0]["start_time"] == "Thu, 15 May 3000 10:00:00 GMT"
    assert response_data["procedimentos"][0]["end_time"] == "Thu, 15 May 3000 10:30:00 GMT"
    assert response_data["procedimentos"][0]["paciente_id"] == "1"

