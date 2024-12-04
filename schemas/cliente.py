from pydantic import BaseModel
from typing import Optional, List
from model.cliente import Cliente


class ClienteSchema(BaseModel):
    """ Define como um novo cliente a ser inserido deve ser representado
    """
    nome: str = "Antonio da Silva"
    email: str = "antonio@gmail.com"
    cep: int = 89022450
    rua: str = "Rua Capinzal"
    complemento: str = "Casa 2"
    numero: int = 2580
    bairro: str = "Garcia"
    cidade: str = "Blumenal"
    uf: str = "SC"

class UpdateClienteSchema(BaseModel):
    """ Define como um cliente a ser editado deve ser representado
    """
    nome: str = "Antonio da Silva"
    email: str = "antonio@gmail.com"
    cep: int = 89022450
    rua: str = "Rua Capinzal"
    complemento: str = "Casa 2"
    numero: int = 2580
    bairro: str = "Garcia"
    cidade: str = "Blumenal"
    uf: str = "SC"

class UpdateClienteByIdSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca para editar. Que será
        feita apenas com base no id do cliente.
    """
    id: int = 1

class ClienteBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id do cliente.
    """
    id: int = 1

class ClienteBuscaDelSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca para deletar. Que será
        feita apenas com base no id do cliente.
    """
    id: int = 1

class ListagemClienteSchema(BaseModel):
    """ Define como uma listagem de clientes será retornada.
    """
    cliente: List[ClienteSchema]


def apresenta_clientes(clientes: List[Cliente]):
    """ Retorna uma representação do cliente seguindo o schema definido em
        ClienteViewSchema.
    """
    result = []
    for cliente in clientes:
        result.append({
            "id": cliente.id,
            "nome": cliente.nome,
            "email": cliente.email,
            "cep": cliente.cep,
            "rua": cliente.rua,
            "complemento": cliente.complemento,
            "numero": cliente.numero,
            "bairro": cliente.bairro,
            "cidade": cliente.cidade,
            "uf": cliente.uf,
            "data": cliente.data
        })

    return {"clientes": result}


class ClienteViewSchema(BaseModel):
    """ Define como um cliente será retornado.
    """
    id: int = 1
    nome: str = "Antonio da Silva"
    email: str = "antonio@gmail.com"
    cep: int = 89022450
    rua: str = "Rua Capinzal"
    complemento: str = "Casa 2"
    numero: int = 2580
    bairro: str = "Garcia"
    cidade: str = "Blumenal"
    uf: str = "SC"


class ClienteDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    id: int


def apresenta_cliente(cliente: Cliente):
    """ Retorna uma representação do cliente seguindo o schema definido em
        ClienteViewSchema.
    """
    return {
        "id": cliente.id,
        "nome": cliente.nome,
        "email": cliente.email,
        "cep": cliente.cep,
        "rua": cliente.rua,
        "complemento": cliente.complemento,
        "numero": cliente.numero,
        "bairro": cliente.bairro,
        "cidade": cliente.cidade,
        "uf": cliente.uf,
        "data" : cliente.data
    }
