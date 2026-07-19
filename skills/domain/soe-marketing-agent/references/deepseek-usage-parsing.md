# DeepSeek API — Lectura de Reportes de Uso

DeepSeek exporta dos CSVs en su panel de usage (platform.deepseek.com/usage).

## Archivos en el ZIP

### `cost-<rango-fechas>.csv`

| Columna | Ejemplo |
|---------|---------|
| `user_id` | UUID del usuario |
| `utc_date` | `20260709` (formato YYYYMMDD) |
| `model` | `deepseek-v4-flash` |
| `wallet_type` | `Paid` |
| `cost` | `0.3953687472000000` USD |
| `currency` | `USD` |

### `amount-<rango-fechas>.csv`

Desglose por API key y tipo de token:

| Columna | Ejemplo |
|---------|---------|
| `type` | `input_cache_hit_tokens`, `input_cache_miss_tokens`, `request_count`, `output_tokens` |
| `price` | Por unidad (ej: `0.0000000028` para cache hit, `0.00000014` para cache miss, `0.00000028` para output) |
| `amount` | Cantidad de tokens o requests |
| `api_key_name` | Nombre asignado a la key en DeepSeek (ej: `AGENTE IA 1`) |

## Métricas clave a calcular

- **Total gastado** — sumar `cost` del cost CSV
- **% Cache hit** — `cache_hit / (cache_hit + cache_miss) * 100` sobre input tokens
- **Requests totales** — sumar `amount` donde `type = request_count`
- **Output tokens** — sumar `amount` donde `type = output_tokens`
- **Desglose por API key** — filtrar `amount-*.csv` por `api_key_name`

## Precios deepseek-v4-flash (Jul 2026)

| Tipo | Precio por token |
|------|-----------------|
| input cache hit | $0.0000000028 |
| input cache miss | $0.00000014 |
| output | $0.00000028 |

## Fórmula de costo estimado por key

```
costo = (cache_hit_tokens * 0.0000000028)
      + (cache_miss_tokens * 0.00000014)
      + (output_tokens * 0.00000028)
```

## Notas

- El saldo se consulta via API: `GET https://api.deepseek.com/user/balance` con header `Authorization: Bearer <api-key>`
- Respuesta: `{"is_available": true, "balance_infos": [{"currency": "CNY", "total_balance": "..."}]}`
- DeepSeek muestra saldo en CNY; la conversión aproximada es ~7.2 CNY por USD
