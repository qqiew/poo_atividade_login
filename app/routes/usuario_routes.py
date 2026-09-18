from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.controllers.usuario_controller import UsuarioController

router = APIRouter(prefix='/api', tags=['login'])
controller = UsuarioController()


class LoginRequest(BaseModel):
    nome: str
    senha: str


@router.post('/login')
def login(dados: LoginRequest):
    usuario = controller.login(dados.nome, dados.senha)
    if usuario is None:
        raise HTTPException(401, 'usuário ou senha inválidos')
    return usuario
