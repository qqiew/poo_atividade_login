# Part B — Encapsulation and Inheritance in KiOferta

Ten-minute presentation notes: where the team applied encapsulation and inheritance
across the KiOferta backend.

## Encapsulation

Every model in the project keeps its state in "protected" attributes (the `_name`
convention) and exposes it only through `mostrar_*` (getter) and `alterar_*` (setter)
methods that validate input before touching the attribute:

- `Produto` (`app/models/produto.py`) — `alterar_nome` rejects an empty name,
  `alterar_preco` rejects a negative price. Nothing outside the class ever writes to
  `_nome` or `_preco` directly.
- `Mercado` (`app/models/mercado.py`) — `alterar_localizacao` validates that latitude
  and longitude are within valid ranges before storing them.
- `Oferta` (`app/models/oferta.py`) — `alterar_preco` enforces that a deal price must
  be positive and strictly lower than the product's normal price.
- `Usuario` (`app/models/usuario.py`, the login module) — the password is stored in
  `_senha` and is never exposed through a getter; the only way to check it is the
  `verificar_senha()` method, which returns a boolean instead of the raw value.

In every case the controller and the routes only ever call these public methods —
they never read or write the underscore-prefixed attributes, so the internal
representation of each model can change without breaking the rest of the app.

## Inheritance

The login module is the clearest example: three profiles from the mock data become
three different classes, all inheriting from a common `Usuario` base class
(`app/models/usuario.py`):

```
Usuario
 └── Visitante      -> mostrar_permissoes(): ['ver_ofertas']
      └── Contribuidor  -> adds 'cadastrar_oferta'
           └── Moderador -> adds 'remover_oferta', 'banir_usuario'
```

- `Usuario` implements everything the three profiles share: id/name handling,
  password verification, and a default (empty) permission list.
- Each subclass overrides only `mostrar_permissoes()` and calls
  `super().mostrar_permissoes()` to extend the list it inherited, instead of
  repeating it. A `Moderador` is a `Contribuidor` that is also a `Visitante` — the
  hierarchy mirrors how the permissions actually build up.
- The profile string coming from the mock data (`'visitante'`, `'contribuidor'`,
  `'moderador'`) is turned into the right class through the `PERFIS` dictionary in
  `carregar_usuarios()`. That is the only place that ever looks at the profile as
  text — once the `Usuario` subclass is built, `UsuarioController.login()` calls the
  same `mostrar_perfil()` / `mostrar_permissoes()` methods on every object without
  knowing or caring which subclass it actually got. That is polymorphism enabled by
  the inheritance above.

The same shape (a mock file, a model with `carregar_*`, a controller, and a router)
is reused for both `produtos` and the new `login` module, which is also a form of
consistent design applied across the codebase.
