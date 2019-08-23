import os
import random

import sqlite3 as sql
from db_tables import ses, Annotation, Recording, RecordingGroup

audio_file = random.choice(os.listdir('/Users/anaemendezmendez/Documents/NYU_PHD/Mark/code/docs/media/audio/Train_data/1'))

recording_id = ses.query(Recording).filter(Recording.file_name == audio_file).first().id

print(recording_id)

audio = ses.query(Annotation).filter(Annotation.recording_id == recording_id).first()
print(audio)

while audio != None:
	audio_file = random.choice(os.listdir('/Users/anaemendezmendez/Documents/NYU_PHD/Mark/code/docs/media/audio/Train_data/1'))

	recording_id = ses.query(Recording).filter(Recording.file_name == audio_file).first().id

	print(recording_id)

	audio = ses.query(Annotation).filter(Annotation.recording_id == recording_id).first()