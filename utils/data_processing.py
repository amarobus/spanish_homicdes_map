import pandas as pd
import geopandas as gpd

def load_and_process_data():
    # Load the GeoJSON file
    municipalities = gpd.read_file('data/georef-spain-municipio@public.geojson')

    # Load homicides data
    crime_municipalities = load_csv_data('data/homicidios_2024.csv', 'enero-junio 2024')
    
    # Load variation data
    var_municipalities = load_csv_data('data/var_2023_2024.csv', 'variacion_2023_2024')

    # Merge data
    merged_df = municipalities.merge(crime_municipalities, on='mun_code', how='inner')
    merged_df = merged_df.merge(var_municipalities, on='mun_code', how='left')
    
    merged_df.reset_index(inplace=True)
    merged_df = merged_df.sort_values(by='enero-junio 2024', ascending=False)
    merged_df['mun_code'] = merged_df['mun_code'].astype(str)
    merged_df['enero-junio 2024'] = merged_df['enero-junio 2024'].astype(float)
    merged_df['variacion_2023_2024'] = merged_df['variacion_2023_2024'].astype(float)

    return merged_df

def load_csv_data(file_path, column_name):
    data = pd.read_csv(
        file_path, 
        delimiter=',', 
        skiprows=5,
        skipfooter=9, 
        engine='python',
        encoding='latin1',
        header=None
    )

    data = data.drop(data.columns[-1], axis=1)
    data.columns = ['mun_name', column_name]
    data = data.iloc[1:]
    names = data['mun_name'].values[::2]
    data = data.iloc[1::2]
    data.loc[:,'mun_name'] = names
    data.set_index('mun_name', inplace=True)
    data['mun_code'] = data.index.str.split(' ').str[0]
    data['mun_code'] = data['mun_code'].apply(lambda x: x if x.isdigit() else 'unknown')
    
    return data

def save_data_to_csv(merged_df):
    merged_df[['mun_code', 'enero-junio 2024', 'variacion_2023_2024']].to_csv('municipalities_crime.csv', index=False)
