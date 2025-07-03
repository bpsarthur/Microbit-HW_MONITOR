# Microbit-HW_MONITOR

Este projeto permite monitorar a temperatura do seu PC (CPU e GPU) e exibi-la em tempo real em um micro:bit via comunicação serial.

## Estrutura dos Arquivos

- **Microbit print temps-main.py**  
  Script para ser carregado no micro:bit. Ele lê dados seriais e exibe a temperatura recebida no display do micro:bit.

- **cpu_temp_sender.py**  
  Script Python para rodar no PC. Ele lê a temperatura da CPU e envia para o micro:bit via porta serial.

- **pc_temp_senderC_&_G.py**  
  Versão aprimorada do script do PC, que envia tanto a temperatura da CPU quanto da GPU para o micro:bit.

- **Microbit print temps.hex**  
  Arquivo compilado para ser carregado diretamente no micro:bit (opcional, gerado a partir do script Python).

- **.gitattributes**  
  Configuração de normalização de final de linha para o Git.

## Como Usar

### 1. No micro:bit

1. Carregue o arquivo [`Microbit print temps-main.py`](Microbit%20print%20temps-main.py) (ou o `.hex`) no seu micro:bit.
2. Conecte o micro:bit ao PC via USB.

### 2. No PC

1. Instale as dependências necessárias:
    ```sh
    pip install psutil pyserial wmi
    ```
    > Para leitura de GPU/CPU no Windows, é recomendado rodar o [Open Hardware Monitor](https://openhardwaremonitor.org/) em segundo plano.

2. Edite o valor de [SERIAL_PORT](http://_vscodecontentref_/0) nos scripts [cpu_temp_sender.py](http://_vscodecontentref_/1) ou [pc_temp_senderC_&_G.py](http://_vscodecontentref_/2) para corresponder à porta do seu micro:bit (ex: `COM3` no Windows).

3. Execute o script desejado:
    ```sh
    python cpu_temp_sender.py
    ```
    ou
    ```sh
    python pc_temp_senderC_&_G.py
    ```

### 3. Visualização

- O micro:bit exibirá a temperatura recebida no display de LEDs.
- Se o dado recebido não estiver no formato esperado, ele será rolado na tela.

## Observações

- O script do micro:bit espera receber dados no formato `C:45` ou similar.
- O script do PC envia a temperatura a cada poucos segundos.
- Para monitorar GPU, use o script [pc_temp_senderC_&_G.py](http://_vscodecontentref_/3).

## Créditos

Scripts desenvolvidos para integração entre PC e micro:bit via serial, utilizando Python e MicroPython.

---

**Pastas e arquivos deste projeto:**
- [Microbit print temps-main.py](http://_vscodecontentref_/4)
- [cpu_temp_sender.py](http://_vscodecontentref_/5)
- [pc_temp_senderC_&_G.py](http://_vscodecontentref_/6)
- Microbit print temps.hex
- [.gitattributes](http://_vscodecontentref_/7)

