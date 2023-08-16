import subprocess

def check_windows_update_status():
    try:
        result = subprocess.run(["powershell", "Get-Service -Name wuauserv"], capture_output=True, text=True, shell=True)
        output = result.stdout.lower()
        
        if "running" in output:
            print("WINDOWS UPDATE esta activo")
            return True
        else:
            print("WINDOWS UPDATE no esta activo")
            return False
    except Exception as e:
        return f"Error: {e}"

def check_real_time_protection():
    try:
        result = subprocess.run(["powershell", "Get-MpPreference | Select-Object -ExpandProperty DisableRealtimeMonitoring"], capture_output=True, text=True, shell=True)
        output = result.stdout.strip()
        if output == "False":
            print("PROTECCION EN TIEMPO REAL esta activo")
            return True
        else:
            print("PROTECCION EN TIEMPO REAL no esta activo")
            return False
    except Exception as e:
        return f"Error: {e}"

def stop_windows_update_service():
    estado_de_windows_update = check_windows_update_status()
    if estado_de_windows_update :
        print("WINDOWS UPDATE esta siendo detenido...")
        try:
            result = subprocess.run(["net", "stop", "wuauserv"], capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                print("WINDOWS UPDATE ha sido detenido")
                return True
            else:
                print("WINDWOS UPDATE no pudo ser detenido")
                return False
        except Exception as e:
            return f"Error: {e}"
    
def stop_real_time_protection():
    estado_de_proteccion_en_tiempo_real = check_real_time_protection()
    if estado_de_proteccion_en_tiempo_real:
        print("PROTECCION EN TIEMPO REAL esta siendo detenido...")
        try:
            result = subprocess.run(["powershell", "Set-MpPreference -DisableRealtimeMonitoring $true"], capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                print("PROTECCION EN TIEMPO REAL ha sido detenido")
                return True
            else:
                print("PROTECCION EN TIEMPO REAL no pudo ser detenido")
                return False
        except Exception as e:
            return f"Error: {e}"
        
def stop_both():
    stop_windows_update_service()
    stop_real_time_protection()

"""
activarlos
"""
def start_windows_update():
    estado_de_windows_update = check_windows_update_status()
    if estado_de_windows_update :
        print("WINDOWS UPDATE esta activo")
    else:
        try:
            result = subprocess.run(["powershell", "Start-Service -Name wuauserv"], capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                print("WINDOWS UPDATE ha sido activado")
                return True
            else:
                print("WINDWOS UPDATE no pudo activarse")
                return False
        except Exception as e:
            return f"Error: {e}"

def start_real_time_protection():
    estado_de_proteccion_en_tiempo_real = check_real_time_protection()
    if estado_de_proteccion_en_tiempo_real:
        print("PROTECCION EN TIEMPO REAL esta activo")
    else:
        try:
            result = subprocess.run(["powershell", "Set-MpPreference -DisableRealtimeMonitoring $false"], capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                print("PROTECCION EN TIEMPO REAL ha sido activado")
                return True
            else:
                print("PROTECCION EN TIEMPO REAL no pudo ser activarse")
                return False
        except Exception as e:
            return f"Error: {e}"
"""
intervalos
"""

import time
import threading
import keyboard

def check(action):
    exit_signal = threading.Event()

    def check_for_exit():
        while not exit_signal.is_set():
            if keyboard.is_pressed("Esc"):
                exit_signal.set()

    exit_thread = threading.Thread(target=check_for_exit)
    exit_thread.start()

    while not exit_signal.is_set():
        action()
        # si se usar mas de 1 segundo, 
        # al momento de hacer el bucle, se detiene
        # y hay que presionar entrer para que continue
        # es mejor dejarlo 1 o memos
        time.sleep(1)
    
    exit_thread.join()


"""
menu
"""
while True:
    print("****************************")
    print("SERVICIOS DE WINDOWS")
    print("****************************")
    print("1. Detener Windows Update y Proteccion en Tiempo Real")
    print("2. Detener Windows Update")
    print("3. Detener Proteccion en Tiempo Real")
    print("4. Activar Windows Update")
    print("5. Activar Proteccion en Tiempo Real")
    print("6. Salir")
    print("(Recodar que para salir de los bucles hay que presionar la tecla ESC)")
    opcion = input("Elige una opción: ")
    match opcion:
        case "1":
            check(stop_both)
        case "2":
            check(stop_windows_update_service)
        case "3":
            check(stop_real_time_protection)
        case "4":
            start_windows_update()
        case "5":
            start_real_time_protection()
        case "6":
            print("Saliendo...")
            break
        case _:
            print("Opción no válida. Por favor, elige una opción válida.")