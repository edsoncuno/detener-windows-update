import subprocess


def check_windows_update_status():
    try:
        result = subprocess.run(
            ["powershell", "Get-Service -Name wuauserv"],
            capture_output=True,
            text=True,
            shell=True,
        )
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
        result = subprocess.run(
            [
                "powershell",
                "Get-MpPreference | Select-Object -ExpandProperty DisableRealtimeMonitoring",
            ],
            capture_output=True,
            text=True,
            shell=True,
        )
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
    if estado_de_windows_update:
        print("WINDOWS UPDATE esta siendo detenido...")
        try:
            result = subprocess.run(
                ["net", "stop", "wuauserv"], capture_output=True, text=True, shell=True
            )
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
            result = subprocess.run(
                ["powershell", "Set-MpPreference -DisableRealtimeMonitoring $true"],
                capture_output=True,
                text=True,
                shell=True,
            )
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
    if estado_de_windows_update:
        print("WINDOWS UPDATE esta activo")
    else:
        try:
            result = subprocess.run(
                ["powershell", "Start-Service -Name wuauserv"],
                capture_output=True,
                text=True,
                shell=True,
            )
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
            result = subprocess.run(
                ["powershell", "Set-MpPreference -DisableRealtimeMonitoring $false"],
                capture_output=True,
                text=True,
                shell=True,
            )
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
import msvcrt


def check(action):
    while True:
        action()
        print("Presiona 'q' para para detener...")
        time.sleep(1)
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key == b"q":
                break


"""
estados actual
"""


def mostrar_estados():
    estado_de_windows_update = check_windows_update_status()
    estado_de_proteccion_en_tiempo_real = check_real_time_protection()

"""
menu
"""
while True:
    print("****************************")
    print("SERVICIOS DE WINDOWS")
    print("****************************")
    print("1. Mostrar Estado Actual de Windows Update y Proteccion en Tiempo Real")
    print("2. Detener Windows Update y Proteccion en Tiempo Real")
    print("3. Detener Windows Update")
    print("4. Detener Proteccion en Tiempo Real")
    print("5. Activar Windows Update")
    print("6. Activar Proteccion en Tiempo Real")
    print("7. Salir")
    opcion = input("Elige una opción: ")
    match opcion:
        case "1":
            mostrar_estados()
        case "2":
            check(stop_both)
        case "3":
            check(stop_windows_update_service)
        case "4":
            check(stop_real_time_protection)
        case "5":
            start_windows_update()
        case "6":
            start_real_time_protection()
        case "7":
            print("Saliendo...")
            break
        case _:
            print("Opción no válida. Por favor, elige una opción válida.")
