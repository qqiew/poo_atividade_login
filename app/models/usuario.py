from app.data.usuarios_mock import USUARIOS


class Usuario:
    def __init__(self, id, nome, senha):
        self._id = id
        self.alterar_nome(nome)
        self._senha = senha

    def mostrar_id(self):
        return self._id

    def mostrar_nome(self):
        return self._nome

    def alterar_nome(self, novo_nome):
        if novo_nome.strip() == '':
            raise ValueError('nome não pode ser vazio')
        self._nome = novo_nome.strip()

    def verificar_senha(self, senha):
        return self._senha == senha

    def mostrar_perfil(self):
        return self.__class__.__name__.lower()

    def mostrar_permissoes(self):
        return []

    def __repr__(self):
        return f'{self.__class__.__name__}({self._nome})'


class Visitante(Usuario):
    def mostrar_permissoes(self):
        return ['ver_ofertas']


class Contribuidor(Visitante):
    def mostrar_permissoes(self):
        return super().mostrar_permissoes() + ['cadastrar_oferta']


class Moderador(Contribuidor):
    def mostrar_permissoes(self):
        return super().mostrar_permissoes() + ['remover_oferta', 'banir_usuario']


PERFIS = {
    'visitante': Visitante,
    'contribuidor': Contribuidor,
    'moderador': Moderador,
}


def carregar_usuarios():
    return [PERFIS[u['perfil']](u['id'], u['nome'], u['senha']) for u in USUARIOS]
