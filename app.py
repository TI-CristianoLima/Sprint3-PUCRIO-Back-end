from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote
from sqlalchemy.exc import IntegrityError
from model import Session, Cliente
from logger import logger
from schemas import *
from flask_cors import CORS


info = Info(title="API de Clientes",
            description="Gerenciamento de clientes", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definindo as tags para documentação
home_tag = Tag(name="Documentação",
               description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
cliente_tag = Tag(
    name="Cliente", description="Adição, visualização, edição e exclusão de clientes à base de dados")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/cliente', tags=[cliente_tag], responses={"200": ClienteViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_cliente(form: ClienteSchema):
    """
    Adiciona um novo cliente a base de dados
    Retorna uma representação dos clientes adicionados
    """

    cliente = Cliente(
        nome=form.nome,
        email=form.email,
        cep=form.cep,
        rua=form.rua,
        complemento=form.complemento,
        numero=form.numero,
        bairro=form.bairro,
        cidade=form.cidade,
        uf=form.uf
    )
    logger.debug(f"Adicionado Cliente: '{cliente.nome}'")
    try:
        # Criando conexão com a base de dados
        session = Session()

        # Adicionando o produto
        session.add(cliente)

        # Efetivando o comando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado cliente: '{cliente.nome}'")

        return apresenta_cliente(cliente), 200

    except IntegrityError as e:
        # Como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Cliente de mesmo nome já salvo na base :/"
        logger.warning(
            f"Erro ao adicionar cliente '{cliente.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # Como um erro fora do previsto
        error_msg = "Não foi possível salvar novo cliente :/"
        logger.warning(
            f"Erro ao adicionar cliente '{cliente.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/clientes', tags=[cliente_tag], responses={"200": ListagemClienteSchema, "404": ErrorSchema})
def get_clientes():
    """
    Faz a busca por todos os clientes cadastrados e retorna uma representação da listagem de clientes.
    """

    logger.debug(f"Coletando clientes")
    # Criando conexão com o banco de dados
    session = Session()
    # Fazebo a busca
    clientes = session.query(Cliente).all()

    if not clientes:
        # Se não há produtos cadastrados
        return {"clientes": []}, 200
    else:
        logger.debug(f"%d clientes encontrados" % len(clientes))
        # Retorna a representação de produtos
        print(clientes)
        return apresenta_clientes(clientes), 200


@app.put('/cliente', tags=[cliente_tag], responses={"200": UpdateClienteSchema, "404": ErrorSchema})
def update_cliente(query: UpdateClienteByIdSchema, form: UpdateClienteSchema):
    """
    Faz a busca por um cliente a partir do id do cliente, edita e retorna uma representação do cliente.
    """
    cliente_id = query.id
    logger.debug(f"Coletando dados sobre produto #{cliente_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    cliente = session.query(Cliente).filter(Cliente.id == cliente_id).first()

    if not cliente:
        # se o cliente não foi encontrado
        error_msg = "Cliente não encontrado na base :/"
        logger.warning(f"Erro ao buscar cliente '{cliente_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        cliente.nome = form.nome
        cliente.email = form.email
        cliente.cep = form.cep
        cliente.rua = form.rua
        cliente.complemento = form.complemento
        cliente.numero = form.numero
        cliente.bairro = form.bairro
        cliente.cidade = form.cidade
        cliente.uf = form.uf

        logger.debug(f"Cliente editado: '{cliente.nome}'")
    try:
        # Criando conexão com a base de dados
        # session = Session()

        # Adicionando o cliente
        # session.add(cliente)

        # Efetivando o comando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Cliente editado: '{cliente.nome}'")

        return apresenta_cliente(cliente), 200
    except IntegrityError as e:
        # Como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Erro ao editar cliente :/"
        logger.warning(
            f"Erro ao adicionar cliente '{cliente.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # Como um erro fora do previsto
        error_msg = "Não foi possível editar cliente :/"
        logger.warning(f"Erro ao editar cliente '{cliente.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/cliente', tags=[cliente_tag], responses={"200": ClienteViewSchema, "404": ErrorSchema})
def get_cliente(query: ClienteBuscaSchema):
    """
    Faz a busca por um cliente a partir do id do cliente retorna uma representação do cliente.
    """
    cliente_id = query.id
    logger.debug(f"Coletando dados sobre produto #{cliente_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    cliente = session.query(Cliente).filter(Cliente.id == cliente_id).first()

    if not cliente:
        # se o cliente não foi encontrado
        error_msg = "Cliente não encontrado na base :/"
        logger.warning(f"Erro ao buscar cliente '{cliente_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Cliente econtrado: '{cliente.nome}'")
        # retorna a representação de cliente
        return apresenta_cliente(cliente), 200


@app.delete('/cliente', tags=[cliente_tag],
            responses={"200": ClienteDelSchema, "404": ErrorSchema})
def del_cliente(query: ClienteBuscaDelSchema):
    """Deleta um Cliente a partir do id de cliente informado

    Retorna uma mensagem de confirmação da remoção.
    """
    cliente_id = query.id
    print(cliente_id)
    logger.debug(f"Deletando dados sobre cliente #{cliente_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Cliente).filter(Cliente.id == cliente_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado cliente #{cliente_id}")
        return {"mesage": "Cliente removido", "ID": cliente_id}
    else:
        # se o cliente não foi encontrado
        error_msg = "Cliente não encontrado na base :/"
        logger.warning(f"Erro ao deletar cliente #'{cliente_id}', {error_msg}")
        return {"mesage": error_msg}, 404
