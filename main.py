import sys
from juegos import Snake
from jugadores import Random, IA

JUGADORES_PERMITIDOS = {"ia": IA, "random": Random}

def print_help():
    print("Como correr el script: \n")
    print("\t python main.py random si ./train.json")

if __name__ == "__main__":
    try:
        tipo_jugador = sys.argv[1].lower()
        entrenar     = sys.argv[2].lower()
        file_path    = sys.argv[3]
    
    except Exception:
        print("Error, parametros pasados de manera incorrecta")
        print_help()
    
    juego = Snake(16)
    if tipo_jugador in JUGADORES_PERMITIDOS:
        jugador = JUGADORES_PERMITIDOS[tipo_jugador](juego)
    else:
        raise Exception("Nombre de jugador no conocido")
    


    # Entrenar puede ser 'si' o 'no', en caso de que sea 'si' se entrena el agente (siempre y cuando sea IA),
    # en caso de que sea 'no', se ve al agente jugar el juego seleccionado.
    if tipo_jugador == "ia":
        jugador.set_path(file_path)
        if entrenar in {"si", "true"}:
            jugador.entrenar()
            jugador.save()
        else:
            jugador.load()
        
    jugador.jugar()

    

    