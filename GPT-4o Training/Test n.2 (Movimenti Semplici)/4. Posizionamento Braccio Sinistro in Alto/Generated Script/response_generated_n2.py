from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory import InterpolationMode
import time

def lift_left_arm():
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Accensione del braccio sinistro
    reachy.turn_on('l_arm')

    # Posizione iniziale del braccio sinistro
    initial_position = {
        reachy.l_arm.l_shoulder_pitch: 0,
        reachy.l_arm.l_shoulder_roll: 0,
        reachy.l_arm.l_arm_yaw: 0,
        reachy.l_arm.l_elbow_pitch: 0,
        reachy.l_arm.l_forearm_yaw: 0,
        reachy.l_arm.l_wrist_pitch: 0,
        reachy.l_arm.l_wrist_roll: 0,
    }

    # Movimento verso la posizione iniziale
    goto(goal_positions=initial_position, duration=1.0)

    # Posizione finale del braccio sinistro (alzato)
    lifted_position = {
        reachy.l_arm.l_shoulder_pitch: -60,  # Alza la spalla
        reachy.l_arm.l_shoulder_roll: 0,
        reachy.l_arm.l_arm_yaw: 0,
        reachy.l_arm.l_elbow_pitch: -90,  # Piegamento del gomito
        reachy.l_arm.l_forearm_yaw: 0,
        reachy.l_arm.l_wrist_pitch: 0,
        reachy.l_arm.l_wrist_roll: 0,
    }

    # Movimento verso l'alto
    goto(goal_positions=lifted_position, duration=1.5, interpolation_mode=InterpolationMode.MINIMUM_JERK)

    # Attendere che il movimento sia completato
    time.sleep(1.5)

    # Spegnere il braccio sinistro
    reachy.turn_off_smoothly('l_arm')

if __name__ == "__main__":
    lift_left_arm()