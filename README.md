# 🌊 Simulador Paralelo de Risco de Inundações

**Disciplina:** PROGRAMAÇÃO CONCORRENTE E DISTRIBUÍDA

**Aluno(s):** Carlos Eduardo Pinheiro Da Silva - Luís Henrique Vieira Holanda

**Turma:** 5° Semestre / Análise e Desenvolvimento de Sistemas

**Professor:** Rafael Marconi Ramos

**Data:** 15/05/2026

---

## 📝 Descrição do Projeto

Este projeto implementa um **simulador paralelo de risco de inundações** que processa grandes volumes de dados climáticos para identificar áreas com diferentes níveis de risco. Utilizando conceitos de computação paralela, o sistema compara o desempenho entre uma versão sequencial e uma versão paralela (com multiprocessing), demonstrando os ganhos de performance obtidos ao distribuir a carga de processamento entre múltiplos núcleos da CPU.

O simulador é capaz de processar grades de até **16 milhões de células (4000×4000)** em poucos segundos, gerando mapas de risco coloridos e métricas de desempenho.

---

## 🎯 Objetivo Geral

Desenvolver e analisar um sistema paralelo para simulação de risco de inundações, utilizando dados climáticos sintéticos (precipitação, escoamento superficial e umidade do solo), comparando o desempenho da versão sequencial com a versão paralela e medindo o **speedup** obtido.

---

## 📋 Objetivos Específicos

1. **Implementar um modelo de risco de inundação** baseado em regras matemáticas que consideram três variáveis ambientais: precipitação, escoamento e umidade do solo.

2. **Desenvolver uma versão sequencial** do simulador para servir como baseline de desempenho.

3. **Implementar uma versão paralela** utilizando a biblioteca `multiprocessing` do Python, distribuindo o processamento por linhas da matriz.

4. **Medir e comparar o desempenho** entre as duas versões, calculando métricas como:
   - Tempo de execução sequencial
   - Tempo de execução paralela
   - Speedup (ganho de performance)
   - Eficiência do paralelismo

5. **Gerar visualizações gráficas** do mapa de risco e da comparação de desempenho para facilitar a análise dos resultados.

6. **Analisar a escalabilidade** do sistema em diferentes tamanhos de grade e números de processos.

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Finalidade |
|------------|--------|------------------------------------------------------------|
| **Python** | 3.13+ | Linguagem principal de desenvolvimento |
| **NumPy** | 1.24+ | Manipulação eficiente de matrizes e arrays multidimensionais |
| **Matplotlib** | 3.7+ | Geração de gráficos e visualização do mapa de risco |
| **Multiprocessing** | Biblioteca padrão | Implementação do paralelismo (Pool, map) |
| **Time** | Biblioteca padrão | Medição de tempo de execução |

---

## 📊 Dataset

### Dados Sintéticos Gerados

Como o projeto foca no estudo da **paralelização** e não no dado em si, utilizamos dados sintéticos gerados aleatoriamente com distribuições estatísticas realistas:

| Variável | Distribuição | Parâmetros | Unidade | Descrição |
|----------|--------------|------------|---------|-----------|
| **Precipitação** | Gamma | shape=2, scale=50 | mm/mês | Volume de chuva acumulada |
| **Escoamento** | Uniforme | 0 a 300 | mm | Água que escorre pela superfície |
| **Umidade do Solo** | Uniforme | 10 a 600 | mm | Saturação do solo |

### Tamanhos Suportados

| Grade | Células | Uso |
|-------|---------|-----|
| 100×100 | 10.000 | Testes rápidos |
| 500×500 | 250.000 | Desenvolvimento |
| 1000×1000 | 1.000.000 | Benchmark principal |
| 2000×2000 | 4.000.000 | Teste de escalabilidade |
| 4000×4000 | 16.000.000 | Demonstração de impacto |
| 5000×5000 | 25.000.000 | Teste de estresse |

---

## ⚙️ Funcionamento do Sistema

### Arquitetura do Simulador
Código Utilizado 

import numpy as np
import time
from multiprocessing import Pool
import matplotlib.pyplot as plt
import os

def calcular_risco(precipitacao, escoamento, umidade_solo):
  
    if precipitacao > 400 and escoamento > 200:
        return 3
    elif precipitacao > 300 or escoamento > 150:
        return 2
    elif precipitacao > 200 or umidade_solo > 400:
        return 1
    else:
        return 0

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

def processar_linha(args):
    
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
    
    altura, largura = dados['precipitacao'].shape
    
   
    args_lista = []
    for i in range(altura):
        args_lista.append((
            i,
            dados['precipitacao'][i, :],
            dados['escoamento'][i, :],
            dados['umidade_solo'][i, :]
        ))
    

    with Pool(processes=num_processos) as pool:
        resultados = pool.map(processar_linha, args_lista)
    
  
    resultado = np.zeros((altura, largura), dtype=int)
    for idx, linha_resultado in resultados:
        resultado[idx, :] = linha_resultado
    
    return resultado


if __name__ == "__main__":
    print("=" * 60)
    print("SIMULADOR PARALELO DE RISCO DE INUNDAÇÕES")
    print("=" * 60)
    
    
    TAMANHO = 1000  # 1000x1000 = 1 milhão de células
    NUM_PROCESSOS = 4  # Número de núcleos para versão paralela
    
    print(f"\n[CONFIGURAÇÃO]")
    print(f"   Grade: {TAMANHO} x {TAMANHO} = {TAMANHO * TAMANHO:,} células")
    print(f"   Processos: {NUM_PROCESSOS} núcleos")
    

    print(f"\n[ETAPA 1] Gerando dados sintéticos...")
    inicio_geracao = time.time()
    
    dados = {
        'precipitacao': np.random.gamma(2, 50, (TAMANHO, TAMANHO)),
        'escoamento': np.random.uniform(0, 300, (TAMANHO, TAMANHO)),
        'umidade_solo': np.random.uniform(10, 600, (TAMANHO, TAMANHO))
    }
    
    fim_geracao = time.time()
    print(f"   ✓ Dados gerados em {fim_geracao - inicio_geracao:.2f} segundos")
    
   
    print(f"\n[ETAPA 2] Executando versão SEQUENCIAL...")
    print(f"   Processando {TAMANHO * TAMANHO:,} células...")
    
    inicio_seq = time.time()
    resultado_seq = simular_sequencial(dados)
    fim_seq = time.time()
    TEMPO_SEQUENCIAL = fim_seq - inicio_seq
    
    print(f"   ✓ TEMPO SEQUENCIAL: {TEMPO_SEQUENCIAL:.4f} segundos")
    
  
    print(f"\n[ETAPA 3] Executando versão PARALELA ({NUM_PROCESSOS} processos)...")
    
    inicio_par = time.time()
    resultado_par = simular_paralelo(dados, num_processos=NUM_PROCESSOS)
    fim_par = time.time()
    TEMPO_PARALELO = fim_par - inicio_par
    
    print(f"   ✓ TEMPO PARALELO: {TEMPO_PARALELO:.4f} segundos")
    
   
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
    
  
    print(f"\n[ETAPA 5] Distribuição do Risco de Inundação:")
    print(f"   " + "-" * 40)
    
    unique, counts = np.unique(resultado_seq, return_counts=True)
    niveis = {0: "🟢 BAIXO", 1: "🟡 MODERADO", 2: "🟠 ALTO", 3: "🔴 EXTREMO"}
    cores = {0: "Verde", 1: "Amarelo", 2: "Laranja", 3: "Vermelho"}
    
    for nivel, count in zip(unique, counts):
        percentual = count / (TAMANHO * TAMANHO) * 100
        print(f"   {niveis[nivel]}: {count:>10,} células ({percentual:>5.1f}%)")
    print(f"   " + "-" * 40)
    
 
    print(f"\n[ETAPA 6] Gerando visualizações...")
    

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
---------------------------------------------------------------

"""
SIMULADOR PARALELO DE RISCO DE INUNDAÇÕES
GRADE: 10.000 x 10.000 = 100 MILHÕES de células
VERSÃO COM MULTIPROCESSING
TESTE COM 1, 2, 4, 8, 12 PROCESSOS
COM CÁLCULO DE SPEEDUP E EFICIÊNCIA
"""

import numpy as np
import time
from multiprocessing import Pool, cpu_count
import matplotlib.pyplot as plt
import gc
import os
import sys

def calcular_risco_vetorizado(precipitacao, escoamento, umidade_solo):
    """Versão VETORIZADA - Processa a matriz inteira de uma vez"""
    resultado = np.zeros_like(precipitacao, dtype=np.int8)
    
    mask_extremo = (precipitacao > 400) & (escoamento > 200)
    resultado[mask_extremo] = 3
    
    mask_alto = ~mask_extremo & ((precipitacao > 300) | (escoamento > 150))
    resultado[mask_alto] = 2
    
    mask_moderado = ~mask_extremo & ~mask_alto & ((precipitacao > 200) | (umidade_solo > 400))
    resultado[mask_moderado] = 1
    
    return resultado

def processar_bloco(args):
    """Processa um bloco da matriz - usado no multiprocessing"""
    inicio_linha, fim_linha, precipitacao, escoamento, umidade_solo = args
    
    p_bloco = precipitacao[inicio_linha:fim_linha, :]
    e_bloco = escoamento[inicio_linha:fim_linha, :]
    u_bloco = umidade_solo[inicio_linha:fim_linha, :]
    
    resultado_bloco = calcular_risco_vetorizado(p_bloco, e_bloco, u_bloco)
    
    return inicio_linha, fim_linha, resultado_bloco

def simular_sequencial(dados):
    """Versão SEQUENCIAL (1 processo) - TEMPO SERIAL"""
    return calcular_risco_vetorizado(
        dados['precipitacao'],
        dados['escoamento'],
        dados['umidade_solo']
    )

def simular_paralelo_multiprocessing(dados, num_processos):
    """
    Versão PARALELA com MULTIPROCESSING
    FUNCIONA NO WINDOWS!
    """
    altura, largura = dados['precipitacao'].shape
    
    # Dividir em blocos
    tamanho_bloco = max(1, altura // num_processos)
    blocos = []
    
    for i in range(0, altura, tamanho_bloco):
        fim = min(i + tamanho_bloco, altura)
        blocos.append((
            i, fim,
            dados['precipitacao'],
            dados['escoamento'],
            dados['umidade_solo']
        ))
    
    # Executar em paralelo com multiprocessing
    with Pool(processes=num_processos) as pool:
        resultados = pool.map(processar_bloco, blocos)
    
    # Montar resultado final
    resultado = np.zeros((altura, largura), dtype=np.int8)
    for inicio, fim, bloco_resultado in resultados:
        resultado[inicio:fim, :] = bloco_resultado
    
    return resultado

# ============================================
# PROGRAMA PRINCIPAL
# ============================================

if __name__ == "__main__":
    print("=" * 80)
    print("🔥 SIMULADOR PARALELO DE RISCO DE INUNDAÇÕES")
    print("GRADE: 10.000 x 10.000 = 100 MILHÕES de células")
    print("VERSÃO COM MULTIPROCESSING")
    print("CÁLCULO DE SPEEDUP E EFICIÊNCIA")
    print("=" * 80)
    
    # ========== CONFIGURAÇÕES ==========
    TAMANHO = 10000  # 10000x10000 = 100 MILHÕES
    PROCESSOS = [1, 2, 4, 8, 12]  # Processos a testar
    
    # ========== CALCULAR MEMÓRIA ==========
    memoria_mb = (TAMANHO * TAMANHO * 3 * 4) / (1024 * 1024)  # 3 matrizes float32
    memoria_gb = memoria_mb / 1024
    
    print(f"\n📊 CONFIGURAÇÃO DA MÁQUINA:")
    print(f"   Grade: {TAMANHO} x {TAMANHO} = {TAMANHO * TAMANHO:,} células")
    print(f"   Processos a testar: {PROCESSOS}")
    print(f"   Núcleos disponíveis: {cpu_count()}")
    print(f"   Sistema Operacional: {os.name}")
    print(f"   Memória estimada: ~{memoria_mb:.0f} MB ({memoria_gb:.1f} GB)")
    
    # ========== AVISO DE MEMÓRIA ==========
    print(f"\n⚠️ ATENÇÃO: Este teste requer cerca de {memoria_gb:.1f} GB de RAM!")
    print(f"   O computador pode ficar lento ou travar se não tiver memória suficiente.")
    
    if memoria_gb > 4:
        resposta = input(f"\n   Continuar mesmo assim? (s/N): ")
        if resposta.lower() != 's':
            print("   ❌ Operação cancelada pelo usuário.")
            sys.exit(0)
    
    # ========== GERAR DADOS ==========
    print(f"\n[ETAPA 1] Gerando 100 milhões de células...")
    print(f"   ⏱️ Isso pode levar alguns minutos...")
    inicio_geracao = time.time()
    
    print(f"   Gerando precipitação...")
    precipitacao = np.random.gamma(2, 50, (TAMANHO, TAMANHO)).astype(np.float32)
    
    print(f"   Gerando escoamento...")
    escoamento = np.random.uniform(0, 300, (TAMANHO, TAMANHO)).astype(np.float32)
    
    print(f"   Gerando umidade do solo...")
    umidade_solo = np.random.uniform(10, 600, (TAMANHO, TAMANHO)).astype(np.float32)
    
    dados = {
        'precipitacao': precipitacao,
        'escoamento': escoamento,
        'umidade_solo': umidade_solo
    }
    
    fim_geracao = time.time()
    print(f"   ✅ Dados gerados em {fim_geracao - inicio_geracao:.2f} segundos")
    
    # ========== EXECUTAR TESTES ==========
    print(f"\n[ETAPA 2] Executando simulações com MULTIPROCESSING...")
    print(f"   ⏱️ Isso pode levar vários minutos!")
    print(f"   " + "=" * 70)
    
    resultados = []
    resultado_sequencial = None
    tempo_sequencial = 0
    
    for num_processos in PROCESSOS:
        print(f"\n   🧵 Testando com {num_processos} processo(s)...")
        
        if num_processos == 1:
            print(f"      Executando VERSÃO SEQUENCIAL (TEMPO SERIAL)...")
            inicio = time.time()
            resultado = simular_sequencial(dados)
            fim = time.time()
            tempo = fim - inicio
            tempo_sequencial = tempo
            tipo = "SEQUENCIAL (SERIAL)"
            resultado_sequencial = resultado
            print(f"      ✅ {tipo}: {tempo:.2f} segundos ({tempo/60:.2f} minutos)")
        else:
            print(f"      Executando VERSÃO PARALELA com {num_processos} processos...")
            inicio = time.time()
            resultado = simular_paralelo_multiprocessing(dados, num_processos)
            fim = time.time()
            tempo = fim - inicio
            tipo = f"PARALELA ({num_processos} processos)"
            print(f"      ✅ {tipo}: {tempo:.2f} segundos ({tempo/60:.2f} minutos)")
        
        resultados.append({
            'processos': num_processos,
            'tempo': tempo,
            'tipo': tipo
        })
        
        if num_processos != 1:
            del resultado
            gc.collect()
    
    # ========== CALCULAR SPEEDUP E EFICIÊNCIA ==========
    print(f"\n[ETAPA 3] CÁLCULO DO SPEEDUP E EFICIÊNCIA")
    print(f"   " + "=" * 70)
    
    print(f"\n   📍 TEMPO SEQUENCIAL (SERIAL - baseline): {tempo_sequencial:.2f} segundos")
    print(f"   ({tempo_sequencial/60:.2f} minutos)\n")
    
    for r in resultados[1:]:
        speedup = tempo_sequencial / r['tempo']
        eficiencia = (speedup / r['processos']) * 100
        r['speedup'] = speedup
        r['eficiencia'] = eficiencia
        print(f"   📍 {r['processos']} processos:")
        print(f"      Tempo: {r['tempo']:.2f}s")
        print(f"      SPEEDUP: {speedup:.2f}x")
        print(f"      EFICIÊNCIA: {eficiencia:.1f}%\n")
    
    # ========== TABELA DE RESULTADOS ==========
    print(f"\n[ETAPA 4] TABELA COMPLETA DE RESULTADOS")
    print(f"   " + "=" * 80)
    print(f"   | {'Processos':^10} | {'Tipo':^22} | {'Tempo (s)':^12} | {'Speedup':^10} | {'Eficiência':^12} |")
    print(f"   " + "-" * 80)
    
    for i, r in enumerate(resultados):
        if i == 0:
            speedup_str = "1.00"
            eficiencia_str = "100.0%"
        else:
            speedup_str = f"{r['speedup']:.2f}x"
            eficiencia_str = f"{r['eficiencia']:.1f}%"
        
        tipo_short = "Sequencial (Serial)" if r['processos'] == 1 else "Paralela"
        print(f"   | {r['processos']:^10} | {tipo_short:^22} | {r['tempo']:^12.2f} | {speedup_str:^10} | {eficiencia_str:^12} |")
    
    print(f"   " + "=" * 80)
    
    # ========== GERAR GRÁFICOS ==========
    print(f"\n[ETAPA 5] Gerando gráficos...")
    
    processos_lista = [r['processos'] for r in resultados]
    tempos_lista = [r['tempo'] for r in resultados]
    speedups_lista = [1.0] + [r['speedup'] for r in resultados[1:]]
    eficiencia_lista = [100.0] + [r['eficiencia'] for r in resultados[1:]]
    
    # GRÁFICO 1: Tempo vs Processos
    plt.figure(figsize=(15, 6))
    
    plt.subplot(1, 3, 1)
    plt.plot(processos_lista, tempos_lista, 'bo-', linewidth=2, markersize=8)
    plt.xlabel('Número de Processos', fontsize=12)
    plt.ylabel('Tempo de Execução (segundos)', fontsize=12)
    plt.title(f'Tempo vs Processos\n{TAMANHO}x{TAMANHO} (100M células)', fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.xticks(processos_lista)
    
    for proc, tempo in zip(processos_lista, tempos_lista):
        plt.annotate(f'{tempo:.1f}s', (proc, tempo), textcoords="offset points", xytext=(0, 10), ha='center')
    
    # GRÁFICO 2: Speedup vs Processos
    plt.subplot(1, 3, 2)
    plt.plot(processos_lista, speedups_lista, 'go-', linewidth=2, markersize=8, label='Speedup Obtido')
    plt.plot(processos_lista, processos_lista, 'r--', linewidth=2, label='Speedup Ideal')
    plt.xlabel('Número de Processos', fontsize=12)
    plt.ylabel('Speedup', fontsize=12)
    plt.title(f'Speedup vs Processos\n{TAMANHO}x{TAMANHO} (100M células)', fontsize=11)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(processos_lista)
    
    for proc, sp in zip(processos_lista, speedups_lista):
        plt.annotate(f'{sp:.2f}x', (proc, sp), textcoords="offset points", xytext=(0, 10), ha='center')
    
    # GRÁFICO 3: Eficiência vs Processos
    plt.subplot(1, 3, 3)
    plt.bar(processos_lista, eficiencia_lista, color='purple', alpha=0.7, edgecolor='black')
    plt.xlabel('Número de Processos', fontsize=12)
    plt.ylabel('Eficiência (%)', fontsize=12)
    plt.title(f'Eficiência vs Processos\n{TAMANHO}x{TAMANHO} (100M células)', fontsize=11)
    plt.grid(True, alpha=0.3, axis='y')
    plt.xticks(processos_lista)
    plt.ylim(0, max(eficiencia_lista) + 20)
    
    for proc, ef in zip(processos_lista, eficiencia_lista):
        plt.annotate(f'{ef:.1f}%', (proc, ef), textcoords="offset points", xytext=(0, 10), ha='center')
    
    plt.tight_layout()
    plt.savefig('resultados_multiprocessing_10000.png', dpi=150)
    print(f"   ✅ Gráfico salvo: resultados_multiprocessing_10000.png")
    
    # GRÁFICO 4: Comparação de Tempo (Barras)
    plt.figure(figsize=(10, 6))
    bars = plt.bar(processos_lista, tempos_lista, 
                   color=['red' if p==1 else 'green' for p in processos_lista], 
                   edgecolor='black', linewidth=1.5)
    plt.xlabel('Número de Processos', fontsize=12)
    plt.ylabel('Tempo de Execução (segundos)', fontsize=12)
    plt.title(f'Comparação de Tempo - 10.000x10.000 (100M células)', fontsize=14)
    plt.grid(True, alpha=0.3, axis='y')
    plt.xticks(processos_lista)
    
    for bar, tempo in zip(bars, tempos_lista):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                 f'{tempo:.1f}s', ha='center', va='bottom', fontsize=9)
    
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='red', label='Sequencial (Serial)'),
                       Patch(facecolor='green', label='Paralela')]
    plt.legend(handles=legend_elements)
    
    plt.tight_layout()
    plt.savefig('comparacao_tempo_10000.png', dpi=150)
    print(f"   ✅ Gráfico salvo: comparacao_tempo_10000.png")
    
    # ========== MAPA DE RISCO ==========
    print(f"\n[ETAPA 6] Gerando mapa de risco...")
    
    # Amostragem para não travar
    fator_amostragem = 100
    amostra = resultado_sequencial[::fator_amostragem, ::fator_amostragem]
    
    plt.figure(figsize=(12, 10))
    im = plt.imshow(amostra, cmap='YlOrRd', interpolation='nearest', vmin=0, vmax=3)
    cbar = plt.colorbar(im, ticks=[0, 1, 2, 3])
    cbar.set_label('Nível de Risco', fontsize=12)
    plt.title(f'Mapa de Risco de Inundação - 10.000x10.000 (100M células)\n'
              f'Tempo Serial: {tempo_sequencial:.1f}s | Melhor Speedup: {max(speedups_lista[1:]):.2f}x',
              fontsize=14)
    plt.xlabel('Longitude (pixels)', fontsize=12)
    plt.ylabel('Latitude (pixels)', fontsize=12)
    plt.tight_layout()
    plt.savefig('mapa_risco_10000.png', dpi=150)
    print(f"   ✅ Mapa salvo: mapa_risco_10000.png")
    
    # ========== DISTRIBUIÇÃO DO RISCO ==========
    print(f"\n[ETAPA 7] Distribuição do Risco:")
    print(f"   " + "-" * 40)
    
    unique, counts = np.unique(resultado_sequencial, return_counts=True)
    niveis = {0: "🟢 BAIXO", 1: "🟡 MODERADO", 2: "🟠 ALTO", 3: "🔴 EXTREMO"}
    
    for nivel, count in zip(unique, counts):
        percentual = count / (TAMANHO * TAMANHO) * 100
        print(f"   {niveis[nivel]}: {count:,} células ({percentual:.1f}%)")
    
    print(f"   " + "-" * 40)
    
    # ========== RESULTADO FINAL ==========
    print(f"\n" + "=" * 80)
    print(f"✅ SIMULAÇÃO CONCLUÍDA COM SUCESSO!")
    print(f"=" * 80)
    
    melhor = max(resultados[1:], key=lambda x: x['speedup'])
    print(f"\n📊 RESUMO FINAL - GRADE 10.000x10.000 (100 MILHÕES):")
    print(f"   • Tempo SEQUENCIAL (SERIAL): {tempo_sequencial:.2f} segundos ({tempo_sequencial/60:.1f} minutos)")
    print(f"")
    
    for r in resultados[1:]:
        print(f"   • {r['processos']} processos: {r['tempo']:.2f}s → Speedup: {r['speedup']:.2f}x | Eficiência: {r['eficiencia']:.1f}%")
    
    print(f"\n   🏆 MELHOR RESULTADO:")
    print(f"      {melhor['processos']} processos")
    print(f"      Speedup: {melhor['speedup']:.2f}x")
    print(f"      Eficiência: {melhor['eficiencia']:.1f}%")
    print(f"      Redução de tempo: {(1 - melhor['tempo']/tempo_sequencial)*100:.1f}%")
    
    print(f"\n📁 ARQUIVOS GERADOS:")
    print(f"   • resultados_multiprocessing_10000.png")
    print(f"   • comparacao_tempo_10000.png")
    print(f"   • mapa_risco_10000.png")
    print(f"\n" + "=" * 80)
    
    gc.collect()
