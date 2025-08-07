# ---------- Standard library imports ----------
import keyboard
import os
import contextlib
import sys
import time
import threading

# ---------- Local library imports ----------
import xpc                                                  # XPlane connect library
import tactcombine                                          # CPP library to combine .tact files
from bhaptics import haptic_player                          # Bhaptic library
from bhaptics.haptic_player import BhapticsPosition

# ---------- Python program imports ----------
import logic1
import logic2
import logic3
import logic4

# ---------- Third-party library imports ----------
with open(os.devnull, 'w') as f, contextlib.redirect_stdout(f): # To avoid initial prints
    import pygame_widgets
    import pygame
    from pygame_widgets.slider import Slider
    from pygame_widgets.textbox import TextBox
    from pygame_widgets.button import Button


# ---------- Processes definition ----------
def gather_data(shared_vars):
    while shared_vars['running']:
        try:
            with xpc.XPlaneConnect() as client:
                Lroll, Lpitch, Lyaw, Lagl, Lspeed, LTAS, Lgear = client.getDREFs([
                    "sim/flightmodel/position/true_phi",
                    "sim/flightmodel/position/true_theta",
                    "sim/flightmodel/position/true_psi",
                    "sim/flightmodel/position/y_agl",
                    "sim/flightmodel/position/groundspeed",
                    "sim/flightmodel/position/true_airspeed",
                    "sim/cockpit/switches/gear_handle_status"])

                shared_vars['roll'] = Lroll[0]
                shared_vars['pitch'] = Lpitch[0]
                shared_vars['yaw'] = Lyaw[0]
                shared_vars['agl'] = Lagl[0]
                shared_vars['speed'] = Lspeed[0]
                shared_vars['TAS'] = LTAS[0]
                shared_vars['GEAR'] = Lgear[0]

                #print(shared_vars['roll'], shared_vars['pitch'], shared_vars['yaw'], shared_vars['agl'])

        except (TimeoutError, ConnectionResetError):
            print("Not connected")

            shared_vars['roll'] = 0
            shared_vars['pitch'] = 0
            shared_vars['yaw'] = 0
            shared_vars['agl'] = 0
            shared_vars['speed'] = 0
            shared_vars['TAS'] = 0
            shared_vars['GEAR'] = True


def roll_processing(shared_vars, vibration_levels):
    while shared_vars['running']:
        roll = shared_vars['roll']
        user_intensity = shared_vars['user_intensity']

        if shared_vars['mode'] == 1:
            intensite_roll, str_roll, vibration_levels = logic1.roll(roll,vibration_levels)

        elif shared_vars['mode'] == 2:
            intensite_roll, str_roll, vibration_levels = logic2.roll(roll,vibration_levels)

        elif shared_vars['mode'] == 3:
            intensite_roll, str_roll, vibration_levels = logic3.roll(roll,vibration_levels)

        elif shared_vars['mode'] == 4:
            intensite_roll, str_roll, vibration_levels = logic4.roll(roll,vibration_levels)

        shared_vars['intensite_roll'] = intensite_roll*user_intensity
        shared_vars['str_roll'] = str_roll

        time.sleep(0.01)


def pitch_processing(shared_vars, vibration_levels):
    while shared_vars['running']:
        pitch = shared_vars['pitch']
        user_intensity = shared_vars['user_intensity']

        if shared_vars['mode'] == 1:
            intensite_pitch, str_pitch, vibration_levels = logic1.pitch(pitch,vibration_levels)

        elif shared_vars['mode'] == 2:
            intensite_pitch, str_pitch, vibration_levels = logic2.pitch(pitch,vibration_levels)

        elif shared_vars['mode'] == 3:
            intensite_pitch, str_pitch, vibration_levels = logic3.pitch(pitch,vibration_levels)

        elif shared_vars['mode'] == 4:
            intensite_pitch, str_pitch, vibration_levels = logic4.pitch(pitch,vibration_levels)

        shared_vars['intensite_pitch'] = intensite_pitch*user_intensity
        shared_vars['str_pitch'] = str_pitch
        time.sleep(0.01)

def make_vibrate(shared_vars): #
    player = haptic_player.HapticPlayer()
    while shared_vars['running']:
        if not(shared_vars['GEAR']):
            if shared_vars['mode'] == 1:
                str_roll = shared_vars['str_roll']
                str_pitch = shared_vars['str_pitch']
                intensite_roll = shared_vars['intensite_roll']
                intensite_pitch = shared_vars['intensite_pitch']

                L1 = ["./python_interface/patterns/logic1/"+str_roll+".tact","./python_interface/patterns/logic1/"+str_pitch+".tact"]
                L2 = [intensite_roll, intensite_pitch]
                path = tactcombine.combine(L1, L2, "./python_interface/patterns/BLANK.tact")
                player.register("Comb", path)
                player.submit_registered("Comb")
                time.sleep(0.1)

            elif shared_vars['mode'] == 2:
                str_roll = shared_vars['str_roll']
                str_pitch = shared_vars['str_pitch']
                intensite_roll = shared_vars['intensite_roll']
                intensite_pitch = shared_vars['intensite_pitch']

                L1 = ["./python_interface/patterns/logic2/"+str_roll+".tact","./python_interface/patterns/logic2/"+str_pitch+".tact"]
                L2 = [intensite_roll, intensite_pitch]
                path = tactcombine.combine(L1, L2, "./python_interface/patterns/BLANK.tact")
                player.register("Comb", path)
                player.submit_registered("Comb")
                time.sleep(0.9)

            elif shared_vars['mode'] == 3:
                str_roll = shared_vars['str_roll']
                str_pitch = shared_vars['str_pitch']
                intensite_roll = shared_vars['intensite_roll']
                intensite_pitch = shared_vars['intensite_pitch']

                L1 = ["./python_interface/patterns/logic3/"+str_roll+".tact","./python_interface/patterns/logic3/"+str_pitch+".tact"]
                L2 = [intensite_roll, intensite_pitch]
                path = tactcombine.combine(L1, L2, "./python_interface/patterns/BLANK.tact")
                player.register("Comb", path)
                player.submit_registered("Comb")
                time.sleep(0.8)

            elif shared_vars['mode'] == 4:
                str_roll = shared_vars['str_roll']
                str_pitch = shared_vars['str_pitch']
                intensite_roll = shared_vars['intensite_roll']
                intensite_pitch = shared_vars['intensite_pitch']

                L1 = ["./python_interface/patterns/logic4/"+str_roll+".tact","./python_interface/patterns/logic4/"+str_pitch+".tact"]
                L2 = [intensite_roll, intensite_pitch]
                path = tactcombine.combine(L1, L2, "./python_interface/patterns/BLANK.tact")
                player.register("Comb", path)
                player.submit_registered("Comb")
                time.sleep(0.1)




# ---------- Main process ----------

if __name__ == '__main__':

    # Shared variables definition
    shared_vars = {
    'roll': 0.0,
    'pitch': 0.0,
    'yaw': 0.0,
    'agl': 0.0,
    'speed': 0.0,
    'TAS': 0.0,
    'GEAR': True,
    'intensite_roll': 0.0,
    'intensite_pitch': 0.0,
    'str_roll': '',
    'str_pitch': '',
    'user_intensity': 1.0,
    'mode': 1,
    'running': True
    }

    vibration_levels = [0]*40  # Liste normale, partagée entre threads

    # Threads start
    t_gather = threading.Thread(target=gather_data, args=(shared_vars,))
    t_roll = threading.Thread(target=roll_processing, args=(shared_vars, vibration_levels))
    t_pitch = threading.Thread(target=pitch_processing, args=(shared_vars, vibration_levels))
    t_vibrate = threading.Thread(target=make_vibrate, args=(shared_vars,))

    t_gather.start()
    t_roll.start()
    t_pitch.start()
    t_vibrate.start()

    # GUI initialization

    pygame.init()
    screen = pygame.display.set_mode((1180, 720))
    pygame.display.set_caption("GUI : XPlane 11/12 - Bhaptic TactSuit x40")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    def stop_program():
        shared_vars['running'] = False

    quit_button = Button(
        screen, 775, 625, 150, 40,
        text='STOP',
        fontSize=30,
        margin=20,
        inactiveColour=(160, 30, 30),
        hoverColour=(150, 0, 0),
        pressedColour=(200, 0, 0),
        textColour=(255,255,255),
        radius=20,
        onClick=stop_program)

    icon = pygame.image.load("./python_interface/assets/IISRI_icon.png")
    pygame.display.set_icon(icon)

    background = pygame.image.load("./python_interface/assets/horizon.png").convert_alpha()
    background = pygame.transform.scale(background, (700, 700))
    plane = pygame.image.load("./python_interface/assets/avion.png").convert_alpha()
    plane = pygame.transform.scale(plane, (300, 300))

    VFront = pygame.image.load("./python_interface/assets/Front.png").convert_alpha()
    VFront = pygame.transform.scale(VFront, (350, 350))
    BFront = pygame.image.load("./python_interface/assets/Back.png").convert_alpha()
    BFront = pygame.transform.scale(BFront, (350, 350))

    Surf = (400, 400)
    CentreSurf = (Surf[0]//2, Surf[1]//2)
    horizon_surface = pygame.Surface(Surf, pygame.SRCALPHA)
    pygame.draw.rect(screen, (255, 255, 255), (50, 100, 400, 400), 2)

    front_positions = {i: (700 + (i % 4) * 40, 180 + (i // 4) * 40 * 1.25) for i in range(20)}
    back_positions = {i: (915 + (i % 4) * 40, 180 + ((i-20) // 4) * 40 * 1.25) for i in range(20, 40)}

    def draw_motor(surface, x, y, intensity):
        intensity = max(0, min(100, intensity))
        alpha = int((intensity / 100) * 255)

        circle_surf = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.circle(circle_surf, (255, 255, 0, alpha), (16, 16), 16)
        surface.blit(circle_surf, (x - 16, y - 16))  # centered around the point (x, y)

    slider = Slider(screen, 660, 550, 200, 20, min=1, max=100, step=1, initial=85, colour=(255,255,255), handleColour=(255,255,0))

    # --- Logic mode selection (1, 2, or 3)
    selected_logic = {'value': 1}  # Valeur partagée dans l'interface

    def set_logic_mode(mode):
        selected_logic['value'] = mode

    logic_btn1 = Button(
        screen, 645, 475, 100, 30,
        text='Logic 1',
        onClick=lambda: set_logic_mode(1),
        fontSize=24,
        radius=10,
        textColour=(230, 230, 230),
        inactiveColour=(70, 130, 180),
        hoverColour=(50, 110, 160),
        pressedColour=(80, 80, 80),
    )

    logic_btn2 = Button(
        screen, 755, 475, 100, 30,
        text='Logic 2',
        onClick=lambda: set_logic_mode(2),
        fontSize=24,
        radius=10,
        textColour=(230, 230, 230),
        inactiveColour=(70, 130, 180),
        hoverColour=(50, 110, 160),
        pressedColour=(80, 80, 80),
    )

    logic_btn3 = Button(
        screen, 865, 475, 100, 30,
        text='Logic 3',
        onClick=lambda: set_logic_mode(3),
        fontSize=24,
        radius=10,
        textColour=(230, 230, 230),
        inactiveColour=(70, 130, 180),
        hoverColour=(50, 110, 160),
        pressedColour=(80, 80, 80),
    )

    logic_btn4 = Button(
        screen, 975, 475, 100, 30,
        text='Logic 4',
        onClick=lambda: set_logic_mode(4),
        fontSize=24,
        radius=10,
        textColour=(230, 230, 230),
        inactiveColour=(70, 130, 180),
        hoverColour=(50, 110, 160),
        pressedColour=(80, 80, 80),
    )


    # GUI loop

    while shared_vars['running']:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                shared_vars['running'] = False  # Arrêt des process

        screen.fill((25, 25, 25))
        pygame.draw.line(screen, (230, 230, 230), (550, 50), (550, 670), 3)
        horizon_surface.fill((0, 0, 0, 0))

        roll = shared_vars['roll']
        pitch = shared_vars['pitch']
        yaw = shared_vars['yaw']

        intensite_roll = shared_vars['intensite_roll']
        agl = shared_vars['agl']
        speed = shared_vars['speed']
        TAS = shared_vars['TAS']


        temp_surface = pygame.Surface((900, 900), pygame.SRCALPHA)
        # Pitch
        pitch_offset = pitch * 4.2
        temp_surface.blit(background, background.get_rect(center=(450, 450 + pitch_offset)))
        # Roll
        rotated = pygame.transform.rotate(temp_surface, roll)
        rect = rotated.get_rect(center=CentreSurf)
        horizon_surface.blit(rotated, rect)

        plane_rect = plane.get_rect(center=CentreSurf)
        horizon_surface.blit(plane, plane_rect)

        screen.blit(horizon_surface, (50, 100))
        pygame.draw.rect(screen, (230, 230, 230), (50, 100, 400, 400), 3)

        font_info = pygame.font.SysFont(None, 36)
        txt = font_info.render(f"Roll :   {roll:.1f} °", True, 	(230, 230, 230))
        screen.blit(txt, (75, 540))
        txt = font_info.render(f"Pitch : {pitch:.1f} °", True, (230, 230, 230))
        screen.blit(txt, (75, 580))
        txt = font_info.render(f"Yaw :   {yaw:.1f} °", True, (230, 230, 230))
        screen.blit(txt, (75, 620))

        txt = font_info.render(f"Intensity : {slider.getValue():.0f} %", True, (255, 220, 0))
        screen.blit(txt, (915, 547))
        shared_vars['user_intensity'] = slider.getValue() / 100

        txt = font_info.render(f"Gspeed : {speed : .1f} m/s", True, (230, 230, 230))
        screen.blit(txt, (245, 540))
        txt = font_info.render(f"TAS : {TAS : .1f} m/s", True, (230, 230, 230))
        screen.blit(txt, (245, 580))
        txt = font_info.render(f"AGL : {agl : .1f} m", True, (230, 230, 230))
        screen.blit(txt, (245, 620))

        txt = font_info.render(f"Logic Mode: {selected_logic['value']}", True, 	(255, 220, 0))
        screen.blit(txt, (785, 430))
        shared_vars['mode'] = selected_logic['value']

        # Display pictures of the vest
        screen.blit(VFront, (585, 90))
        screen.blit(BFront, (798, 85))

        # Display the front motors and label
        txt = font_info.render("Front :", True, (230, 230, 230))
        screen.blit(txt, (722, 70))
        for i, (x, y) in front_positions.items():
            draw_motor(screen, x, y, vibration_levels[i])

        # Display the back motors and label
        txt = font_info.render("Back :", True, (230, 230, 230))
        screen.blit(txt, (938, 70))
        for i, (x, y) in back_positions.items():
            draw_motor(screen, x, y, vibration_levels[i])


        pygame_widgets.update(event)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

    # Waiting for all the process to stop
    sys.exit()
