import json
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField
from wtforms.validators import DataRequired


class BookLibraryForm(FlaskForm):
  namebook = StringField('namebook', validators=[DataRequired()])
  author = StringField('author', validators=[DataRequired()])
  yearbook = StringField('yearbook', validators=[DataRequired()])
  coverimage = StringField('coverimage', validators=[DataRequired()])
  description = TextAreaField('description', validators=[DataRequired()])
  

class BooksLibrary:
  def __init__(self):
    try:
      with open("bookslibrary.json", "r") as f:
        self.bookslibrary = json.load(f)
    except FileNotFoundError:
      self.bookslibrary = []

  def all(self):
    return self.bookslibrary

  def get(self, id):
    return self.bookslibrary[id]

  def create(self, data):
    self.bookslibrary.append(data)
    self.save_all()

  def save_all(self):
    with open("bookslibrary.json", "w") as f:
      json.dump(self.bookslibrary, f)

  def update(self, id, data):
    data.pop('csrf_token')
    self.bookslibrary[id] = data
    self.save_all()

  def delete(self, id):
    book_id = self.get(id)
    if book_id:
      self.bookslibrary.remove(book_id)
      self.save_all()
      return True
    return False

  def update(self, id, data):
    book_id = self.get(id)
    if book_id:
      index = self.bookslibrary.index(book_id)
      self.bookslibrary[index] = data
      self.save_all()
      return True
    return False


bookslibrary = BooksLibrary()
