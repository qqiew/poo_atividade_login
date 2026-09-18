# Parte B — Encapsulamento e Herança no KiOferta

Roteiro para a apresentação de dez minutos: onde a equipe aplicou encapsulamento
e herança no backend do KiOferta.

## Encapsulamento

Todas as models do projeto guardam seu estado em atributos "protegidos" (convenção
`_nome`) e só os expõem por meio de métodos `mostrar_*` (getter) e `alterar_*`
(setter), que validam a entrada antes de alterar o atributo:

- `Produto` (`app/models/produto.py`) — `alterar_nome` rejeita nome vazio,
  `alterar_preco` rejeita preço negativo. Nada fora da classe escreve diretamente
  em `_nome` ou `_preco`.
- `Mercado` (`app/models/mercado.py`) — `alterar_localizacao` valida se latitude
  e longitude estão dentro dos intervalos válidos antes de armazená-las.
- `Oferta` (`app/models/oferta.py`) — `alterar_preco` garante que o preço da oferta
  seja maior que zero e estritamente menor que o preço normal do produto.
- `Usuario` (`app/models/usuario.py`, módulo de login) — a senha fica em `_senha`
  e nunca é exposta por um getter; a única forma de conferi-la é o método
  `verificar_senha()`, que devolve um booleano em vez do valor bruto.

Em todos os casos, o controller e as rotas só chamam esses métodos públicos —
nunca leem nem escrevem diretamente os atributos com underscore. Assim, a
representação interna de cada model pode mudar sem quebrar o resto da aplicação.

## Herança

O módulo de login é o exemplo mais claro: os três perfis do mock viram três
classes diferentes, todas herdando de uma classe base `Usuario`
(`app/models/usuario.py`):

```
Usuario
 └── Visitante      -> mostrar_permissoes(): ['ver_ofertas']
      └── Contribuidor  -> soma 'cadastrar_oferta'
           └── Moderador -> soma 'remover_oferta', 'banir_usuario'
```

- `Usuario` implementa tudo o que os três perfis têm em comum: id/nome,
  verificação de senha e uma lista de permissões padrão (vazia).
- Cada subclasse sobrescreve apenas `mostrar_permissoes()` e chama
  `super().mostrar_permissoes()` para estender a lista herdada, em vez de
  repeti-la. Um `Moderador` é um `Contribuidor`, que por sua vez é um
  `Visitante` — a hierarquia reflete como as permissões realmente se acumulam.
- O texto do perfil vindo do mock (`'visitante'`, `'contribuidor'`,
  `'moderador'`) é transformado na classe certa através do dicionário `PERFIS`
  em `carregar_usuarios()`. Esse é o único lugar que ainda olha o perfil como
  texto — depois que o objeto `Usuario` é criado, `UsuarioController.login()`
  chama os mesmos métodos `mostrar_perfil()` / `mostrar_permissoes()` em
  qualquer um deles, sem saber nem se importar com qual subclasse recebeu.
  Isso é o polimorfismo que a herança acima permite.

A mesma estrutura (um arquivo de mock, uma model com `carregar_*`, um
controller e um router) é reaproveitada tanto no módulo `produtos` quanto no
novo módulo `login`, o que também é uma forma de design consistente aplicado
em todo o projeto.
