class Carepichas:
    def __init__(self, nombre, edad, playada):
        self.nombre = nombre
        self.edad = edad
        self.playada = playada

    def descripcion(self):
            print(f"Nombre: {self.nombre}, Edad: {self.edad}, Playada: {self.playada}")

            
Amigos = Carepichas('GABRIEL','19','MERALOCA')
Amigos1= Carepichas('DEIBY','19','LA MAS DIVA')
Amigos2 = Carepichas('KENNEH','21','UN PAPIS')

Amigos.descripcion()
Amigos1.descripcion()
Amigos2.descripcion()