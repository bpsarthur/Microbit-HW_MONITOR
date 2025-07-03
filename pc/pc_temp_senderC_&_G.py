import psutil
import serial
import time
import wmi

# --- Configuração ---
# Encontre a porta serial correta do seu micro:bit.
# No Windows, será 'COMx' (ex: 'COM3').
# No macOS ou Linux, será '/dev/tty.usbmodem...' ou '/dev/ttyACM...'.
SERIAL_PORT = 'COM3'  # !!! ALTERE PARA A PORTA DO SEU MICRO:BIT !!!
BAUD_RATE = 115200

# --- Funções para Obter Temperaturas ---

def obter_temperatura_cpu():
    """Obtém a temperatura da CPU."""
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
                         return int(entry.current)
    except Exception as e:
        print(f"Não foi possível obter a temperatura da CPU com psutil: {e}")

    # Para Windows, método mais confiável usando WMI
    try:
        w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
        temperature_infos = w.Sensor()
        for sensor in temperature_infos:
            if sensor.SensorType == 'Temperature' and 'cpu' in sensor.Name.lower():
                return int(sensor.Value)
    except Exception as e:
        print(f"Não foi possível obter a temperatura da CPU com WMI. O OpenHardwareMonitor está em execução? Erro: {e}")

    return None

def obter_temperatura_gpu():
    """Obtém a temperatura da GPU (principalmente para Windows usando WMI)."""
    try:
        w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
        temperature_infos = w.Sensor()
        for sensor in temperature_infos:
            if sensor.SensorType == 'Temperature' and 'gpu' in sensor.Name.lower():
                return int(sensor.Value)
    except Exception as e:
        print(f"Não foi possível obter a temperatura da GPU com WMI. O OpenHardwareMonitor está em execução? Erro: {e}")
    return None

# --- Programa Principal ---

if __name__ == "__main__":
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Conectado à {SERIAL_PORT} em {BAUD_RATE} baud.")
    except serial.SerialException as e:
        print(f"Erro: Não foi possível abrir a porta serial {SERIAL_PORT}. Verifique o nome da porta e se o micro:bit está conectado.")
        exit()

    while True:
        temp_cpu = obter_temperatura_cpu()
        temp_gpu = obter_temperatura_gpu()

        if temp_cpu is not None:
            mensagem = f"C {temp_cpu}\n"
            ser.write(mensagem.encode('utf-8'))
            print(f"Enviado: {mensagem.strip()}")

        if temp_gpu is not None:
            mensagem = f"G {temp_gpu}\n"
            ser.write(mensagem.encode('utf-8'))
            print(f"Enviado: {mensagem.strip()}")

        time.sleep(5)  # Envia dados a cada 5 segundos