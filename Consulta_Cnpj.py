import flet as ft
import pandas as pd
import requests
import time
import os

def main(page: ft.Page):
    page.title = "Consulta de CNPJs - Receita Federal"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#F2F2F2"
    page.window_width = 600
    page.window_height = 550

    titulo = ft.Text("Consulta CNPJ - Receita Federal", size=22, weight="bold")

    caminho_arquivo = ft.TextField(label="Selecione o arquivo Excel", read_only=True, width=500)
    resultado_log = ft.Text(value="", size=12, selectable=True)
    progresso = ft.ProgressBar(width=500, visible=False)

    file_picker = ft.FilePicker()

    def selecionar_arquivo(e):
        file_picker.pick_files(allowed_extensions=["xlsx"])

    def arquivo_escolhido(e: ft.FilePickerResultEvent):
        if e.files:
            caminho_arquivo.value = e.files[0].path
            resultado_log.value = ""
            page.update()

    file_picker.on_result = arquivo_escolhido
    page.overlay.append(file_picker)

    def consultar_cnpj(cnpj, days=30):
        url = f"https://receitaws.com.br/v1/cnpj/{cnpj}/days/{days}"
        headers = {
            "Accept": "application/json",
            "Authorization": " API     }
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                atividade = data.get("atividade_principal", [{}])[0]
                return {
                    'CNPJ': data.get('cnpj'),
                    'Situação': data.get('situacao'),
                    'Razão Social': data.get('nome'),
                    'Nome Fantasia': data.get('fantasia'),
                    'Natureza Jurídica': data.get('natureza_juridica'),
                    'Atividade Principal': atividade.get("text"),
                    'Código Atividade Principal': atividade.get("code"),
                    'Tipo': data.get('tipo'),
                    'UF': data.get('uf'),
                    'Municipio': data.get('municipio'),
                    'Bairro': data.get('bairro'),
                    'Logradouro': data.get('logradouro'),
                    'Número': data.get('numero'),
                    'Complemento Endereço': data.get('complemento'),
                    'CEP': data.get('cep'),
                    'Telefone': data.get('telefone'),
                    'E-mail': data.get('email'),
                    'Porte': data.get('porte'),
                    'Data Situação Cadastral': data.get('data_situacao'),
                    'Abertura': data.get('abertura'),
                    'Última Atualização': data.get('ultima_atualizacao'),
                    'Status': data.get('status'),
                    'Motivo Situação': data.get('motivo_situacao'),
                    'Situação Especial': data.get('situacao_especial'),
                    'Data Situação Especial': data.get('data_situacao_especial'),
                    'Capital Social': data.get('capital_social'),
                    'Qualificação': data.get('qsa')[0].get('qual') if data.get('qsa') else None,
                    'Nome Qualificação': data.get('qsa')[0].get('nome') if data.get('qsa') else None,
                    'Erro': None
                }
            else:
                return {'CNPJ': cnpj, 'Erro': f"HTTP {response.status_code}"}
        except Exception as err:
            return {'CNPJ': cnpj, 'Erro': str(err)}

    def iniciar_consulta(e):
        if not caminho_arquivo.value:
            resultado_log.value = "⚠️ Selecione um arquivo primeiro."
            page.update()
            return

        try:
            df = pd.read_excel(caminho_arquivo.value, sheet_name="Input_CNPJ")
            df.columns = df.columns.str.strip()
            if "CNPJ" not in df.columns:
                resultado_log.value = "❌ A coluna 'CNPJ' não foi encontrada na aba 'Input_CNPJ'."
                progresso.visible = False
                page.update()
                return

            df["CNPJ"] = df["CNPJ"].astype(str).str.replace(r"\D", "", regex=True)
            df = df[df["CNPJ"].str.len() == 14].drop_duplicates()

            resultados = []
            progresso.visible = True
            page.update()

            for i, cnpj in enumerate(df["CNPJ"]):
                resultado_log.value = f"🔎 Consultando {cnpj} ({i+1}/{len(df)})"
                page.update()
                dados = consultar_cnpj(cnpj)
                resultados.append(dados)

            df_final = pd.DataFrame(resultados)
            nome_saida = os.path.join(os.path.dirname(caminho_arquivo.value), "resultado_cnpjs_receita.xlsx")
            df_final.to_excel(nome_saida, index=False)

            resultado_log.value = f"✅ Consulta finalizada!\nArquivo salvo como:\n{nome_saida}"
            progresso.visible = False
            page.update()

        except Exception as erro:
            resultado_log.value = f"❌ Erro: {erro}"
            progresso.visible = False
            page.update()

    btn_arquivo = ft.TextButton("Selecionar Excel", on_click=selecionar_arquivo)
    btn_consultar = ft.ElevatedButton("Iniciar Consulta", on_click=iniciar_consulta, bgcolor="#B0B0B0", color="black")

    page.add(
        ft.Column([
            titulo,
            caminho_arquivo,
            btn_arquivo,
            btn_consultar,
            progresso,
            resultado_log
        ], spacing=20)
    )

ft.app(target=main)
