# Contrato de dados

## Princípios

1. O schema é a fonte da verdade.
2. Campos desconhecidos são rejeitados ou ignorados de forma explícita.
3. Toda mudança precisa de exemplo e teste de contrato.
4. O app e o site nunca compartilham código de negócio; compartilham o contrato.

## Versão inicial (v1)

- `TelemetryBundle`: sessão + voltas + frames + metadados.
- `TrackGeometry`: centerline, setores, start/finish, versão.
- `SessionMode`: `hotlap`, `practice`, `race`.
- `Game`: `gt7`, `ac` (futuro).
- `other_cars`: opcional, para jogos que expõem outros carros (AC).

## Compatibilidade

- O servidor deve aceitar a versão atual e a anterior.
- O app declara `schema_version` no manifest.
- Campos novos são opcionais até virar obrigatórios em uma major.
