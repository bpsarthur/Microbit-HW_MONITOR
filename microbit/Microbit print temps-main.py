# Script Melhorado para micro:bit
# Este script é executado no seu micro:bit.
# Ele recebe dados de temperatura de um PC e os exibe de forma clara.

from microbit import sleep, display, Image, uart
# --- Configuração ---
# A taxa de transmissão deve ser a mesma do script do PC
BAUD_RATE = 115200

# --- Inicialização ---
# Configura a comunicação serial
uart.init(baudrate=BAUD_RATE)

# Mostra um ícone de inicialização para que o usuário saiba que está pronto
display.show(Image.HAPPY)
sleep(1000)
display.clear()

# --- Loop Principal ---
while True:
    # Mostra uma animação de espera (um ponto piscando)
    # para que o usuário saiba que está aguardando dados.
    display.set_pixel(0, 0, 5)
    sleep(500)
    display.set_pixel(0, 0, 0)
    sleep(500)

    # Verifica se há algum dado aguardando no buffer serial
    if uart.any():
        data = uart.readline()
        if data:
            try:
                # Converte os bytes recebidos em uma string
                received_string = str(data, 'utf-8').strip()

                # O PC envia dados como "C:45". Queremos extrair o número.
                # Encontra a posição dos dois pontos (:)
                colon_index = received_string.find(':')
                
                if colon_index != -1:
                    # Extrai a parte da string após os dois pontos
                    temp_value_str = received_string[colon_index + 1:]
                    
                    # Exibe apenas o número no display
                    display.show(temp_value_str)
                    sleep(4000) # Mantém a temperatura na tela por 4 segundos
                    display.clear()
                else:
                    # Se o formato for inesperado, rola os dados brutos na tela
                    display.scroll(received_string, delay=90)

            except (ValueError, IndexError):
                # Se ocorrer um erro (ex: os dados não são um número),
                # exibe uma mensagem de erro para ajudar na depuração.
                display.scroll("Err", delay=90)
