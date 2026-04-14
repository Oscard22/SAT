import os
import sys
import random
import msvcrt
import time
from colorama import init, Fore, Back, Style

# Inicializar colorama para colores en terminal
init(autoreset=True)

# Definir color gris claro personalizado (código 8 en la paleta de Windows)
GRIS_CLARO = '\033[48;5;117m'  # Fondo gris claro (código 7 en la paleta de 256 colores)
RESET = Style.RESET_ALL

class JuegoLaberinto:
    def __init__(self):
        # Configuración del laberinto (ligeramente modificado para más espacio)
        self.laberinto = [
            "████████████████████",
            "█P                █",
            "█ █ ███ ██████ ██ █",
            "█ █      █     █  █",
            "█ ███████ ███ █  ██",
            "█      █  █ █ █   █",
            "██████ ███  █ █  ██",
            "█             █   █",
            "█ █ ███ ███████ █ █",
            "█ █   █      █  █ █",
            "█ █████ ███ ███ █ █",
            "█           █  █  █",
            "█████ █████████ ███",
            "█                 █",
            "█ ████████████ ██ █",
            "█ █     ██     █  █",
            "█ ██ █████ ███ ██ █",
            "█    █         █  █",
            "████ ███S██████████",
            "████████████████████"
        ]
        
        # MÁS PREGUNTAS - 10 preguntas variadas
        self.preguntas = [
            # Pregunta 1
            {
                "pregunta": "¿Cuál es la capital de Francia?",
                "opciones": ["a) Londres", "b) París", "c) Madrid", "d) Berlín"],
                "correcta": "b",
                "tipo": "opcion_multiple",
                "pista": "Ciudad del amor y la Torre Eiffel"
            },
            # Pregunta 2
            {
                "pregunta": "¿Cuánto es 7 + 3?",
                "respuesta": "10",
                "tipo": "numerica",
                "pista": "Es un número de dos dígitos"
            },
            # Pregunta 3
            {
                "pregunta": "Resuelve: Si tienes 5 manzanas y comes 2, ¿cuántas te quedan?",
                "respuesta": "3",
                "tipo": "numerica",
                "pista": "Resta simple"
            },
            # Pregunta 4
            {
                "pregunta": "¿Qué color obtienes al mezclar azul y amarillo?",
                "opciones": ["a) Rojo", "b) Verde", "c) Morado", "d) Naranja"],
                "correcta": "b",
                "tipo": "opcion_multiple",
                "pista": "Color de la naturaleza y la esperanza"
            },
            # Pregunta 5
            {
                "pregunta": "¿Cuál es el planeta más cercano al Sol?",
                "opciones": ["a) Venus", "b) Marte", "c) Mercurio", "d) Tierra"],
                "correcta": "c",
                "tipo": "opcion_multiple",
                "pista": "Es el más pequeño y el más rápido"
            },
            # Pregunta 6
            {
                "pregunta": "¿Cuántos lados tiene un triángulo?",
                "respuesta": "3",
                "tipo": "numerica",
                "pista": "El prefijo 'tri' significa tres"
            },
            # Pregunta 7
            {
                "pregunta": "¿En qué año llegó el hombre a la Luna?",
                "opciones": ["a) 1965", "b) 1969", "c) 1972", "d) 1958"],
                "correcta": "b",
                "tipo": "opcion_multiple",
                "pista": "Finales de los 60s, misión Apollo 11"
            },
            # Pregunta 8
            {
                "pregunta": "¿Cuál es el resultado de 12 ÷ 4?",
                "respuesta": "3",
                "tipo": "numerica",
                "pista": "Es la cuarta parte de 12"
            },
            # Pregunta 9
            {
                "pregunta": "¿Qué animal es conocido como el 'rey de la selva'?",
                "opciones": ["a) Elefante", "b) Tigre", "c) León", "d) Jirafa"],
                "correcta": "c",
                "tipo": "opcion_multiple",
                "pista": "Tiene melena (el macho)"
            },
            # Pregunta 10
            {
                "pregunta": "¿Cuál es la capital de España?",
                "opciones": ["a) Barcelona", "b) Madrid", "c) Sevilla", "d) Valencia"],
                "correcta": "b",
                "tipo": "opcion_multiple",
                "pista": "Está en el centro del país"
            }
        ]
        
        # Posiciones para las preguntas (coordenadas x, y)
        self.posicion_preguntas = [
            (3, 2), (15, 4), (8, 7), (12, 9), (5, 12),
            (17, 14), (10, 16), (4, 18), (14, 15), (7, 10)
        ]
        
        self.preguntas_respondidas = set()
        
        # Posición inicial del jugador
        self.jugador_x = 1
        self.jugador_y = 1
        
        # Colores para el laberinto (ahora con fondo gris claro)
        self.colores = {
            '█': Back.BLACK + ' ' + RESET,
            'P': Back.GREEN + Fore.WHITE + 'P' + RESET,
            'S': Back.RED + Fore.WHITE + 'S' + RESET,
            ' ': GRIS_CLARO + ' ' + RESET,  # Fondo gris claro para caminos
            '?': Back.YELLOW + Fore.BLACK + '?' + RESET,
            '✓': Back.GREEN + Fore.BLACK + '✓' + RESET,
            '!': Back.CYAN + Fore.BLACK + '!' + RESET
        }
        
        # Historial para el replay
        self.historial_movimientos = []
        self.pasos = 0
        self.pregunta_actual = None
        self.modo_pregunta = False
        
    def limpiar_pantalla(self):
        """Limpia la pantalla de la terminal"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def dibujar_laberinto(self):
        """Dibuja el laberinto con colores"""
        print(Fore.CYAN + "=" * 70)
        print(Fore.YELLOW + "            🏃 LABERINTO MÁGICO - BÚSQUEDA DEL TESORO 🏃")
        print(Fore.CYAN + "=" * 70)
        
        # Leyenda de colores
        print(Fore.WHITE + "🧱 Pared  " + Back.GREEN + " P " + RESET + " Tú  " +
              Back.YELLOW + " ? " + RESET + " Pregunta  " +
              Back.GREEN + " ✓ " + RESET + " Respondida  " +
              Back.RED + " S " + RESET + " Salida  " +
              GRIS_CLARO + "   " + RESET + " Camino")
        print(Fore.CYAN + "-" * 70)
        
        for y, fila in enumerate(self.laberinto):
            linea_colorida = f"{y:2d} "  # Número de fila
            for x, caracter in enumerate(fila):
                if x == self.jugador_x and y == self.jugador_y:
                    linea_colorida += Back.GREEN + Fore.WHITE + 'P' + RESET
                elif (x, y) in self.preguntas_respondidas:
                    linea_colorida += Back.GREEN + Fore.BLACK + '✓' + RESET
                elif (x, y) in self.posicion_preguntas and (x, y) not in self.preguntas_respondidas:
                    # Animación para preguntas no respondidas
                    if random.choice([True, False]):
                        linea_colorida += Back.YELLOW + Fore.BLACK + '?' + RESET
                    else:
                        linea_colorida += Back.YELLOW + Fore.BLACK + '!' + RESET
                elif caracter == '█':
                    linea_colorida += Back.BLACK + ' ' + RESET
                elif caracter == 'S':
                    linea_colorida += Back.RED + Fore.WHITE + 'S' + RESET
                else:
                    linea_colorida += GRIS_CLARO + ' ' + RESET  # Fondo gris claro
            print(linea_colorida)
        
        print(Fore.CYAN + "=" * 70)
        print(Fore.WHITE + f"📊 Pasos: {self.pasos} | Posición: ({self.jugador_x}, {self.jugador_y})")
        print(Fore.YELLOW + "🎮 Controles: WASD para mover | E para responder pregunta | Q para salir")
        print(Fore.CYAN + "=" * 70)
    
    def mostrar_mensaje_pregunta(self, pregunta_idx):
        """Muestra un mensaje especial cuando estás frente a una pregunta"""
        self.limpiar_pantalla()
        print(Fore.MAGENTA + "╔" + "═" * 68 + "╗")
        print(Fore.MAGENTA + "║" + Fore.YELLOW + "                    📝 ¡HAS ENCONTRADO UNA PREGUNTA! 📝".center(68) + Fore.MAGENTA + "║")
        print(Fore.MAGENTA + "╠" + "═" * 68 + "╣")
        
        pregunta = self.preguntas[pregunta_idx]
        print(Fore.MAGENTA + "║" + Fore.CYAN + f" PREGUNTA: {pregunta['pregunta']}".ljust(68) + Fore.MAGENTA + "║")
        print(Fore.MAGENTA + "║" + Fore.YELLOW + f" 💡 PISTA: {pregunta['pista']}".ljust(68) + Fore.MAGENTA + "║")
        print(Fore.MAGENTA + "╠" + "═" * 68 + "╣")
        print(Fore.MAGENTA + "║" + Fore.GREEN + "                     ¡PRESIONA 'E' PARA RESPONDER!".center(68) + Fore.MAGENTA + "║")
        print(Fore.MAGENTA + "║" + Fore.WHITE + "             (O puedes moverte y volver más tarde)".center(68) + Fore.MAGENTA + "║")
        print(Fore.MAGENTA + "╚" + "═" * 68 + "╝")
        print(Fore.YELLOW + "\nPresiona cualquier tecla para continuar...")
        msvcrt.getch()
    
    def hacer_pregunta(self, pregunta_idx):
        """Realiza una pregunta al jugador"""
        pregunta = self.preguntas[pregunta_idx]
        
        while True:  # Permitir reintentos
            self.limpiar_pantalla()
            print(Fore.MAGENTA + "╔" + "═" * 68 + "╗")
            print(Fore.MAGENTA + "║" + Fore.YELLOW + "                       📝 RESPONDE LA PREGUNTA 📝".center(68) + Fore.MAGENTA + "║")
            print(Fore.MAGENTA + "╠" + "═" * 68 + "╣")
            
            # Mostrar pregunta con formato
            print(Fore.MAGENTA + "║" + Fore.CYAN + f" {pregunta['pregunta']}".ljust(68) + Fore.MAGENTA + "║")
            print(Fore.MAGENTA + "║" + Fore.YELLOW + f" 💡 Pista: {pregunta['pista']}".ljust(68) + Fore.MAGENTA + "║")
            print(Fore.MAGENTA + "╠" + "═" * 68 + "╣")
            
            if pregunta["tipo"] == "opcion_multiple":
                for opcion in pregunta["opciones"]:
                    print(Fore.MAGENTA + "║" + Fore.WHITE + f"   {opcion}".ljust(68) + Fore.MAGENTA + "║")
                print(Fore.MAGENTA + "╠" + "═" * 68 + "╣")
                print(Fore.MAGENTA + "║" + Fore.GREEN + "   Ingresa la letra de tu respuesta (a/b/c/d):".ljust(68) + Fore.MAGENTA + "║")
                print(Fore.MAGENTA + "╚" + "═" * 68 + "╝")
                
                respuesta = input(Fore.CYAN + "➤ ").lower().strip()
                
                if respuesta in ['a', 'b', 'c', 'd']:
                    if respuesta == pregunta["correcta"]:
                        print(Fore.GREEN + "\n✅ ¡CORRECTO! +10 puntos")
                        time.sleep(1.5)
                        return True
                    else:
                        print(Fore.RED + "\n❌ Incorrecto. ¡Intenta de nuevo!")
                        time.sleep(1.5)
                else:
                    print(Fore.RED + "\n❌ Por favor ingresa a, b, c o d")
                    time.sleep(1.5)
            else:
                print(Fore.MAGENTA + "║" + Fore.WHITE + "   Responde con el número:".ljust(68) + Fore.MAGENTA + "║")
                print(Fore.MAGENTA + "╚" + "═" * 68 + "╝")
                
                respuesta = input(Fore.CYAN + "➤ ").strip()
                
                if respuesta == pregunta["respuesta"]:
                    print(Fore.GREEN + "\n✅ ¡CORRECTO! +10 puntos")
                    time.sleep(1.5)
                    return True
                else:
                    print(Fore.RED + "\n❌ Incorrecto. ¡Intenta de nuevo!")
                    time.sleep(1.5)
    
    def verificar_pregunta_en_posicion(self):
        """Verifica si hay una pregunta en la posición actual"""
        for idx, (x, y) in enumerate(self.posicion_preguntas):
            if self.jugador_x == x and self.jugador_y == y:
                if (x, y) not in self.preguntas_respondidas:
                    self.mostrar_mensaje_pregunta(idx)
                    self.pregunta_actual = idx
                    return True
        self.pregunta_actual = None
        return False
    
    def responder_pregunta_actual(self):
        """Responde la pregunta en la posición actual"""
        if self.pregunta_actual is not None:
            pos = self.posicion_preguntas[self.pregunta_actual]
            if pos not in self.preguntas_respondidas:
                if self.hacer_pregunta(self.pregunta_actual):
                    self.preguntas_respondidas.add(pos)
                    print(Fore.GREEN + "🎉 ¡Pregunta respondida correctamente! Puedes seguir avanzando.")
                    time.sleep(1.5)
                    return True
            else:
                print(Fore.YELLOW + "⚠️ Ya respondiste esta pregunta.")
                time.sleep(1)
        else:
            print(Fore.RED + "❌ No hay ninguna pregunta aquí para responder.")
            time.sleep(1)
        return False
    
    def mover(self, dx, dy):
        """Intenta mover al jugador"""
        nueva_x = self.jugador_x + dx
        nueva_y = self.jugador_y + dy
        
        # Verificar límites
        if nueva_y < 0 or nueva_y >= len(self.laberinto):
            return False
        if nueva_x < 0 or nueva_x >= len(self.laberinto[0]):
            return False
        
        # Verificar si es pared
        if self.laberinto[nueva_y][nueva_x] == '█':
            print(Fore.RED + "¡Pared! No puedes pasar.")
            time.sleep(0.3)
            return False
        
        # Guardar movimiento en historial
        self.historial_movimientos.append((self.jugador_x, self.jugador_y))
        
        # Mover jugador
        self.jugador_x = nueva_x
        self.jugador_y = nueva_y
        self.pasos += 1
        
        # Verificar si hay pregunta en nueva posición
        self.verificar_pregunta_en_posicion()
        return True
    
    def verificar_victoria(self):
        """Verifica si el jugador llegó a la salida"""
        return self.laberinto[self.jugador_y][self.jugador_x] == 'S'
    
    def jugar(self):
        """Bucle principal del juego"""
        self.limpiar_pantalla()
        
        # Pantalla de bienvenida
        print(Fore.GREEN + "╔" + "═" * 68 + "╗")
        print(Fore.GREEN + "║" + Fore.YELLOW + "             🎮 BIENVENIDO AL LABERINTO MÁGICO 🎮".center(68) + Fore.GREEN + "║")
        print(Fore.GREEN + "╠" + "═" * 68 + "╣")
        print(Fore.GREEN + "║" + Fore.CYAN + "   OBJETIVO:".ljust(68) + Fore.GREEN + "║")
        print(Fore.GREEN + "║" + Fore.WHITE + "   • Llega a la salida (S) para ganar".ljust(68) + Fore.GREEN + "║")
        print(Fore.GREEN + "║" + Fore.WHITE + "   • Encuentra las preguntas (?) en el camino".ljust(68) + Fore.GREEN + "║")
        print(Fore.GREEN + "║" + Fore.WHITE + "   • Presiona 'E' cuando estés sobre una '?'".ljust(68) + Fore.GREEN + "║")
        print(Fore.GREEN + "║" + Fore.WHITE + "   • Responde correctamente para poder avanzar".ljust(68) + Fore.GREEN + "║")
        print(Fore.GREEN + "║" + Fore.YELLOW + "   • Tienes 10 preguntas para responder".ljust(68) + Fore.GREEN + "║")
        print(Fore.GREEN + "╚" + "═" * 68 + "╝")
        
        input(Fore.YELLOW + "\nPresiona Enter para comenzar la aventura...")
        
        while True:
            self.limpiar_pantalla()
            self.dibujar_laberinto()
            
            # Verificar victoria
            if self.verificar_victoria():
                self.limpiar_pantalla()
                print(Fore.GREEN + "🎉" * 35)
                print(Fore.YELLOW + "       ¡FELICIDADES! HAS COMPLETADO EL LABERINTO")
                print(Fore.GREEN + "🎉" * 35)
                print(Fore.CYAN + f"\n📊 Estadísticas:")
                print(Fore.CYAN + f"   • Pasos totales: {self.pasos}")
                print(Fore.CYAN + f"   • Preguntas respondidas: {len(self.preguntas_respondidas)} de {len(self.preguntas)}")
                print(Fore.CYAN + f"   • Preguntas restantes: {len(self.preguntas) - len(self.preguntas_respondidas)}")
                
                # Calcular puntuación
                puntuacion = len(self.preguntas_respondidas) * 10
                print(Fore.YELLOW + f"\n   🏆 PUNTUACIÓN TOTAL: {puntuacion} puntos 🏆")
                
                self.menu_post_victoria()
                break
            
            # Obtener tecla
            if msvcrt.kbhit():
                tecla = msvcrt.getch().decode('utf-8').lower()
                
                if tecla == 'q':
                    print(Fore.YELLOW + "👋 ¡Gracias por jugar!")
                    break
                elif tecla == 'e':
                    self.responder_pregunta_actual()
                elif tecla == 'w':
                    self.mover(0, -1)
                elif tecla == 's':
                    self.mover(0, 1)
                elif tecla == 'a':
                    self.mover(-1, 0)
                elif tecla == 'd':
                    self.mover(1, 0)
    
    def menu_post_victoria(self):
        """Menú después de completar el laberinto"""
        while True:
            print(Fore.MAGENTA + "\n" + "╔" + "═" * 68 + "╗")
            print(Fore.MAGENTA + "║" + Fore.YELLOW + "                    🎮 OPCIONES DISPONIBLES 🎮".center(68) + Fore.MAGENTA + "║")
            print(Fore.MAGENTA + "╠" + "═" * 68 + "╣")
            print(Fore.MAGENTA + "║" + Fore.CYAN + "   1. 🔄 Jugar de nuevo (reiniciar todo)".ljust(68) + Fore.MAGENTA + "║")
            print(Fore.MAGENTA + "║" + Fore.CYAN + "   2. 📊 Ver estadísticas detalladas".ljust(68) + Fore.MAGENTA + "║")
            print(Fore.MAGENTA + "║" + Fore.CYAN + "   3. 🎬 Replay automático de tu recorrido".ljust(68) + Fore.MAGENTA + "║")
            print(Fore.MAGENTA + "║" + Fore.CYAN + "   4. 🧩 Ver todas las preguntas (con respuestas)".ljust(68) + Fore.MAGENTA + "║")
            print(Fore.MAGENTA + "║" + Fore.CYAN + "   5. 🗺️  Ver mapa del tesoro (posición de preguntas)".ljust(68) + Fore.MAGENTA + "║")
            print(Fore.MAGENTA + "║" + Fore.CYAN + "   6. ❌ Salir del juego".ljust(68) + Fore.MAGENTA + "║")
            print(Fore.MAGENTA + "╚" + "═" * 68 + "╝")
            
            opcion = input(Fore.GREEN + "➤ Elige una opción (1-6): ").strip()
            
            if opcion == '1':
                self.reiniciar_juego()
                self.jugar()
                break
            elif opcion == '2':
                self.mostrar_estadisticas()
            elif opcion == '3':
                self.reproducir_replay()
            elif opcion == '4':
                self.mostrar_preguntas_completas()
            elif opcion == '5':
                self.mostrar_mapa_preguntas()
            elif opcion == '6':
                print(Fore.YELLOW + "👋 ¡Hasta luego! ¡Gracias por jugar!")
                sys.exit()
            else:
                print(Fore.RED + "❌ Opción no válida")
                time.sleep(1)
    
    def reiniciar_juego(self):
        """Reinicia el estado del juego"""
        self.jugador_x = 1
        self.jugador_y = 1
        self.preguntas_respondidas = set()
        self.historial_movimientos = []
        self.pasos = 0
        self.pregunta_actual = None
    
    def mostrar_estadisticas(self):
        """Muestra estadísticas detalladas del juego"""
        self.limpiar_pantalla()
        print(Fore.MAGENTA + "╔" + "═" * 68 + "╗")
        print(Fore.MAGENTA + "║" + Fore.YELLOW + "                    📊 ESTADÍSTICAS DETALLADAS 📊".center(68) + Fore.MAGENTA + "║")
        print(Fore.MAGENTA + "╠" + "═" * 68 + "╣")
        print(Fore.MAGENTA + "║" + Fore.CYAN + f"   Pasos totales: {self.pasos}".ljust(68) + Fore.MAGENTA + "║")
        print(Fore.MAGENTA + "║" + Fore.CYAN + f"   Preguntas respondidas: {len(self.preguntas_respondidas)}/{len(self.preguntas)}".ljust(68) + Fore.MAGENTA + "║")
        print(Fore.MAGENTA + "║" + Fore.CYAN + f"   Porcentaje completado: {(len(self.preguntas_respondidas)/len(self.preguntas)*100):.1f}%".ljust(68) + Fore.MAGENTA + "║")
        print(Fore.MAGENTA + "║" + Fore.GREEN + f"   Puntuación: {len(self.preguntas_respondidas) * 10} puntos".ljust(68) + Fore.MAGENTA + "║")
        print(Fore.MAGENTA + "║" + Fore.YELLOW + f"   Posición final: ({self.jugador_x}, {self.jugador_y})".ljust(68) + Fore.MAGENTA + "║")
        print(Fore.MAGENTA + "╚" + "═" * 68 + "╝")
        input(Fore.YELLOW + "\nPresiona Enter para continuar...")
    
    def mostrar_preguntas_completas(self):
        """Muestra todas las preguntas con sus respuestas"""
        self.limpiar_pantalla()
        print(Fore.MAGENTA + "╔" + "═" * 68 + "╗")
        print(Fore.MAGENTA + "║" + Fore.YELLOW + "                    🧩 TODAS LAS PREGUNTAS 🧩".center(68) + Fore.MAGENTA + "║")
        print(Fore.MAGENTA + "╠" + "═" * 68 + "╣")
        
        for idx, pregunta in enumerate(self.preguntas):
            estado = "✓" if self.posicion_preguntas[idx] in self.preguntas_respondidas else " "
            color = Fore.GREEN if self.posicion_preguntas[idx] in self.preguntas_respondidas else Fore.WHITE
            
            print(Fore.MAGENTA + "║" + color + f"   {estado} P{idx+1}: {pregunta['pregunta'][:50]}...".ljust(68) + Fore.MAGENTA + "║")
            
            if pregunta["tipo"] == "opcion_multiple":
                resp_text = f"Respuesta: {pregunta['correcta']}) {pregunta['opciones'][ord(pregunta['correcta'])-97][3:]}"
            else:
                resp_text = f"Respuesta: {pregunta['respuesta']}"
            
            print(Fore.MAGENTA + "║" + Fore.YELLOW + f"      {resp_text}".ljust(68) + Fore.MAGENTA + "║")
            print(Fore.MAGENTA + "║" + Fore.CYAN + f"      📍 Posición: ({self.posicion_preguntas[idx][0]}, {self.posicion_preguntas[idx][1]})".ljust(68) + Fore.MAGENTA + "║")
            
            if idx < len(self.preguntas) - 1:
                print(Fore.MAGENTA + "║" + " " * 68 + "║")
        
        print(Fore.MAGENTA + "╚" + "═" * 68 + "╝")
        input(Fore.YELLOW + "\nPresiona Enter para continuar...")
    
    def mostrar_mapa_preguntas(self):
        """Muestra un mapa con la posición de las preguntas"""
        self.limpiar_pantalla()
        print(Fore.MAGENTA + "╔" + "═" * 68 + "╗")
        print(Fore.MAGENTA + "║" + Fore.YELLOW + "                    🗺️  MAPA DEL TESORO 🗺️".center(68) + Fore.MAGENTA + "║")
        print(Fore.MAGENTA + "╠" + "═" * 68 + "╣")
        
        # Crear una cuadrícula simple para mostrar posiciones
        for y in range(0, 20, 2):
            linea = Fore.MAGENTA + "║   "
            for x in range(0, 20, 2):
                encontrada = False
                for idx, (px, py) in enumerate(self.posicion_preguntas):
                    if px // 2 == x // 2 and py // 2 == y // 2:
                        if (px, py) in self.preguntas_respondidas:
                            linea += Fore.GREEN + f"P{idx+1}✓ "
                        else:
                            linea += Fore.YELLOW + f"P{idx+1}? "
                        encontrada = True
                        break
                if not encontrada:
                    linea += Fore.BLUE + ".   "
            print(linea + Fore.MAGENTA + "║")
        
        print(Fore.MAGENTA + "╠" + "═" * 68 + "╣")
        print(Fore.MAGENTA + "║" + Fore.GREEN + "   P1✓ = Respondida  " + Fore.YELLOW + "P1? = Sin responder  " + Fore.BLUE + ". = Vacío".ljust(68) + Fore.MAGENTA + "║")
        print(Fore.MAGENTA + "╚" + "═" * 68 + "╝")
        input(Fore.YELLOW + "\nPresiona Enter para continuar...")
    
    def reproducir_replay(self):
        """Reproduce el recorrido del jugador"""
        if not self.historial_movimientos:
            print(Fore.RED + "❌ No hay historial de movimientos para reproducir")
            time.sleep(1.5)
            return
        
        self.limpiar_pantalla()
        print(Fore.YELLOW + "🎬 REPRODUCIENDO RECORRIDO... (Presiona Ctrl+C para detener)")
        time.sleep(1.5)
        
        # Guardar estado actual
        x_temp, y_temp = self.jugador_x, self.jugador_y
        preguntas_temp = self.preguntas_respondidas.copy()
        pasos_temp = self.pasos
        
        # Reiniciar para el replay
        self.jugador_x, self.jugador_y = 1, 1
        self.preguntas_respondidas = set()
        self.pasos = 0
        
        try:
            for paso, (x, y) in enumerate(self.historial_movimientos):
                self.limpiar_pantalla()
                self.jugador_x, self.jugador_y = x, y
                self.pasos = paso + 1
                
                # Simular preguntas respondidas hasta este punto
                for i, (px, py) in enumerate(self.posicion_preguntas):
                    if i < len(self.preguntas_respondidas):  # Simulación simple
                        self.preguntas_respondidas.add((px, py))
                
                self.dibujar_laberinto()
                print(Fore.YELLOW + f"⏯️  Paso {paso + 1} de {len(self.historial_movimientos)}")
                time.sleep(0.2)
        except KeyboardInterrupt:
            print(Fore.YELLOW + "\n\n⏸️  Replay detenido")
        
        # Restaurar estado
        self.jugador_x, self.jugador_y = x_temp, y_temp
        self.preguntas_respondidas = preguntas_temp
        self.pasos = pasos_temp
        input(Fore.YELLOW + "\nPresiona Enter para continuar...")

# Función principal
def main():
    try:
        juego = JuegoLaberinto()
        juego.jugar()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n👋 ¡Juego terminado! ¡Hasta luego!")
    except Exception as e:
        print(Fore.RED + f"❌ Error: {e}")
        input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()