import streamlit as st
import pandas as pd
import io 
from openpyxl.styles import Font, PatternFill, Alignment

st.title("📈 Simulador de Poupança")
# 1. Novos Widgets: O usuário define as regras
valor_mensal = st.number_input("Insira aqui o valor (R$) que você quer guardar:", min_value=0.0, value=50.0, step=10.0)
meses_escolhido = st.slider("insira o tempo que esse valor irá ficar guardado (meses):", min_value=1, max_value=24, value=12)
juros = st.number_input("Digite a taxa de juros (%):", min_value=1.0, value=1.5, step= 0.01)

# 2. A sua lógica de loop (agora usando a variável valor_mensal)
num = 0
valor_acumulado = []
saldo_atual = 0
meses_lista = []
while num != meses_escolhido:
    num = num + 1
    saldo_atual = (saldo_atual * (juros/100)) + valor_mensal + saldo_atual# Usamos a escolha do usuário aqui!
    valor_acumulado.append(saldo_atual)
    meses_lista.append(num) # Guarda 1, 2, 3...

# 3. Exibição dos dados
df = pd.DataFrame(valor_acumulado, index=meses_lista, columns=['Saldo (R$)'])

st.write(f"Guardando **R$ {valor_mensal:.2f}** por mês, em **{meses_escolhido} meses** você terá:")
st.line_chart(df)

# estilização da planilha //

buffer = io.BytesIO()

with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
    df.to_excel(writer, index=True, sheet_name='Simulacao')
    
    # 1. Pegamos a folha que o Pandas acabou de criar
    aba = writer.sheets['Simulacao']
    aba.column_dimensions['A'].width = 10
    aba.column_dimensions['B'].width = 20

    # 2. Criamos o nosso "Kit de Decoração"
    cor_fundo_azul = PatternFill(start_color="0000FF", end_color="0000FF", fill_type="solid")
    letra_branca_negrito = Font(color="FFFFFF", bold=True)
    centralizado = Alignment(horizontal="center")

    # 3. Aplicamos na primeira linha (Cabeçalho)
    # worksheet[1] seleciona todas as células da linha 1
    for celula in aba[1]:
        celula.fill = cor_fundo_azul
        celula.font = letra_branca_negrito
        celula.alignment = centralizado

    # 4. Ajuste extra: Formatar a coluna B como Moeda (R$)
    # Vamos percorrer as células da coluna B (pulando o cabeçalho)
    for row in range(2, len(df) + 2):
        aba[f'B{row}'].number_format = '"R$ " #,##0.00'

# O botão de download continua igual
st.download_button(
    label="📥 Baixar Planilha",
    data=buffer.getvalue(),
    file_name="meu_investimento.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
# //
