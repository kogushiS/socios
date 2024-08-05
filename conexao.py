import streamlit as st
import pyodbc
import mysql.connector
from sqlalchemy import create_engine
import pandas as pd
from sqlalchemy.orm import sessionmaker


class Conexao:
    @classmethod
    @st.cache_data(ttl=18000)
    def conecta_bd(cls): # utilizando sqlalchemy
        # usuario -> : -> senha -> @ -> host -> / -> banco de dados
        # substitua 'mysql_user', 'mysql_pwd', 'mysql_host', 'mysql_db' pelos seus dados
        #engine = create_engine('mysql+mysqlconnector://mysql_user:mysql_pwd@mysql_host/mysql_db')
        engine = create_engine('''mysql+mysqlconnector://
                                fi4byiqhhsahga3n:y52xg4wke9o8rqcy@
                                zf4nk2bcqjvif4in.cbetxkdyhwsb.us-east-1.rds.amazonaws.com/
                                hjaca1510cfzrytk''')
            
        # Realizar consulta na tabela vendas
        query_vendas = """
            SELECT data_venda, dinheiro, pix, debito_mastercard, debito_visa, debito_elo, credito_mastercard,
                credito_visa, credito_elo, hiper, american_express, alelo, sodexo, ticket_rest, vale_refeicao,
                dinersclub, qtd_rodizio, socio, periodo, ifood, dt_atualizado, ID
            FROM vendas
            ORDER BY ID DESC
        """

        query_compras = """SELECT data_compra, data_vencimento, data_pagamento, fornecedor, valor_compra, valor_pago,
                qtd, numero_boleto, grupo_produto, produto, classificacao, forma_pagamento, observacao, dt_atualizado, ID
                FROM compras 
                ORDER BY ID DESC"""

        query_func_cadastro = """ SELECT ID, nome, rg, cpf, carteira_trabalho, endereco, numero, bairro, cidade, telefone,
                banco, agencia, conta, data_contratacao, setor, cargo, salario, documentacao_admissional, data_exame_admissional,
                contabilidade_admissional, observacao_admissional, data_desligamento, devolucao_uniforme, data_exame_demissional,
                data_homologacao, tipo_desligamento, contabilidade_recisao, observacao_demissional, status_admissao, status_recisao,
                dt_atualizado
                FROM cadastro_funcionario
                ORDER BY ID DESC """
        
        query_func_pg_func = """ SELECT ID, nome, data_pagamento, valor_pago, tipo_pagamento, forma_pagamento, dt_atualizado, ID_cadastro
                                FROM pg_funcionario
                                ORDER BY ID DESC """
        query_cadastro_fornecedor = """ SELECT ID, nome_empresa, cnpj, nome_contato, telefone, email, endereco, cep, numero, 
                                                bairro, dt_atualizado
                                        FROM cadastro_fornecedor
                                        ORDER BY ID DESC """
        query_vallet = """
            SELECT data_vallet, dinheiro, pix, debito_mastercard, debito_visa, debito_elo, credito_mastercard,
                credito_visa, credito_elo, hiper, american_express, alelo, sodexo, ticket_rest, vale_refeicao,
                dinersclub, qtd_veiculo, periodo, dt_atualizado, ID
            FROM vallet
            ORDER BY ID DESC
        """

        # Conectar e executar a consulta
        with engine.connect() as connection:
            df_vendas = pd.read_sql(query_vendas, connection)
        with engine.connect() as connection:
            df_compras = pd.read_sql(query_compras, connection)
        with engine.connect() as connection:
            df_cadastro_funcionarios = pd.read_sql(query_func_cadastro, connection)
        with engine.connect() as connection:
            df_pg_funcionario = pd.read_sql(query_func_pg_func, connection)
        with engine.connect() as connection:
            df_cadastro_fornecedor = pd.read_sql(query_cadastro_fornecedor, connection)
        with engine.connect() as connection:
            df_vallet = pd.read_sql(query_vallet, connection)
            
        fornecedor = df_cadastro_fornecedor['nome_empresa'].unique()
        grupo_produto = df_compras['grupo_produto'].unique()
        classificacao = df_compras['classificacao'].unique()
        numero_boleto = df_compras['numero_boleto'].unique()
        produto = df_compras['produto'].unique()
        id_compra = df_compras['ID'].unique()
        nome_funcionario = df_cadastro_funcionarios['nome'].unique()

        # Mostrar o DataFrame resultante
        return (df_vendas, # df_vendas
                df_compras, fornecedor, grupo_produto, classificacao, numero_boleto, produto, id_compra, # df_compras
                df_cadastro_funcionarios, nome_funcionario, # df_cadastro_funcionarios
                df_pg_funcionario, #df_pagamento dos funcionarios
                df_cadastro_fornecedor,
                df_vallet
                )
    
    def conecta_mysql(self):
        engine = create_engine('''mysql+mysqlconnector://
                                fi4byiqhhsahga3n:y52xg4wke9o8rqcy@
                                zf4nk2bcqjvif4in.cbetxkdyhwsb.us-east-1.rds.amazonaws.com/
                                hjaca1510cfzrytk''')
        Session = sessionmaker(bind=engine)
        self.session = Session()
        print('Conectado ao banco - conecta_mysql')       

    def conecta_mysql2(self): 
        self.conn = mysql.connector.connect(
        host= 'zf4nk2bcqjvif4in.cbetxkdyhwsb.us-east-1.rds.amazonaws.com',
        user='fi4byiqhhsahga3n',
        password='y52xg4wke9o8rqcy',
        database='hjaca1510cfzrytk')

    def desconecta_bd(self):
        self.cursor.close()
        self.conexao.close()