# Simulador Paralelo de Risco de Inundações

** Disciplina:*PROGRAMAÇÃO CONCORRENTE E DISTRIBUÍDA* 
** Aluno(s):*Carlos Eduardo Pinheiro Da Silva - Luís Henrique Vieira Holanda*
** Turma:*5° Semestre/ Análise e Desenvolvimento de Sistemas*
** Professor:*Rafael Marconi Ramos*
** Data:*15/05/2026*

# Descrição do Projeto

# Objetivo Geral
Desenvolver e analisar um sistema paralelo para simulação de risco de inundações, utilizando dados climáticos sintéticos (precipitação, escoamento superficial e umidade do solo), comparando o desempenho da versão sequencial com a versão paralela e medindo o **speedup** obtido.
# Objetivos Específicos
1. **Implementar um modelo de risco de inundação** baseado em regras matemáticas que consideram três variáveis ambientais: precipitação, escoamento e umidade do solo.
2. **Desenvolver uma versão sequencial** do simulador para servir como baseline de desempenho.
3. **Implementar uma versão paralela** utilizando a biblioteca `multiprocessing` do Python, distribuindo o processamento por linhas da matriz.
4. **Medir e comparar o desempenho** entre as duas versões, calculando métricas como:
   - Tempo de execução sequencial
   - Tempo de execução paralela
   - Speedup (ganho de performance)
   - Eficiência do paralelismo

5. **Gerar visualizações gráficas** do mapa de risco e da comparação de desempenho para facilitar a análise dos resultados.
| Tecnologia | Versão | Finalidade |
|------------|--------|------------|
| **Python** | 3.13+ | Linguagem principal de desenvolvimento |
| **NumPy** | 1.24+ | Manipulação eficiente de matrizes e arrays multidimensionais |
| **Matplotlib** | 3.7+ | Geração de gráficos e visualização do mapa de risco |
| **Multiprocessing** | Biblioteca padrão | Implementação do paralelismo (Pool, map) |
| **Time** | Biblioteca padrão | Medição de tempo de execução |

6. **Analisar a escalabilidade** do sistema em diferentes tamanhos de grade e números de processos.
# Tecnologias Utilizadas

# Dataset

# Dados Sintéticos Gerados
Como o projeto foca no estudo da **paralelização** e não no dado em si, utilizamos dados sintéticos gerados aleatoriamente com distribuições estatísticas realistas:

| Variável | Distribuição | Parâmetros | Unidade | Descrição |
|----------|--------------|------------|---------|-----------|
| **Precipitação** | Gamma | shape=2, scale=50 | mm/mês | Volume de chuva acumulada |
| **Escoamento** | Uniforme | 0 a 300 | mm | Água que escorre pela superfície |
| **Umidade do Solo** | Uniforme | 10 a 600 | mm | Saturação do solo |

# Tamanhos Suportados
| Grade | Células | Uso |
|-------|---------|-----|
| 100×100 | 10.000 | Testes rápidos |
| 500×500 | 250.000 | Desenvolvimento |
| 1000×1000 | 1.000.000 | Benchmark principal |
| 2000×2000 | 4.000.000 | Teste de escalabilidade |
| 5000×5000 | 25.000.000 | Demonstração de impacto |
# Funcionamento do Sistema

# Arquitetura do Simulador
