import sqlite3


class ConexionBaseDatos:
    """Gestiona exclusivamente la conexión a SQLite y la definición del esquema."""

    def __init__(self, db_path: str = "labtrack.db"):
        self.db_path = db_path
        self.conexion = sqlite3.connect(self.db_path)
        self.conexion.execute("PRAGMA foreign_keys = ON;")
        self._inicializar_esquema()

    def _inicializar_esquema(self):
        cursor = self.conexion.cursor()
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS personal (
                id_miembro TEXT PRIMARY KEY,
                tipo TEXT NOT NULL,
                nombre TEXT NOT NULL,
                especialidad TEXT NOT NULL,
                atributo_extra TEXT
            );

            CREATE TABLE IF NOT EXISTS experimentos (
                id_experimento TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                version TEXT NOT NULL,
                estado TEXT NOT NULL,
                id_miembro_responsable TEXT NOT NULL,
                FOREIGN KEY (id_miembro_responsable) REFERENCES personal(id_miembro)
            );

            CREATE TABLE IF NOT EXISTS trazabilidad (
                id_evento INTEGER PRIMARY KEY AUTOINCREMENT,
                id_experimento TEXT NOT NULL,
                id_miembro TEXT NOT NULL,
                accion TEXT NOT NULL,
                FOREIGN KEY (id_experimento) REFERENCES experimentos(id_experimento)
            );
        """)
        self.conexion.commit()

    def cerrar(self):
        if self.conexion:
            self.conexion.close()
