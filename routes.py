from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


import entities
from base import Base


app = Flask(__name__)
engine = create_engine('sqlite:///database/quiz.sqlite', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)


@app.get('/')
def home():
    info = session.query(entities.Pizza.name, entities.Pizza.description, entities.PizzaBase.name).join(entities.PizzaBase).filter(entities.PizzaBase.id == entities.Pizza.base_id).all()
    return render_template('home.html', info=info)
