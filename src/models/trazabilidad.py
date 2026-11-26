from datetime import datetime

class EventoTrazabilidad:
    """Registro de auditoría inmutable: una vez creado, sus atributos no pueden alterarse."""

    def __init__(self, accion: str, id_miembro: str = "SISTEMA"):
        if not accion or not accion.strip():
            raise ValueError("La descripción de la acción de trazabilidad no puede estar vacía.")

        object.__setattr__(self, "_timestamp", datetime.now())
        object.__setattr__(self, "_accion", accion.strip())
        object.__setattr__(self, "_id_miembro", id_miembro)

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    @property
    def accion(self) -> str:
        return self._accion

    @property
    def id_miembro(self) -> str:
        return self._id_miembro
    
    @property
    def id_investigador(self) -> str:
        return self._id_miembro
    
    def __setattr__(self, name, value):
        raise AttributeError("EventoTrazabilidad es inmutable y no permite modificar sus atributos.")

    def __str__(self) -> str:
        fecha_str = self._timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return f"[{fecha_str}] (Usuario: {self._id_miembro}) -> {self._accion}"