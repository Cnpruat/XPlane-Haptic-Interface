def roll(roll,vibration_levels,threshold_roll,invert):
    intensite_roll = 0
    str_roll = "NOTHING"

    if invert is True :
        roll = -roll

    if roll > threshold_roll:
        str_r = "RIGHT_"

        roll_use = abs(roll)
        if (roll_use > threshold_roll) and (roll_use < 24):
            intensite_roll = ((roll_use-threshold_roll)*(100/21))/100
            str_roll = str_r + "1"

            for i in [0,4,8,12,23,27,31,35]:
                vibration_levels[i] = intensite_roll*100

        elif (roll_use >= 24) and (roll_use < 46):
            intensite_roll = ((roll_use-24)*(100/21))/100
            str_roll = str_r + "2"

            for i in [0,4,8,12,23,27,31,35]:
                vibration_levels[i] = intensite_roll*100

        elif (roll_use >= 46) and (roll_use < 68):
            intensite_roll = ((roll_use-46)*(100/21))/100
            str_roll =  str_r + "3"

            for i in [0,4,8,12,23,27,31,35]:
                vibration_levels[i] = intensite_roll*100

        elif (roll_use >= 68) and (roll_use < 90):
            intensite_roll = ((roll_use-68)*(100/21))/100
            str_roll = str_r + "4"

            for i in [0,4,8,12,23,27,31,35]:
                vibration_levels[i] = intensite_roll*100

        elif (roll_use >= 90):
            intensite_roll = 1
            str_roll = str_r + "MAX"

            for i in [0,4,8,12,23,27,31,35]:
                vibration_levels[i] = 100



    elif roll < -threshold_roll:
        str_r = "LEFT_"

        roll_use = abs(roll)
        if (roll_use > threshold_roll) and (roll_use < 24):
            intensite_roll = ((roll_use-threshold_roll)*(100/21))/100
            str_roll = str_r + "1"

            for i in [3,7,11,15,20,24,28,32]:
                vibration_levels[i] = intensite_roll*100

        elif (roll_use >= 24) and (roll_use < 46):
            intensite_roll = ((roll_use-24)*(100/21))/100
            str_roll = str_r + "2"

            for i in [3,7,11,15,20,24,28,32]:
                vibration_levels[i] = intensite_roll*100

        elif (roll_use >= 46) and (roll_use < 68):
            intensite_roll = ((roll_use-46)*(100/21))/100
            str_roll =  str_r + "3"

            for i in [3,7,11,15,20,24,28,32]:
                vibration_levels[i] = intensite_roll*100

        elif (roll_use >= 68) and (roll_use < 90):
            intensite_roll = ((roll_use-68)*(100/21))/100
            str_roll = str_r + "4"

            for i in [3,7,11,15,20,24,28,32]:
                vibration_levels[i] = intensite_roll*100

        elif (roll_use >= 90):
            intensite_roll = 1
            str_roll = str_r + "MAX"

            for i in [3,7,11,15,20,24,28,32]:
                vibration_levels[i] = 100


    else:
        str_r = ""

    return intensite_roll, str_roll, vibration_levels




def pitch(pitch,vibration_levels,threshold_pitch,invert):
    intensite_pitch = 0
    str_pitch = "NOTHING"

    if invert is True :
        pitch = -pitch

    for i in [21,22,25,26,29,30,33,34]:
                vibration_levels[i] = 0
    if pitch > threshold_pitch:
        str_p = "UP_"

        pitch_use = abs(pitch)
        if (pitch_use > threshold_pitch) and (pitch_use < 14):
            intensite_pitch = ((pitch_use-threshold_pitch)*(100/11))/100
            str_pitch = str_p + "1"

            for i in [1,2,5,6,9,10,13,14]:
                vibration_levels[i] = intensite_pitch*100

        elif (pitch_use >= 14) and (pitch_use < 26):
            intensite_pitch = ((pitch_use-14)*(100/11))/100
            str_pitch = str_p + "2"

            for i in [1,2,5,6,9,10,13,14]:
                vibration_levels[i] = intensite_pitch*100

        elif (pitch_use >= 26) and (pitch_use < 38):
            intensite_pitch = ((pitch_use-26)*(100/11))/100
            str_pitch = str_p + "3"

            for i in [1,2,5,6,9,10,13,14]:
                vibration_levels[i] = intensite_pitch*100

        elif (pitch_use >= 38) and (pitch_use < 50):
            intensite_pitch = ((pitch_use-38)*(100/11))/100
            str_pitch = str_p + "4"

            for i in [1,2,5,6,9,10,13,14]:
                vibration_levels[i] = intensite_pitch*100

        elif (pitch_use >= 50):
            intensite_pitch = 1
            str_pitch = str_p + "MAX"

            for i in [1,2,5,6,9,10,13,14]:
                vibration_levels[i] = 100


    elif pitch < -threshold_pitch:
        str_p = "DOWN_"

        pitch_use = abs(pitch)
        if (pitch_use > threshold_pitch) and (pitch_use < 14):
            intensite_pitch = ((pitch_use-threshold_pitch)*(100/11))/100
            str_pitch = str_p + "1"

            for i in [1,2,5,6,9,10,13,14]:
                vibration_levels[i] = intensite_pitch*100

        elif (pitch_use >= 14) and (pitch_use < 26):
            intensite_pitch = ((pitch_use-14)*(100/11))/100
            str_pitch = str_p + "2"

            for i in [1,2,5,6,9,10,13,14]:
                vibration_levels[i] = intensite_pitch*100

        elif (pitch_use >= 26) and (pitch_use < 38):
            intensite_pitch = ((pitch_use-26)*(100/11))/100
            str_pitch = str_p + "3"

            for i in [1,2,5,6,9,10,13,14]:
                vibration_levels[i] = intensite_pitch*100

        elif (pitch_use >= 38) and (pitch_use < 50):
            intensite_pitch = ((pitch_use-38)*(100/11))/100
            str_pitch = str_p + "4"

            for i in [1,2,5,6,9,10,13,14]:
                vibration_levels[i] = intensite_pitch*100

        elif (pitch_use >= 50):
            intensite_pitch = 1
            str_pitch = str_p + "4"

            for i in [1,2,5,6,9,10,13,14]:
                vibration_levels[i] = 100

    else:
        str_p = ""

    return intensite_pitch, str_pitch, vibration_levels