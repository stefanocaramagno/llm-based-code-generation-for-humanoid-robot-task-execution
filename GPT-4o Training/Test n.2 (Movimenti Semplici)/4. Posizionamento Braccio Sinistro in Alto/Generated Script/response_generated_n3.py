from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
import time

# Funzione per muovere il braccio sinistro verso l'alto
def raise_left_arm(duration):
    # Definire le posizioni angolari del braccio sinistro per alzarlo
    left_arm_position = {
        reachy.l_arm.l_shoulder_pitch: 45,  # Alzare la spalla
        reachy.l_arm.l_shoulder_roll: 0,    # Mantenere il braccio in posizione neutra
        reachy.l_arm.l_arm_yaw: 0,           # Mantenere il polso in posizione neutra
        reachy.l_arm.l_elbow_pitch: -90,     # Posizione dell'avambraccio
        reachy.l_arm.l_forearm_yaw: 0,       # Mantenere il polso in posizione neutra
        reachy.l_arm.l_wrist_pitch: 0,       # Mantenere il polso in posizione neutra
        reachy.l_arm.l_wrist_roll: 0,        # Mantenere il polso in posizione neutra
    }

    # Accendere il braccio sinistro
    reachy.turn_on('l_arm')

    # Muovere il braccio sinistro verso l'alto
    goto(goal_positions=left_arm_position, duration=duration)

# Codice eseguibile principale
if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Alzare il braccio sinistro in un periodo di 2 secondi
    raise_left_arm(duration=2.0)

    # Attendere un momento per osservare la posizione
    time.sleep(2)

    # Spegnere il braccio sinistro in modo graduale
    reachy.turn_off_smoothly('l_arm')

    # Uscire dal programma
    exit()