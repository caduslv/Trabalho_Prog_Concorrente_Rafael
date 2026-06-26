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
 ## Ambiente Experimental
| Item                        | Descrição                                    |
| --------------------------- | -------------------------------------------- |
| Processador                 |12th Gen Intel(R) Core(TM) i5-12500   3.00 GHz|
| Número de núcleos           |6 núcleos (cores) físicos                     |
| Memória RAM                 |16,0 GB (utilizável: 15,7 GB)                 |
| Sistema Operacional         |Windows 11 Pro                                |
| Linguagem utilizada         |Python                                        |
| Biblioteca de paralelização |concurrent.futures                            |
| Compilador / Versão         | CPython/ 3.13                                |
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
---
## Metodologia de Testes
## Orientações

Descrever:
Os experimentos foram realizados utilizando um programa desenvolvido na linguagem Python, executado no interpretador CPython, no ambiente de desenvolvimento Visual Studio Code. O objetivo dos testes foi analisar o desempenho da execução paralela na soma de números inteiros armazenados em um arquivo.
* Como o tempo de execução foi medido:
O tempo de execução foi medido utilizando a função time() da biblioteca padrão time do Python. O tempo inicial foi registrado antes do início da execução do algoritmo e o tempo final foi registrado após o término do processamento. O tempo total foi calculado pela diferença entre o tempo final e o tempo inicial.
* Quantas execuções foram realizadas:

* Se foi utilizada média dos tempos:
Foi utilizada a média aritmética dos tempos obtidos nas execuções para representar o tempo final de cada configuração. Essa média foi calculada somando todos os tempos medidos e dividindo pelo número total de execuções realizadas.
* Qual tamanho da entrada foi usado:

---
### Configurações testadas

Os experimentos devem ser realizados nas seguintes configurações:

* 1 thread/processo (versão serial)
* 2 threads/processos
* 4 threads/processos
* 8 threads/processos
* 12 threads/processos

### Procedimento experimental

Descrever:

* Número de execuções para cada configuração:
Cada configuração de threads (1, 2, 4, 8 e 12) foi executada 5 vezes para reduzir possíveis variações nos resultados causadas por interferências do sistema ou outros processos em execução.
* Forma de cálculo da média:
Após a execução das 5 repetições para cada configuração, foi calculada a média aritmética dos tempos obtidos. A média foi utilizada como valor representativo do tempo de execução da configuração, permitindo comparações consistentes entre diferentes números de threads.
Média=5T1​+T2​+T3​+T4​+T5​/5
* Condições de execução (ex: máquina dedicada, carga do sistema, etc.)
Os experimentos foram realizados em um computador com processador Intel Core i5-12500 e 16 GB de memória RAM.
Sistema operacional utilizado: Microsoft Windows.
Durante os testes, a máquina foi mantida com baixa carga de processamento, evitando a execução de programas pesados em paralelo, garantindo que o desempenho medido refletisse principalmente a execução do algoritmo.
---
# 4. Resultados Experimentais

Preencha a tabela com os **tempos médios de execução** obtidos.

## Orientações

* O tempo deve ser informado em **segundos**
* Utilizar a **média das execuções**

| Nº Threads/Processos | Tempo de Execução (s) |
| -------------------- | --------------------- |
| 1                    |                       |
| 2                    |                       |
| 4                    |                       |
| 8                    |                       |
| 12                   |                       |

---

# 5. Cálculo de Speedup e Eficiência

## Fórmulas Utilizadas

### Speedup

```
Speedup(p) = T(1) / T(p)​
```

Onde:

* **T(1)** = tempo da execução serial
* **T(p)** = tempo com p threads/processos

### Eficiência

```
Eficiência(p) = Speedup(p) / p

```

Onde:

* **p** = número de threads ou processos

---

# 6. Tabela de Resultados

Preencha a tabela abaixo utilizando os tempos medidos.

| Threads/Processos | Tempo (s) | Speedup | Eficiência |
| ----------------- | --------- | ------- | ---------- |
| 1                 |           |         |            |
| 2                 |           |         |            |
| 4                 |           |         |            |
| 8                 |           |         |            |
| 12                |           |         |            |

---

# 7. Gráfico de Tempo de Execução

Construa um gráfico mostrando o **tempo de execução em função do número de threads/processos**.

## Orientações

* Eixo X: número de threads/processos
* Eixo Y: tempo de execução (segundos)

Inserir o gráfico abaixo:

![Gráfico Tempo Execução](graficos/)

---

# 8. Gráfico de Speedup

Construa um gráfico mostrando o **speedup obtido**.

## Orientações

* Eixo X: número de threads/processos
* Eixo Y: speedup
* Incluir também a **linha de speedup ideal (linear)** para comparação

Inserir o gráfico abaixo:

![Gráfico Speedup](graficos/)

---

# 9. Gráfico de Eficiência

Construa um gráfico mostrando a **eficiência da paralelização**.

## Orientações

* Eixo X: número de threads/processos
* Eixo Y: eficiência
* Valores entre 0 e 1

Inserir o gráfico abaixo:

![Gráfico Eficiência](graficos/)

---

# 10. Análise dos Resultados

Realize uma análise crítica dos resultados obtidos.
## Questões a serem respondidas

* O speedup obtido foi próximo do ideal?

* A aplicação apresentou escalabilidade?

* Em qual ponto a eficiência começou a cair?

* O número de threads ultrapassa o número de núcleos físicos da máquina?

* Houve overhead de paralelização?

Discutir possíveis causas para:

* perda de desempenho:

* gargalos no algoritmo:

* sincronização entre threads/processos:

* comunicação entre processos:

* contenção de memória ou cache


---

# 11. Conclusão

Apresente as conclusões do experimento.

## Sugestões de pontos a comentar

* O paralelismo trouxe ganho significativo de desempenho?

* Qual foi o melhor número de threads/processos?

* O programa escala bem com o aumento do paralelismo?

* Quais melhorias poderiam ser feitas na implementação?

Reduzir sincronização e junção de resultados, minimizando overhead.

---
