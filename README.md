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

## Estrutura

```
schema/v1/
  telemetry.schema.json
  track-geometry.schema.json
src/revlabs_schema/
bindings/
examples/
tests/
docs/
scripts/
CHANGELOG.md
```

## Uso

```bash
uv venv .venv
uv pip install --python .venv/Scripts/python.exe -e ".[dev]"
.venv/Scripts/python.exe scripts/export_schema.py
.venv/Scripts/python.exe -m pytest -q
```

Em Linux/macOS, use `.venv/bin/python`.

## Licença

MIT. Veja [LICENSE](LICENSE).
