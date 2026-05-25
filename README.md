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
