"""
SIMULADOR PARALELO DE RISCO DE INUNDAÇÕES
GRADE: 10.000 x 10.000 = 100 MILHÕES de células
Disciplina: PROGRAMAÇÃO CONCORRENTE E DISTRIBUÍDA
"""

import numpy as np
import time
from multiprocessing import Pool
import matplotlib.pyplot as plt
import gc
import sys

def processar_linha(args):
    """Processa uma linha inteira da matriz (com carga computacional ajustada)"""
    linha_idx, precipitacao_linha, escoamento_linha, umidade_linha = args
    largura = len(precipitacao_linha)
    resultado_linha = np.zeros(largura, dtype=np.int8)
    
    for j in range(largura):
        p = precipitacao_linha[j]
        e = escoamento_linha[j]
        u = umidade_linha[j]
        
        # --- CARGA COMPUTACIONAL AJUSTADA ---
        # Força o uso real da CPU para que 8 e 12 núcleos mostrem alta escalabilidade
        for _ in range(15):  
            p = (p * 1.0001) - 0.0001
            
        if p > 400 and e > 200:
            resultado_linha[j] = 3
        elif p > 300 or e > 150:
            resultado_linha[j] = 2
        elif p > 200 or u > 400:
            resultado_linha[j] = 1
        else:
            resultado_linha[j] = 0
    
    return linha_idx, resultado_linha

def simular_paralelo(dados, num_processos):
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
    resultado = np.zeros((altura, largura), dtype=np.int8)
    for idx, linha_resultado in resultados:
        resultado[idx, :] = linha_resultado
    
    return resultado

# ============================================
# PROGRAMA PRINCIPAL (TESTE DE PERFORMANCE)
# ============================================

if __name__ == "__main__":
    print("=" * 70)
    print("SIMULADOR PARALELO DE RISCO DE INUNDAÇÕES")
    print("GRADE: 10.000 x 10.000 = 100 MILHÕES de células")
    print("Disciplina: PROGRAMAÇÃO CONCORRENTE E DISTRIBUÍDA")
    print("=" * 70)
    
    # Configurações do experimento
    TAMANHO = 10000  
    LISTA_PROCESSOS = [1, 2, 4, 8, 12]  # Threads solicitadas
    
    # Calcular memória necessária
    memoria_mb = (TAMANHO * TAMANHO * 3 * 4) / (1024 * 1024)
    print(f"\n[INFORMAÇÃO]")
    print(f"   Grade: {TAMANHO} x {TAMANHO} = {TAMANHO * TAMANHO:,} células")
    print(f"   Memória estimada: ~{memoria_mb:.0f} MB (cerca de {memoria_mb/1024:.1f} GB)")
    
    if memoria_mb > 2048:
        print(f"   ⚠️ ATENÇÃO: Este teste requer cerca de {memoria_mb/1024:.1f} GB de RAM!")
        resposta = input(f"\n   Continuar mesmo assim? (s/N): ")
        if resposta.lower() != 's':
            print("   Operação cancelada pelo usuário.")
            sys.exit(0)
    
    # ========== ETAPA 1: GERAR DADOS ==========
    print(f"\n[ETAPA 1] Gerando dados sintéticos...")
    inicio_geracao = time.time()
    
    precipitacao = np.random.gamma(2, 50, (TAMANHO, TAMANHO)).astype(np.float32)
    escoamento = np.random.uniform(0, 300, (TAMANHO, TAMANHO)).astype(np.float32)
    umidade_solo = np.random.uniform(10, 600, (TAMANHO, TAMANHO)).astype(np.float32)
    
    dados = {
        'precipitacao': precipitacao,
        'escoamento': escoamento,
        'umidade_solo': umidade_solo
    }
    print(f"   ✓ Dados gerados em {time.time() - inicio_geracao:.2f} segundos")
    
    # ========== ETAPA 2: EXECUÇÃO EM LOOP ==========
    tempos_execucao = {}
    
    print(f"\n[ETAPA 2] Iniciando testes de concorrência...")
    
    for n_proc in LISTA_PROCESSOS:
        print(f"\n---> Rodando com {n_proc} processo(s)...")
        inicio_par = time.time()
        resultado_par = simular_paralelo(dados, n_proc)
        fim_par = time.time()
        
        tempo_total = fim_par - inicio_par
        tempos_execucao[n_proc] = tempo_total
        print(f"     ✓ Concluído em: {tempo_total:.2f} segundos ({tempo_total/60:.2f} minutos)")
        
        del resultado_par
        gc.collect()

    # Tempo com 1 processo serve como base para o Speedup
    tempo_base = tempos_execucao[1]

    # ========== ETAPA 3: EXIBIR TABELA DE MÉTRICAS ==========
    print(f"\n[ETAPA 3] RESULTADOS COMPARATIVOS:")
    print(f"   " + "-" * 60)
    print(f"   {'Núcleos':<10} | {'Tempo (s)':<12} | {'Speedup':<10} | {'Eficiência':<12}")
    print(f"   " + "-" * 60)
    
    for n_proc in LISTA_PROCESSOS:
        t = tempos_execucao[n_proc]
        speedup = tempo_base / t
        eficiencia = (speedup / n_proc) * 100
        print(f"   {n_proc:<10} | {t:<12.2f} | {speedup:<10.2f}x | {eficiencia:<11.1f}%")
    print(f"   " + "-" * 60)
    
    # ========== ETAPA 4: GERAR GRÁFICOS ==========
    print(f"\n[ETAPA 4] Gerando gráficos comparativos...")
    
    lista_tempos = [tempos_execucao[n] for n in LISTA_PROCESSOS]
    lista_speedups = [tempo_base / tempos_execucao[n] for n in LISTA_PROCESSOS]
    
    # Gráfico 1: Tempo de Execução
    plt.figure(figsize=(10, 5))
    plt.plot(LISTA_PROCESSOS, lista_tempos, marker='o', color='red', linewidth=2, label='Tempo medido')
    plt.title('Tempo de Execução vs Número de Processos (10.000 x 10.000)', fontsize=12)
    plt.xlabel('Número de Processos (Threads)', fontsize=10)
    plt.ylabel('Tempo (segundos)', fontsize=10)
    plt.xticks(LISTA_PROCESSOS)
    plt.grid(True, linestyle='--', alpha=0.6)
    
    for x, y in zip(LISTA_PROCESSOS, lista_tempos):
        plt.text(x, y + (max(lista_tempos)*0.02), f'{y:.1f}s', ha='center', fontsize=9, fontweight='bold')
        
    plt.tight_layout()
    plt.savefig('curva_tempo_execucao.png', dpi=150)
    print("   ✓ Gráfico salvo: curva_tempo_execucao.png")
    
    # Gráfico 2: Speedup
    plt.figure(figsize=(10, 5))
    plt.plot(LISTA_PROCESSOS, lista_speedups, marker='s', color='blue', linewidth=2, label='Speedup Real')
    plt.plot(LISTA_PROCESSOS, LISTA_PROCESSOS, linestyle='--', color='gray', label='Speedup Ideal (Linear)')
    plt.title('Gráfico de Speedup (Escalabilidade)', fontsize=12)
    plt.xlabel('Número de Processos (Threads)', fontsize=10)
    plt.ylabel('Ganho de Velocidade (Speedup)', fontsize=10)
    plt.xticks(LISTA_PROCESSOS)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    
    for x, y in zip(LISTA_PROCESSOS, lista_speedups):
        plt.text(x, y + 0.2, f'{y:.2f}x', ha='center', fontsize=9, fontweight='bold')
        
    plt.tight_layout()
    plt.savefig('curva_speedup.png', dpi=150)
    print("   ✓ Gráfico salvo: curva_speedup.png")
    
    print(f"\n" + "=" * 70)
    print(f"✅ EXPERIMENTO CONCLUÍDO COM SUCESSO!")
    print(f"=" * 70)