import psutil
import serial
import time
import wmi

# --- Configuration ---
# Find the correct serial port for your micro:bit.
# On Windows, it will be 'COMx' (e.g., 'COM3').
# On macOS or Linux, it will be '/dev/tty.usbmodem...' or '/dev/ttyACM...'.
SERIAL_PORT = 'COM3'  # !!! CHANGE THIS TO YOUR MICRO:BIT'S PORT !!!
BAUD_RATE = 115200

# --- Functions to Get Temperatures ---

def get_cpu_temperature():
    """Gets the CPU temperature."""
    try:
        # psutil.sensors_temperatures() can provide CPU temps on some systems (mainly Linux)
        temps = psutil.sensors_temperatures()
        if 'coretemp' in temps:
            return int(temps['coretemp'][0].current)
        # Fallback for other systems or if coretemp is not available
        if hasattr(psutil, "sensors_temperatures"):
             temps = psutil.sensors_temperatures()
             if temps:
                 for name, entries in temps.items():
                     for entry in entries:
                         return int(entry.current)
    except Exception as e:
        print(f"Could not get CPU temperature with psutil: {e}")

    # For Windows, a more reliable method using WMI
    try:
        w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
        temperature_infos = w.Sensor()
        for sensor in temperature_infos:
            if sensor.SensorType == 'Temperature' and 'cpu' in sensor.Name.lower():
                return int(sensor.Value)
    except Exception as e:
        print(f"Could not get CPU temperature with WMI. Is OpenHardwareMonitor running? Error: {e}")

    return None

def get_gpu_temperature():
    """Gets the GPU temperature (primarily for Windows using WMI)."""
    try:
        w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
        temperature_infos = w.Sensor()
        for sensor in temperature_infos:
            if sensor.SensorType == 'Temperature' and 'gpu' in sensor.Name.lower():
                return int(sensor.Value)
    except Exception as e:
        print(f"Could not get GPU temperature with WMI. Is OpenHardwareMonitor running? Error: {e}")
    return None

# --- Main Program ---

if __name__ == "__main__":
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")
    except serial.SerialException as e:
        print(f"Error: Could not open serial port {SERIAL_PORT}. Please check the port name and ensure the micro:bit is connected.")
        exit()

    while True:
        cpu_temp = get_cpu_temperature()
        gpu_temp = get_gpu_temperature()

        if cpu_temp is not None:
            message = f"C={cpu_temp}\n"
            ser.write(message.encode('utf-8'))
            print(f"Sent: {message.strip()}")

        if gpu_temp is not None:
            message = f"G={gpu_temp}\n"
            ser.write(message.encode('utf-8'))
            print(f"Sent: {message.strip()}")

        time.sleep(5)  # Send data every 5 seconds