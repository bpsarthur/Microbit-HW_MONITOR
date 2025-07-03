# Script do PC: pc_cpu_temp_sender.py
# Este script roda no seu computador.
# Ele obtém a temperatura da CPU e envia para o micro:bit via serial.

import psutil
import serial
import time
import wmi

# --- Configuração ---
# Encontre a porta serial correta do seu micro:bit.
# No Windows, será 'COMx' (ex: 'COM3').
# No macOS ou Linux, será '/dev/tty.usbmodem...' ou '/dev/ttyACM...'.

# !!! ALTERE PARA A PORTA DO SEU MICRO:BIT !!!
SERIAL_PORT = 'COM3'
BAUD_RATE = 115200

# --- Função para Obter Temperatura da CPU ---

def obter_temperatura_cpu():
    """
    Obtém a temperatura da CPU usando psutil ou WMI como alternativa.
    Para o WMI funcionar no Windows, o Open Hardware Monitor deve estar em execução.
    """
    try:
        # psutil.sensors_temperatures() pode fornecer temperaturas da CPU em alguns sistemas (principalmente Linux)
        temps = psutil.sensors_temperatures()
        if 'coretemp' in temps:
            return int(temps['coretemp'][0].current)
        # Alternativa para outros sistemas ou se coretemp não estiver disponível
        if hasattr(psutil, "sensors_temperatures"):
             temps = psutil.sensors_temperatures()
             if temps:
                 for name, entries in temps.items():
                     for entry in entries:
                         # Procura por nomes comuns de sensores de temperatura da CPU
                         if 'cpu' in entry.label.lower() or 'core' in entry.label.lower():
                            return int(entry.current)
    except Exception as e:
        print(f"Não foi possível obter a temperatura da CPU com psutil: {e}")

    # Para Windows, método mais confiável usando WMI e Open Hardware Monitor
    try:
        w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
        temperature_infos = w.Sensor()
        for sensor in temperature_infos:
            if sensor.SensorType == 'Temperature' and 'cpu' in sensor.Name.lower():
                return int(sensor.Value)
    except Exception as e:
        print(f"Não foi possível obter a temperatura da CPU com WMI. O OpenHardwareMonitor está em execução? Erro: {e}")

    return None

# --- Programa Principal ---

if __name__ == "__main__":
    print("Iniciando o Enviador de Temperatura da CPU do PC...")
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Conectado à {SERIAL_PORT} em {BAUD_RATE} baud.")
    except serial.SerialException as e:
        print(f"Erro: Não foi possível abrir a porta serial {SERIAL_PORT}.")
        print("Verifique o nome da porta e se o micro:bit está conectado.")
        exit()

    while True:
        cpu_temp = obter_temperatura_cpu()

        if cpu_temp is not None:
            # Adiciona "C:" como prefixo para clareza no display
            mensagem = f"{cpu_temp}\n"
            ser.write(mensagem.encode('utf-8'))
            print(f"Enviado: {mensagem.strip()}")
        else:
            print("Não foi possível obter a temperatura da CPU.")

        time.sleep(2)  # Envia dados a cada 2 segundos
