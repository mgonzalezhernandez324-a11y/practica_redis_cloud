# Interfaz de texto simple para usar en consola.
# Presenta un menú interactivo que llama a las funciones
# de `almacen_usuario` usando `obtener_conexion()`.


import json
from typing import Any
from dotenv import load_dotenv
from cliente_redis import obtener_conexion
from almacen_usuarios import (
        crear_usuario_json,
        leer_usuario_json,
        actualizar_usuario_json,
        eliminar_usuario,
        listar_usuarios,
    )
# Cargar variables de entorno desde .env para asegurar REDIS_URL
load_dotenv()


def imprimir(obj: Any) -> None:
    # Imprime en consola `obj` formateado como JSON legible.

    # Usa `ensure_ascii=False` para mantener caracteres UTF-8 y sangría.

    print(json.dumps(obj, ensure_ascii=False, indent=2))



def prompt_json(prompt: str) -> str:
    # Solicita al usuario una cadena JSON desde `input` y la valida.

    # Lanza `ValueError` si la entrada está vacía o si no es JSON válido.
    # Retorna la cadena JSON original si es válida.

    texto = input(prompt).strip()
    if not texto:
        raise ValueError("Entrada JSON vacía")
    # validar JSON
    json.loads(texto)
    return texto



def menu() -> None:
    # Menú interactivo en consola para gestionar usuarios en Redis.

    # Realiza un bucle mostrando opciones y llama a las funciones de



    # `almacen_usuarios` usando una conexión obtenida con `obtener_conexion()`.

    try:
        conexion = obtener_conexion()
    except Exception as e:
        print(f"ERROR: no se pudo conectar a Redis: {e}")
        return
    while True:
        print("\n--- Menú usuarios Redis ---")
        print("1) Crear usuario (introduce JSON)")
        print("2) Leer usuario (id)")
        print("3) Actualizar usuario (id + JSON)")
        print("4) Eliminar usuario (id)")
        print("5) Listar usuarios")
        print("6) Salir")

        opcion = input("Selecciona opción: ").strip()
        try:
            if opcion in ("1", "crear"):
                try:
                    datos = prompt_json("JSON usuario: ")
                except Exception as e:
                    print(f"JSON inválido: {e}")
                    continue
                creado = crear_usuario_json(conexion, datos)
                imprimir({"creado": bool(creado)})

            elif opcion in ("2", "leer"):
                idu = input("id_usuario: ").strip()
                usuario = leer_usuario_json(conexion, idu)
                imprimir({"usuario": usuario})

            elif opcion in ("3", "actualizar"):
                idu = input("id_usuario: ").strip()
                try:
                    datos = prompt_json("JSON actualización: ")
                except Exception as e:
                    print(f"JSON inválido: {e}")
                    continue
                modo = input("modo (mezclar/reemplazar) [mezclar]: ").strip() or
"mezclar"
                actualizado = actualizar_usuario_json(conexion, idu, datos, modo=modo)
                imprimir({"actualizado": bool(actualizado)})
            elif opcion in ("4", "eliminar"):
                idu = input("id_usuario: ").strip()
                eliminado = eliminar_usuario(conexion, idu)



                imprimir({"eliminado": bool(eliminado)})

            elif opcion in ("5", "listar"):
                usuarios = listar_usuarios(conexion)
                imprimir({"total": len(usuarios), "usuarios": usuarios})

            elif opcion in ("6", "salir", "exit"):
                print("Adiós")
                break

            else:
                print("Opción no reconocida")

        except Exception as e:
            print(f"ERROR: {e}")   



def main() -> int:
    # Punto de entrada para la interfaz de texto.

    # Ejecuta `menu()` y gestiona `KeyboardInterrupt` devolviendo códigos
    # de salida apropiados (0 éxito, 1 interrumpido).

    try:
        menu()
        return 0
    except KeyboardInterrupt:
        print("\nInterrumpido")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())