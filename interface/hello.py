from flask import Flask, render_template, request, redirect, url_for
import sqlite3 as sql
from db_tables import Base, Annotation, Recording, RecordingGroup, eng
import os
import random
from sqlalchemy.orm import relationship, sessionmaker


app = Flask(__name__, static_folder="../docs/media", template_folder="../docs")

@app.route('/hello/<user>')
def hello_name(user):
   return render_template('test2.html', name = user)

@app.route('/result')
def result():
   dict = {'phy':50,'che':60,'maths':70}
   return render_template('result.html', result = dict)

@app.route('/audio', methods=['POST', 'GET'])
def student():
   Base.metadata.bind = eng
   Session = sessionmaker(bind=eng)
   ses = Session()
   flag = True
   i = 0

   mturk_code = 12345

   while flag:
      audio_file = random.choice(os.listdir('/Users/anaemendezmendez/Documents/NYU_PHD/Mark/code/docs/media/audio/Train_data/1'))

      recording_id = ses.query(Recording).filter(Recording.file_name == audio_file).first().id

      print(recording_id)

      audio = ses.query(Annotation).filter(Annotation.recording_id == recording_id).first()

      print(audio)


      if audio is None:
         return render_template('css_test.html', audio_file=audio_file, recording_id=recording_id)

      i = i + 1
      
      if i == len(os.listdir('/Users/anaemendezmendez/Documents/NYU_PHD/Mark/code/docs/media/audio/Train_data/1')):
         return render_template('done_study.html', mturk_code=mturk_code)

@app.route('/responses', methods=['POST', 'GET'])
def addrec():
   annotations = []
   if request.method == 'POST':
      Base.metadata.bind = eng
      Session = sessionmaker(bind=eng)
      ses = Session()
      try:
         ann = request.form['1.The sound present in the recording is a']
         print(ann)
         
         #annotations.append(Annotation(class_label=ann))
         #ses.commit()

         recording_id = request.form['recording_id']
         print(recording_id)

         annotation = Annotation(class_label=ann, recording_id=recording_id)
         ses.add(annotation)
         ses.commit()


         msg = "Record successfully added"
      except:
         #con.rollback()
         msg = "error in insert operation"
      
      
      return redirect(url_for("student"))
         

@app.route('/list')
def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from annotations")
   
   rows = cur.fetchall();
   return render_template("list.html",rows = rows)


if __name__ == '__main__':
   app.run(debug = True)