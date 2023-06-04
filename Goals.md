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
uma para receber pedidos e colocá-los na queue
tenta comunicar com o servidor e não tenha resposta cria ele um.

Para desligar o servidor, basta avisa o listener thread que não há mais pedidos, e termina.

- Vizualizar o progresso da queue.


---------------------------------------------

- Calcular o tempo de execução da queue terminar:

- argparser para decidir o input, output(opcional), linguagem input(opcional), linguagem output(opcional). 
