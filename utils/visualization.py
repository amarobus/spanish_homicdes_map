import json
import plotly.graph_objects as go
import streamlit as st

@st.cache_data
def create_choropleth(_merged_df, column, title):
    geojson = json.loads(_merged_df.to_json())
    
    fig = go.Figure(go.Choroplethmapbox(
        geojson=geojson,
        locations=_merged_df['mun_code'],
        z=_merged_df[column],
        colorscale='RdBu_r' if column == 'variacion_2023_2024' else 'Reds',
        zmin=-max(abs(_merged_df[column].min()), abs(_merged_df[column].max())) if column == 'variacion_2023_2024' else _merged_df[column].min(),
        zmax=max(abs(_merged_df[column].min()), abs(_merged_df[column].max())) if column == 'variacion_2023_2024' else _merged_df[column].max(),
        zmid=0 if column == 'variacion_2023_2024' else None,
        marker_opacity=0.7,
        marker_line_width=0.5,
        colorbar_title=title,
        hovertemplate='<b>%{text}</b><br>' +
                      f'{title}: %{{z}}<extra></extra>',
        text=_merged_df['mun_name'],
        featureidkey="properties.mun_code"
    ))

    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=5,
        mapbox_center={"lat": 40.4168, "lon": -3.7038},
        height=600,
        annotations=[
            dict(
                text='Gráfico creado por <b>@datanalysislab</b>. Origen datos: Portal Estadístico de Criminalidad. Se permite difusión con cita (<b>@datanalysislab</b>).',
                align='left',
                showarrow=False,
                xref='paper',
                yref='paper',
                x=0.01,
                y=-0.05,
                font=dict(size=14),
                opacity=0.8,
            )
        ]
    )
    
    return fig
