import json
import re
from typing import Opcional, List, Dict, Any
from redis import Redis


PREFIJO_USUARIO = "usuario:"


def validar_id_usuario(id_usuario: str) -> None:
    # verifica que 'id_usuario' cumpla el patron permitido.
    
    # lanza 'valueError' si el identificador no coincide con.
    # el patron de 3-40 caracteres alfanumericos, guion bajo o guion.

    if not re.fullmatch(r"[A-Za-z0-9_-]{3,40}", id_usuario):
        raise valueError("id_usuario invalido. Usa 3-40 caracteres alfanumericos, _
_")


def construir_clave_usuario(id_usuario: str) -> str:
    # construye y devuelve la clave Redis para un 'id_usuario'.

    # ejemplo: si el prefijo es 'usuario:' y 'id_usuario' es 'juan',
    # devuelve 'usuario:juan'.

    return f"{PREFIJO_USUARIO}{id_usuario}"

def normalizar_id_usuario(datos: Dict[str, Any]) -> str:
    # extrae y valida el 'id_usuario' a partir de un diccionario.

    # busca las claves 'id_usuario' o 'id', las normaliza a cadena,
    # comprueba su validez con 'validar_id_usuario' y la retorna.
    # lanza 'valueError' si no existe o no es valida


id_usuario = datos.get("id_usuario", datos.get("id"))
if id_usuario is None:
    raise valueError("El JSON debe incluir 'id_usuario' o 'id'.")
id_usuario = str(id_usuario).strip()
validar_id_usuario(id_usuario)
return id_usuario


def crear_usuario_json(conexion: Redis, usuario_json: str) -> bool:
    # crea un nuevo usuario almacenado en Redis a partir de 'usuario_json'.

    # - 'conexion': instancia de 'Redis'.
    # - 'usuario_json': cadena JSON que representa un objeto usuario.

    # devuelve 'True' si la clave fue creada (no existia), 'False' en caso contrario
    # lanza 'ValueError' si el JSON no representa un objeto.

    datos = json.loads(usuario_json)
    if not isinstance(datos, dict):
        raise ValueError("El JSON debe ser un objeto.")
    
    id_usuario = normalizar_id_usuario(datos)
    datos["id_usuario"] = id_usuario

    clave = construir_clave_usuario(id_usuario)
    valor = json.dumps(datos, ensure_ascii=False)

    creado = conexion.set(clave, valor, nx=True)
    return bool(creado)

def leer_usuario_json(conexion: Redis, id_usuario: str) -> Opcional[Dict[str, Any]]:
    # lee y devuelve el objeto usuario almacenado en Redis.

    # Retorna un diccionario con los datos del usuario o 'None' si no existe.
    # valida 'id_usuario' antes de leer.

    id_usuario = str(id_usuario).strip()
    validar_id_usuario(id_usuario)

    valor = conexion.get(construir_clave_usuario(id_usuario))
    if valor is None:
        return None

    datos = json.loads(valor)
    if isinstance(datos, dict)and "id_usuario" not in datos:
        datos["id_usuario"] = id_usuario
    return datos

def actualizar_usuario_json(
    conexion: Redis,
    id_usuario: str,
    json_actualizacion: str,
    modo: str = "mezclar"
) -> bool:
    # actualiza un usuario existente en Redis.

    # - 'json_actualizacion' debe ser un objeto JSON.
    # - 'modo' puede ser 'mezclar' (por defecto) para fusuonar campos,
    #  o 'reemplazar' para sustituir todo el objeto.

    # devuelve 'True' si la actualizacion tuvo exito, 'False' si no existe.

    actual = leer_usuario_json(conexion, id_usuario)
    if actual is None:
        return False
    
    nuevos_datos = json.loads(json_actualizacion)
    if not isinstance(nuevos_datos, dict):
       raise ValueError("El JSON de actualización debe ser un objeto.") 

    if modo == "reemplazar":
        resultado = nuevos_datos
    elif modo == "mezclar":
        resultado = dict(actual)
        resultado.update(nuevos_datos)
    else:
        raise ValueError("Modo inválido. Usa 'mezclar' o 'reemplazar'.")

    resultado["id_usuario"] = id_usuario 

    conexion.set(
        construir_clave_usuario(id_usuario),
        json.dumps(resultado, ensure_ascii=False)
    )
    return True 


def eliminar_usuario(conexion: Redis, id_usuario: str) -> bool:
    # Elimina el usuario identificado por `id_usuario` de Redis.

    # Devuelve `True` si la eliminación afectó a una clave, `False` en caso contrario.

    eliminado = conexion.delete(construir_clave_usuario(id_usuario))
    return eliminado == 1



def listar_usuarios(conexion: Redis) -> List[Dict[str, Any]]:
    # Devuelve la lista de todos los usuarios almacenados en Redis. 

    # Actualmente obtiene las claves con el patrón global y para cada
    # clave intenta leer el JSON de usuario. Retorna una lista de diccionarios.

    ids = sorted(conexion.keys("*"))
    resultado = []
    for id_usuario in ids:
        datos = leer_usuario_json(conexion, id_usuario.replace(PREFIJO_USUARIO, ""))
        if datos:
            resultado.append(datos)
    return resultado
    

