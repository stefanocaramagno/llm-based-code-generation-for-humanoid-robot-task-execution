from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory import InterpolationMode
import time
from threading import Thread

# Funzione per eseguire il gesto di saluto
def wave_hand():
    # Accensione del braccio destro
    reachy.turn_on('r_arm')

    # Definizione delle posizioni per il saluto
    start_position = {
        reachy.r_arm.r_shoulder_pitch: -30,
        reachy.r_arm.r_shoulder_roll: 10,
        reachy.r_arm.r_arm_yaw: 0,
        reachy.r_arm.r_elbow_pitch: 45,
        reachy.r_arm.r_forearm_yaw: 0,
        reachy.r_arm.r_wrist_pitch: 0,
        reachy.r_arm.r_wrist_roll: 0,
    }

    wave_up_position = {
        reachy.r_arm.r_shoulder_pitch: -30,
        reachy.r_arm.r_shoulder_roll: 10,
        reachy.r_arm.r_arm_yaw: 0,
        reachy.r_arm.r_elbow_pitch: 45,
        reachy.r_arm.r_forearm_yaw: 0,
        reachy.r_arm.r_wrist_pitch: 30,
        reachy.r_arm.r_wrist_roll: 0,
    }

    wave_down_position = {
        reachy.r_arm.r_shoulder_pitch: -30,
        reachy.r_arm.r_shoulder_roll: 10,
        reachy.r_arm.r_arm_yaw: 0,
        reachy.r_arm.r_elbow_pitch: 45,
        reachy.r_arm.r_forearm_yaw: 0,
        reachy.r_arm.r_wrist_pitch: -30,
        reachy.r_arm.r_wrist_roll: 0,
    }

    # Muovere il braccio nella posizione di partenza
    goto(goal_positions=start_position, duration=1.0, interpolation_mode=InterpolationMode.MINIMUM_JERK)
    time.sleep(1.0)

    # Eseguire il gesto di saluto
    for _ in range(3):  # Ripetere il gesto di saluto 3 volte
        goto(goal_positions=wave_up_position, duration=0.5, interpolation_mode=InterpolationMode.MINIMUM_JERK)
        time.sleep(0.5)
        goto(goal_positions=wave_down_position, duration=0.5, interpolation_mode=InterpolationMode.MINIMUM_JERK)
        time.sleep(0.5)

    # Tornare alla posizione di partenza
    goto(goal_positions=start_position, duration=1.0, interpolation_mode=InterpolationMode.MINIMUM_JERK)
    time.sleep(1.0)

    # Spegnere il braccio destro
    reachy.turn_off_smoothly('r_arm')

# Codice eseguibile principale
if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Avviare il gesto di saluto in un thread
    t = Thread(target=wave_hand)
    t.start()

    # Aspettare che il thread finisca
    t.join()

    # Uscire dal programma
    exit()