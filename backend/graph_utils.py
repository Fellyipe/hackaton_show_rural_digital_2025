import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon

def parse_src_file(data):
    """
    Aceita um caminho para arquivo ou um DataFrame e retorna uma lista de coordenadas (x, y).
    """
    coordinates = []
    
    if isinstance(data, str):  # Se for um caminho, abre o arquivo
        with open(data, 'r') as f:
            header = f.readline()  # Ignora cabeçalho
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.replace(',', ' ').replace(';', ' ').split()
                if len(parts) >= 2:
                    try:
                        x = float(parts[0])
                        y = float(parts[1])
                        coordinates.append((x, y))
                    except ValueError:
                        continue

    elif isinstance(data, pd.DataFrame):  # Se for um DataFrame, processa diretamente
        coordinates = list(zip(data.iloc[:, 0], data.iloc[:, 1]))

    return coordinates

def compute_centroid(coordinates):
    """
    Calcula o centróide (média dos x e dos y) a partir de uma lista de coordenadas.
    """
    xs = [pt[0] for pt in coordinates]
    ys = [pt[1] for pt in coordinates]
    return (np.mean(xs), np.mean(ys))

def idw_interpolation(coordinates, values, grid_x, grid_y, power=2):
    """
    Realiza a interpolação IDW para cada ponto (grid_x, grid_y) dado um conjunto de pontos (coordinates)
    e seus respectivos valores (values). O parâmetro 'power' define a potência do peso.
    """
    grid_z = np.empty(grid_x.shape)
    grid_z.fill(np.nan)
    xs = np.array([pt[0] for pt in coordinates])
    ys = np.array([pt[1] for pt in coordinates])
    values = np.array(values)
    
    # Loop sobre cada ponto do grid
    for i in range(grid_x.shape[0]):
        for j in range(grid_x.shape[1]):
            x0 = grid_x[i, j]
            y0 = grid_y[i, j]
            # Calcula a distância de (x0,y0) a cada ponto amostrado
            distances = np.sqrt((xs - x0)**2 + (ys - y0)**2)
            # Se o ponto do grid coincidir com um ponto de dados, usa o valor exato
            if np.any(distances == 0):
                grid_z[i, j] = values[np.argmin(distances)]
            else:
                weights = 1 / distances**power
                grid_z[i, j] = np.sum(weights * values) / np.sum(weights)
    return grid_z

def perform_idw_analysis(coordinates, values, boundary_polygon, grid_resolution=100, power=2):
    """
    Realiza a interpolação IDW dentro de um limite definido.
    
    Parâmetros:
      - coordinates: lista de tuplas (x, y) dos pontos amostrados.
      - values: lista de valores associados a cada coordenada.
      - boundary_polygon: lista de tuplas (x, y) que definem o polígono de limite (deve ser fechado ou
        será fechado automaticamente para plotagem).
      - grid_resolution: número de pontos em cada dimensão do grid de interpolação.
      - power: parâmetro de potência do IDW.
      
    A função:
      1. Calcula o centróide dos pontos.
      2. Cria um grid baseado na caixa delimitadora do polígono.
      3. Para cada ponto do grid que estiver dentro do polígono, realiza a interpolação IDW.
      4. Plota o mapa interpolado com cores (aqui usamos o cmap 'RdYlGn' como exemplo).
    """
    # Calcula o centróide
    centroid = compute_centroid(coordinates)
    
    # Define os limites do grid com base no polígono
    xs_boundary = [pt[0] for pt in boundary_polygon]
    ys_boundary = [pt[1] for pt in boundary_polygon]
    min_x, max_x = min(xs_boundary), max(xs_boundary)
    min_y, max_y = min(ys_boundary), max(ys_boundary)
    
    # Cria o grid
    grid_x, grid_y = np.meshgrid(
        np.linspace(min_x, max_x, grid_resolution),
        np.linspace(min_y, max_y, grid_resolution)
    )
    
    # Define o polígono para testes (se não estiver fechado, fechamos)
    if boundary_polygon[0] != boundary_polygon[-1]:
        boundary_polygon.append(boundary_polygon[0])
    polygon = Polygon(boundary_polygon)
    
    # Realiza a interpolação IDW somente nos pontos do grid que estiverem dentro do polígono
    grid_z = np.empty(grid_x.shape)
    grid_z.fill(np.nan)
    xs_data = np.array([pt[0] for pt in coordinates])
    ys_data = np.array([pt[1] for pt in coordinates])
    values = np.array(values)
    
    for i in range(grid_x.shape[0]):
        for j in range(grid_x.shape[1]):
            pt = Point(grid_x[i, j], grid_y[i, j])
            if polygon.contains(pt):
                distances = np.sqrt((xs_data - grid_x[i, j])**2 + (ys_data - grid_y[i, j])**2)
                if np.any(distances == 0):
                    grid_z[i, j] = values[np.argmin(distances)]
                else:
                    weights = 1 / distances**power
                    grid_z[i, j] = np.sum(weights * values) / np.sum(weights)
    
    # Cálculo da média dos valores interpolados (ignorando os NaNs)
    avg_value = np.nanmean(grid_z)
    
    # Plotagem do resultado
    plt.figure(figsize=(10, 8))
    plt.imshow(
        grid_z,
        origin='lower',
        extent=(min_x, max_x, min_y, max_y),
        cmap='RdYlGn',
        interpolation='nearest'
    )
    plt.colorbar(label='Valor interpolado')
    
    # Plota os pontos de dados e o centróide
    plt.scatter(xs_data, ys_data, c='black', marker='o', label='Pontos de dados')
    plt.scatter(*centroid, c='blue', marker='x', s=100, label='Centróide')
    
    # Plota o limite definido
    bx, by = zip(*boundary_polygon)
    plt.plot(bx, by, c='red', linewidth=2, label='Limite definido')
    
    plt.title('Análise IDW dentro do limite definido')
    plt.legend()
    plt.xlabel('Coordenada X')
    plt.ylabel('Coordenada Y')
    plt.show()
    
    return grid_z, centroid, avg_value

# Exemplo de uso:
if __name__ == '__main__':
    # Suponha que você tenha um arquivo "coordenadas.src" com conteúdo como:
    # 10,20
    # 15,25
    # 20,22
    src_file = 'coordenadas.src'
    coords = parse_src_file(src_file)
    
    # Suponha também que cada coordenada possua um valor associado (por exemplo, uma medida de um parâmetro)
    # Aqui usamos valores fictícios:
    values = [30, 45, 50]  # deve ter o mesmo tamanho de 'coords'
    
    # Se o sistema deve posicionar o cliente no centróide, você pode obter:
    client_position = compute_centroid(coords)
    print("Posição do cliente (centróide):", client_position)
    
    # O usuário define os limites do modelo (por exemplo, via interface gráfica) e envia as coordenadas do polígono:
    # Exemplo: polígono retangular (lista de tuplas)
    limite = [(8, 18), (22, 18), (22, 28), (8, 28)]
    
    # Realiza a análise IDW dentro do limite definido
    grid, centroid, avg = perform_idw_analysis(coords, values, limite, grid_resolution=100, power=2)
    print("Valor médio interpolado:", avg)
