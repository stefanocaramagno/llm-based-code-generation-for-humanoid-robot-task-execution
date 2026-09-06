from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory import InterpolationMode
import time

# Funzione per eseguire il gesto di saluto
def wave_hand(reachy):
    # Accensione del braccio destro
    reachy.turn_on('r_arm')

    # Posizione iniziale del braccio
    initial_position = {
        reachy.r_arm.r_shoulder_pitch: -30,
        reachy.r_arm.r_shoulder_roll: 0,
        reachy.r_arm.r_arm_yaw: 0,
        reachy.r_arm.r_elbow_pitch: 70,
        reachy.r_arm.r_forearm_yaw: 0,
        reachy.r_arm.r_wrist_pitch: 0,
        reachy.r_arm.r_wrist_roll: 0,
    }

    # Posizione alzata della mano per il saluto
    wave_position = {
        reachy.r_arm.r_shoulder_pitch: -10,
        reachy.r_arm.r_shoulder_roll: 0,
        reachy.r_arm.r_arm_yaw: 0,
        reachy.r_arm.r_elbow_pitch: 90,
        reachy.r_arm.r_forearm_yaw: 0,
        reachy.r_arm.r_wrist_pitch: 30,
        reachy.r_arm.r_wrist_roll: 0,
    }

    # Eseguire il movimento di saluto
    for _ in range(3):  # Esegui il gesto di saluto 3 volte
        # Muovere verso la posizione alzata
        goto(goal_positions=wave_position, duration=1.0, interpolation_mode=InterpolationMode.MINIMUM_JERK)
        time.sleep(0.5)  # Attendere un momento nella posizione alzata

        # Tornare alla posizione iniziale
        goto(goal_positions=initial_position, duration=1.0, interpolation_mode=InterpolationMode.MINIMUM_JERK)
        time.sleep(0.5)  # Attendere un momento nella posizione iniziale

    # Spegnere il braccio destro in modo graduale
    reachy.turn_off_smoothly('r_arm')

# Codice eseguibile principale
if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Eseguire il gesto di saluto
    wave_hand(reachy)

    # Uscire dal programma
    exit()