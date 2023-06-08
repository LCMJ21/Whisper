serviço remoto de transcrição whisper
Whisper (openAI, ou sua vertente C++) + modelo hugginface (large-v2)

P submete audio A

servidor:

guarda A
regista pedido numa queue
avisa de que vai demorar (estima o tempo necessário), e diz onde vai ficar o resultado final
quando termina o trabalho, coloca-o no local combinado

prever um instalador (?)

Tarefas:

- 2 threads:
uma para receber pedidos e colocá-los na queue ✓
tenta comunicar com o servidor e não tenha resposta cria ele um. ✓

Para desligar o servidor, basta avisa o listener thread que não há mais pedidos, e termina. ✓

- Vizualizar o progresso da queue. (adicionar tempo/tamanho ficheiro)

- Calcular o tempo de execução da queue terminar: CRIS
    - calcular o tempo de execução de cada pedido para adicionar à media
    - tempo do pedido atual
    - guarda em ficheiro ao desligar

- argparser para decidir o input, output(opcional), linguagem input(opcional), linguagem output(opcional). ✓

- adicionar ao flit para ter instalação mais fácil

- traduções com ou sem googe translate ?

- COrrer as 2 threads em background

Extras: CRIS
- Listar linguas disponiveis para input audio em help
- Verficar se as liguas de input a audio são suportadas
