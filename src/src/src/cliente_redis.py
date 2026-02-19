import os 
from dataclasses import dataclass
from redis import Redis
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class ConfiguracionRedis:
    url: str


def obtener_configuracion() -> ConfiguracionRedis:
    # lee la configuracion de Redis dese las variables de entorno.

    # Retorna una instancia inmutable de 'configuracionRedis' con la URL.
    # Usa 'REDIS_URL' o el valor por defecto 'redis://localhost:6379/0'.

    url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    return ConfiguracionRedis(url=url)

def obtener_conexion()-> Redis:
    # crea y devuelve una conexion 'Redis' usando la configuracion.

    # Realiza un 'ping()' para verificar la conexion antes de retornarla.
    # Llanza exepciones de 'redis' si no se puede conectar.

    config = obtener_configuracion()
    conexion = Redis.from_url(config.url, decode_responses=True)
    conexion.ping()
    return conexion
    
