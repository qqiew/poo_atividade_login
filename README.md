Herança aplicada a um backend: a tela de login
Cada equipe cria o módulo de login (extremamente simplificado ) da API, seguindo exatamente o módulo produtos, que já está pronto no repositório. É a parte prática: o aplicativo manda nome e senha, e a API responde o que aquele usuário pode fazer. Quem decide as permissões é a herança que você estudou na aula 5.
Na Parte B cada equipe informar onde foi aplicado encapsulamento e herançaao próprio KiOferta e apresenta para a turma em dez minutos.

As duas partes são feitas pela mesma equipe, de três a quatro pessoas ja definidos.

O módulo de login
O que você recebe pronto
Arquivo	O que é
app/data/produtos_mock.py	Dados mockados dos produtos
app/models/produto.py	A model Produto e a função carregar_produtos()
app/controllers/produto_controller.py	O ProdutoController
app/routes/produto_routes.py	As rotas GET /api/produtos, GET /api/produtos/categoria/{categoria} e GET /api/produtos/{id}
app/data/usuarios_mock.py	Os usuários mockados que o seu login vai usar
main.py	Já liga o módulo produtos, com o import e o include_router
O módulo produtos é o modelo. Leia os quatro arquivos antes de começar: o caminho é sempre o mesmo.

main.py  ->  routes  ->  controller  ->  model  ->  data (mock)

Os dados mockados
# app/data/usuarios_mock.py
USUARIOS = [
    {'id': 1, 'nome': 'bia', 'senha': 'bia123', 'perfil': 'visitante'},
    {'id': 2, 'nome': 'ana', 'senha': 'ana123', 'perfil': 'contribuidor'},
    {'id': 3, 'nome': 'caio', 'senha': 'caio123', 'perfil': 'moderador'},
]

São três usuários com três perfis diferentes: cada um precisa virar um objeto de uma classe diferente. É assim que a herança da equipe é verificada.

Não altere este arquivo. A correção usa exatamente estes dados.

Dica: do texto do perfil para a classe
O mock guarda o perfil como texto, 'moderador'. A model precisa transformar esse texto na classe Moderador. Duas formas são aceitas:
# com if
if u['perfil'] == 'moderador':
    usuario = Moderador(u['id'], u['nome'], u['senha'])

# com um dicionário: em Python a própria classe é um objeto
PERFIS = {'visitante': Visitante, 'contribuidor': Contribuidor, 'moderador': Moderador}
usuario = PERFIS[u['perfil']](u['id'], u['nome'], u['senha'])

Esse if é permitido aqui, na hora de criar o objeto. Depois de criado, ninguém mais pergunta o perfil.

Como testar
uvicorn main:app --reload

Abra http://127.0.0.1:8000/docs e teste, nesta ordem:

Como entregar
ao clonar o repo, subam para o próprio github, mesmo feito em equipe cada membro sobe em sue github e o link do github no teams

---

## Módulo de login (notas de implementação)

O módulo de login segue exatamente a mesma estrutura em camadas do módulo `produtos`
(`main.py -> routes -> controller -> model -> data`):

| Arquivo | O que é |
| --- | --- |
| `app/data/usuarios_mock.py` | Usuários mockados (fornecido, não alterado) |
| `app/models/usuario.py` | Classe base `Usuario` e as subclasses `Visitante`, `Contribuidor` e `Moderador`, além da função `carregar_usuarios()` |
| `app/controllers/usuario_controller.py` | `UsuarioController`, expondo `login(nome, senha)` |
| `app/routes/usuario_routes.py` | Rota `POST /api/login` |

Cada um dos três perfis mockados vira uma instância de uma classe diferente,
encadeadas por herança: `Visitante -> Contribuidor -> Moderador`, em que cada
subclasse estende a lista de permissões da classe anterior via
`super().mostrar_permissoes()`. Veja [`PARTE_B.md`](PARTE_B.md) para o texto
completo sobre onde encapsulamento e herança foram aplicados no KiOferta.

### Como rodar localmente

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Abra `http://127.0.0.1:8000/docs` e teste `POST /api/login` com, por exemplo:

```json
{"nome": "caio", "senha": "caio123"}
```

que retorna:

```json
{"id": 3, "nome": "caio", "perfil": "moderador", "permissoes": ["ver_ofertas", "cadastrar_oferta", "remover_oferta", "banir_usuario"]}
```

Nome ou senha incorretos retornam `401 Unauthorized`.