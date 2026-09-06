from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory import InterpolationMode
import time
from threading import Thread

# Variabile globale per tenere traccia se il thread è in esecuzione
thread_running = False

# Funzione per eseguire il gesto di saluto
def wave_hand():
    global thread_running

    # Accendere il braccio destro
    reachy.turn_on('r_arm')

    # Posizione iniziale (braccio lungo il corpo)
    initial_position = {
        reachy.r_arm.r_shoulder_pitch: -90,
        reachy.r_arm.r_shoulder_roll: 0,
        reachy.r_arm.r_arm_yaw: 0,
        reachy.r_arm.r_elbow_pitch: 0,
        reachy.r_arm.r_forearm_yaw: 0,
        reachy.r_arm.r_wrist_pitch: 0,
        reachy.r_arm.r_wrist_roll: 0,
    }

    # Movimento verso la posizione iniziale
    goto(initial_position, duration=1.0)

    # Movimento di saluto
    for _ in range(3):  # Ripetere il gesto di saluto 3 volte
        # Alzare la mano
        wave_up = {
            reachy.r_arm.r_shoulder_pitch: -60,
            reachy.r_arm.r_elbow_pitch: -30,
            reachy.r_arm.r_wrist_pitch: 30,
            reachy.r_arm.r_wrist_roll: 30,
        }
        goto(wave_up, duration=0.5)
        time.sleep(0.5)

        # Riportare la mano nella posizione iniziale
        goto(initial_position, duration=0.5)
        time.sleep(0.5)

    # Spegnere il braccio
    reachy.turn_off_smoothly('r_arm')

    # Aggiornare lo stato del thread
    thread_running = False

# Codice eseguibile principale
if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Creare e avviare un thread per eseguire il gesto di saluto
    t = Thread(target=wave_hand)
    t.daemon = True
    t.start()

    # Impostare lo stato del thread come in esecuzione
    thread_running = True

    # Aspettare che il gesto di saluto sia completato
    while thread_running:
        time.sleep(0.1)

    # Uscire dal programma
    exit()