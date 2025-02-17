# Shadow Wizards
O jogo Shadow Wizards consiste em um jogo multijogador de batalha localizado em um mapa fechado, no qual os jogadores são divididos em dois times ou em um formato de cada um por si.

As partidas do jogo são realizadas em um servidor local (LAN), com suporte de até 4 jogadores simultâneos. Para organizar uma partida, os jogadores devem estar na mesma rede de internet e na mesma versão do jogo. 

Cada partida tem duração de no máximo 3 minutos, e o vencedor é aquele que conseguir a maior quantidade de pontos de acordo com os objetivos do modo de jogo selecionado.

## Mapas do Jogo
### Mapa 1 - Mata-Mata
No mapa de Mata-Mata, os jogadores batalham cada um por si para determinar aquele que conseguirá o maior número de eliminações. 
  
### Mapa 2 - Payload
No mapa de Payload, os jogadores são divididos em dois times. O grande objetivo do modo de jogo é levar o carrinho o mais longe o possível na direção da base inimiga.

Caso um dos times leve o carrinho até a linha de chegada antes que o cronômetro chegue a zero, o jogo finaliza com o time responsável como o grande vencedor.

### Mapa 3 - Capture the Flag
No mapa Capture the Flag, os jogadores são divididos em dois times, cada um em um lado do mapa e suas bandeiras estão localizadas no ponto de entrega da sua base. O objetivo é ir até a base inimiga, capturar a bandeira adversária e trazê-la até o ponto de captura da própria base.

O time vencedor é aquele que conseguir capturar o maior número de bandeiras adversárias.

Caso um dos times leve 4 bandeiras adversárias para sua área de captura antes que o cronômetro chegue a 0, a partida é encerrada e o time é declarado vencedor.

### Mapa 4 - Domination 
No mapa de Domination, os jogadores são divididos em dois times, e o grande objetivo do modo de jogo é dominar pelo máximo de tempo a área de dominação, localizada no centro do mapa. 

Para dominar a região é preciso que somente jogadores do próprio time estejam ocupando a área. Caso algum jogador adversário também ocupe a área, a zona é declarada como não tomada.

Caso um dos times consiga 100 pontos antes do fim do cronômetro, a partida é encerrada com o time responsável como vencedor.

## Manual de Execução
### Instalação dos Requerimentos do Jogo
Criar ambiente virtual:
```    
sudo apt install python3.12-venv
python3.12 -m venv env
source env/bin/activate
```
Instalar imports:
```
pip install -r requirements.txt
```

### Execução do Jogo
```
python3 main.py
```

### Iniciar uma Partida
Para iniciar uma partida, primeiro o host do servidor deverá seguir os seguintes passos:

1. Clicar no botão "Host Lobby"
2. Já na tela de Host, agora deverá ser pressionado o botão "Open Lobby". Aguarde até que o texto do botão mude para "Lobby: 0/4 players"
3. Após concluir o passo 2, o processo de criar o servidor está concluído. O jogador pode pressionar a tecla "Esc" para retornar ao menu principal
4. Para entrar no servidor, o jogador deve pressionar o botão "Join Lobby", do menu principal
5. Agora, dentro da interface para entrar em um lobby, o jogador deverá pressionar o botão "Find Lobby" e aguardar até que o texto do botão seja "Lobby Found"
6. Quando o lobby for encontrado, outros eventuais jogadores podem repetir os passos 4 e 5 para entrarem também no servidor
7. Após todos os jogadores da partida entrarem no servidor, o responsável pelo host deverá pressionar a tecla "Esc" para retornar ao menu principal
8. Dentro do menu principal, o host deverá agora retornar à página "Host Lobby"
9. Agora, em "Host Lobby", o jogador poderá pressionar o botão "Start Match" para inciar a partida

### Informações Adicionais para Iniciar uma Partida
- Dentro da página de "Host Lobby", o jogador responsável pelo servidor tem a possibilidade de selecionar o modo de jogo desejado para a partida clicando em um dos botões à direita. Caso o jogador não selecione manualmente nenhum modo de jogo, a partida acontecerá em um mapa aleatório.
- Na interface de "Join Lobby" cada um dos players do jogo têm a opção de selecionar o personagem desejado para a partida, clicando no ícone de um deles, posicionados à direta da tela. A habilidade de cada personagem é descrita do lado esquerdo da tela.
- É possível organizar uma partida com mais de um jogador localmente, basta executar o código do jogo outras vezes em terminais separados e seguir os mesmos passos para executar em LAN, porém não será possível controlar jogadores de janelas diferentes da selecionada.
- Iniciar a partida com somente um jogador é possível, porém não é garantido que todas as funcionalidades funcionem como o esperado.

## Comandos do Jogo
| Tecla | Ação |
| ------ | ------ |
| W | Mover para frente |
| A | Mover para a esquerda |
| S | Mover para trás |
| D | Mover para a direita |
| Tab (segurar) | Exibir o placar |
| Esc | Fecha o jogo |

