from datetime import datetime, timezone
from uuid import UUID, uuid4
from fastapi import HTTPException
from app.schemas.cliente import ClienteCreate, ClienteRead, ClienteUpdate

class ClienteDB(ClienteCreate):
    id: UUID
    ativo: bool
    created_at: datetime


_cliente: dict[UUID, ClienteDB] = {}

def criar(dados: ClienteCreate) -> ClienteDB:
    if dados.cnpj:

        cnpj_existe = any(cliente.cnpj == dados.cnpj for cliente in _cliente.values())

        if cnpj_existe:
            raise HTTPException(
                status_code=409,
                detail="Já existe um cliente cadastrado com este CNPJ!"
            )

    novo_cliente = ClienteDB(
        **dados.model_dump(),
        id=uuid4(),
        ativo=True,
        created_at=datetime.now(timezone.utc)
    )
    _cliente[novo_cliente.id] = novo_cliente
    return novo_cliente
        

def listar(ativo: bool | None = None) -> list[ClienteRead]:

    return [
        c for c in _cliente.values() 
        if (ativo is None) or (c.ativo == ativo)
    ]


def obter(cliente_id: UUID) -> ClienteRead:
    if not cliente_id == _cliente.values():
        raise HTTPException(
            status_code=404,
            detail="Nenhum cliente encontrado"
        )
    else:
        encontrado = [c for c in _cliente.values()  if cliente_id]
        return encontrado

def atualizar(cliente_id: UUID, dados:ClienteUpdate) -> ClienteRead:
    cliente = obter(cliente_id)
    valoresParaAtualizar = dados.model_dump(exclude_unset=True)

    if "cnpj" in valoresParaAtualizar:
        cnpjJaExiste = any(c.cnpj == dados.cnpj for id_cadastrado, c in _cliente.items() if id_cadastrado != cliente_id)

        if cnpjJaExiste:
            raise HTTPException(
                status_code=409,
                 detail="Este CNPJ já está cadastrado."
            )
    
    clienteAtualizado = cliente.model_copy(update=valoresParaAtualizar)
    _cliente[cliente_id] = clienteAtualizado

    return ClienteRead.model_validade(clienteAtualizado)
        
    

def deletar(cliente_id: UUID) -> None:
    cliente = obter(cliente_id)
    clienteDesativado = cliente.model_copy(update = {"ative": False})

    _cliente[cliente_id] = clienteDesativado