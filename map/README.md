# Codificação dos Mapas em Arquivos JSON

Este readme descreve a estrutura e significados das informações armazenadas nos arquivos JSON dos mapas.

## Atributos

Todos os arquivos possuem os atributos: 
| Atributo | Significado |
| -------- | ----------- |
| height | Quantidade de tiles no eixo y |
| width | Quantidade de tiles no eixo x |
| tile_size | Tamanho (em pixels) de cada tile |
| spawn_points | Coordenadas (em tiles) do spawn point de cada player (1-4) |
| tiles | Códigos de identificação dos tiles do mapa por posição [i, j] |
| objectives | Objetivos do modo de jogo |

### Significado do ID dos tiles
| ID | Siginificado |
| -- | ------------ |
| 0 | Piso |
| 1 | Borda do mapa |
| 2 | Barreira de prédio |
| 3 | Barreira de cones |
| 4 | Barreira de container |
| 5 | Barreira de carros em mão dupla |
| 6 | Barreira de carros em mão simples |
| 7 | Caminho da payload |
| 8 | Área de spawn do player 1 |
| 9 | Área de spawn do player 2 |
|10 | Área de spawn do player 3 |
|11 | Área de spawn do player 4 |