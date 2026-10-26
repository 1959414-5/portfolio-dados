# Power BI: Do pedido ao recebimento

Projeto Power BI no formato PBIP (modelo em TMDL e relatório em PBIR), com dados 100% sintéticos.

## Como abrir
1. Abra `DoPedidoAoRecebimento.pbip` no Power BI Desktop (clique duplo).
2. Se o Power BI pedir, ative em Arquivo > Opções > Recursos em versão prévia: "Salvar como projeto do Power BI (.pbip)" e o formato de relatório PBIR.
3. Os dados são lidos de `../dados/`. O caminho está no parâmetro `PastaDados` (Transformar dados > Gerenciar parâmetros). Se o seu repositório estiver em outra pasta, altere o parâmetro e termine com `\`.
4. Clique em Atualizar. Depois, Arquivo > Salvar como para gerar o `.pbix`, se quiser.

## O que tem
- 7 tabelas (4 dimensões e 3 fatos), 8 relacionamentos e 29 medidas DAX.
- 3 páginas: Vendas, Clientes (CRM) e Financeiro.
- Data de corte dos dados: 31/12/2025.
