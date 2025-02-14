import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point

# 🔹 1. Carregar o CSV
csv_path = "dados-teste.csv"  # Substitua pelo caminho correto
df = pd.read_csv(csv_path)

# 🔹 2. Criar Geometria a partir de Latitude e Longitude
df["geometry"] = df.apply(lambda row: Point(row["longitude"], row["latitude"]), axis=1)
gdf = gpd.GeoDataFrame(df, geometry="geometry")

# 🔹 3. Criar o Mapa
fig, ax = plt.subplots(figsize=(10, 6))

# 🔹 4. Plotar os pontos e colorir conforme o nível de potássio
gdf.plot(column="potassio", cmap="YlOrRd", legend=True, ax=ax, markersize=100)

# 🔹 5. Configurar o Mapa
plt.title("Mapa de Potássio no Solo")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.grid(True)

# 🔹 6. Salvar a Imagem
plt.savefig("mapa_solo.png", dpi=300)
plt.show()
