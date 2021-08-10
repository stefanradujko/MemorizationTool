import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from random import randint

engine = sqlalchemy.create_engine('sqlite:///flashcard.db?check_same_thread=False')
Base = declarative_base()


class Flashcard(Base):
    __tablename__ = 'flashcard'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    question = sqlalchemy.Column(sqlalchemy.String)
    answer = sqlalchemy.Column(sqlalchemy.String)
    box = sqlalchemy.Column(sqlalchemy.Integer)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def dodaj_karticu():
    while True:
        pitanje = input('Question:\n')
        if len(pitanje) > 1:
            break
    while True:
        odgovor = input('Answer:\n')
        if len(odgovor) > 1:
            break
    kutija = randint(1, 3)
    za_dodati = Flashcard(question=pitanje, answer=odgovor, box=kutija)
    session.add(za_dodati)
    session.commit()


def podmeni():
    while True:
        print('1. Add a new flashcard\n2. Exit\n')
        izbor = input()
        if izbor == '1':
            dodaj_karticu()
        elif izbor == '2':
            break
        else:
            print(f'{izbor} is not an option')


def izmeni_karticu(kartica):
    while True:
        izbor = input('press "d" to delete the flashcard:\npress "e" to edit the flashcard:\n')
        if izbor == 'd':
            session.delete(kartica)
            session.commit()
            break
        elif izbor == 'e':
            np = input(f'current question: {kartica.question}\nplease write a new question:\n')
            if len(np) > 1:
                kartica.question = np
                session.commit()
            no = input(f'current answer: {kartica.answer}\nplease write a new answer:\n')
            if len(no) > 1:
                kartica.answer = no
                session.commit()
                break
        else:
            print(f'{izbor} is not an option')


def vezba(kartica):
    while True:
        znas_li = input('press "y" if your answer is correct:\npress "n" if your answer is wrong:\n')
        if znas_li == 'y':
            if kartica.box != 3:
                kartica.box += 1
            else:
                session.delete(kartica)
            session.commit()
            break
        elif znas_li == 'n':
            kartica.box = 1
            session.commit()
            break
        else:
            print(f'{znas_li} is not an option')


def provezbaj():
    tabela = session.query(Flashcard).all()
    if len(tabela) == 0:
        print('There is no flashcard to practice!')
        return
    for i in range(0, len(tabela)):
        odg = input(f'Question: {tabela[i].question}\
                \npress "y" to see the answer:\npress "n" to skip:\npress "u" to update:\n')
        if odg == 'y':
            print(f'Answer: {tabela[i].answer}')
            vezba(tabela[i])
        elif odg == 'n':
            vezba(tabela[i])
            continue
        elif odg == 'u':
            izmeni_karticu(tabela[i])


def meni():
    while True:
        print('1. Add flashcards\n2. Practice flashcards\n3. Exit\n')
        izbor = input()
        if izbor == '1':
            podmeni()
        elif izbor == '2':
            provezbaj()
        elif izbor == '3':
            print('Bye!')
            break
        else:
            print(f'{izbor} is not an option')


meni()
