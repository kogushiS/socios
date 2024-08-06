import streamlit as st
from sqlalchemy import text, insert, Table, MetaData, Column, Integer, Float, String, DateTime
from datetime import datetime
from filtro import Filtros
from conexao import Conexao
import pandas as pd
import numpy as np
import calendar
import time
import altair as alt


class Vallet:
    def __init__(self) -> None:
        self.filtro = Filtros()

    def atualizar_vallet(self):
        consulta = Conexao.conecta_bd()
        self.df_vallet = consulta[12]
        return self.df_vallet

    def navegacao_vallet(self):
        tab1, tab2 = st.tabs(["Resumo", "Vallet"])
        with tab1:
            self.cards_resumo_vallet()
            self.caixas_expansivas_vallet()
        with tab2:
            with st.expander("Lançamento vallet", expanded=True):
                self.widget_vallet()
            with st.expander('Edição Vallet'):
                self.editar_vallet()

    def cards_resumo_vallet(self):
        self.dataframe_vallet()
    # Conteúdo formatado com CSS
        credito_html = f"""
        <div style='text-align: center; border: 1px solid #ddd; padding: 10px; border-radius: 5px; margin-bottom: 20px;'>
            <strong>Crédito</strong><br>
            <span style='font-size: 0.95em;'>{'R${:,.2f}'.format(self.credito_vallet)}</span><br>
            <span style='color: green; font-size: 0.8em'>{'{:.4}%'.format(self.credito_vallet / self.total_vallet * 100)}</span>
        </div>
        """

        debito_html = f"""
        <div style='text-align: center; border: 1px solid #ddd; padding: 10px; border-radius: 5px; margin-bottom: 20px;'>
            <strong>Débito</strong><br>
            <span style='font-size: 0.95em;'>{'R${:,.2f}'.format(self.debito_vallet)}</span><br>
            <span style='color: green; font-size: 0.8em'>{'{:.4}%'.format(self.debito_vallet / self.total_vallet * 100)}</span>
        </div>
        """

        dinheiro_html = f"""
        <div style='text-align: center; border: 1px solid #ddd; padding: 10px; border-radius: 5px; margin-bottom: 20px;'>
            <strong>Dinheiro</strong><br>
            <span style='font-size: 0.95em;'>R${'{:,.2f}'.format(self.dinheiro_vallet)}</span><br>
            <span style='color: green; font-size: 0.8em'>{'{:.4}%'.format(self.dinheiro_vallet / self.total_vallet * 100)}</span>
        </div>
        """
        
        pix_html = f"""
        <div style='text-align: center; border: 1px solid #ddd; padding: 10px; border-radius: 5px; margin-bottom: 20px;'>
            <strong>Pix</strong><br>
            <span style='font-size: 0.95em;'>R${'{:,.2f}'.format(self.pix_vallet)}</span><br>
            <span style='color: green; font-size: 0.8em'>{'{:.4}%'.format(self.pix_vallet / self.total_vallet * 100)}</span>
        </div>
        """
        beneficio_html = f"""
        <div style='text-align: center; border: 1px solid #ddd; padding: 10px; border-radius: 5px; margin-bottom: 20px;'>
            <strong>Beneficio</strong><br>
            <span style='font-size: 0.95em;'>R${'{:,.2f}'.format(self.outros_cartoes_vallet)}</span><br>
            <span style='color: green; font-size: 0.8em'>{'{:.4}%'.format(self.outros_cartoes_vallet / self.total_vallet * 100)}</span>
        </div>
        """
        taxa_html = f"""
        <div style='text-align: center; border: 1px solid #ddd; padding: 10px; border-radius: 5px; margin-bottom: 46px;'>
            <strong>Taxa</strong><br>
            <span style='font-size: 0.95em;'>{'R${:,.2f}'.format(self.taxa_vallet)}</span><br>
        </div>
        """
        qtd_veiculo_html = f"""
        <div style='text-align: center; border: 1px solid #ddd; padding: 10px; border-radius: 5px; margin-bottom: 46px;'>
            <strong>Qtde Veículo</strong><br>
            <span style='font-size: 0.95em;'>{'{:,}'.format(self.qtd_veiculo)}</span><br>
        </div>
        """
        total_vallet_html = f"""
        <div style='text-align: center; border: 1px solid #ddd; padding: 10px; border-radius: 5px; margin-bottom: 46px;'>
            <strong>Total Vallet</strong><br>
            <span style='font-size: 0.95em;'>R${'{:,.2f}'.format(self.total_vallet)}</span><br>
        </div>
        """
        cols = st.columns(4)
        with cols[0]:
            st.markdown(credito_html, unsafe_allow_html=True)
            st.markdown(debito_html, unsafe_allow_html=True)
        with cols[1]:
            st.markdown(dinheiro_html, unsafe_allow_html=True)
            st.markdown(pix_html, unsafe_allow_html=True)
        with cols[2]:
            st.markdown(beneficio_html, unsafe_allow_html=True)
            st.markdown(taxa_html, unsafe_allow_html=True)
        with cols[3]:
            st.markdown(qtd_veiculo_html, unsafe_allow_html=True)
            st.markdown(total_vallet_html, unsafe_allow_html=True)

    def dataframe_vallet(self):
        self.atualizar_vallet()
        df_vallet = self.df_vallet

        # Convertendo a coluna 'data_vallet' para o formato datetime
        df_vallet['data_vallet'] = pd.to_datetime(df_vallet['data_vallet'])

        colunas = ['qtd_veiculo', 'dinheiro', 'pix', 'debito_mastercard', 'debito_visa', 'debito_elo', 'credito_mastercard', 'credito_visa',
                    'credito_elo', 'hiper', 'american_express', 'alelo', 'sodexo', 'ticket_rest', 'vale_refeicao', 'dinersclub']
        
        for item in colunas:
            df_vallet[item] = pd.to_numeric(df_vallet[item], errors='coerce')

        df_vallet['total'] = df_vallet[['dinheiro', 'pix', 'debito_mastercard', 'debito_visa', 'debito_elo', 'credito_mastercard', 
                                        'credito_visa', 'credito_elo', 'hiper', 'american_express', 'alelo', 'sodexo', 'ticket_rest',
                                        'vale_refeicao', 'dinersclub']].sum(axis=1)
    
        # Subtraindo 30 dias da coluna 'data_vallet'
        df_vallet['data_30'] = df_vallet['data_vallet'] - pd.DateOffset(days=30)

        # Criar um conjunto de pares (data_30, periodo) ou seja a data e periodo precisa corresponder
        existent_dates_and_periods = set(zip(df_vallet['data_30'], df_vallet['periodo']))
        # Criar um dicionário dos valores correspondentes por data e período
        valor_por_data_e_periodo = df_vallet.set_index(['data_vallet', 'periodo'])['total'].to_dict()

        # Aplicar a busca para valores correspondentes (inserindo novas colunas data e valor referente a 30 dias atrás)
        df_vallet['data_30'] = df_vallet.apply(lambda row: row['data_30'] if (row['data_30'], row['periodo']) in existent_dates_and_periods else pd.NaT, axis=1)
        df_vallet['valor_total_30'] = df_vallet.apply(lambda row: valor_por_data_e_periodo.get((row['data_30'], row['periodo']), 0), axis=1)

        self.df_vallet = df_vallet
        # Filtrando data
        data_inicial = str(self.filtro.data_inicial)     # formato da data'2023-05-01'
        data_final = str(self.filtro.data_final)
        self.df_vallet['data_vallet'] = pd.to_datetime(self.df_vallet['data_vallet'], format='%Y-%m-%d')
        
        filtro_data = (self.df_vallet['data_vallet'] >= data_inicial) & (self.df_vallet['data_vallet'] <= data_final)

        # filtrando periodo
        # Verificar se a lista 'self.filtro.varPeriodo' está vazia
        if self.filtro.varPeriodo:
            filtro_periodo = self.df_vallet['periodo'].isin(self.filtro.varPeriodo)
        else:
            filtro_periodo = pd.Series([True] * len(self.df_vallet)) # se a lista estiver vazia, considera todos os valores como verdadeiros  

        self.valores_vallet_30dias = self.df_vallet[filtro_data & filtro_periodo]

        # removendo datas devido array mais abaixo
        self.valores_vallet = self.valores_vallet_30dias.drop(['data_30', 'valor_total_30'], axis=1)

        # Convertendo a coluna 'coluna_string' para números
        self.valores_vallet['qtd_veiculo'] = pd.to_numeric(self.valores_vallet['qtd_veiculo'], errors='coerce')
        # Converter as colunas para o tipo de dados numérico, tratando valores não numéricos como NaN
        self.valores_vallet['debito_mastercard'] = pd.to_numeric(self.valores_vallet['debito_mastercard'], errors='coerce')
        self.valores_vallet['debito_visa'] = pd.to_numeric(self.valores_vallet['debito_visa'], errors='coerce')
        self.valores_vallet['debito_elo'] = pd.to_numeric(self.valores_vallet['debito_elo'], errors='coerce')
        self.valores_vallet['credito_mastercard'] = pd.to_numeric(self.valores_vallet['credito_mastercard'], errors='coerce')
        self.valores_vallet['credito_visa'] = pd.to_numeric(self.valores_vallet['credito_visa'], errors='coerce')
        self.valores_vallet['credito_elo'] = pd.to_numeric(self.valores_vallet['credito_elo'], errors='coerce')
        self.valores_vallet['alelo'] = pd.to_numeric(self.valores_vallet['alelo'], errors='coerce')
        self.valores_vallet['american_express'] = pd.to_numeric(self.valores_vallet['american_express'], errors='coerce')
        self.valores_vallet['hiper'] = pd.to_numeric(self.valores_vallet['hiper'], errors='coerce')
        self.valores_vallet['sodexo'] = pd.to_numeric(self.valores_vallet['sodexo'], errors='coerce')
        self.valores_vallet['ticket_rest'] = pd.to_numeric(self.valores_vallet['ticket_rest'], errors='coerce')
        self.valores_vallet['vale_refeicao'] = pd.to_numeric(self.valores_vallet['vale_refeicao'], errors='coerce')
        self.valores_vallet['dinersclub'] = pd.to_numeric(self.valores_vallet['dinersclub'], errors='coerce')

        # Converter a coluna 'data_vallet' para o tipo datetime
        self.valores_vallet['data_vallet'] = pd.to_datetime(self.valores_vallet['data_vallet'])

        # Preencher os valores NaN com zero
        self.valores_vallet = self.valores_vallet.fillna(0)

        def calcular_taxa(row):
            return (row['debito_mastercard'] + row['debito_visa']) * 0.0119 + \
                    (row['debito_elo'] + row['hiper']) * 0.0169 + \
                    (row['credito_mastercard'] + row['credito_visa']) * 0.0364 + \
                    (row['credito_elo'] + row['american_express']) * 0.0414 + \
                    row['alelo'] * 0.065 + \
                    row['vale_refeicao'] * 0.0685 + \
                    row['ticket_rest'] * 0.06 + \
                    row['sodexo'] * 0.069 + \
                    row['dinersclub'] * 0.0414

        # foi necessário realizar esse if pois quando calcular o lucro de meses que vallet esta vazio gera um erro
        if not self.valores_vallet.empty:
            # Aplicar a função calcular_taxa a cada linha do DataFrame e armazenar os resultados em uma nova coluna 'taxa'
            self.valores_vallet['taxa'] = self.valores_vallet.apply(calcular_taxa, axis=1)

            self.df_vallet_valores = self.valores_vallet.drop(['data_vallet', 'periodo', 'dt_atualizado', 'ID'], axis=1)
            self.array_vallet = np.array(self.df_vallet_valores)

            # garantir que array esta como string e assim poder aplicar replace
            self.array_vallet = self.array_vallet.astype(str)
            self.array_vallet = np.char.replace(self.array_vallet, ',', '.')

            # substiturir valores vazios por nan e assim converter valores para float
            self.array_vallet[self.array_vallet == ''] = 0 #'nan'
            self.array_vallet = self.array_vallet.astype(float)
            
            # Somando todas as linhas por colunas
            # somando cada coluna da array -> exemplo [279, 1548, 1514, 4848...] -> cada valor é o total de cada coluna
            self.total_colunas_vallet = np.nansum(self.array_vallet, axis=0)

            self.dinheiro_vallet = self.total_colunas_vallet[0]
            self.pix_vallet = self.total_colunas_vallet[1]
            self.debito_martercard_vallet = self.total_colunas_vallet[2]
            self.debito_visa_vallet = self.total_colunas_vallet[3]
            self.debito_elo_vallet = self.total_colunas_vallet[4]
            self.credito_mastercard_vallet = self.total_colunas_vallet[5]
            self.credito_visa_vallet = self.total_colunas_vallet[6]
            self.credito_elo_vallet = self.total_colunas_vallet[7]
            self.hiper_vallet = self.total_colunas_vallet[8]
            self.american_express_vallet = self.total_colunas_vallet[9]
            self.alelo_vallet = self.total_colunas_vallet[10]
            self.sodexo_vallet = self.total_colunas_vallet[11]
            self.ticket_rest_vallet = self.total_colunas_vallet[12]
            self.vale_refeicao_vallet = self.total_colunas_vallet[13]
            self.dinersclub_vallet = self.total_colunas_vallet[14]
            self.qtd_veiculo = int(self.total_colunas_vallet[15])

            self.taxa_vallet = (self.valores_vallet['taxa'].sum())

        else:
            self.dinheiro_vallet = 0
            self.pix_vallet = 0
            self.debito_martercard_vallet = 0
            self.debito_visa_vallet = 0
            self.debito_elo_vallet = 0
            self.credito_mastercard_vallet = 0
            self.credito_visa_vallet = 0
            self.credito_elo_vallet = 0
            self.hiper_vallet = 0
            self.american_express_vallet = 0
            self.alelo_vallet = 0
            self.sodexo_vallet = 0
            self.ticket_rest_vallet = 0
            self.vale_refeicao_vallet = 0
            self.dinersclub_vallet = 0
            self.qtd_veiculo = 0
            self.taxa_vallet = 0

        self.debito_vallet = self.debito_martercard_vallet + self.debito_visa_vallet + self.debito_elo_vallet
        self.credito_vallet = self.credito_mastercard_vallet + self.credito_visa_vallet + self.credito_elo_vallet
        self.outros_cartoes_vallet = self.hiper_vallet + self.american_express_vallet + self.alelo_vallet + self.sodexo_vallet + self.ticket_rest_vallet + self.vale_refeicao_vallet + self.dinersclub_vallet
        self.total_vallet = self.dinheiro_vallet + self.pix_vallet + self.debito_vallet + self.credito_vallet + self.outros_cartoes_vallet

    def widget_vallet(self):
        # Forms pode ser declarado utilizando a sintaxe 'with'
        with st.form(key='lançar_vallet', clear_on_submit=True):
            # st.title = ('Lançamento de VAllet')
            col1, col2, col3, col4, col5, col6= st.columns(6)
            with col1:
                self.data_vallet = st.date_input('Data', format='DD/MM/YYYY')
                self.periodo_vallet = st.selectbox('Período', ['Almoço', 'Jantar'], placeholder='', index=0)
                self.qtd_veiculo = st.number_input(label='Qtd Veículos', value=int('1'), step=5, min_value=1, max_value=500)
            with col2:
                self.dinheiro_vallet = st.number_input(label='Dinheiro', value=float('0.00'), step=10.00, min_value=0.00, max_value=25000.00)
                self.pix_vallet = st.number_input(label='Pix', value=float('0.00'), step=10.00, min_value=0.00, max_value=25000.00)
                self.hiper_vallet = st.number_input(label='Hiper', value=float('0.00'), step=10.00, min_value=0.00, max_value=25000.00)
            with col3:
                self.debito_visa_vallet = st.number_input(label='Débito Visa', value=float('0.00'), step=10.00, min_value=0.00, max_value=25000.00)
                self.debito_mastercard_vallet = st.number_input(label='Débito Master', value=float('0.00'), step=10.00, min_value=0.00, max_value=25000.00)
                self.debito_elo_vallet = st.number_input(label='Débito Elo', value=float('0.00'), step=10.00, min_value=0.00, max_value=25000.00)
            with col4:
                self.credito_visa_vallet = st.number_input(label='Crédito Visa', value=float('0.00'), step=10.00, min_value=0.00, max_value=25000.00)
                self.credito_mastercard_vallet = st.number_input(label='Crédito Master', value=float('0.00'), step=10.00, min_value=0.00, max_value=25000.00)
                self.credito_elo_vallet = st.number_input(label='Crédito Elo', value=float('0.00'), step=10.00, min_value=0.00, max_value=25000.00)
            with col5:
                self.vale_refeicao_vallet = st.number_input(label='Vale Refeição', value=float('0.00'), step=10.00, min_value=0.00, max_value=25000.00)
                self.sodexo_vallet = st.number_input(label='Sodexo', value=float('0.00'), step=10.00, min_value=0.00, max_value=25000.00)
                self.alelo_vallet = st.number_input(label='Alelo', value=float('0.00'), step=10.00, min_value=0.00, max_value=25000.00)
            with col6:
                self.ticket_rest_vallet = st.number_input(label='Ticket Restaurante', value=float('0.00'), step=10.00, min_value=0.00, max_value=25000.00)
                self.american_express_vallet = st.number_input(label='American Express', value=float('0.00'), step=10.00, min_value=0.00, max_value=25000.00)  
                self.dinersclub_vallet = st.number_input(label='DinersClub', value=float('0.00'), step=10.00, min_value=0.00, max_value=25000.00)
                submit_button = st.form_submit_button(label='Enviar', use_container_width=True)
        if submit_button:
            self.salvar_vallet()

    def salvar_vallet(self):
        if self.data_vallet == '':
            st.error('A data não foi preenchida!', icon="🚨")
        else:            
            dt_atualizo = datetime.now().strftime("%Y/%m/%d, %H:%M:%S")
            self.conecta_mysql()
            metadata = MetaData()
            vallet_table = Table('vallet', metadata,
                Column('ID', Integer, primary_key=True),
                Column('data_vallet', DateTime),
                Column('periodo', String),
                Column('qtd_veiculo', Integer),
                Column('dinheiro', Float),
                Column('pix', Float),
                Column('debito_mastercard', Float),
                Column('debito_visa', Float),
                Column('debito_elo', Float),
                Column('credito_mastercard', Float),
                Column('credito_visa', Float),
                Column('credito_elo', Float),
                Column('american_express', Float),
                Column('alelo', Float),
                Column('hiper', Float),
                Column('sodexo', Float),
                Column('ticket_rest', Float),
                Column('vale_refeicao', Float),
                Column('dinersclub', Float),
                Column('dt_atualizado', DateTime)
            )    
            # Definindo os valores para inserção
            valores = {
                'data_vallet': self.data_vallet,
                'periodo': self.periodo_vallet,
                'qtd_veiculo': int(self.qtd_veiculo),
                'dinheiro': float(self.dinheiro_vallet),
                'pix': float(self.pix_vallet),
                'debito_mastercard': float(self.debito_mastercard_vallet),
                'debito_visa': float(self.debito_visa_vallet),
                'debito_elo': float(self.debito_elo_vallet),
                'credito_mastercard': float(self.credito_mastercard_vallet),
                'credito_visa': float(self.credito_visa_vallet),
                'credito_elo': float(self.credito_elo_vallet),
                'american_express': float(self.american_express_vallet),
                'alelo': float(self.alelo_vallet),
                'hiper': float(self.hiper_vallet),
                'sodexo': float(self.sodexo_vallet),
                'ticket_rest': float(self.ticket_rest_vallet),    
                'vale_refeicao': float(self.vale_refeicao_vallet),
                'dinersclub': float(self.dinersclub_vallet),
                'dt_atualizado': dt_atualizo
            }
            # Criando uma instrução de INSERT
            stmt = insert(vallet_table).values(valores)
            # Executando a instrução de INSERT
            self.session.execute(stmt)
            # Confirmar a transação
            self.session.commit()
            # Fechando a sessão
            self.session.close()
            print('Fechado conexão - salvar_vallet')

            # precisei criar uma mensagem vazia para depois deixa-la vazia novamente depois de utiliza-la
            msg_lancamento = st.empty()
            msg_lancamento.success("Lançamento Realizado com Sucesso!")
            time.sleep(5)
            msg_lancamento.empty()

    def editar_vallet(self):
        self.dataframe_vallet()
        df = self.valores_vallet
        df.loc[:, 'data_vallet'] = pd.to_datetime(df['data_vallet'], errors='coerce')
        
        col1, col2, col3, col4, col5 = st.columns([1.5, 1.5, 1, 1, 3])  
        with col1:
            self.filtro_ID_vallet = st.multiselect('Selecione ID para edição', df['ID'], placeholder='Escolha um ID')
            if self.filtro_ID_vallet:
                df = df[df['ID'].isin(self.filtro_ID_vallet)]
        with col2:
            filtro_datas = df['data_vallet'].dt.strftime('%d/%m/%Y').unique()
            filtro_data_vallet = st.selectbox('Filtrar data', filtro_datas, 
                                                            index=None, 
                                                            placeholder='Escolha uma data') if len(filtro_datas) > 0 else None
            if filtro_data_vallet:
                filtro_data_vallet = pd.to_datetime(filtro_data_vallet, format='%d/%m/%Y')
                df = df[df['data_vallet'] == filtro_data_vallet]

        # pegando o nome das colunas
        coluna_vallet = self.valores_vallet.columns.tolist()

        # alterei nome das colunas para o widget
        coluna_vallet = ['Data', 'Dinheiro', 'Pix', 'Debito Master', 'Debito Visa', 'Debito Elo', 'Credito Master', 
                            'Credito Visa', 'Credito Elo', 'Hiper', 'American Express', 'Alelo', 'Sodexo', 'Ticket Rest', 
                            'Vale Refeição', 'DinersClub', 'Rodízio', 'Período', 'Data Atualização', 'ID']
        # witdget
        excluir_coluna = st.multiselect('Excluir coluna', coluna_vallet, placeholder='Selecione a coluna', key='excluir_coluna_vallet_edit')
        
        # necessário voltar para o nome da coluna original, para tabela a seguir
        nomes_alterados = {
            'Data': 'data_vallet',
            'Dinheiro': 'dinheiro', 'Pix': 'pix',
            'Debito Master': 'debito_mastercard', 'Debito Visa': 'debito_visa', 'Debito Elo': 'debito_elo',
            'Credito Master': 'credito_mastercard', 'Credito Visa': 'credito_visa', 'Credito Elo': 'credito_elo', 
            'Hiper': 'hiper', 'American Express': 'american_express', 'Alelo': 'alelo', 'Sodexo': 'sodexo', 'Ticket Rest': 'ticket_rest', 
            'Vale Refeição': 'vale_refeicao', 'DinersClub': 'dinersclub',
            'Qtde Veículo': 'qtd_veiculo',
            'Período': 'periodo',
            'Data Atualização': 'dt_atualizado',
            'ID': 'ID'
                }

        # excluir as colunas selecionadas no widget
        excluir_coluna = [nomes_alterados[coluna] if coluna in nomes_alterados else coluna for coluna in excluir_coluna]

        df = self.valores_vallet.drop(excluir_coluna, axis=1)
        if len(self.filtro_ID_vallet) > 0:  # Se houver IDs filtrados, aplique o filtro
            df = df[df['ID'].isin(self.filtro_ID_vallet)]
        
        if filtro_data_vallet:
            df = df[df['data_vallet'] == filtro_data_vallet]

        # Bloquear algumas colunas da edição
        colunas_bloqueadas = {
        'dt_atualizado': {'editable': False},
        'ID': {'editable': False}
        }
        
        colunas_formatada = {
            'ID': st.column_config.NumberColumn('ID', format='%d'),
            'data_vallet': st.column_config.DateColumn('Data Vallet', format='DD/MM/YYYY'),   
            'periodo': st.column_config.SelectboxColumn('Período', options=['Almoço', 'Jantar'], required=True),
            'qtd_veiculo': st.column_config.NumberColumn('Qtde Veículo', format='%d', min_value=1, max_value=500),
            'dinheiro': st.column_config.NumberColumn('Dinheiro', format='$%f', min_value=0, max_value=25000),
            'pix': st.column_config.NumberColumn('Pix', format='$%f', min_value=0, max_value=25000),
            'debito_mastercard': st.column_config.NumberColumn('Debito Master', format='$%f', min_value=0, max_value=25000),
            'debito_visa': st.column_config.NumberColumn('Debito Visa', format='$%f', min_value=0, max_value=25000),
            'debito_elo': st.column_config.NumberColumn('Debito Elo', format='$%f', min_value=0, max_value=25000),
            'credito_mastercard': st.column_config.NumberColumn('Credito Master', format='$%f', min_value=0, max_value=25000),
            'credito_visa': st.column_config.NumberColumn('Credito Visa', format='$%f', min_value=0, max_value=25000),
            'credito_elo': st.column_config.NumberColumn('Credito Elo', format='$%f', min_value=0, max_value=25000),
            'alelo': st.column_config.NumberColumn('Alelo', format='$%f', min_value=0, max_value=25000),
            'hiper': st.column_config.NumberColumn('Hiper', format='$%f', min_value=0, max_value=25000),
            'american_express': st.column_config.NumberColumn('American Express', format='$%f', min_value=0, max_value=25000),
            'sodexo': st.column_config.NumberColumn('Sodexo', format='$%f', min_value=0, max_value=25000),
            'ticket_rest': st.column_config.NumberColumn('Ticket Rest', format='$%f', min_value=0, max_value=25000),
            'vale_refeicao': st.column_config.NumberColumn('Vale Refeição', format='$%f', min_value=0, max_value=25000),
            'dinersclub': st.column_config.NumberColumn('DinersClub', format='$%f', min_value=0, max_value=25000),
            'dt_atualizado': st.column_config.DatetimeColumn('Atualizado', format='DD/MM/YYYY- h:mm A'),
        }
        # Aplicando a formatação apenas nas colunas que ainda existem
        colunas_formatadas_existem = {key: value for key, value in colunas_formatada.items() if key in df.columns}

        # num_rows = 'dynamic' é um parametro para habilitar a inclusão de linhas
        # disabled = deixa as colunas ineditavel
        tabela_editavel = st.data_editor(df, 
                                            disabled=colunas_bloqueadas, 
                                            column_config=colunas_formatadas_existem, 
                                            column_order=['ID', 'data_vallet', 'periodo', 'qtd_veiculo', 'dinheiro', 'pix', 
                                                            'debito_mastercard', 'debito_visa', 'debito_elo', 'credito_mastercard', 
                                                            'credito_visa', 'credito_elo', 'alelo', 'hiper', 'american_express', 
                                                            'sodexo', 'ticket_rest', 'vale_refeicao', 'dinersclub',
                                                            'dt_atualizado'], 
                                            hide_index=True)
        
        # Função para atualizar dados no banco de dados
        def update_data_vallet(df):
            df = df.drop(['taxa', 'total'], axis=1)

            # atualização acontece apenas nas colunas disponivel
            self.conecta_mysql2()
            cursor = self.conn.cursor()
            data_atual = datetime.now().strftime("%Y/%m/%d, %H:%M:%S")
            
            # Obter as colunas disponíveis
            colunas_disponiveis = df.columns.tolist()

            for index, row in df.iterrows():
                query = "UPDATE vallet SET "
                valores = []
                for coluna in colunas_disponiveis:
                    # Verificar se a coluna está presente no índice da linha atual
                    if coluna in row.index:
                        valor = row[coluna]
                        # Se o valor for uma string, adicione aspas simples ao redor dele
                        if isinstance(valor, str):
                            valor = f"'{valor}'"
                        # Se a coluna for uma coluna de data ou hora, formate-a corretamente
                        if 'data' in coluna or 'dt_atualizado' in coluna:
                            valor = f"STR_TO_DATE('{valor}', '%Y-%m-%d %H:%i:%s')"
                        valores.append(f"{coluna} = {valor}")
                # Adicionar a data_atual à lista de valores
                valores.append(f"dt_atualizado = STR_TO_DATE('{data_atual}', '%Y/%m/%d, %H:%i:%s')")
                # Construir a parte SET da query
                query += ', '.join(valores)
                # Adicionar a condição WHERE ID = {row['ID']}
                query += f" WHERE ID = {row['ID']}"
                try:
                    cursor.execute(query)
                except Exception as e:
                    print(f"Erro ao executar a query: {query}")
                    print(f"Erro detalhado: {e}")
                        
            self.conn.commit()
            cursor.close()
            self.conn.close()
            print('Fechado conexão - update_data_vallet')

        with col3:
            if st.button('Salvar Alterações'):
                if len(self.filtro_ID_vallet) > 0 or filtro_data_vallet is not None:
                    update_data_vallet(tabela_editavel)
                    with col4:
                        # precisei criar uma mensagem vazia para depois deixa-la vazia novamente depois de utiliza-la
                        msg_lancamento = st.empty()
                        msg_lancamento.success("Edição realizada com Sucesso!")
                        time.sleep(10)
                        msg_lancamento.empty()
                else:
                    with col5:
                        msg_lancamento = st.empty()
                        msg_lancamento.error('Selecione uma data ou ID que deseja editar!', icon="🚨")
                        time.sleep(10)
                        msg_lancamento.empty()
        with col4:
            if st.button('Deletar Vallet'):
                if len(self.filtro_ID_vallet) > 1 or len(self.filtro_ID_vallet) == 0:
                    with col5:
                        msg_lancamento = st.empty()
                        msg_lancamento.error("Selecione um único ID!", icon="🚨")
                        time.sleep(5)
                        msg_lancamento.empty()
                else:
                    self.deletar_vallet()
                    with col5:
                        msg_lancamento = st.empty()
                        msg_lancamento.success("ID deletado com Sucesso!")
                        time.sleep(5)
                        msg_lancamento.empty()

    def deletar_vallet(self):
        try:
            if isinstance(self.filtro_ID_vallet, list) and len(self.filtro_ID_vallet) == 1:
                filtro_ID_vallet = self.filtro_ID_vallet[0]
            else:
                filtro_ID_vallet = self.filtro_ID_vallet
            
            self.conecta_mysql()
            comando = text("DELETE FROM vallet WHERE ID = :ID")
            valores = {'ID': filtro_ID_vallet}
            
            # Execute a instrução SQL usando os valores e placeholders seguros
            self.session.execute(comando, valores)
            # Comite as mudanças
            self.session.commit()

        except Exception as e:
            # Em caso de erro, desfazer a transação
            self.session.rollback()
            st.error(f'Ocorreu um erro: {e}')
        finally:
            self.session.close()
            print('Fechado conexão - deletar_vallet')

    def caixas_expansivas_vallet(self):
        # pegando a coluna data
        self.valores_vallet_np = np.array(self.valores_vallet)
        self.data_vallet = np.array([ts.strftime('%d/%m/%Y') for ts in self.valores_vallet_np[:, 0]])
        # somando total de valores para cada dia (coluna total de uma tabela)
        # somando todas as linhas da coluna 0 até a 14 -> o mesmo que ter uma coluna total de uma tabela
        # total de vendas desconsiderando consumo dos sócios
        self.array_total_vallet = np.nansum(self.array_vallet[:, 0:15], axis=1)

        with st.expander('Tabela Vallet'):
            # pegando o nome das colunas
            coluna_vendas = self.valores_vallet.columns.tolist()

            # alterei nome das colunas para o widget
            # não inclui a coluna Rodízio pois não posso excluir essa coluna devido o subset na configuração da tabela_vendas que me mostra a max do rodizio
            coluna_vendas = ['Data', 'Dinheiro', 'Pix', 'Debito Master', 'Debito Visa', 'Debito Elo', 'Credito Master', 
                             'Credito Visa', 'Credito Elo', 'Hiper', 'American Express', 'Alelo', 'Sodexo', 'Ticket Rest', 
                             'Vale Refeição', 'DinersClub', 'Período', 'Data Atualização', 'ID']
            # witdget
            excluir_coluna = st.multiselect('Excluir coluna', coluna_vendas, placeholder='Selecione a coluna')
            
            # necessário voltar para o nome da coluna original, para tabela a seguir
            nomes_alterados = {
                'Data': 'data_venda',
                'Dinheiro': 'dinheiro', 'Pix': 'pix',
                'Debito Master': 'debito_mastercard', 'Debito Visa': 'debito_visa', 'Debito Elo': 'debito_elo',
                'Credito Master': 'credito_mastercard', 'Credito Visa': 'credito_visa', 'Credito Elo': 'credito_elo', 
                'Hiper': 'hiper', 'American Express': 'american_express', 'Alelo': 'alelo', 'Sodexo': 'sodexo', 
                'Ticket Rest': 'ticket_rest', 'Vale Refeição': 'vale_refeicao', 'DinersClub': 'dinersclub',
                'Qtde Veículo': 'qtd_veiculo',
                'Período': 'periodo', 
                'Data Atualização': 'dt_atualizado',
                'ID': 'ID'
                    }

            # excluir as colunas selecionadas no widget
            excluir_coluna = [nomes_alterados[coluna] if coluna in nomes_alterados else coluna for coluna in excluir_coluna]

            formas_pagamento = ['dinheiro', 'pix',
                                'debito_mastercard', 'debito_visa', 'debito_elo',
                                'credito_mastercard', 'credito_visa', 'credito_elo',
                                'alelo', 'american_express',
                                'sodexo', 'ticket_rest', 'vale_refeicao', 'hiper']

            df = self.valores_vallet.copy()
            df['total'] = df[formas_pagamento].sum(axis=1).round(2)

            df = df.drop(excluir_coluna, axis=1)

            colunas_formatada = {
            'ID': st.column_config.NumberColumn('ID', format='%d', min_value=1, max_value=500),
            'data_vallet': st.column_config.DateColumn('Data', format='DD/MM/YYYY'),
            'periodo': st.column_config.SelectboxColumn('Período', options=['Almoço', 'Jantar'], required=True),
            'qtd_veiculo': st.column_config.NumberColumn('Qtde Veículo', format='%d', min_value=1, max_value=500),
            'dinheiro': st.column_config.NumberColumn('Dinheiro', format='$%f', min_value=0, max_value=25000),
            'pix': st.column_config.NumberColumn('Pix', format='$%f', min_value=0, max_value=25000),
            'debito_mastercard': st.column_config.NumberColumn('Debito Master', format='$%f', min_value=0, max_value=25000),
            'debito_visa': st.column_config.NumberColumn('Debito Visa', format='$%f', min_value=0, max_value=25000),
            'debito_elo': st.column_config.NumberColumn('Debito Elo', format='$%f', min_value=0, max_value=25000),
            'credito_mastercard': st.column_config.NumberColumn('Credito Master', format='$%f', min_value=0, max_value=25000),
            'credito_visa': st.column_config.NumberColumn('Credito Visa', format='$%f', min_value=0, max_value=25000),
            'credito_elo': st.column_config.NumberColumn('Credito Elo', format='$%f', min_value=0, max_value=25000),
            'alelo': st.column_config.NumberColumn('Alelo', format='$%f', min_value=0, max_value=25000),
            'hiper': st.column_config.NumberColumn('Hiper', format='$%f', min_value=0, max_value=25000),
            'american_express': st.column_config.NumberColumn('American Express', format='$%f', min_value=0, max_value=25000),
            'sodexo': st.column_config.NumberColumn('Sodexo', format='$%f', min_value=0, max_value=25000),
            'ticket_rest': st.column_config.NumberColumn('Ticket Rest', format='$%f', min_value=0, max_value=25000),
            'vale_refeicao': st.column_config.NumberColumn('Vale Refeição', format='$%f', min_value=0, max_value=25000),
            'dinersclub': st.column_config.NumberColumn('DinersClub', format='$%f', min_value=0, max_value=25000),
            'total': st.column_config.NumberColumn('Total', format='$%f', min_value=0, max_value=2000),
            'dt_atualizado': st.column_config.DatetimeColumn('Atualizando', format='DD/MM/YYYY- h:mm A'),
            }

            # Aplicando a formatação apenas nas colunas que ainda existem
            colunas_formatadas_existem = {key: value for key, value in colunas_formatada.items() if key in df.columns}

            tabela_vallet = st.dataframe(df,
                                         hide_index=True,
                                         column_config=colunas_formatadas_existem,
                                         column_order=['ID', 'data_vallet',
                                                        'periodo', 
                                                        'qtd_veiculo',
                                                        'dinheiro', 'pix', 
                                                        'debito_mastercard', 'debito_visa', 'debito_elo',
                                                        'credito_mastercard', 'credito_visa', 'credito_elo',
                                                        'alelo', 'hiper', 'american_express', 'sodexo',
                                                        'ticket_rest', 'vale_refeicao', 'dinersclub', 'total',
                                                        'dt_atualizado'])
            
        with st.expander('Gráfico Vallet - Visão diária e por período'):
            # ([3,1]) -> essa informação é a proporção de 3 para 1 da coluna 1 para a coluna 2
            col1, col2 = st.columns([3,1])
            with col1:    
                # Converta a matriz em um DataFrame
                colunas = ['Data', 'Valor']
                grafico_vendas = np.column_stack((self.data_vallet, self.array_total_vallet))    
                df = pd.DataFrame(grafico_vendas, columns=colunas)

                # Convertendo a coluna de datas para o tipo datetime para que consiga ordenar o eixo x (data) do gráfico
                df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')
                # Ordenando o DataFrame pela coluna de datas
                df = df.sort_values(by=['Data'])
                # deixando o ajuste do distanciamento das barras automatico
                if not df['Data'].empty:
                    largura_ideal = 950 / len(df['Data'])
                else:
                    largura_ideal = 950
                
                # Gráfico de barras - vendas
                graf_vendas = alt.Chart(df).mark_bar(
                                                    cornerRadiusTopLeft=10, cornerRadiusTopRight=10, size=largura_ideal).encode(
                                                    x = alt.X(
                                                        'Data:T', 
                                                        axis=alt.Axis(title='Data',
                                                                      format='%d/%m/%Y',
                                                                      labelAngle=-90)),
                                                    y = alt.Y(
                                                        'Valor:Q',
                                                        axis=alt.Axis(
                                                            title='Valor Vallet')),
                                                    tooltip = ['Data', 'Valor']
                                                    ) #.properties(
                                                        # title= 'Vendas diária')
                
                # rotulos = graf_vendas.mark_text(dy= -6, size=17).encode(text='Valor')

                linha_media = alt.Chart(df).mark_rule(color='red').encode(y='mean(Valor):Q')
                
                st.altair_chart(graf_vendas + linha_media, use_container_width=True)

            with col2:
                periodo = self.valores_vallet_np[:, 17]

                # Converta a matriz em um DataFrame
                coluna2 = ['Periodo', 'Valor']
                df_periodo = np.column_stack((periodo, self.array_total_vallet))
                grafico_pizza_venda = pd.DataFrame(df_periodo, columns=coluna2)
            
                grafico_pizza_venda = alt.Chart(grafico_pizza_venda).mark_arc(innerRadius=25, outerRadius=60).encode(
                    theta = alt.Theta(field='Valor', type='quantitative', stack=True),
                    color = alt.Color(field='Periodo', type='nominal') 
                ).properties(title= 'Gráfico por período')  #width=700, height=450, 
                st.altair_chart(grafico_pizza_venda, use_container_width=True)

        with st.expander('Gráfico Mensal'):
            # df_ano_mes = self.df_vendas # esse df_vendas não tem filtro na data pega todos os meses
            df_ano_mes = self.valores_vallet.drop(columns=['total', 'taxa'], axis=1)
            
            # # df_ano_mes['data_venda'] = pd.to_datetime(df_ano_mes['data_venda'], format='%d/%m/%Y')
            df_ano_mes['ano'] = df_ano_mes['data_vallet'].dt.year
            df_ano_mes['mes'] = df_ano_mes['data_vallet'].dt.month
            df_ano_mes['mes'] = df_ano_mes['data_vallet'].dt.month.apply(lambda x: calendar.month_abbr[x])
            
            # Filtro do ano
            df_filtrado = df_ano_mes.loc[(df_ano_mes['data_vallet'].dt.year == df_ano_mes['ano'])]
            df_ano_mes = df_filtrado.drop(['data_vallet', 'ID', 'periodo', 'qtd_veiculo', 'dt_atualizado', 'ano', 'mes'], axis=1)
            df_ano_mes = np.array(df_ano_mes)

            # garantir que array esta como string e assim poder aplicar replace
            df_ano_mes = df_ano_mes.astype(str)
            # substiturir valores vazios por nan e assim converter valores para float
            df_ano_mes[df_ano_mes == ''] = 0 #'nan'
            df_ano_mes = df_ano_mes.astype(float)
            
            data = np.array(df_filtrado['mes'])
            valor = np.nansum(df_ano_mes, axis=1)
            
            colunas = ['Meses', 'Valor']
            array_vendas_mes = np.column_stack((data, valor))
            df_vendas_mes = pd.DataFrame(array_vendas_mes, columns=colunas)

            # Defina a ordem dos meses em uma lista
            ordem_meses = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

            # Converta a coluna 'Meses' para um tipo categórico com a ordem especificada
            df_vendas_mes['Meses'] = pd.Categorical(df_vendas_mes['Meses'], categories=ordem_meses, ordered=True)

            # Gráfico de barras - ticket médio
            graf_vendas_mes = alt.Chart(df_vendas_mes).mark_bar(cornerRadiusTopLeft=10, cornerRadiusTopRight=10).encode(
                    x = alt.X('Meses:O', sort=ordem_meses),
                    # x = alt.X('Meses:O', sort=ordem_meses) 
                    y = alt.Y('sum(Valor):Q', title='Vallet Mensal'),
                    # tooltip = ['Data', 'Valor']
                    ) #.properties(title= 'Vendas Mensais')
            
            rotulos_valores = graf_vendas_mes.mark_text(
            align='left',
            baseline='middle',
            dx=-30,  # Ajuste horizontal para posicionar o rótulo
            dy=10,  # Ajuste vertical para posicionar o rótulo
            fontSize = 15,
            color='black    ',  # Cor do texto
             ).encode(
            text=alt.Text('sum(Valor):Q')  # Use a soma dos valores como texto
            )

            st.altair_chart(graf_vendas_mes + rotulos_valores, use_container_width=True)
