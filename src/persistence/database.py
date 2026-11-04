import sqlite3
import os

class GestorBaseDatos:
    def __init__(self, ruta_db="labtrack.db"):
        """Inicializa la conexión y crea las tablas si no existen."""
        self.conexion = sqlite3.connect(ruta_db)
        self.crear_tablas()

    def crear_tablas(self):
        cursor = self.conexion.cursor()
        
        # TABLA 1: Personal (Maneja el polimorfismo guardando el 'tipo')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS personal (
                id_miembro TEXT PRIMARY KEY,
                tipo TEXT,
                nombre TEXT,
                especialidad TEXT,
                atributo_extra TEXT
            )
        ''')
        
        # TABLA 2: Experimentos (Conectada al personal mediante Foreign Key)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS experimentos (
                id_experimento TEXT PRIMARY KEY,
                nombre TEXT,
                version TEXT,
                estado TEXT,
                id_miembro_responsable TEXT,
                FOREIGN KEY(id_miembro_responsable) REFERENCES personal(id_miembro)
            )
        ''')
        
        # TABLA 3: Trazabilidad (El corazón del proyecto)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trazabilidad (
                id_evento INTEGER PRIMARY KEY AUTOINCREMENT,
                id_experimento TEXT,
                id_miembro TEXT,
                accion TEXT,
                FOREIGN KEY(id_experimento) REFERENCES experimentos(id_experimento),
                FOREIGN KEY(id_miembro) REFERENCES personal(id_miembro)
            )
        ''')
        self.conexion.commit()

    def guardar_personal(self, miembro):
        """Traduce un objeto Investigador o Tecnico a SQLite."""
        cursor = self.conexion.cursor()
        
        # Detectamos de qué clase hija es para el polimorfismo
        tipo = miembro.__class__.__name__ 
        # Sacamos el atributo específico ('rol' si es investigador, 'turno' si es técnico)
        extra = getattr(miembro, 'rol', getattr(miembro, 'turno', ''))
        
        # Usamos INSERT OR REPLACE para que sirva tanto para crear como para actualizar
        cursor.execute('''
            INSERT OR REPLACE INTO personal (id_miembro, tipo, nombre, especialidad, atributo_extra)
            VALUES (?, ?, ?, ?, ?)
        ''', (miembro.id_miembro, tipo, miembro.nombre, miembro.especialidad, extra))
        self.conexion.commit()

    def guardar_experimento(self, experimento):
        """Guarda un experimento, su responsable y sus eventos de trazabilidad en cascada."""
        cursor = self.conexion.cursor()
        
        # 1. Guardamos primero al responsable para no violar la Foreign Key
        self.guardar_personal(experimento.investigador_principal)
        
        # 2. Guardamos el experimento en sí
        cursor.execute('''
            INSERT OR REPLACE INTO experimentos (id_experimento, nombre, version, estado, id_miembro_responsable)
            VALUES (?, ?, ?, ?, ?)
        ''', (experimento.id_experimento, experimento.nombre, experimento.version, experimento.estado, experimento.investigador_principal.id_miembro))
        
        # 3. Guardamos los eventos de trazabilidad nuevos
        # Borramos los anteriores de este experimento para evitar duplicados al actualizar
        cursor.execute('DELETE FROM trazabilidad WHERE id_experimento = ?', (experimento.id_experimento,))
        
        for evento in experimento.historial_eventos:
            cursor.execute('''
                INSERT INTO trazabilidad (id_experimento, id_miembro, accion)
                VALUES (?, ?, ?)
            ''', (experimento.id_experimento, evento.id_investigador, evento.accion)) # Usa id_miembro si lo cambiaste en EventoTrazabilidad
            
        self.conexion.commit()