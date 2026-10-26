-- Modelo relacional (SQLite). Carregue os CSVs da pasta dados/ (ex.: pandas.to_sql ou .import).
-- Fatos: fato_vendas (1 linha por item de pedido), fato_titulos (1 linha por parcela), fato_metas.
-- Dimensões: dim_cliente, dim_produto, dim_vendedor, dim_calendario.
-- Data de corte dos dados: 2025-12-31.
CREATE TABLE dim_vendedor (VendedorID INTEGER PRIMARY KEY, Vendedor TEXT, Regiao TEXT);
CREATE TABLE dim_produto  (ProdutoID INTEGER PRIMARY KEY, Produto TEXT, Categoria TEXT, CustoUnitario REAL, PrecoLista REAL);
CREATE TABLE dim_cliente  (ClienteID INTEGER PRIMARY KEY, Cliente TEXT, Segmento TEXT, Porte TEXT, Regiao TEXT, UF TEXT, Cidade TEXT, VendedorID INTEGER, DataCadastro TEXT);
CREATE TABLE fato_vendas  (PedidoID INTEGER, Data TEXT, ClienteID INTEGER, VendedorID INTEGER, ProdutoID INTEGER, Quantidade INTEGER,
                           PrecoLista REAL, PrecoUnitario REAL, ValorBruto REAL, Receita REAL, Custo REAL, DescontoPct REAL);
CREATE TABLE fato_titulos (TituloID INTEGER PRIMARY KEY, PedidoID INTEGER, Parcela INTEGER, ClienteID INTEGER, DataEmissao TEXT, DataVencimento TEXT,
                           DataPagamento TEXT, Valor REAL, Situacao TEXT, DiasAtraso INTEGER, FaixaAtraso TEXT, FaixaOrdem INTEGER);
CREATE TABLE fato_metas   (DataMes TEXT, VendedorID INTEGER, MetaReceita REAL);
