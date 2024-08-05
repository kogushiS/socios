import streamlit as st

st.set_page_config(
    page_title="Koguchi",
    page_icon="🍣",
    layout='wide',
    initial_sidebar_state='expanded',
    menu_items={
        'Report a Bug': "mailto:edsonbarboza2006@hotmail.com",
        'About': 'Aplicativo desenvolvido por Edson Barboza com objetivo de realizar a Gestão e \
        Controle de Restaurante. Entre em contato (11-9696-51094) e deixe-me saber como esta sendo sua experiência com o aplicativo.'
    })

from conexao import Conexao
from filtro import Filtros
from tela_principal import TelaPrincipal
from vendas import Vendas
from vallet import Vallet
from compras import Compras
from funcionarios import FuncNavegacao, FuncCadastro, FuncAdmissao, FuncPagamento, FuncRescisao, FuncResumo
from exportacao import Exportacao


class Aplication(Conexao, TelaPrincipal, Vendas, Vallet, Compras, FuncNavegacao, FuncCadastro, FuncAdmissao, FuncPagamento, FuncRescisao, FuncResumo, Exportacao):
    def __init__(self):
        self.filtro = Filtros()
        self.home()


if __name__ == "__main__":
    Aplication()