from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from typing import Union

from model import Base


class Cliente(Base):
    __tablename__ = 'cliente'

    id = Column("pk_cliente", Integer, primary_key=True)
    nome = Column(String(140), unique=True)
    email = Column(String(140), unique=True)
    cep = Column(Integer)
    rua = Column(String(140))
    complemento = Column(String(50))
    numero = Column(Integer)
    bairro = Column(String)
    cidade = Column(String)
    uf = Column(String)
    data = Column(DateTime, default=datetime.now())

    def __init__(self, nome: str, email: str, cep: int, rua: str, complemento: str, numero: int, bairro: str, cidade: str, uf: str,
                 data: Union[DateTime, None] = None):
        """
        Cria um Cliente

        Arguments:
            nome: nome do cliente.
            email: email do cliente
            cep: cep do cliente preenchido automaticamente pela api em caso de cep valido
            endereco: endereco do cliente preenchido automaticamente pela api em caso de cep valido
            complemento: complemento do endereco
            numero: numero do imovel
            bairro: bairro do cliente  preenchido automaticamente pela api em caso de cep valido
            cidade: cidade do cliente  preenchido automaticamente pela api em caso de cep valido
            uf: uf do cliente  preenchido automaticamente pela api em caso de cep valido
            data_insercao: data de quando o produto foi inserido à base
        """
        self.nome = nome
        self.email = email
        self.cep = cep
        self.rua = rua
        self.complemento = complemento
        self.numero = numero
        self.bairro = bairro
        self.cidade = cidade
        self.uf = uf

        # se não for informada, será o data exata da inserção no banco
        if data:
            self.data = data
