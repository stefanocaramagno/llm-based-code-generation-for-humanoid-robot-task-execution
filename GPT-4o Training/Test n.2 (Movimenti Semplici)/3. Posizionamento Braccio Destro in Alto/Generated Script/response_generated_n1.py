from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory import InterpolationMode
import time

# Funzione per alzare il braccio destro
def raise_right_arm():
    # Definire una posizione sopraelevata per il braccio destro
    elevated_position = {
        reachy.r_arm.r_shoulder_pitch: -30,  # Alzare la spalla
        reachy.r_arm.r_shoulder_roll: 0,     # Mantenere il rollo della spalla
        reachy.r_arm.r_arm_yaw: 0,            # Mantenere l'orientamento del braccio
        reachy.r_arm.r_elbow_pitch: -90,      # Estendere l'avambraccio
        reachy.r_arm.r_forearm_yaw: 0,       # Mantenere l'orientamento dell'avambraccio
        reachy.r_arm.r_wrist_pitch: 0,        # Mantenere l'orientamento del polso
        reachy.r_arm.r_wrist_roll: 0,         # Mantenere il rollo del polso
    }

    # Accendere il braccio destro
    reachy.turn_on('r_arm')

    # Muovere il braccio destro verso la posizione elevata
    goto(
        goal_positions=elevated_position,
        duration=2.0,  # Durata del movimento in secondi
        interpolation_mode=InterpolationMode.MINIMUM_JERK
    )

    # Mantenere la posizione per un attimo
    time.sleep(2.0)

    # Spegnere il braccio destro
    reachy.turn_off_smoothly('r_arm')

# Codice eseguibile principale
if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Eseguire il movimento di alzata del braccio destro
    raise_right_arm()

    # Uscire dal programma
    exit()