from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory import InterpolationMode
import time

# Funzione per alzare il braccio sinistro
def raise_left_arm(duration=2.0):
    # Posizione angolare per alzare il braccio sinistro
    left_arm_position = {
        reachy.l_arm.l_shoulder_pitch: 30,  # Alzare la spalla sinistra
        reachy.l_arm.l_shoulder_roll: 0,    # Mantieni il roll
        reachy.l_arm.l_arm_yaw: 0,          # Mantieni il yaw
        reachy.l_arm.l_elbow_pitch: -90,     # Estendere il gomito
        reachy.l_arm.l_forearm_yaw: 0,      # Mantieni il yaw del forearm
        reachy.l_arm.l_wrist_pitch: 0,       # Mantieni il pitch del polso
        reachy.l_arm.l_wrist_roll: 0,        # Mantieni il roll del polso
    }

    # Accensione del braccio sinistro
    reachy.turn_on('l_arm')

    # Movimento del braccio verso la posizione desiderata
    goto(
        goal_positions=left_arm_position,
        duration=duration,
        interpolation_mode=InterpolationMode.MINIMUM_JERK
    )

    # Attendere che il movimento sia completato
    time.sleep(duration)

# Codice eseguibile principale
if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Alzare il braccio sinistro
    raise_left_arm()

    # Spegnere il braccio sinistro in modo graduale
    reachy.turn_off_smoothly('l_arm')

    # Uscire dal programma
    exit()