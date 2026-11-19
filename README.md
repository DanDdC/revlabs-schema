# revlabs-schema

Contrato público de dados do RevLabs.

Este repositório define, valida e versiona os formatos usados por:

- `revlabs-telemetry` — app de captura
- `revlabs-expanded` — site, API e engine de análise

## Escopo

- JSON Schema canônico
- modelos Pydantic
- tipos TypeScript/Rust gerados
- fixtures e testes de contrato
- versionamento semântico

## Estrutura planejada

```
schema/v1/
  telemetry.schema.json
  track-geometry.schema.json
  examples/
src/revlabs_schema/
bindings/
tests/
docs/
CHANGELOG.md
```

## Versionamento

- `v1.0.0`: primeira versão estável
- mudança compatível: `v1.1.0`
- mudança incompatível: `v2.0.0`

Os consumidores fixam uma tag. O servidor aceita a versão atual e, durante
migração, a anterior.

## Licença

MIT. Veja [LICENSE](LICENSE).
