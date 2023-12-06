import pandas as pd
import streamlit as st
import requests
import time
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
                        "RANKING":courseBestsellerIndex,
                        "PARCELAMENTO":courseNumberOfPayments,
                        "DESCRICAO":courseDescription
                    }
                    metadata.append(data)
            return metadata
def main():
    st.set_page_config(page_title="Pitcha Descomplica",page_icon=":bookmark_tabs:,")
    st.title('Robotic Process Automation (RPA)')
    st.markdown("Marcelo Seixas - Pitch Descomplica :bookmark_tabs:")
    st.markdown('''RPA raspagem de dados feito 100% em Python, demonstração de extração do link https://descomplica.com.br/pos-graduacao/ 
            Os dados são extraídos do próprio site usando uma técnica chamada "Scrap" e transforma os dados em planilha.  
            ''')
    
    st.markdown('Clique abaixo nas opções de extação 	:point_down: ')
    tab1, tab2 = st.tabs(["Dados em Dataframe", "Personalizar dados"])

    with tab1:
        st.text("Dados em planilha")
        if st.button('Extrair dados em planilha'):
            with st.status("Iniciando RPA...", expanded=True) as status:
                st.write("Acessando https://descomplica.com.br/pos-graduacao/...")
                st.write('Coletando informações do HTML...')
                dados_df = Extractor()
                status.update(label="Dados coletados com sucesso!", state="complete", expanded=False)
            df = pd.DataFrame(dados_df)
            st.dataframe(df)
    with tab2:
        st.text("Planilha personalizada")

        options = st.multiselect(
                    'Selecione as colunas para visualização',
                    ['ID CATEGORIA', 'CATEGORIA', 'VOLUME CAT', 'ID CURSO','CURSO','TIPO','STATUS',
                    'VALOR ANTERIOR','VALOR ATUAL','RANKING','PARCELAMENTO','DESCRICAO'],

                    ['CURSO','DESCRICAO']
                    )
        if st.button('Extrair em planilha personalizado'):
            
            with st.status("Iniciando RPA...", expanded=True) as status:
                st.write("Acessando https://descomplica.com.br/pos-graduacao/...")
                st.write('Coletando informações do HTML...')
                dados_df = Extractor()
                status.update(label="Dados coletados com sucesso!", state="complete", expanded=False)
            df = pd.DataFrame(dados_df, columns=options)
            st.dataframe(df)
                 
if __name__ == "__main__":
    main()