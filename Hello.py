# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger
import requests
LOGGER = get_logger(__name__)

def Extractor():
    endpoint_descomplica = 'https://flowpress.prd.descomplica.com.br/graduacao/wp-json/wp/v2/'
    metadata = []
    cat_pos = f'{endpoint_descomplica}cat_pos_graduacao?per_page=99&orderby=name&order=asc'

    response_cat_pos = requests.get(cat_pos)
    if response_cat_pos.status_code == 200:
        content_cat_pos = response_cat_pos.json()
        for cat in content_cat_pos:
            id_cat = cat['id']
            name_cat = cat['name']
            course_count = cat['course_count']

            url_course = f'{endpoint_descomplica}pos_graduacao_search/?cat_pos_graduacao={id_cat}'
            respose_menu = requests.get(url_course)
            list_courses = respose_menu.json()
            for course in list_courses:
                id_course = course['id']
                title = course['title']
                type_ = course['type']
                status = course['status']
                old_price = course['acf']['courseOldPrice']
                current_price = course['acf']['courseCurrentPrice']
                current_price1 = course['acf']['courseCurrentPrice1']
                courseDescription = course['acf']['courseDescription']
                courseBestsellerIndex = course['acf']['courseBestsellerIndex']
                courseNumberOfPayments = course['acf']['courseNumberOfPayments']
                data = {
                        "ID CATEGORIA":id_cat,
                        "CATEGORIA":name_cat,
                        "CURSOS NA CATEGORIA":course_count,
                        "ID CURSO":id_course,
                        "TITULO":title,
                        "TIPO":type_,
                        "STATUS":status,
                        "VALOR ANTERIOR":old_price,
                        "VALOR ATUAL":current_price,
                        "AJUSTE ANTERIOR":current_price1,
                        "COLOCACAO":courseBestsellerIndex,
                        "PARCELAMENTO":courseNumberOfPayments,
                        "DESCRICAO":courseDescription

                }
        return metadata

def run():
    st.set_page_config(
        page_title="Pitcha Descomplica",
        page_icon=":bookmark_tabs:")
    if st.button('Extraçao'):
        try:
            dados_df = Extractor()
            df = pd.DataFrame(dados_df)
            st.dataframe(df)
        except:
            pass
    st.sidebar.success("Sobre")
    st.markdown(
    """
    Esse é meu Pitcha da descomplica.
    Nesse projeto mostro técnicas de RPA.
    Automações que podem ajudar no dia a dia de uma corporação,
    com o uso de robôs para fazer tarefas que demandam tempo.
    Além de demandar tempo o uso de humanos em algumas tarefas
    podem não ser tão assetivos quando de um robô,
    Dentre vários benefícios a redução de custo é a principal,
    pois um robô trabalha a qualquer horário sem sálario!  
    """
    )

run()
