import streamlit as st
from utils.data_processing import load_and_process_data, save_data_to_csv
from utils.visualization import create_choropleth

st.set_page_config(layout="wide", page_title="Homicidios en España")

def main():
    st.title('Homicidios dolosos y asesinatos consumados por municipio')

    # Load and process data
    merged_df = load_and_process_data()
    # save_data_to_csv(merged_df)

    # Display the maps
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Número de homicidios (enero-junio 2024)")
        st.plotly_chart(create_choropleth(merged_df, 'enero-junio 2024', 'Homicidios'), use_container_width=True)
    with col2:
        st.subheader("Variación respecto a enero-junio 2023 (%)")
        st.plotly_chart(create_choropleth(merged_df, 'variacion_2023_2024', 'Variación (%)'), use_container_width=True)

    # Add some statistics
    st.subheader('Estadísticas')
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de homicidios", f"{merged_df['enero-junio 2024'].sum():.0f}")
    col2.metric("Promedio por municipio", f"{merged_df['enero-junio 2024'].mean():.1f}".replace('.', ','))
    col3.metric("Municipio con más casos", merged_df.loc[merged_df['enero-junio 2024'].idxmax(), 'mun_name'])
    col4.metric("Variación promedio", f"{merged_df['variacion_2023_2024'].mean():.1f}%".replace('.', ','))

    # Add a table with top 10 municipalities
    st.subheader('Top 10 municipios con más casos')
    top_10 = merged_df.nlargest(10, 'enero-junio 2024')[['mun_name', 'enero-junio 2024', 'variacion_2023_2024']]
    top_10 = top_10.reset_index(drop=True)
    top_10.index += 1  # Start index at 1 instead of 0
    
    # Rename the columns
    top_10 = top_10.rename(columns={
        'mun_name': 'Municipio',
        'enero-junio 2024': 'Número de homicidios (enero-junio 2024)',
        'variacion_2023_2024': 'Variación (enero-junio) 2023-2024'
    })
    
    st.table(top_10.style.format({
        'Número de homicidios (enero-junio 2024)': '{:.0f}',
        'Variación (enero-junio) 2023-2024': lambda x: f"{x:.1f}%".replace('.', ',')
    }))

    # Add a search functionality
    st.subheader('Buscar municipio')
    search_term = st.text_input('Ingrese el nombre del municipio')
    if search_term:
        result = merged_df[merged_df['mun_name'].str.contains(search_term, case=False)]
        if not result.empty:
            st.dataframe(result[['mun_name', 'enero-junio 2024', 'variacion_2023_2024']].style.format({
                'enero-junio 2024': '{:.0f}',
                'variacion_2023_2024': lambda x: f"{x:.1f}%".replace('.', ',')
            }))
        else:
            st.write('No se encontraron resultados.')

    # Add information from the CSV file in an expandable section
    with st.expander("Información sobre los datos"):
        st.markdown("""
        **Notas:**
        - NIPO 126-20-005-0
        - (*) Se computan datos provenientes de la Policía Nacional, Guardia Civil, Policías Autonómicas y Policías Locales que proporcionan datos al Sistema Estadístico de Criminalidad. En agresiones sexuales con penetración se computan agresiones sexuales con penetración y abusos sexuales con penetración.
        - (**) Indicadores estadísticos de criminalidad utilizados por la Oficina Estadística Europea (EUROSTAT).
        - (***) Datos de 2024 pendientes de consolidar.
        
        **Fuente:** Ministerio del Interior
        """)

if __name__ == "__main__":
    main()
