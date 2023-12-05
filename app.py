import pandas as pd
import streamlit as st
import requests

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
                    type = course['type']
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
                        "TIPO":type,
                        "STATUS":status,
                        "VALOR ANTERIOR":old_price,
                        "VALOR ATUAL":current_price,
                        "AJUSTE ANTERIOR":current_price1,
                        "COLOCACAO":courseBestsellerIndex,
                        "PARCELAMENTO":courseNumberOfPayments,
                        "DESCRICAO":courseDescription

                    }
                    metadata.append(data)
            return metadata
def main():
    st.title('Robotic Process Automation')
    st.text('Rapagem de dados site Descomplica')
    st.text('Para extrair dados dos cursos pós clique abaixo')
    #st.set_page_config(page_title="Pitcha Descomplica",page_icon=":bookmark_tabs:,")
    
    
    st.write("Pitcha Descomplica	:bookmark_tabs:")
    st.text('Demonstração de extração de dados do site Descomplica dos cursos de pós e tratamento dos dados com o uso de robô')

    if st.button('Extrair Dataframe'):
            
        dados_df = Extractor()
        if len(dados_df) > 0:
                df = pd.DataFrame(dados_df) # <- gera o Dataframe aqui

                tab1, tab2, tab3 = st.tabs(["Dados em Dataframe", "Dados em gráfico", "Personalizar dados"])

                with tab1:
                    st.header("Dados em Dataframe")
                    df = pd.DataFrame(dados_df)
                    st.dataframe(df)

                with tab2:
                    st.header("Dados em gráfico")
                    df = pd.DataFrame(dados_df)
                    st.dataframe(df)
                    st.line_chart(df, y="VALOR ATUAL", x='TITULO', color='VALOR ANTERIOR')

                with tab3:
                    st.header("Personalizar dados")

                    options = st.multiselect(
                    'Selecione as colunas para visualização',
                    ['ID CATEGORIA', 'CATEGORIA', 'CURSOS NA CATEGORIA', 'ID CURSO','TITULO','TIPO','STATUS',
                    'VALOR ANTERIOR','VALOR ATUAL','AJUSTE ANTERIOR','VALOR ATUAL','COLOCACAO','PARCELAMENTO','DESCRICAO'],

                    ['TITULO','VALOR ATUAL']
                    )

                    df = pd.DataFrame(dados_df, columns=options)
                    st.dataframe(df)
        else:
            st.warning('Erro ao gerar dados')
                 
if __name__ == "__main__":
    main()