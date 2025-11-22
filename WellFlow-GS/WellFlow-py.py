import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

FUNC_PATH = "C:/Users/Gustavo/Documents/WellFlow-GS/funcionariosMC.xlsx"
SIT_PATH = "C:/Users/Gustavo/Documents/WellFlow-GS/situacoesMC.xlsx"

OUT_DIR = "wellflow_outputs"
os.makedirs(OUT_DIR, exist_ok=True)

CSV_OUTPUT = os.path.join(OUT_DIR, "relatorio_wellflow.csv")

def carregar_dados():
    df_func = pd.read_excel(FUNC_PATH)
    df_sit = pd.read_excel(SIT_PATH)
    df_func.columns = [c.strip() for c in df_func.columns]
    df_sit.columns = [c.strip() for c in df_sit.columns]
    return df_func, df_sit

def coletar_inputs(nome):
    print(f"\nOlá {nome}! Vamos registrar como foi seu dia.")
    while True:
        try:
            humor = int(input("Como está seu humor hoje? (1 a 5): ").strip())
            if 1 <= humor <= 5:
                break
            print("Digite um número entre 1 e 5.")
        except:
            print("Entrada inválida.")
    conflito = input("Houve conflito hoje? (s/n): ").strip().lower()
    conflito = 1 if conflito == "s" else 0
    sobrecarga = input("Se sentiu sobrecarregado hoje? (s/n): ").strip().lower()
    sobrecarga = 1 if sobrecarga == "s" else 0
    return {"humor": humor, "conflito": conflito, "sobrecarga": sobrecarga}

def safe_get(row, key, default=0):
    try:
        val = row.get(key, default)
        if pd.isna(val):
            return default
        return float(val)
    except:
        return default

def calcular_score(func, entrada):
    score_base = (
        (6 - safe_get(func, "relacao_gestor", 3)) +
        (6 - safe_get(func, "relacao_colegas", 3)) +
        safe_get(func, "nivel_estresse", 3) +
        safe_get(func, "carga_tarefas_diaria", 3)
    )
    score_dia = entrada["conflito"] * 2 + entrada["sobrecarga"] * 2 + (6 - entrada["humor"])
    return score_base + score_dia

def impacto_num(texto):
    texto = str(texto).lower()
    if "alto" in texto:
        return 3
    if "médio" in texto or "medio" in texto:
        return 2
    return 1

def calcular_situacao(sit, score_func):
    impacto = impacto_num(sit.get("impacto"))
    return score_func + impacto

def escolher_situacao(df_sit, score_func):
    candidatos = []
    for _, row in df_sit.iterrows():
        score = calcular_situacao(row, score_func)
        candidatos.append((score, row))
    melhor = sorted(candidatos, key=lambda x: x[0], reverse=True)[0][1]
    return {
        "descricao": melhor["descricao"],
        "impacto": melhor["impacto"],
        "solucao": melhor["solucao_recomendada"]
    }

def processar_funcionario(func, df_sit, entrada):
    score = calcular_score(func, entrada)
    situacao = escolher_situacao(df_sit, score)
    return {
        "Funcionario": func["nome"],
        "Humor": entrada["humor"],
        "Conflito": entrada["conflito"],
        "Sobrecarga": entrada["sobrecarga"],
        "Score Final": score,
        "Situação Detectada": situacao["descricao"],
        "Impacto": situacao["impacto"],
        "Recomendação": situacao["solucao"],
        "Data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def salvar_relatorio(dados):
    df = pd.DataFrame([dados])
    df.to_csv(CSV_OUTPUT, index=False)
    print(f"\n[OK] Relatório salvo em {CSV_OUTPUT}")

def gerar_graficos():
    if not os.path.exists(CSV_OUTPUT):
        print("Nenhum relatório encontrado.")
        return
    df = pd.read_csv(CSV_OUTPUT)
    plt.figure()
    plt.bar(["Score"], [df["Score Final"].iloc[0]])
    plt.title("Score do Funcionário")
    plt.savefig(os.path.join(OUT_DIR, "grafico_score.png"))
    plt.close()
    print("[OK] Gráfico gerado.")

def menu_gerente(df_func):
    print("\n=== Login do Gerente ===")
    senha = input("Senha: ").strip()
    if senha != "admin123":
        print("Senha incorreta.")
        return
    print("\nAcesso concedido!")

    def submenu():
        while True:
            print("\n--- Menu do Gerente ---")
            print("1) Ver último relatório")
            print("2) Gerar gráfico")
            print("3) Ver resumo semanal (mock)")
            print("4) Consultar funcionário por ID")
            print("5) Voltar")
            op = input("Escolha: ").strip()

            if op == "1":
                if os.path.exists(CSV_OUTPUT):
                    df = pd.read_csv(CSV_OUTPUT)
                    print(df.to_string(index=False))
                else:
                    print("Nenhum relatório encontrado.")

            elif op == "2":
                gerar_graficos()

            elif op == "3":
                mock = pd.DataFrame({
                    "Funcionario": ["João", "Ana", "Carlos"],
                    "Média Humor": [3.5, 4.2, 2.8],
                    "Conflitos": [1, 0, 2]
                })
                print(mock.to_string(index=False))

            elif op == "4":
                print("\nFuncionários cadastrados:")
                print(df_func[["id_funcionario", "nome"]])
                fid = input("Digite o ID: ").strip()
                if fid not in df_func["id_funcionario"].astype(str).values:
                    print("ID não encontrado.")
                    continue
                func = df_func[df_func["id_funcionario"].astype(str) == fid].iloc[0]
                print("\nDados do funcionário:")
                print(func)

            elif op == "5":
                break

            else:
                print("Opção inválida.")

    submenu()

def menu():
    df_func, df_sit = carregar_dados()
    while True:
        print("\n=== WellFlow – Menu Principal ===")
        print("1) Área do funcionário")
        print("2) Área do gerente")
        print("3) Sair")

        op = input("Escolha: ").strip()

        if op == "1":
            print("\nFuncionários disponíveis:")
            print(df_func[["id_funcionario", "nome"]])
            fid = input("\nDigite o ID do funcionário: ").strip()
            if fid not in df_func["id_funcionario"].astype(str).values:
                print("ID inválido.")
                continue
            func = df_func[df_func["id_funcionario"].astype(str) == fid].iloc[0]
            entrada = coletar_inputs(func["nome"])
            resultado = processar_funcionario(func, df_sit, entrada)
            salvar_relatorio(resultado)
            print("\nResultado final:")
            print(pd.DataFrame([resultado]).to_string(index=False))

        elif op == "2":
            menu_gerente(df_func)

        elif op == "3":
            print("Encerrando o sistema...")
            sys.exit()

        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu()
