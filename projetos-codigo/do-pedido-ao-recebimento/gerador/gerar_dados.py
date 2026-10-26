"""Gera dados 100% sintéticos da 'Distribuidora Horizonte Sul' (empresa fictícia).
Uso: python gerar_dados.py   (semente fixa: resultado reproduzível)
Padrões inseridos de propósito: sazonalidade de fim de ano, clientes que deixam de comprar,
um vendedor que dá desconto acima do padrão, categoria de margem baixa e perfis que atrasam mais."""
import numpy as np, pandas as pd, os
rng = np.random.default_rng(42)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dados")
os.makedirs(OUT, exist_ok=True)
INI, CORTE = pd.Timestamp("2024-01-01"), pd.Timestamp("2025-12-31")
MES = ["jan","fev","mar","abr","mai","jun","jul","ago","set","out","nov","dez"]
DIA = ["segunda","terça","quarta","quinta","sexta","sábado","domingo"]

nomes = ["Carlos Mendes","Juliana Prado","Rafael Teixeira","Marina Duarte","Eduardo Lima","Patrícia Rocha","Bruno Carvalho","Fernanda Alves","Thiago Ribeiro","Camila Souza"]
REG = ["Sul","Sudeste","Centro-Oeste","Nordeste"]
dv = pd.DataFrame({"VendedorID": range(1, 11), "Vendedor": nomes, "Regiao": [REG[i % 4] for i in range(10)]})
VEND_DESCONTO = 7  # Bruno Carvalho: desconto acima do padrão

cats = {"Cabos e Fios": (0.62, 25, 180), "Iluminação": (0.58, 30, 350), "Quadros e Disjuntores": (0.60, 40, 520),
        "Ferramentas": (0.64, 35, 420), "Tubos e Conexões": (0.82, 12, 160), "Automação": (0.50, 90, 900)}
tipos = ["Linha Básica","Linha Plus","Linha Pro","Linha Industrial","Linha Compacta","Linha Premium","Linha Econômica","Linha Reforçada"]
prod = []
for c, (cr, lo, hi) in cats.items():
    for t in tipos:
        lista = round(float(rng.uniform(lo, hi)), 2)
        prod.append([len(prod) + 1, f"{c.split(' ')[0]} {t}", c, round(lista * (cr + rng.uniform(-.03, .03)), 2), lista])
dp = pd.DataFrame(prod, columns=["ProdutoID", "Produto", "Categoria", "CustoUnitario", "PrecoLista"])
pop = rng.dirichlet(np.ones(len(dp)) * 2)

N = 420
seg = rng.choice(["Varejo","Indústria","Construção","Serviços","Agro"], N, p=[.28,.20,.22,.18,.12])
porte = rng.choice(["Pequeno","Médio","Grande"], N, p=[.55,.33,.12])
reg = rng.choice(REG, N, p=[.30,.40,.15,.15])
cid = {"Sul":["Curitiba","Londrina","Maringá","Joinville"],"Sudeste":["São Paulo","Campinas","Belo Horizonte","Ribeirão Preto"],
       "Centro-Oeste":["Goiânia","Cuiabá","Campo Grande"],"Nordeste":["Recife","Salvador","Fortaleza"]}
uf = {"Curitiba":"PR","Londrina":"PR","Maringá":"PR","Joinville":"SC","São Paulo":"SP","Campinas":"SP","Belo Horizonte":"MG","Ribeirão Preto":"SP",
      "Goiânia":"GO","Cuiabá":"MT","Campo Grande":"MS","Recife":"PE","Salvador":"BA","Fortaleza":"CE"}
cidade = [str(rng.choice(cid[r])) for r in reg]
pref = ["Aurora","Horizonte","Vale Verde","Boa Vista","Ipê","Estrela","Pioneira","Nova Era","Cedro","Atlântica"]
cad = [INI if rng.random() < .75 else INI + pd.Timedelta(days=int(rng.integers(30, 640))) for _ in range(N)]
vend_reg = {r: dv.loc[dv.Regiao == r, "VendedorID"].tolist() for r in REG}
dc = pd.DataFrame({"ClienteID": range(1, N + 1),
    "Cliente": [f"{rng.choice(pref)} {s} {i+1:03d}" for i, s in enumerate(seg)],
    "Segmento": seg, "Porte": porte, "Regiao": reg, "UF": [uf[c] for c in cidade], "Cidade": cidade,
    "VendedorID": [int(rng.choice(vend_reg[r])) for r in reg], "DataCadastro": cad})
churn = {}
for i in range(N):
    if porte[i] != "Grande" and rng.random() < .20:
        churn[i + 1] = INI + pd.Timedelta(days=int(rng.integers(400, 640)))
base = {"Pequeno": 4, "Médio": 9, "Grande": 20}
season = [.80,.85,.95,.95,1,1,1,1.05,1.1,1.15,1.3,1.4]
qty_scale = {"Pequeno": 12, "Médio": 30, "Grande": 80}
disc_base = {"Pequeno": .02, "Médio": .05, "Grande": .09}
meses = pd.period_range(INI, CORTE, freq="M")

rows, oid = [], 0
for _, c in dc.iterrows():
    for m in meses:
        ini_m, fim_m = m.start_time, min(m.end_time.normalize(), CORTE)
        if fim_m < c.DataCadastro: continue
        for _ in range(rng.poisson(base[c.Porte] / 12 * season[m.month - 1])):
            d = ini_m + pd.Timedelta(days=int(rng.integers(0, (fim_m - ini_m).days + 1)))
            if d < c.DataCadastro or (c.ClienteID in churn and d > churn[c.ClienteID]): continue
            oid += 1
            k = int(rng.integers(1, 5 if c.Porte != "Grande" else 7))
            for p in rng.choice(len(dp), size=k, replace=False, p=pop):
                pr = dp.iloc[p]
                disc = disc_base[c.Porte] + (.04 if pr.Categoria == "Tubos e Conexões" else 0) + (.07 if c.VendedorID == VEND_DESCONTO else 0) + rng.normal(0, .015)
                disc = float(np.clip(disc, 0, .30))
                q = max(1, int(rng.lognormal(np.log(qty_scale[c.Porte]), .5)))
                pu = round(pr.PrecoLista * (1 - disc), 2)
                rows.append([oid, d, c.ClienteID, c.VendedorID, int(pr.ProdutoID), q, pr.PrecoLista, pu,
                             round(q * pr.PrecoLista, 2), round(q * pu, 2), round(q * pr.CustoUnitario, 2), round(disc, 4)])
fv = pd.DataFrame(rows, columns=["PedidoID","Data","ClienteID","VendedorID","ProdutoID","Quantidade","PrecoLista","PrecoUnitario","ValorBruto","Receita","Custo","DescontoPct"])

mau = set(int(x) for x in rng.choice(dc.ClienteID, int(N * .10), replace=False))
ped = fv.groupby("PedidoID").agg(Data=("Data","first"), ClienteID=("ClienteID","first"), Receita=("Receita","sum")).reset_index()
cli = dc.set_index("ClienteID")
tit = []
for _, p in ped.iterrows():
    c = cli.loc[p.ClienteID]
    parc = 1 if rng.random() < .65 else 2
    prazo = 60 if (c.Porte == "Grande" and rng.random() < .5) else 30
    mean = 1 + (12 if c.Segmento == "Construção" else 0) + (6 if c.Porte == "Grande" else 0) + (25 if p.ClienteID in mau else 0)
    for k in range(1, parc + 1):
        venc = p.Data + pd.Timedelta(days=prazo * k)
        atraso = max(0, int(round(rng.normal(mean - 4, 6 + mean * .4))))
        calote = p.ClienteID in mau and rng.random() < .15
        pag = venc + pd.Timedelta(days=atraso)
        pago = (not calote) and pag <= CORTE
        dias = (CORTE - venc).days
        if pago: sit, faixa, ordem = "Pago", "Pago", 0
        elif dias <= 0: sit, faixa, ordem = "A vencer", "A vencer", 1
        else:
            sit = "Vencido"
            faixa, ordem = ("1 a 30 dias", 2) if dias <= 30 else ("31 a 60 dias", 3) if dias <= 60 else ("61 a 90 dias", 4) if dias <= 90 else ("Acima de 90 dias", 5)
        tit.append([len(tit) + 1, int(p.PedidoID), k, int(p.ClienteID), p.Data, venc, pag if pago else None,
                    round(p.Receita / parc, 2), sit, atraso if pago else None, faixa, ordem])
ft = pd.DataFrame(tit, columns=["TituloID","PedidoID","Parcela","ClienteID","DataEmissao","DataVencimento","DataPagamento","Valor","Situacao","DiasAtraso","FaixaAtraso","FaixaOrdem"])

mm = fv.assign(Mes=fv.Data.dt.to_period("M")).groupby(["VendedorID", "Mes"]).Receita.sum().reset_index()
fm = []
for v in dv.VendedorID:
    media = mm[mm.VendedorID == v].Receita.mean()
    for m in meses:
        fm.append([m.start_time, v, round(media * (1.05 if m.year == 2024 else 1.12), -2)])
fm = pd.DataFrame(fm, columns=["DataMes", "VendedorID", "MetaReceita"])

dd = pd.date_range(INI, CORTE)
cal = pd.DataFrame({"Data": dd, "Ano": dd.year, "MesNum": dd.month, "NomeMes": [MES[m - 1] for m in dd.month],
    "MesAno": [f"{MES[m-1]}/{str(y)[2:]}" for m, y in zip(dd.month, dd.year)], "AnoMes": dd.year * 100 + dd.month,
    "Trimestre": ["T" + str((m - 1) // 3 + 1) for m in dd.month], "DiaSemana": [DIA[x] for x in dd.weekday]})

for nome, df in {"dim_calendario": cal, "dim_cliente": dc, "dim_produto": dp, "dim_vendedor": dv,
                 "fato_vendas": fv, "fato_titulos": ft, "fato_metas": fm}.items():
    for col in df.columns:
        if str(df[col].dtype).startswith("datetime"): df[col] = df[col].dt.strftime("%Y-%m-%d")
    df.to_csv(os.path.join(OUT, nome + ".csv"), index=False, encoding="utf-8")
    print(nome, len(df))
