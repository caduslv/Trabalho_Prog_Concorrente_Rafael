"""
SIMULADOR PARALELO DE RISCO DE INUNDAÇÕES
Autor: Projeto Acadêmico
Descrição: Comparação entre versão sequencial e paralela
"""

import numpy as np
import time
from multiprocessing import Pool
import matplotlib.pyplot as plt
import os

def calcular_risco(precipitacao, escoamento, umidade_solo):
    """Calcula nível de risco para uma célula"""
    if precipitacao > 400 and escoamento > 200:
        return 3
    elif precipitacao > 300 or escoamento > 150:
        return 2
    elif precipitacao > 200 or umidade_solo > 400:
        return 1
    else:
        return 0

def simular_sequencial(dados):
    """Versão SEQUENCIAL - processa célula por célula (baseline)"""
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

def processar_linha(args):
    """Processa uma linha inteira da matriz (usado no paralelo)"""
    linha_idx, precipitacao_linha, escoamento_linha, umidade_linha = args
    largura = len(precipitacao_linha)
    resultado_linha = np.zeros(largura, dtype=int)
    
    for j in range(largura):
        if precipitacao_linha[j] > 400 and escoamento_linha[j] > 200:
            resultado_linha[j] = 3
        elif precipitacao_linha[j] > 300 or escoamento_linha[j] > 150:
            resultado_linha[j] = 2
        elif precipitacao_linha[j] > 200 or umidade_linha[j] > 400:
            resultado_linha[j] = 1
        else:
            resultado_linha[j] = 0
    
    return linha_idx, resultado_linha

def simular_paralelo(dados, num_processos=4):
    """Versão PARALELA - distribui linhas entre processos"""
    altura, largura = dados['precipitacao'].shape
    
    # Prepara argumentos para cada linha
    args_lista = []
    for i in range(altura):
        args_lista.append((
            i,
            dados['precipitacao'][i, :],
            dados['escoamento'][i, :],
            dados['umidade_solo'][i, :]
        ))
    
    # Executa em paralelo
    with Pool(processes=num_processos) as pool:
        resultados = pool.map(processar_linha, args_lista)
    
    # Monta matriz final
    resultado = np.zeros((altura, largura), dtype=int)
    for idx, linha_resultado in resultados:
        resultado[idx, :] = linha_resultado
    
    return resultado

# ============================================
# PROGRAMA PRINCIPAL
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("SIMULADOR PARALELO DE RISCO DE INUNDAÇÕES")
    print("=" * 60)
    
    # Configurações
    TAMANHO = 1000  # 1000x1000 = 1 milhão de células
    NUM_PROCESSOS = 4  # Número de núcleos para versão paralela
    
    print(f"\n[CONFIGURAÇÃO]")
    print(f"   Grade: {TAMANHO} x {TAMANHO} = {TAMANHO * TAMANHO:,} células")
    print(f"   Processos: {NUM_PROCESSOS} núcleos")
    
    # ========== ETAPA 1: GERAR DADOS ==========
    print(f"\n[ETAPA 1] Gerando dados sintéticos...")
    inicio_geracao = time.time()
    
    dados = {
        'precipitacao': np.random.gamma(2, 50, (TAMANHO, TAMANHO)),
        'escoamento': np.random.uniform(0, 300, (TAMANHO, TAMANHO)),
        'umidade_solo': np.random.uniform(10, 600, (TAMANHO, TAMANHO))
    }
    
    fim_geracao = time.time()
    print(f"   ✓ Dados gerados em {fim_geracao - inicio_geracao:.2f} segundos")
    
    # ========== ETAPA 2: EXECUÇÃO SEQUENCIAL ==========
    print(f"\n[ETAPA 2] Executando versão SEQUENCIAL...")
    print(f"   Processando {TAMANHO * TAMANHO:,} células...")
    
    inicio_seq = time.time()
    resultado_seq = simular_sequencial(dados)
    fim_seq = time.time()
    TEMPO_SEQUENCIAL = fim_seq - inicio_seq
    
    print(f"   ✓ TEMPO SEQUENCIAL: {TEMPO_SEQUENCIAL:.4f} segundos")
    
    # ========== ETAPA 3: EXECUÇÃO PARALELA ==========
    print(f"\n[ETAPA 3] Executando versão PARALELA ({NUM_PROCESSOS} processos)...")
    
    inicio_par = time.time()
    resultado_par = simular_paralelo(dados, num_processos=NUM_PROCESSOS)
    fim_par = time.time()
    TEMPO_PARALELO = fim_par - inicio_par
    
    print(f"   ✓ TEMPO PARALELO: {TEMPO_PARALELO:.4f} segundos")
    
    # ========== ETAPA 4: CÁLCULO DAS MÉTRICAS ==========
    print(f"\n[ETAPA 4] Métricas de Desempenho:")
    print(f"   " + "-" * 40)
    print(f"   Tempo Sequencial:  {TEMPO_SEQUENCIAL:.4f} s")
    print(f"   Tempo Paralelo:    {TEMPO_PARALELO:.4f} s")
    
    SPEEDUP = TEMPO_SEQUENCIAL / TEMPO_PARALELO
    EFICIENCIA = (SPEEDUP / NUM_PROCESSOS) * 100
    
    print(f"   Speedup:           {SPEEDUP:.2f}x")
    print(f"   Eficiência:        {EFICIENCIA:.1f}%")
    print(f"   Economia de tempo: {TEMPO_SEQUENCIAL - TEMPO_PARALELO:.4f} s")
    print(f"   " + "-" * 40)
    
    # ========== ETAPA 5: DISTRIBUIÇÃO DO RISCO ==========
    print(f"\n[ETAPA 5] Distribuição do Risco de Inundação:")
    print(f"   " + "-" * 40)
    
    unique, counts = np.unique(resultado_seq, return_counts=True)
    niveis = {0: "🟢 BAIXO", 1: "🟡 MODERADO", 2: "🟠 ALTO", 3: "🔴 EXTREMO"}
    cores = {0: "Verde", 1: "Amarelo", 2: "Laranja", 3: "Vermelho"}
    
    for nivel, count in zip(unique, counts):
        percentual = count / (TAMANHO * TAMANHO) * 100
        print(f"   {niveis[nivel]}: {count:>10,} células ({percentual:>5.1f}%)")
    print(f"   " + "-" * 40)
    
    # ========== ETAPA 6: GERAR GRÁFICOS ==========
    print(f"\n[ETAPA 6] Gerando visualizações...")
    
    # Gráfico 1: Mapa de Risco
    plt.figure(figsize=(12, 8))
    im = plt.imshow(resultado_seq, cmap='YlOrRd', interpolation='nearest', vmin=0, vmax=3)
    cbar = plt.colorbar(im, ticks=[0, 1, 2, 3])
    cbar.set_label('Nível de Risco', fontsize=12)
    plt.title(f'Mapa de Risco de Inundação\n'
              f'Grade: {TAMANHO}x{TAMANHO} células | Speedup: {SPEEDUP:.2f}x',
              fontsize=14)
    plt.xlabel('Longitude (pixels)', fontsize=12)
    plt.ylabel('Latitude (pixels)', fontsize=12)
    plt.tight_layout()
    plt.savefig('mapa_risco.png', dpi=150)
    print(f"   ✓ Mapa salvo: mapa_risco.png")
    
    # Gráfico 2: Comparação de Desempenho
    plt.figure(figsize=(8, 5))
    bars = plt.bar(['Sequencial', f'Paralelo ({NUM_PROCESSOS} núcleos)'], 
                   [TEMPO_SEQUENCIAL, TEMPO_PARALELO], 
                   color=['#ff6b6b', '#51cf66'], 
                   edgecolor='black', linewidth=1.5)
    plt.ylabel('Tempo de Execução (segundos)', fontsize=12)
    plt.title('Comparação de Desempenho', fontsize=14)
    plt.grid(axis='y', alpha=0.3)
    
    for bar, tempo in zip(bars, [TEMPO_SEQUENCIAL, TEMPO_PARALELO]):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
                 f'{tempo:.2f}s', ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('comparacao_desempenho.png', dpi=150)
    print(f"   ✓ Gráfico salvo: comparacao_desempenho.png")
    
    # Gráfico 3: Gráfico de Speedup
    plt.figure(figsize=(8, 5))
    plt.bar(['Speedup'], [SPEEDUP], color=['#4dabf7'], edgecolor='black', linewidth=1.5)
    plt.axhline(y=NUM_PROCESSOS, color='r', linestyle='--', label=f'Ideal ({NUM_PROCESSOS}x)')
    plt.ylabel('Speedup', fontsize=12)
    plt.title('Ganho de Performance (Speedup)', fontsize=14)
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.text(0, SPEEDUP + 0.1, f'{SPEEDUP:.2f}x', ha='center', fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.savefig('speedup.png', dpi=150)
    print(f"   ✓ Gráfico salvo: speedup.png")
    
    # ========== RESULTADO FINAL ==========
    print(f"\n" + "=" * 60)
    print(f"✅ SIMULAÇÃO CONCLUÍDA COM SUCESSO!")
    print(f"=" * 60)
    print(f"\n📊 RESUMO DOS RESULTADOS:")
    print(f"   • Tempo Sequencial:  {TEMPO_SEQUENCIAL:.4f} segundos")
    print(f"   • Tempo Paralelo:    {TEMPO_PARALELO:.4f} segundos")
    print(f"   • Speedup:           {SPEEDUP:.2f}x")
    print(f"   • Eficiência:        {EFICIENCIA:.1f}%")
    print(f"\n📁 Arquivos gerados na pasta:")
    print(f"   • mapa_risco.png")
    print(f"   • comparacao_desempenho.png")
    print(f"   • speedup.png")
    print(f"\n" + "=" * 60)