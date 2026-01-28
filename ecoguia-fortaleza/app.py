import json
import math
import os


def carregar_dados():
    try:
        # Pega o diretório onde o arquivo app.py está
        diretorio_base = os.path.dirname(os.path.abspath(__file__))
        caminho_arquivo = os.path.join(diretorio_base, "ecopontos.json")

        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Erro: Arquivo não encontrado.")
        return None


# --- 2. CÁLCULO DE DISTÂNCIA ---
def calcular_distancia_km(lat1, lon1, lat2, lon2):
    # Raio da Terra em km
    R = 6371.0

    # Converter graus para radianos
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Diferença das coordenadas
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Fórmula
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance


# --- 3. FUNÇÃO PARA ACHAR O MAIS PRÓXIMO ---
def encontrar_mais_proximo(dados, lat_user, lon_user):
    pontos = dados.get("pontos_coleta", [])
    ponto_mais_proximo = None
    menor_distancia = float("inf")

    for ponto in pontos:
        # Pula se não tiver coordenada
        if ponto["latitude"] is None or ponto["longitude"] is None:
            continue

        dist = calcular_distancia_km(
            lat_user, lon_user, ponto["latitude"], ponto["longitude"]
        )

        if dist < menor_distancia:
            menor_distancia = dist
            ponto_mais_proximo = ponto

    return ponto_mais_proximo, menor_distancia


# --- 4. EXECUÇÃO PRINCIPAL ---
def main():
    dados = carregar_dados()
    if not dados:
        return

    print("\n  SISTEMA ECOGUIA FORTALEZA - TERMINAL ")

    while True:
        print("\nMENU:")
        print("1. Listar todos")
        print("2. Buscar por nome")
        print("3.  Encontrar Ecoponto mais próximo (Teste de GPS)")
        print("0. Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            for p in dados["pontos_coleta"]:
                print(f"- {p['nome_local']}")

        elif opcao == "2":
            termo = input("Digite o nome: ").lower()
            for p in dados["pontos_coleta"]:
                if termo in p["nome_local"].lower():
                    print(f" {p['nome_local']} - {p['endereco']}")

        elif opcao == "3":
            print("\n--- TESTE DE COORDENADAS ---")
            try:
                # coordenadas de teste
                print(
                    "Digite sua localização (Exemplo Unifor: Lat -3.7698, Long -38.4772)"
                )
                meu_lat = float(input("Sua Latitude: "))
                meu_lon = float(input("Sua Longitude: "))

                ponto, dist = encontrar_mais_proximo(dados, meu_lat, meu_lon)

                print(f"\n O Ecoponto mais próximo é:")
                print(f"Nome: {ponto['nome_local']}")
                print(f"Endereço: {ponto['endereco']}")
                print(f"Distância: {dist:.2f} km daqui")

            except ValueError:
                print("Erro: Digite apenas números com ponto (ex: -3.75)")

        elif opcao == "0":
            break


if __name__ == "__main__":
    main()
