-- Análises exploratórias usadas para validar o modelo do Power BI (SQLite).

-- 1) Receita, margem e desconto médio por categoria
SELECT p.Categoria,
       ROUND(SUM(v.Receita), 0)                                   AS receita,
       ROUND(100.0 * (SUM(v.Receita) - SUM(v.Custo)) / SUM(v.Receita), 1) AS margem_pct,
       ROUND(100.0 * (1 - SUM(v.Receita) / SUM(v.ValorBruto)), 1) AS desconto_pct
FROM fato_vendas v JOIN dim_produto p USING (ProdutoID)
GROUP BY p.Categoria ORDER BY margem_pct;

-- 2) Desconto médio por vendedor (procura de desvios)
SELECT d.Vendedor, ROUND(100.0 * (1 - SUM(v.Receita) / SUM(v.ValorBruto)), 1) AS desconto_pct
FROM fato_vendas v JOIN dim_vendedor d USING (VendedorID)
GROUP BY d.Vendedor ORDER BY desconto_pct DESC;

-- 3) Curva ABC de clientes (acumulado de receita com função de janela)
WITH r AS (SELECT ClienteID, SUM(Receita) AS receita FROM fato_vendas GROUP BY ClienteID),
a AS (SELECT ClienteID, receita,
             SUM(receita) OVER (ORDER BY receita DESC) * 1.0 / SUM(receita) OVER () AS acum FROM r)
SELECT CASE WHEN acum <= 0.80 THEN 'A' WHEN acum <= 0.95 THEN 'B' ELSE 'C' END AS classe,
       COUNT(*) AS clientes, ROUND(SUM(receita), 0) AS receita
FROM a GROUP BY classe ORDER BY classe;

-- 4) Segmentos de CRM por recência (dias desde a última compra até 2025-12-31) e frequência
WITH u AS (SELECT ClienteID, MAX(Data) AS ultima, COUNT(DISTINCT PedidoID) AS pedidos FROM fato_vendas GROUP BY ClienteID),
s AS (SELECT ClienteID, pedidos, CAST(julianday('2025-12-31') - julianday(ultima) AS INTEGER) AS recencia FROM u)
SELECT CASE WHEN recencia > 180 THEN 'Perdido' WHEN recencia > 90 THEN 'Em risco'
            WHEN pedidos >= 15 THEN 'Fiel' ELSE 'Ativo' END AS segmento_crm,
       COUNT(*) AS clientes
FROM s GROUP BY segmento_crm ORDER BY clientes DESC;

-- 5) Contas a receber por faixa de atraso (posição em 2025-12-31)
SELECT FaixaAtraso, COUNT(*) AS titulos, ROUND(SUM(Valor), 0) AS valor
FROM fato_titulos GROUP BY FaixaAtraso, FaixaOrdem ORDER BY FaixaOrdem;

-- 6) Inadimplência (vencido / total já vencido) por porte e segmento de cliente
SELECT c.Porte, c.Segmento,
       ROUND(100.0 * SUM(CASE WHEN t.Situacao = 'Vencido' THEN t.Valor END) /
             SUM(CASE WHEN t.DataVencimento <= '2025-12-31' THEN t.Valor END), 1) AS inadimplencia_pct
FROM fato_titulos t JOIN dim_cliente c USING (ClienteID)
GROUP BY c.Porte, c.Segmento ORDER BY inadimplencia_pct DESC;
