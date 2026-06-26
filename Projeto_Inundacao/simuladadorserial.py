import numpy as np
import time
import matplotlib.pyplot as plt


# =========================
# FUNÇÃO DE RISCO
# =========================
def calcular_risco(precipitacao, escoamento, umidade_solo):
    if precipitacao > 400 and escoamento > 200:
        return 3
    elif precipitacao > 300 or escoamento > 150:
        return 2
    elif precipitacao > 200 or umidade_solo > 400:
        return 1
    else:
        return 0


# =========================
# VERSÃO SEQUENCIAL
# =========================
def simular_sequencial(dados):
    altura, largura = dados['precipitacao'].shape
    resultado = np.zeros((altura, largura), dtype=int)

    for i in range(altura):
        for j in range(largura):
            resultado[i, j] = calcular_risco(
                dados['precipitacao'][i, j],
                dados['escoamento'][i, j],
                dados['umidade_solo'][i, j]
            )

    return resultado


# =========================
# MAIN (SOMENTE SERIAL)
# =========================
if __name__ == "__main__":

    print("=" * 60)
    print("SIMULADOR SERIAL DE RISCO DE INUNDAÇÕES")
    print("=" * 60)

    TAMANHO = 300  # pode aumentar se quiser
    print(f"\nGrade: {TAMANHO} x {TAMANHO}")

    print("\nGerando dados...")
    dados = {
        'precipitacao': np.random.gamma(2, 50, (TAMANHO, TAMANHO)),
        'escoamento': np.random.uniform(0, 300, (TAMANHO, TAMANHO)),
        'umidade_solo': np.random.uniform(10, 600, (TAMANHO, TAMANHO))
    }

    print("\nExecutando simulação sequencial...")

    inicio = time.time()
    resultado = simular_sequencial(dados)
    tempo = time.time() - inicio

    print("\nRESULTADO FINAL:")
    print(f"Tempo sequencial: {tempo:.4f} segundos")

    # =========================
    # VISUALIZAÇÃO
    # =========================
    plt.figure(figsize=(8, 6))
    plt.imshow(resultado, cmap='YlOrRd', vmin=0, vmax=3)
    plt.colorbar(label="Nível de risco")
    plt.title("Mapa de Risco de Inundação (Sequencial)")
    plt.tight_layout()
    plt.show()
    