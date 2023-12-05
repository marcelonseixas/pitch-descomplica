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
                        "ID CATEGORIA":str(id_cat),
                        "CATEGORIA":name_cat,
                        "VOLUME CAT":course_count,
                        "ID CURSO":str(id_course),
                        "CURSO":title,
                        "TIPO":str(type).replace('_',' '),
                        "STATUS":status,
                        "VALOR ANTERIOR":old_price,
                        "VALOR ATUAL":current_price,
                        #"AJUSTE ANTERIOR":current_price1,
                        "RANKING":courseBestsellerIndex,
                        "PARCELAMENTO":courseNumberOfPayments,
                        "DESCRICAO":courseDescription
                    }
                    metadata.append(data)
            return metadata
def main():
    st.title('Robotic Process Automation')
    st.markdown('''
            Extação de dados usando RPA demostrativo.
            A Extração de dados se torna muito mais rápida e assertiva com a utilização de RPA.
            Além da extração é possível visualizar e personalizar os dados.
            
            Extração do link https://descomplica.com.br/pos-graduacao/ 

            Os dados são extraídos do próprio site usando um RPA que trata os dados e aprensenta nesse site.
            by: Marcelo Seixas     
            ''')
    #st.set_page_config(page_title="Pitcha Descomplica",page_icon=":bookmark_tabs:,")
    st.info('Clique abaixo nas opções de extação ')
    
    st.write("Pitcha Descomplica	:bookmark_tabs: :black_left_pointing_double_triangle_with_vertical_bar: :rewind: \
            :black_right_pointing_triangle_with_double_vertical_bar: 	:double_vertical_bar: :fast_forward: :black_right_pointing_double_triangle_with_vertical_bar:   ")

    tab1, tab2 = st.tabs(["Dados em Dataframe", "Personalizar dados"])

    with tab1:
        st.header("Dados em planilha")
        if st.button('Extrair dados em planilha'):
            with st.spinner('Extraindo dados aguarde...'):
                dados_df = Extractor()
            st.success('Extração concluída!')
            df = pd.DataFrame(dados_df)
            st.dataframe(df)

 
    with tab2:
        st.header("Planilha personalizada")

        options = st.multiselect(
                    'Selecione as colunas para visualização',
                    ['ID CATEGORIA', 'CATEGORIA', 'VOLUME CAT', 'ID CURSO','CURSO','TIPO','STATUS',
                    'VALOR ANTERIOR','VALOR ATUAL','RANKING','PARCELAMENTO','DESCRICAO'],

                    ['CURSO','VALOR ATUAL']
                    )
        if st.button('Extrair em planilha personalizado'):
            with st.spinner('Extraindo dados aguarde...'):
                dados_df = Extractor()
            st.success('Extração concluída!')
            df = pd.DataFrame(dados_df, columns=options)
            st.dataframe(df)
    
            
                 
if __name__ == "__main__":
    main()