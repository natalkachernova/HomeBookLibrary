import os
import csv

from flask import Flask, render_template, request

UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def form_view():
  if request.method == "POST":
    file = request.files['file']
    
    data = request.form
    namebook = data.get('namebook')
    author = data.get('authorname') 
    yearbook = data.get('yearbook')
    imagetitlefile = file.filename
    description = data.get('description')

    with open('bookslibrary.csv', 'a', newline='') as csvfile:
        fieldnames = ['namebook', 'author', 'yearbook', 'imagetitlefile','description']
        writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=fieldnames)
        #writer.writeheader()
        writer.writerow({'namebook': namebook,
                         'author': author,
                         'yearbook': yearbook,
                         'imagetitlefile': imagetitlefile,
                         'description': description})
        #завантаження файлу малюнку на сервер
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return "Data saved"
  return render_template('form.html')

if __name__ == '__main__':
  app.run(debug=True)
