from app.models.usuario import carregar_usuarios


class UsuarioController:
    def __init__(self):
        self._usuarios = carregar_usuarios()

    def login(self, nome, senha):
        for usuario in self._usuarios:
            if usuario.mostrar_nome() == nome and usuario.verificar_senha(senha):
                return self._para_dicionario(usuario)
        return None

    def _para_dicionario(self, usuario):
        return {
            'id': usuario.mostrar_id(),
            'nome': usuario.mostrar_nome(),
            'perfil': usuario.mostrar_perfil(),
            'permissoes': usuario.mostrar_permissoes(),
        }
