"""
Este módulo contiene la configuración y la función para la conexión a la base de datos PostgreSQL.
"""

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# URI de conexión a PostgreSQL
DATABASE_URI = "postgresql://usuariosgamers_user:ogeJ1nFI1aAu3iv6cOrDEcFoNbkziUeV@dpg-cvusba3e5dus73e0idp0-a/usuariosgamers"

def connectionBD():
    """
    Establece una conexión con la base de datos.

    Returns:
        engine (sqlalchemy.engine.base.Engine): El motor de conexión a la base de datos si es exitoso.
        None: Si ocurre un error en la conexión.
    """
    try:
        engine = create_engine(DATABASE_URI)
        # Probar conexión
        with engine.connect() as connection:
            print("Conexión exitosa a la base de datos")
        return engine
    except SQLAlchemyError as err:
        print(f"Error en la conexión a la base de datos: {err}")
        return None

if __name__ == "__main__":
    connectionBD()
