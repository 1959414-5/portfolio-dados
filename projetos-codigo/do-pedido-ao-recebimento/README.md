# Do pedido ao recebimento (estudo com dados sintéticos)

Empresa fictícia (Distribuidora Horizonte Sul). Pergunta central: onde se perde dinheiro entre vender, manter o cliente e receber?

- `gerador/gerar_dados.py`: gera os CSVs (semente fixa, reproduzível). Padrões inseridos de propósito: sazonalidade de fim de ano, clientes que deixam de comprar, um vendedor com desconto acima do padrão, categoria de margem baixa e perfis que atrasam mais.
- `dados/`: 7 tabelas em CSV (4 dimensões e 3 fatos). Data de corte: 31/12/2025.
- `sql/`: modelo relacional e 6 análises de validação (SQLite).
- `powerbi/`: projeto PBIP com modelo, medidas DAX e 3 páginas. Veja `powerbi/LEIA-ME.md`.

Todos os dados são fictícios e não representam nenhuma empresa real.
