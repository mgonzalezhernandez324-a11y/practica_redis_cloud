import pytest
from src.cliente_redis import obtener_conexion
from src.almacen_usuarios import (
    crear_usuario_json,
    leer_usuario_json,
    actualizar_usuario_json,
    eliminar_usuario,
    listar_usuarios
)



@pytest.fixture(scope="function")
def conexion():
    r = obtener_conexion()
    return r

def test_crear_usuario(conexion):
    datos = '{"id_usuario":"u001","nombre":"Ana","rol":"alumno"}'
    assert crear_usuario_json(conexion, datos) is True
    usuario = leer_usuario_json(conexion, "u001")
    assert usuario["nombre"] == "Ana"

def test_no_crear_usuario_duplicado(conexion):
    datos = '{"id_usuario":"u002","nombre":"Luis"}'
    crear_usuario_json(conexion, datos)
    assert crear_usuario_json(conexion, datos) is False

def test_actualizar_usuario(conexion):
    crear_usuario_json(conexion, '{"id_usuario":"u003","nombre":"Carla"}')
    actualizar_usuario_json(conexion, "u003", '{"rol":"docente"}')
    usuario = leer_usuario_json(conexion, "u003")
    assert usuario["rol"] == "docente"

def test_eliminar_usuario(conexion):
    crear_usuario_json(conexion, '{"id_usuario":"u004","nombre":"Mario"}')
    assert eliminar_usuario(conexion, "u004") is True
    assert leer_usuario_json(conexion, "u004") is None

def test_listar_usuarios(conexion):
    crear_usuario_json(conexion, '{"id_usuario":"u005","nombre":"A"}')
    crear_usuario_json(conexion, '{"id_usuario":"u006","nomb


    usuarios = listar_usuarios(conexion)
    assert len(usuarios) == 5