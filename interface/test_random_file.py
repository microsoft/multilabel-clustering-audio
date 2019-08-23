import os
import random

import sqlite3 as sql
from db_tables import ses, Annotation, Recording, RecordingGroup

audio = random.choice(os.listdir('/Users/anaemendezmendez/Documents/NYU_PHD/Mark/code/docs/media/audio/Train_data/1'))
audio_list = os.listdir('/Users/anaemendezmendez/Documents/NYU_PHD/Mark/code/docs/media/audio/Train_data/1')
print(audio_list)

recording_group = RecordingGroup()
ses.add(recording_group)
ses.commit()

recordings = []
for i in range(len(audio_list)):
	recording = Recording(file_name=audio_list[i], id_hash=audio_list[i], recording_group_id=1)

	recordings.append(recording)

ses.add_all(recordings)
ses.commit()

random.shuffle(audio_list)

print(audio_list[0])
print(audio)




round_p = 0.2
ans_p = 0.5
defin_p1 = 0.5
defin_p2 = 0.6
defin_p3 = 0.7
defin_p4 = 0.8
defin_p5 = 0.9

expected_defin = ((round_p * ans_p * ans_p) * 5) + (round_p * ans_p * defin_p1) + (round_p * ans_p * defin_p2) + (round_p * ans_p * defin_p3) + (round_p * ans_p * defin_p4) + (round_p * ans_p * defin_p5)
print(expected_defin)

expected_conf = 0.5
base = 0.1
#2.5 = base + expected_defin * bonus

# base = 1 (for participating in entire study, labeling 20 recordings), total_bonus = 2.5, bonus_per_recording = 0.125

# base = 0.5 (for participating in entire study, labeling 20 recordings), total_bonus = 3.34, bonus_per_recording = 0.17

# base = 0.2 (for participating in entire study, labeling 20 recordings), total_bonus = 4, bonus_per_recording = 0.2

bonus = (2.5 - base)/expected_defin

print("total bonus definetti = "+str(bonus))

bonus_p_recording = bonus/20.

print("bonus per recording definetti = "+str(bonus_p_recording))


# base = 1 (for participating in entire study, labeling 20 recordings), total_bonus = 3.0, bonus_per_recording = 0.15

# base = 0.5 (for participating in entire study, labeling 20 recordings), total_bonus = 4, bonus_per_recording = 0.2

# base = 0.2 (for participating in entire study, labeling 20 recordings), total_bonus = 4.6, bonus_per_recording = 0.23

base_conf = 0.2

bonus_conf = (2.5 - base_conf)/expected_conf

print("total bonus confidence = "+str(bonus_conf))

bonus_p_recording_conf = bonus_conf/20.

print("bonus per recording confidence = "+str(bonus_p_recording_conf))




