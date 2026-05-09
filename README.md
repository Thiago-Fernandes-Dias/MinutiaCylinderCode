# Minutia Cylinder-Code (MCC)

=======================================================================================

R. Cappelli, M. Ferrara, D. Maltoni, Minutia Cylinder-Code: A New Representation and Matching Technique
for Fingerprint Recognition.  IEEE Transactions on Pattern Analysis and Machine Intelligence, 32(12), 2128-2141 (2010).

=======================================================================================

Algoritmo local de correspondência de impressões digitais. Constrói estruturas de dados 3D
chamadas cilindros a partir dos ângulos e posições das minúcias. Suporta o padrão ISO/IEC
19794-2 (não o formato, mas a correspondência exclusiva baseada apenas em minúcias). É robusto
a deformações e utiliza bordas suaves para levar em conta as propriedades relativas entre as
minúcias mais próximas.

Fase I)  Cria todos os cilindros a partir do conjunto de minúcias. Cada cilindro é representado
        por um vetor de ponto flutuante ou binário, dependendo do algoritmo utilizado na
        construção. Um cilindro é considerado inválido se não possui relações suficientes com
        outros cilindros.

Fase II) Calcula a matriz de similaridades entre todos os cilindros válidos.

Fase III) Consolidação: o algoritmo implementa quatro tipos de consolidação.
        - LSS:   Busca pelos melhores pares de cilindros sem considerar repetições de atribuição.
        - LSA:   A atribuição é feita por meio do algoritmo húngaro.
        - LSS-R: As similaridades são ajustadas por um algoritmo de reforço baseado na relação
                 das minúcias com outras minúcias candidatas. A atribuição é feita por LSS.
        - LSA-R: Combinação do LSA com o algoritmo de reforço.


=======================================================================================

## Compilação (Ubuntu 24.04)

### Dependências

```bash
sudo apt install g++ make libopenmpi-dev openmpi-bin
```

| Pacote              | Finalidade                                      |
|---------------------|-------------------------------------------------|
| `g++`               | Compilador C++ (GNU)                            |
| `make`              | Automação da compilação                         |
| `libopenmpi-dev`    | Headers e bibliotecas do OpenMPI                |
| `openmpi-bin`       | Wrapper `mpic++` e utilitários de execução MPI  |

### Compilação

```bash
make            # compila o executável mcc
make clean      # remove artefatos de compilação
make check-deps # verifica as dependências
```

### Execução

```bash
./mcc <impressao1> <impressao2> -N {8|16} -C {LSS|LSSR|LSA|LSAR|LGS|NHS} [-H] [-B]
```

- `-N 8|16`: número de células por lado da base do cilindro
- `-C`: estratégia de consolidação (LSS, LSSR, LSA, LSAR, LGS, NHS)
- `-H`: ativa extração de convex hull
- `-B`: ativa operações bit-a-bit para os cilindros