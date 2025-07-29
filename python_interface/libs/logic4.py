def roll(roll,vibration_levels):
    intensite_roll = 0
    str_roll = "NOTHING"

    if roll > 2:
        str_roll = "RIGHT"
        roll_use = abs(roll)

        if (roll_use > 2) and (roll_use < 90):
            intensite_roll = ((roll_use)*(100/90))/100
            for i in [0,16,3,7,11,15,19,20,24,28,32,36,23,39]:
                vibration_levels[i] = 0
            for i in [4,8,12,27,31,35]:
                vibration_levels[i] = intensite_roll*100

        elif (roll_use >= 90):
            intensite_roll = 1
            for i in [0,16,3,7,11,15,19,20,24,28,32,36,23,39]:
                vibration_levels[i] = 0
            for i in [4,8,12,27,31,35]:
                vibration_levels[i] = 100

    elif roll < 2:
        str_roll = "LEFT"
        roll_use = abs(roll)

        if (roll_use > 2) and (roll_use < 90):
            intensite_roll = ((roll_use)*(100/90))/100
            for i in [0,4,8,12,16,3,19,20,36,23,27,31,35,39]:
                vibration_levels[i] = 0
            for i in [7,11,15,24,28,32]:
                vibration_levels[i] = intensite_roll*100

        elif (roll_use >= 90):
            intensite_roll = 1
            for i in [0,4,8,12,16,3,19,20,36,23,27,31,35,39]:
                vibration_levels[i] = 0
            for i in [7,11,15,24,28,32]:
                vibration_levels[i] = 100

    else:
        str_roll = ""

    return intensite_roll, str_roll, vibration_levels




def pitch(pitch,vibration_levels):
    intensite_pitch = 0
    str_pitch = "NOTHING"

    if pitch > 2:
        str_pitch = "UP"
        pitch_use = abs(pitch)

        if (pitch_use > 2) and (pitch_use < 50):
            intensite_pitch = ((pitch_use)*(100/50))/100
            for i in [1,2,5,6,9,10,13,14,17,18,21,22,37,38]:
                vibration_levels[i] = 0
            for i in [25,26,29,30,33,34]:
                vibration_levels[i] = intensite_pitch*100

        elif (pitch_use >= 50):
            intensite_pitch = 1

            for i in [1,2,5,6,9,10,13,14,17,18,21,22,37,38]:
                vibration_levels[i] = 0
            for i in [25,26,29,30,33,34]:
                vibration_levels[i] = 100


    elif pitch < 2:
        str_pitch = "DOWN"
        pitch_use = abs(pitch)

        if (pitch_use > 2) and (pitch_use < 50):
            intensite_pitch = ((pitch_use)*(100/50))/100
            for i in [1,2,21,22,25,26,29,30,33,34,37,38]:
                vibration_levels[i] = 0
            for i in [5,6,9,10,13,14]:
                vibration_levels[i] = intensite_pitch*100



        elif (pitch_use >= 50):
            intensite_pitch = 1

            for i in [1,2,21,22,25,26,29,30,33,34,37,38]:
                vibration_levels[i] = 0
            for i in [5,6,9,10,13,14]:
                vibration_levels[i] = 100

    else:
        str_pitch = ""

    return intensite_pitch, str_pitch, vibration_levels