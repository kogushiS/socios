import streamlit as st
from pygwalker.api.streamlit import StreamlitRenderer
from sqlalchemy import text, insert, Table, MetaData, Column, Integer, String, DateTime, Float
import altair as alt
import pandas as pd
import numpy as np
from datetime import datetime
import calendar
import time
from filtro import Filtros
from conexao import Conexao
from st_aggrid import GridOptionsBuilder
gb = GridOptionsBuilder()


class Vendas: 
    def __init__(self) -> None:
        self.filtro = Filtros()

    def atualizar(self):
        consulta = Conexao.conecta_bd()
        self.df_vendas = consulta[0]
        return self.df_vendas
        
    def navegacao_vendas(self):
        tab1, tab2 = st.tabs(["Resumo", "Vendas"])
        with tab1:
            self.cards_resumo_vendas()
            self.caixas_expansivas_vendas()
        with tab2:
            with st.expander("Lançamento das vendas", expanded=True):
                self.widget_vendas()
            with st.expander('Edição Vendas'):
                self.lancamento_vendas_table()
        # with tab3:
        #     with st.expander("Lançamento Vallet", expanded=False):
        #         self.widget_vallet()
        #     with st.expander('Edição Vallet'):
        #         st.write('Em desenvolvimento')

    def cards_resumo_vendas(self):
        self.dataframe_vendas()
        # Conteúdo formatado com CSS
        credito_html = f"""
        <div style='text-align: center; border: 1px solid #ddd; padding: 10px; border-radius: 5px; margin-bottom: 20px;'>
            <strong>Crédito</strong><br>
            <span style='font-size: 0.95em;'>{'R${:,.2f}'.format(self.credito)}</span><br>
            <span style='color: green; font-size: 0.8em'>{'{:.4}%'.format(self.credito / self.total_vendas * 100)}</span>
        </div>
        """
        debito_html = f"""
        <div style='text-align: center; border: 1px solid #ddd; padding: 10px; border-radius: 5px; margin-bottom: 20px;'>
            <strong>Débito</strong><br>
            <span style='font-size: 0.95em;'>{'R${:,.2f}'.format(self.debito)}</span><br>
            <span style='color: green; font-size: 0.8em'>{'{:.4}%'.format(self.debito / self.total_vendas * 100)}</span>
        </div>
        """
        dinheiro_html = f"""
        <div style='text-align: center; border: 1px solid #ddd; padding: 10px; border-radius: 5px; margin-bottom: 20px;'>
            <strong>Dinheiro</strong><br>
            <span style='font-size: 0.95em;'>R${'{:,.2f}'.format(self.dinheiro)}</span><br>
            <span style='color: green; font-size: 0.8em'>{'{:.4}%'.format(self.dinheiro / self.total_vendas * 100)}</span>
        </div>
        """
        pix_html = f"""
        <div style='text-align: center; border: 1px solid #ddd; padding: 10px; border-radius: 5px; margin-bottom: 20px;'>
            <strong>Pix</strong><br>
            <span style='font-size: 0.95em;'>R${'{:,.2f}'.format(self.pix)}</span><br>
            <span style='color: green; font-size: 0.8em'>{'{:.4}%'.format(self.pix / self.total_vendas * 100)}</span>
        </div>
        """
        beneficio_html = f"""
        <div style='text-align: center; border: 1px solid #ddd; padding: 10px; border-radius: 5px; margin-bottom: 20px;'>
            <strong>Beneficio</strong><br>
            <span style='font-size: 0.95em;'>R${'{:,.2f}'.format(self.outros_cartoes)}</span><br>
            <span style='color: green; font-size: 0.8em'>{'{:.4}%'.format(self.outros_cartoes / self.total_vendas * 100)}</span>
        </div>
        """
        ifood_html = f"""
        <div style='text-align: center; border: 1px solid #ddd; padding: 10px; border-radius: 5px; margin-bottom: 20px;'>
            <strong>Ifood</strong><br>
            <span style='font-size: 0.95em;'>R${'{:,.2f}'.format(self.ifood)}</span><br>
            <span style='color: green; font-size: 0.8em'>{'{:.4}%'.format(self.ifood / self.total_vendas * 100)}</span>
        </div>
        """
        taxa_html = f"""
        <div style='text-align: center; border: 1px solid #ddd; padding: 10px; border-radius: 5px; margin-bottom: 46px;'>
            <strong>Taxa</strong><br>
            <span style='font-size: 0.95em;'>R${'{:,.2f}'.format(self.taxa)}</span><br>
        </div>
        """
        rodizio_html = f"""
        <div style='text-align: center; border: 1px solid #ddd; padding: 10px; border-radius: 5px; margin-bottom: 46px;'>
            <strong>Rodízio</strong><br>
            <span style='font-size: 0.95em;'>{'{:,}'.format(self.rodizio)}</span><br>
        </div>
        """
        total_vendas_html = f"""
        <div style='text-align: center; border: 1px solid #ddd; padding: 10px; border-radius: 5px; margin-bottom: 46px;'>
            <strong>Total Vendas</strong><br>
            <span style='font-size: 0.95em;'>R${'{:,.2f}'.format(self.total_vendas)}</span><br>
        </div>
        """
        lucro_html = f"""
        <div style='text-align: center; border: 1px solid #ddd; padding: 10px; border-radius: 5px; margin-bottom: 46px;'>
            <strong>Lucro</strong><br>
            <span style='font-size: 0.95em;'>R${'{:,.2f}'.format(self.lucro)}</span><br>
        </div>
        """
        ticket_medio_html = f"""
        <div style='text-align: center; border: 1px solid #ddd; padding: 10px; border-radius: 5px; margin-bottom: 46px;'>
            <strong>Ticket Médio</strong><br>
            <span style='font-size: 0.95em;'>R${'{:,.2f}'.format(self.ticket_medio)}</span><br>
        </div>
        """

        cols = st.columns(6)
        with cols[0]:
            st.markdown(credito_html, unsafe_allow_html=True)
            st.markdown(debito_html, unsafe_allow_html=True)
        with cols[1]:
            st.markdown(dinheiro_html, unsafe_allow_html=True)
            st.markdown(pix_html, unsafe_allow_html=True)
        with cols[2]:
            st.markdown(beneficio_html, unsafe_allow_html=True)
            st.markdown(ifood_html, unsafe_allow_html=True)
        with cols[3]:
            st.markdown(taxa_html, unsafe_allow_html=True)
            st.markdown(rodizio_html, unsafe_allow_html=True)
        with cols[4]:
            st.markdown(total_vendas_html, unsafe_allow_html=True)
            st.markdown(lucro_html, unsafe_allow_html=True)
        with cols[5]:
            st.markdown(ticket_medio_html, unsafe_allow_html=True)

    def dataframe_vendas(self):
        self.atualizar()
        df_vendas = self.df_vendas

        # Convertendo a coluna 'data_venda' para o formato datetime
        df_vendas['data_venda'] = pd.to_datetime(df_vendas['data_venda'])

        colunas = ['qtd_rodizio', 'dinheiro', 'pix', 'debito_mastercard', 'debito_visa', 'debito_elo', 'credito_mastercard', 'credito_visa', 'socio',
                    'credito_elo', 'hiper', 'american_express', 'alelo', 'sodexo', 'ticket_rest', 'vale_refeicao', 'dinersclub', 'ifood']
        
        for item in colunas:
            df_vendas[item] = pd.to_numeric(df_vendas[item], errors='coerce')

        df_vendas['total'] = df_vendas[['dinheiro', 'pix', 'debito_mastercard', 'debito_visa', 'debito_elo', 'credito_mastercard', 
                                        'credito_visa', 'credito_elo', 'hiper', 'american_express', 'alelo', 'sodexo', 'ticket_rest',
                                        'vale_refeicao', 'dinersclub', 'ifood']].sum(axis=1)
    
        # Subtraindo 30 dias da coluna 'data_venda'
        df_vendas['data_30'] = df_vendas['data_venda'] - pd.DateOffset(days=30)

        # Criar um conjunto de pares (data_30, periodo) ou seja a data e periodo precisa corresponder
        existent_dates_and_periods = set(zip(df_vendas['data_30'], df_vendas['periodo']))
        # Criar um dicionário dos valores correspondentes por data e período
        valor_por_data_e_periodo = df_vendas.set_index(['data_venda', 'periodo'])['total'].to_dict()

        # Aplicar a busca para valores correspondentes (inserindo novas colunas data e valor referente a 30 dias atrás)
        df_vendas['data_30'] = df_vendas.apply(lambda row: row['data_30'] if (row['data_30'], row['periodo']) in existent_dates_and_periods else pd.NaT, axis=1)
        df_vendas['valor_total_30'] = df_vendas.apply(lambda row: valor_por_data_e_periodo.get((row['data_30'], row['periodo']), 0), axis=1)

        self.df_vendas = df_vendas
        # Filtrando data
        data_inicial = str(self.filtro.data_inicial)     # formato da data'2023-05-01'
        data_final = str(self.filtro.data_final)
        self.df_vendas['data_venda'] = pd.to_datetime(self.df_vendas['data_venda'], format='%Y-%m-%d')
        
        filtro_data = (self.df_vendas['data_venda'] >= data_inicial) & (self.df_vendas['data_venda'] <= data_final)

        # filtrando periodo
        # Verificar se a lista 'self.filtro.varPeriodo' está vazia
        if self.filtro.varPeriodo:
            filtro_periodo = self.df_vendas['periodo'].isin(self.filtro.varPeriodo)
        else:
            filtro_periodo = pd.Series([True] * len(self.df_vendas)) # se a lista estiver vazia, considera todos os valores como verdadeiros  

        self.valores_vendas_30dias = self.df_vendas[filtro_data & filtro_periodo]

        # removendo datas devido array mais abaixo
        self.valores_vendas = self.valores_vendas_30dias.drop(['data_30', 'valor_total_30'], axis=1)

        # Convertendo a coluna 'coluna_string' para números
        self.valores_vendas['qtd_rodizio'] = pd.to_numeric(self.valores_vendas['qtd_rodizio'], errors='coerce')
        # Converter as colunas para o tipo de dados numérico, tratando valores não numéricos como NaN
        self.valores_vendas['debito_mastercard'] = pd.to_numeric(self.valores_vendas['debito_mastercard'], errors='coerce')
        self.valores_vendas['debito_visa'] = pd.to_numeric(self.valores_vendas['debito_visa'], errors='coerce')
        self.valores_vendas['debito_elo'] = pd.to_numeric(self.valores_vendas['debito_elo'], errors='coerce')
        self.valores_vendas['credito_mastercard'] = pd.to_numeric(self.valores_vendas['credito_mastercard'], errors='coerce')
        self.valores_vendas['credito_visa'] = pd.to_numeric(self.valores_vendas['credito_visa'], errors='coerce')
        self.valores_vendas['credito_elo'] = pd.to_numeric(self.valores_vendas['credito_elo'], errors='coerce')
        self.valores_vendas['alelo'] = pd.to_numeric(self.valores_vendas['alelo'], errors='coerce')
        self.valores_vendas['american_express'] = pd.to_numeric(self.valores_vendas['american_express'], errors='coerce')
        self.valores_vendas['hiper'] = pd.to_numeric(self.valores_vendas['hiper'], errors='coerce')
        self.valores_vendas['sodexo'] = pd.to_numeric(self.valores_vendas['sodexo'], errors='coerce')
        self.valores_vendas['ticket_rest'] = pd.to_numeric(self.valores_vendas['ticket_rest'], errors='coerce')
        self.valores_vendas['vale_refeicao'] = pd.to_numeric(self.valores_vendas['vale_refeicao'], errors='coerce')
        self.valores_vendas['dinersclub'] = pd.to_numeric(self.valores_vendas['dinersclub'], errors='coerce')
        self.valores_vendas['ifood'] = pd.to_numeric(self.valores_vendas['ifood'], errors='coerce')
        self.valores_vendas['socio'] = pd.to_numeric(self.valores_vendas['socio'], errors='coerce')

        # Converter a coluna 'data_venda' para o tipo datetime
        self.valores_vendas['data_venda'] = pd.to_datetime(self.valores_vendas['data_venda'])

        # Preencher os valores NaN com zero
        self.valores_vendas = self.valores_vendas.fillna(0)

        def calcular_taxa(row):
            return (row['debito_mastercard'] + row['debito_visa']) * 0.0119 + \
                    (row['debito_elo'] + row['hiper']) * 0.0169 + \
                    (row['credito_mastercard'] + row['credito_visa']) * 0.0364 + \
                    (row['credito_elo'] + row['american_express']) * 0.0414 + \
                    row['alelo'] * 0.065 + \
                    row['vale_refeicao'] * 0.0685 + \
                    row['ticket_rest'] * 0.06 + \
                    row['sodexo'] * 0.069 + \
                    row['dinersclub'] * 0.0414 + \
                    row['pix'] * 0.0079
        
        # Aplicar a função calcular_taxa a cada linha do DataFrame e armazenar os resultados em uma nova coluna 'taxa'
        self.valores_vendas['taxa'] = self.valores_vendas.apply(calcular_taxa, axis=1)

        self.df_vendas_valores = self.valores_vendas.drop(['data_venda', 'periodo', 'dt_atualizado', 'ID'], axis=1)
        self.array_vendas = np.array(self.df_vendas_valores)

        # garantir que array esta como string e assim poder aplicar replace
        self.array_vendas = self.array_vendas.astype(str)
        self.array_vendas = np.char.replace(self.array_vendas, ',', '.')

        # substiturir valores vazios por nan e assim converter valores para float
        self.array_vendas[self.array_vendas == ''] = 0 #'nan'
        self.array_vendas = self.array_vendas.astype(float)
        
        # Somando todas as linhas por colunas
        # somando cada coluna da array -> exemplo [279, 1548, 1514, 4848...] -> cada valor é o total de cada coluna
        self.total_colunas = np.nansum(self.array_vendas, axis=0)
    
        self.dinheiro = self.total_colunas[0]
        self.pix = self.total_colunas[1]
        self.debito_martercard = self.total_colunas[2]
        self.debito_visa = self.total_colunas[3]
        self.debito_elo = self.total_colunas[4]
        self.credito_mastercard = self.total_colunas[5]
        self.credito_visa = self.total_colunas[6]
        self.credito_elo = self.total_colunas[7]
        self.hiper = self.total_colunas[8]
        self.american_express = self.total_colunas[9]
        self.alelo = self.total_colunas[10]
        self.sodexo = self.total_colunas[11]
        self.ticket_rest = self.total_colunas[12]
        self.vale_refeicao = self.total_colunas[13]
        self.dinersclub = self.total_colunas[14]
        self.rodizio = int(self.total_colunas[15])
        self.socio = self.total_colunas[16]
        self.ifood = self.total_colunas[17]
        self.taxa = (self.valores_vendas['taxa'].sum())

        self.debito = self.debito_martercard + self.debito_visa + self.debito_elo
        self.credito = self.credito_mastercard + self.credito_visa + self.credito_elo + self.american_express
        self.outros_cartoes = self.hiper + self.alelo + self.sodexo + self.ticket_rest + self.vale_refeicao + self.dinersclub
        self.total_vendas = self.dinheiro + self.pix + self.debito + self.credito + self.outros_cartoes + self.ifood
        self.ticket_medio = self.total_vendas / self.rodizio

        # dataframe pg_funcionario
        self.dataframe_pg_funcionario()
        df_pg_fuc = self.valores_pg_func
        df_pg_fuc.loc[:, 'valor_pago'] = pd.to_numeric(df_pg_fuc['valor_pago'])

        # dataframe contas pagas
        self.dataframe_compras()
        self.dataframe_vallet()

        self.fundo_caixa = 0 #float(self.total_vendas * 0.02)
        self.lucro = self.total_vendas + self.total_vallet - self.taxa - self.taxa_vallet - df_pg_fuc['valor_pago'].sum() - self.valor_compras[0] - self.fundo_caixa

    def widget_vendas(self):
        # Forms pode ser declarado utilizando a sintaxe 'with'
        with st.form(key='lançar_vendas', clear_on_submit=True):
            # st.title = ('Lançamento de Vendas')
            col1, col2, col3, col4, col5, col6= st.columns(6)
            with col1:
                self.data_venda = st.date_input('Data', format='DD/MM/YYYY')
                self.ifood = st.number_input(label='Ifood', value=float(0.00), step=10.00, min_value=0.00, max_value=5000.00)
                self.periodo = st.selectbox('Período', ['Almoço', 'Jantar'], index=None, placeholder='')
                self.rodizio = st.number_input(label='Qtd Rodízio', value=int('1'), step=5, min_value=1, max_value=500)
            with col2:
                self.socio = st.number_input('Sócio', value=float(0.00), step=10.00, min_value=0.00, max_value=5000.00)
                self.dinheiro = st.number_input(label='Dinheiro', value=float('0.00'), step=10.00, min_value=0.00, max_value=25000.00)
                self.pix = st.number_input(label='Pix', value=float('0.00'), step=10.00, min_value=0.00, max_value=25000.00)
            with col3:
                self.debito_visa = st.number_input(label='Débito Visa', value=float('0.00'), step=10.00, min_value=0.00, max_value=25000.00)
                self.debito_mastercard = st.number_input(label='Débito Master', value=float('0.00'), step=10.00, min_value=0.00, max_value=25000.00)
                self.debito_elo = st.number_input(label='Débito Elo', value=float('0.00'), step=10.00, min_value=0.00, max_value=25000.00)
            with col4:
                self.credito_visa = st.number_input(label='Crédito Visa', value=float('0.00'), step=10.00, min_value=0.00, max_value=25000.00)
                self.credito_mastercard = st.number_input(label='Crédito Master', value=float('0.00'), step=10.00, min_value=0.00, max_value=25000.00)
                self.credito_elo = st.number_input(label='Crédito Elo', value=float('0.00'), step=10.00, min_value=0.00, max_value=25000.00)
            with col5:
                self.vale_refeicao = st.number_input(label='Vale Refeição', value=float('0.00'), step=10.00, min_value=0.00, max_value=25000.00)
                self.sodexo = st.number_input(label='Sodexo', value=float('0.00'), step=10.00, min_value=0.00, max_value=25000.00)
                self.alelo = st.number_input(label='Alelo', value=float('0.00'), step=10.00, min_value=0.00, max_value=25000.00)
            with col6:
                self.ticket_rest = st.number_input(label='Ticket Restaurante', value=float('0.00'), step=10.00, min_value=0.00, max_value=25000.00)
                self.american_express = st.number_input(label='American Express', value=float('0.00'), step=10.00, min_value=0.00, max_value=25000.00)  
                self.dinersclub = st.number_input(label='DinersClub', value=float('0.00'), step=10.00, min_value=0.00, max_value=25000.00)
                submit_button = st.form_submit_button(label='Enviar', use_container_width=True)
        if submit_button:
            self.salvar_vendas()
   
    def salvar_vendas(self):
        if self.data_venda == '':
            st.error('A data da venda não foi preenchida!', icon="🚨")
        elif self.periodo == None:
            st.error('O período não foi preenchido!', icon="🚨")
        elif self.rodizio == '':
            st.error('O período não foi preenchido.', icon="🚨") #⚠
        else:            
            dt_atualizo = datetime.now().strftime("%Y/%m/%d, %H:%M:%S")
            self.conecta_mysql()

            metadata = MetaData()
            vendas_table = Table('vendas', metadata,
                Column('ID', Integer, primary_key=True),
                Column('data_venda', DateTime),
                Column('periodo', String),
                Column('qtd_rodizio', Integer),
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
                Column('socio', Float),
                Column('ifood', Float),
                Column('dt_atualizado', DateTime)
            )
            
            # Definindo os valores para inserção
            valores = {
                'data_venda': self.data_venda,
                'periodo': self.periodo,
                'qtd_rodizio': int(self.rodizio),
                'dinheiro': float(self.dinheiro),
                'pix': float(self.pix),
                'debito_mastercard': float(self.debito_mastercard),
                'debito_visa': float(self.debito_visa),
                'debito_elo': float(self.debito_elo),
                'credito_mastercard': float(self.credito_mastercard),
                'credito_visa': float(self.credito_visa),
                'credito_elo': float(self.credito_elo),
                'american_express': float(self.american_express),
                'alelo': float(self.alelo),
                'hiper': float(self.hiper),
                'sodexo': float(self.sodexo),
                'ticket_rest': float(self.ticket_rest),    
                'vale_refeicao': float(self.vale_refeicao),
                'dinersclub': float(self.dinersclub),
                'socio': float(self.socio),
                'ifood': float(self.ifood),
                'dt_atualizado': dt_atualizo
            }

            # Criando uma instrução de INSERT
            stmt = insert(vendas_table).values(valores)
            # Executando a instrução de INSERT
            self.session.execute(stmt)
            # Confirmar a transação
            self.session.commit()
            # Fechando a sessão
            self.session.close()
            print('Fechado conexão - salvar_vendas')

            # precisei criar uma mensagem vazia para depois deixa-la vazia novamente depois de utiliza-la
            msg_lancamento = st.empty()
            msg_lancamento.success("Lançamento Realizado com Sucesso!")
            time.sleep(5)
            msg_lancamento.empty()
            # fazer com que apos 5 segundos a mensagem de sucesso apague PENDENTE

    def deletar_vendas(self):
        try:
            if isinstance(self.filtro_ID_vendas, list) and len(self.filtro_ID_vendas) == 1:
                filtro_ID_vendas = self.filtro_ID_vendas[0]
            else:
                filtro_ID_vendas = self.filtro_ID_vendas
            
            self.conecta_mysql()
            comando = text("DELETE FROM vendas WHERE ID = :ID")
            valores = {'ID': filtro_ID_vendas}
            
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
            print('Fechado conexão - deletar_vendas')

    def lancamento_vendas_table(self):
        df = self.valores_vendas
        df.loc[:, 'data_venda'] = pd.to_datetime(df['data_venda'], errors='coerce')
        
        col1, col2, col3, col4, col5 = st.columns([1.5, 1.5, 1, 1, 3])  
        with col1:
            self.filtro_ID_vendas = st.multiselect('Selecione ID para edição', df['ID'], placeholder='Escolha um ID')
            if self.filtro_ID_vendas:
                df = df[df['ID'].isin(self.filtro_ID_vendas)]
        with col2:
            filtro_datas = df['data_venda'].dt.strftime('%d/%m/%Y').unique()
            filtro_data_vendas = st.selectbox('Filtrar data', filtro_datas, 
                                                            index=None, 
                                                            placeholder='Escolha uma data') if len(filtro_datas) > 0 else None
            if filtro_data_vendas:
                filtro_data_vendas = pd.to_datetime(filtro_data_vendas, format='%d/%m/%Y')
                df = df[df['data_venda'] == filtro_data_vendas]

        # pegando o nome das colunas
        coluna_vendas = self.valores_vendas.columns.tolist()

        # alterei nome das colunas para o widget
        coluna_vendas = ['Data Venda', 'Dinheiro', 'Pix', 'Debito Master', 'Debito Visa', 'Debito Elo', 'Credito Master', 
                            'Credito Visa', 'Credito Elo', 'Hiper', 'American Express', 'Alelo', 'Sodexo', 'Ticket Rest', 
                            'Vale Refeição', 'DinersClub', 'Rodízio', 'Sócio', 'ifood', 'Período', 'Data Atualização', 'ID']
        # witdget
        excluir_coluna = st.multiselect('Excluir coluna', coluna_vendas, placeholder='Selecione a coluna', key='excluir_coluna_vendas_edit')
        
        # necessário voltar para o nome da coluna original, para tabela a seguir
        nomes_alterados = {
            'Data Venda': 'data_venda',
            'Dinheiro': 'dinheiro', 'Pix': 'pix',
            'Debito Master': 'debito_mastercard', 'Debito Visa': 'debito_visa', 'Debito Elo': 'debito_elo',
            'Credito Master': 'credito_mastercard', 'Credito Visa': 'credito_visa', 'Credito Elo': 'credito_elo', 
            'Hiper': 'hiper', 'American Express': 'american_express', 'Alelo': 'alelo', 'Sodexo': 'sodexo', 'Ticket Rest': 'ticket_rest', 
            'Vale Refeição': 'vale_refeicao', 'DinersClub': 'dinersclub',
            'Rodízio': 'qtd_rodizio',
            'Sócio': 'socio',
            'Ifood': 'ifood',
            'Período': 'periodo',
            'Data Atualização': 'dt_atualizado',
            'ID': 'ID'
                }

        # excluir as colunas selecionadas no widget
        excluir_coluna = [nomes_alterados[coluna] if coluna in nomes_alterados else coluna for coluna in excluir_coluna]

        df = self.valores_vendas.drop(excluir_coluna, axis=1)
        if len(self.filtro_ID_vendas) > 0:  # Se houver IDs filtrados, aplique o filtro
            df = df[df['ID'].isin(self.filtro_ID_vendas)]
        
        if filtro_data_vendas:
            df = df[df['data_venda'] == filtro_data_vendas]

        # Bloquear algumas colunas da edição
        colunas_bloqueadas = {
        'dt_atualizado': {'editable': False},
        'ID': {'editable': False}
        }
        
        colunas_formatada = {
            'ID': st.column_config.NumberColumn('ID', format='%d'),
            'data_venda': st.column_config.DateColumn('Data Venda', format='DD/MM/YYYY'),   
            'periodo': st.column_config.SelectboxColumn('Período', options=['Almoço', 'Jantar'], required=True),
            'qtd_rodizio': st.column_config.NumberColumn('Rodízio', format='%d', min_value=1, max_value=500),
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
            'ifood': st.column_config.NumberColumn('Ifood', format='$%f', min_value=0, max_value=5000),
            'socio': st.column_config.NumberColumn('Sócio', format='$%f', min_value=0, max_value=2000),
            'dt_atualizado': st.column_config.DatetimeColumn('Atualizado', format='DD/MM/YYYY- h:mm A'),
        }
        # Aplicando a formatação apenas nas colunas que ainda existem
        colunas_formatadas_existem = {key: value for key, value in colunas_formatada.items() if key in df.columns}

        # num_rows = 'dynamic' é um parametro para habilitar a inclusão de linhas
        # disabled = deixa as colunas ineditavel
        tabela_editavel = st.data_editor(df, 
                                            disabled=colunas_bloqueadas, 
                                            column_config=colunas_formatadas_existem, 
                                            column_order=['ID', 'data_venda', 'ifood', 'periodo', 'qtd_rodizio', 'dinheiro', 'pix', 
                                                            'debito_mastercard', 'debito_visa', 'debito_elo', 'credito_mastercard', 
                                                            'credito_visa', 'credito_elo', 'alelo', 'hiper', 'american_express', 
                                                            'sodexo', 'ticket_rest', 'vale_refeicao', 'dinersclub', 'socio',
                                                            'dt_atualizado'], 
                                            hide_index=True)
        
        # Função para atualizar dados no banco de dados
        def update_data_vendas(df):
            df = df.drop(['taxa', 'total'], axis=1)

            # atualização acontece apenas nas colunas disponivel
            self.conecta_mysql2()
            cursor = self.conn.cursor()
            data_atual = datetime.now().strftime("%Y/%m/%d, %H:%M:%S")
            
            # Obter as colunas disponíveis
            colunas_disponiveis = df.columns.tolist()

            for index, row in df.iterrows():
                query = "UPDATE vendas SET "
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
            print('Fechado conexão - update_data_vendas')

        with col3:
            if st.button('Salvar Alterações'):
                if len(self.filtro_ID_vendas) > 0 or filtro_data_vendas is not None:
                    update_data_vendas(tabela_editavel)
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
            if st.button('Deletar Vendas'):
                if len(self.filtro_ID_vendas) > 1 or len(self.filtro_ID_vendas) == 0:
                    with col5:
                        msg_lancamento = st.empty()
                        msg_lancamento.error("Selecione um único ID!", icon="🚨")
                        time.sleep(5)
                        msg_lancamento.empty()
                else:
                    self.deletar_vendas()
                    with col5:
                        msg_lancamento = st.empty()
                        msg_lancamento.success("ID deletado com Sucesso!")
                        time.sleep(5)
                        msg_lancamento.empty()
    
    def caixas_expansivas_vendas(self):
        # pegando a coluna data
        self.valores_vendas_np = np.array(self.valores_vendas)
        self.data_vendas = np.array([ts.strftime('%d/%m/%Y') for ts in self.valores_vendas_np[:, 0]])
        # somando total de valores para cada dia (coluna total de uma tabela)
        # somando todas as linhas da coluna 0 até a 14 -> o mesmo que ter uma coluna total de uma tabela
        # total de vendas desconsiderando consumo dos sócios
        self.array_total_vendas = np.nansum(self.array_vendas[:, 0:15], axis=1)

        with st.expander('Tabela das vendas'):
            # pegando o nome das colunas
            coluna_vendas = self.valores_vendas.columns.tolist()

            # alterei nome das colunas para o widget
            # não inclui a coluna Rodízio pois não posso excluir essa coluna devido o subset na configuração da tabela_vendas que me mostra a max do rodizio
            coluna_vendas = ['Data Venda', 'Dinheiro', 'Pix', 'Debito Master', 'Debito Visa', 'Debito Elo', 'Credito Master', 
                             'Credito Visa', 'Credito Elo', 'Hiper', 'American Express', 'Alelo', 'Sodexo', 'Ticket Rest', 
                             'Vale Refeição', 'DinersClub', 'Sócio', 'Ifood', 'Período', 'Data Atualização', 'ID']
            # witdget
            excluir_coluna = st.multiselect('Excluir coluna', coluna_vendas, placeholder='Selecione a coluna')
            
            # necessário voltar para o nome da coluna original, para tabela a seguir
            nomes_alterados = {
                'Data Venda': 'data_venda',
                'Dinheiro': 'dinheiro', 'Pix': 'pix',
                'Debito Master': 'debito_mastercard', 'Debito Visa': 'debito_visa', 'Debito Elo': 'debito_elo',
                'Credito Master': 'credito_mastercard', 'Credito Visa': 'credito_visa', 'Credito Elo': 'credito_elo', 
                'Hiper': 'hiper', 'American Express': 'american_express', 'Alelo': 'alelo', 'Sodexo': 'sodexo', 
                'Ticket Rest': 'ticket_rest', 'Vale Refeição': 'vale_refeicao', 'DinersClub': 'dinersclub',
                'Rodízio': 'qtd_rodizio',
                'Sócio': 'socio',
                'Ifood': 'ifood', 
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
                                'sodexo', 'ticket_rest', 'vale_refeicao', 'hiper',
                                'ifood', 'socio']

            df = self.valores_vendas.copy()
            df['total'] = df[formas_pagamento].sum(axis=1).round(2)

            df = df.drop(excluir_coluna, axis=1)

            # df = self.valores_vendas.drop(excluir_coluna, axis=1)

            # df['data_venda'] = pd.to_datetime(df['data_venda']).dt.strftime('%d/%m/%Y')

            colunas_formatada = {
            'ID': st.column_config.NumberColumn('ID', format='%d', min_value=1, max_value=500),
            'data_venda': st.column_config.DateColumn('Data Venda', format='DD/MM/YYYY'),
            'periodo': st.column_config.SelectboxColumn('Período', options=['Almoço', 'Jantar'], required=True),
            'qtd_rodizio': st.column_config.NumberColumn('Rodízio', format='%d', min_value=1, max_value=500),
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
            'ifood': st.column_config.NumberColumn('Ifood', format='$%f', min_value=0, max_value=5000),
            'socio': st.column_config.NumberColumn('Sócio', format='$%f', min_value=0, max_value=2000),
            'total': st.column_config.NumberColumn('Total', format='$%f', min_value=0, max_value=2000),
            'dt_atualizado': st.column_config.DatetimeColumn('Atualizando', format='DD/MM/YYYY- h:mm A'),
            }

            # Aplicando a formatação apenas nas colunas que ainda existem
            colunas_formatadas_existem = {key: value for key, value in colunas_formatada.items() if key in df.columns}

            tabela_vendas = st.dataframe(df,
                                         hide_index=True,
                                         column_config=colunas_formatadas_existem,
                                         column_order=['ID', 'data_venda',
                                                        'ifood', 
                                                        'periodo', 
                                                        'qtd_rodizio',
                                                        'dinheiro', 'pix', 
                                                        'debito_mastercard', 'debito_visa', 'debito_elo',
                                                        'credito_mastercard', 'credito_visa', 'credito_elo',
                                                        'alelo', 'hiper', 'american_express', 'sodexo',
                                                        'ticket_rest', 'vale_refeicao', 'dinersclub', 'total', 'socio',
                                                        'dt_atualizado'])
            
        with st.expander('Gráfico das Vendas - Visão diária e por período'):
            # ([3,1]) -> essa informação é a proporção de 3 para 1 da coluna 1 para a coluna 2
            col1, col2 = st.columns([3,1])
            with col1:    
                # Converta a matriz em um DataFrame
                colunas = ['Data', 'Valor']
                grafico_vendas = np.column_stack((self.data_vendas, self.array_total_vendas))    
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
                                                    y = alt.Y('Valor:Q',
                                                              axis=alt.Axis(title='Valor Venda')),
                                                    tooltip = ['Data', 'Valor']
                                                    ).properties(
                                                        title= 'Vendas diária')
                
                # rotulos = graf_vendas.mark_text(dy= -6, size=17).encode(text='Valor')

                linha_media = alt.Chart(df).mark_rule(color='red').encode(
                    y='mean(Valor):Q')
                
                st.altair_chart(graf_vendas + linha_media, use_container_width=True)

            with col2:
                periodo = self.valores_vendas_np[:, 18]

                # Converta a matriz em um DataFrame
                coluna2 = ['Periodo', 'Valor']
                df_periodo = np.column_stack((periodo, self.array_total_vendas))
                grafico_pizza_venda = pd.DataFrame(df_periodo, columns=coluna2)
            
                grafico_pizza_venda = alt.Chart(grafico_pizza_venda).mark_arc(innerRadius=25, outerRadius=60).encode(
                    theta = alt.Theta(field='Valor', type='quantitative', stack=True),
                    color = alt.Color(field='Periodo', type='nominal') 
                ).properties(title= 'Gráfico por período')  #width=700, height=450, 
                st.altair_chart(grafico_pizza_venda, use_container_width=True)

        with st.expander('Gráfico do Ticket Médio'):
            # incuido coluna ticket medio
            array_ticket_medio = np.column_stack((self.array_vendas, (self.array_vendas[:,18]) / self.array_vendas[:, 15]))
            
            # convertendo a coluna ticket media para duas casas decimais
            self.ticket_medio = np.round(array_ticket_medio[:, 20], 2)
            
            colunas = ['Data', 'Valor']
            array_ticket_medio = np.column_stack((self.data_vendas, self.ticket_medio))
            df_ticket = pd.DataFrame(array_ticket_medio, columns=colunas)

            # Gráfico de barras - ticket médio
            graf_ticket_medio = alt.Chart(df_ticket).mark_line(strokeWidth=2, interpolate='basis').encode(
                    x = 'Data:N',
                    y = alt.Y('Valor:Q', scale=alt.Scale(domain=[80, 180]), axis=alt.Axis(title='Ticket Médio')),
                    tooltip = ['Data', 'Valor']
                    ) #.properties(title= 'Ticket Médio')
                       
            linha = alt.Chart(df_ticket).mark_rule(color='red').encode(
                    y='mean(Valor):Q')
            
            # Adicionando rótulos aos pontos da linha
            rotulo_linha = linha.mark_text(
                align='left',
                baseline='line-bottom', # top middle bottom alphabetic', 'line-top', 'line-bottom'
                color='red',
                fontSize=17,
                fontWeight=600,
                dx=3,  # deslocamento do texto no eixo x
                dy=-10
            ).encode(
                text=alt.Text('mean(Valor):Q', format='.2f'))
            
            st.altair_chart(graf_ticket_medio + linha + rotulo_linha, use_container_width=True)

        with st.expander('Gráfico Mensal'):
            # df_ano_mes = self.df_vendas # esse df_vendas não tem filtro na data pega todos os meses
            df_ano_mes = self.valores_vendas.drop(columns=['total', 'taxa'], axis=1)
            
            # # df_ano_mes['data_venda'] = pd.to_datetime(df_ano_mes['data_venda'], format='%d/%m/%Y')
            df_ano_mes['ano'] = df_ano_mes['data_venda'].dt.year
            df_ano_mes['mes'] = df_ano_mes['data_venda'].dt.month
            df_ano_mes['mes'] = df_ano_mes['data_venda'].dt.month.apply(lambda x: calendar.month_abbr[x])
            
            # Filtro do ano
            df_filtrado = df_ano_mes.loc[(df_ano_mes['data_venda'].dt.year == df_ano_mes['ano'])]
            df_ano_mes = df_filtrado.drop(['data_venda', 'socio', 'ID', 'periodo', 'qtd_rodizio', 'dt_atualizado', 'ano', 'mes'], axis=1)
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
                    y = alt.Y(
                        'sum(Valor):Q',
                        axis=alt.Axis(title='Valor de Venda')),
                    # tooltip = ['Data', 'Valor']
                    ).properties(title= 'Vendas Mensais')
            
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

    def tableau_vendas(self):
        df = self.valores_vendas_30dias.drop(['ID', 'dt_atualizado', 'data_30'], axis=1)
        df['data_venda'] = pd.to_datetime(df['data_venda'], format='%Y-%m-%d')
        colunas = ['qtd_rodizio',
                    'ifood',
                    'dinheiro', 'pix', 
                    'debito_mastercard', 'debito_visa', 'debito_elo', 
                    'credito_mastercard', 'credito_visa', 'credito_elo', 
                    'hiper', 'american_express', 'alelo', 'sodexo', 'ticket_rest', 'vale_refeicao', 'dinersclub',
                    'socio', 'valor_total_30']
        
        for item in colunas:
            df[item] = pd.to_numeric(df[item], errors='coerce')

        df['Total débito'] = df[['debito_mastercard', 'debito_visa', 'debito_elo',]].sum(axis=1)
        df['Total crédito'] = df[['credito_mastercard', 'credito_visa', 'credito_elo']].sum(axis=1)
        df['Outros Cartões'] = df[['hiper', 'american_express', 'alelo', 'sodexo', 'ticket_rest', 'vale_refeicao', 'dinersclub']].sum(axis=1)
        df = df.drop(['debito_mastercard', 'debito_visa', 'debito_elo', 'credito_mastercard', 'credito_visa', 'credito_elo', 
                      'hiper', 'american_express', 'alelo', 'sodexo', 'ticket_rest', 'vale_refeicao', 'dinersclub'], axis=1)

        df = df.rename(columns={
            'data_venda': 'Data',
            'ifood': 'Ifood',
            'dinheiro': 'Dinheiro',
            'pix': 'Pix',
            'qtd_rodizio': 'Rodízio',
            'socio': 'Sócios',
            'periodo': 'Período',
            'total': 'Total',
            'valor_total_30': 'Total -30d'
        })

        grafico_dinamico = StreamlitRenderer(df, spec="./json/vendas.json", spec_io_mode="rw")
        renderer = grafico_dinamico
        renderer.explorer()
