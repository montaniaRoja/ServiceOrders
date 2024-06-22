import sqlite3


class OrdenesDeServicio:
    def __init__(self, db_name='ordenes_servicio.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS ordenes_servicio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_orden TEXT,
            cliente TEXT,
            equipo TEXT,
            problema TEXT,
            trabajo TEXT,
            tecnico TEXT,
            estado TEXT,
            fecha_estimada_fin TEXT,
            costo REAL,
            notas TEXT
        )
        '''
        self.conn.execute(query)
        self.conn.commit()

    def agregar_orden(self, fecha_orden, cliente, equipo, problema, trabajo, tecnico, estado, fecha_estimada_fin, costo,
                      notas):
        query = '''
        INSERT INTO ordenes_servicio (fecha_orden, cliente, equipo, problema, trabajo, tecnico, estado, fecha_estimada_fin, costo, notas)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        self.conn.execute(query, (
        fecha_orden, cliente, equipo, problema, trabajo, tecnico, estado, fecha_estimada_fin, costo, notas))
        self.conn.commit()

    def obtener_ordenes(self):
        query = 'SELECT * FROM ordenes_servicio'
        cursor = self.conn.execute(query)
        return cursor.fetchall()

    def obtener_orden_por_id(self, orden_id):
        query = 'SELECT * FROM ordenes_servicio WHERE id = ?'
        cursor = self.conn.execute(query, (orden_id,))
        return cursor.fetchone()

    def actualizar_estado(self, orden_id, nuevo_estado):
        query = 'UPDATE ordenes_servicio SET estado = ? WHERE id = ?'
        self.conn.execute(query, (nuevo_estado, orden_id))
        self.conn.commit()
