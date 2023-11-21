class Reserva:
    #Se complementará con más campos después de definir la clase habitación
    def __init__(self, nombre, apellido, fecha_ingreso, fecha_salida, habitaciones, estado):
        self.nombre = nombre
        self.apellido = apellido
        self.fecha_ingreso = fecha_ingreso
        self.fecha_salida = fecha_salida
        self.habitaciones = habitaciones
        self.estado = estado

    def toDBCollection(self):
        return {
            'nombre': self.nombre,
            'apellido': self.apellido,
            'fecha_ingreso': self.fecha_ingreso,
            'fecha_salida': self.fecha_salida,
            'habitaciones': self.habitaciones,
            'estado': self.estado
        }
    
    def calcular_total(self):
        # Agrega la lógica para calcular el total a pagar
        pass
