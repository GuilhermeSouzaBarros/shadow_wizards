# Documentação dos Mapas

Bem vindo a documentação dos mapas do jogo +-+

## Índices
1. [Introdução](#introdução)
2. [Significado dos tipos de tiles](#significado-dos-tipos-de-tiles)
3. [Mapas do jogo](#mapas-do-jogo)

## Introdução
As características dos mapas do jogo foram organizadas em arquivos .json. Estes arquivos, quando lidos, mandam para o programa as informações organizadas da mesma forma que foi estipulada (dentro de dicionários, listas, tuplas...).

## Significado dos Tipos de Tiles 
- Tipo 0: tile de chão do mapa. Não possui colisão com nenhum objeto;
- Tipo 1: tile de obstáculo destrutível;
- Tipo 2: tile de obstáculos indestrutível;
- Tipo 3: tile de barreira lateral do mapa;
- Tipo 4: tile de barreira superior do mapa;
- Tipo mod5: tiles de spawn point dos players;
- Tipo 7: tile de trilho do carrinho de objetivo;
- Tipo 8: tile de último trilho do carrinho de objetivo.

## Mapas do Jogo
- Todos os mapas do jogo possuem 25 tiles de largura e 15 de altura (23 de largura e 13 de altura desconsiderando as barreiras). 

1. [Mapa 1 - Mata-Mata](#mapa-1)
2. [Mapa 2 - Conquiste a Carga](#mapa-2)
3. [Mapa 3 - Capture a Bandeira](#mapa-3)
4. [Mapa 4 - Dominação](#mapa-4)

### Mapa 1
No modo de jogo mata-mata o objetivo dos jogadores é obter o maior número de kills o possível. Os jogadores são divididos em times individuais e o grande vencedor é aquele que acumular o maior número de mortes em seu nome.
Os jogadores nascem nos 4 cantos do mapa e podem utilizar de habilidades para destruir blocos destrutíveis, a fim de abrir mais espaço no mapa para batalhar. O mapa não conta com nenhum tipo de objetivo especial.

### Mapa 2
No modo de jogo conquiste a carga o objetivo dos jogadores é levar a carga para o outro lado do mapa. Os jogadores são divididos em 2 times, e o vencedor é aquele que levar a carga mais longe o possível no sentido da base do time inimigo. Caso algum time leve a carga o máximo possível para o outro lado, a partida acaba antes do fim do cronometro. Já no caso de empate, o time vencedor é aquele que possuir mais mortes e, caso persista o empate, o jogo termina sem nenhum time vencedor.
Os jogadores da mesma equipe nascem juntos na base da sua equipe, que estão localizadas no canto superior esquerdo e inferior direito do mapa. A carga começa no centro do mapa, exatamente na metade do caminho entre a base dos dois times. Para mover a carga, ao menos um membro do time deve estar dentro da área delimitada pela carga, sem que um jogador da outra equipe ocupe o mesmo espaço. 
O movimento do carrinho é ditado pelos pontos de controle, determinados na lista de caminhos. Quando o carrinho chega até ao tile correspondente ao ponto de controle, ele deve mudar a sua direção de movimentação. **INCOMPLETO**

### Mapa 3
No modo de jogo de capture a bandeira o objetivo dos jogadores é obter a maior quantidade possível de pontos no decorrer da partida, principalmente através da captura de bandeiras. Os jogadores são divididos em 2 times, e o vencedor é aquele que obter a maior quantidade de pontos no decorrer da partida. Para obter pontos, o time deverá capturar bandeiras e eliminar jogadores do time adversário.
Os jogadores da mesma equipe nascem do mesmo lado no mapa, mas em cantos opostos, e os pontos de captura de cada equipe estão localizados na metade do lado de sua equipe, junto de suas bandeiras. Para capturar bandeiras, as equipes devem pegar a bandeira adversária e leva-lá para o seu ponto de captura. Quando um jogador que está com a bandeira morre, a bandeira retorna para o seu ponto inicial.
Para pegar a bandeira, o jogador deverá colidir com a mesma.

### Mapa 4
No modo de jogo de dominação o objetivo dos jogadores é obter a maior quantidade possível de pontos no decorrer da partida. Para obter pontos, os jogadores deverão ficar tempo na região de dominação, sem que algum jogador da equipe adversária ocupe ou mesmo espaço, ou através de eliminações de adversários.