from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext


from db import SessionLocal
from models import User, Note
from states.noteState import Note as NoteState

router = Router()
session = SessionLocal()


@router.message(Command("start"))
async def cmd_start(msg: Message):
    if not session.query(User).filter_by(tg_id=msg.from_user.id).first():
        user = User(
            username=msg.from_user.username,
            tg_id=msg.from_user.id
        )
        try:
            session.add(user)
            session.commit()
            session.refresh(user)
        except Exception as e:
            print(e)

    await msg.answer(
        "Привет, тут ты можешь делать заметки =)"
        "Чтобы добавить <b>новую</b> заметку, введи /new."
        "Чтобы посмотреть <b>все</b> заметки, введи /all"
    )



@router.message(Command("all"))
async def all_notes(msg: Message):
    user = session.query(User).filter_by(tg_id=msg.from_user.id).first()

    if user:
        user_notes = user.notes
        note_list = ""
        for note in user_notes:
            note_list += f"{note.body}\n\n"
        await msg.answer(f"Держи: \n {note_list}")
    else:
        await msg.answer(
            "Кажется, вы еще ничего не добавили =("
            "Поробуйте команду /new."
        )


@router.message(Command("new"))
async def cmd_new(msg: Message, state: FSMContext):
    await msg.answer(
        "Отлично, введи текст заметки..."
    )
    await state.set_state(NoteState.body)


@router.message(NoteState.body)
async def new_note_state(msg: Message, state: FSMContext):
    user = session.query(User).filter_by(tg_id=msg.from_user.id).first()
    if not user:
        user = User(
            username=msg.from_user.username,
            tg_id=msg.from_user.id
        )
        try:
            session.add(user)
            session.commit()
            session.refresh(user)
        except Exception as e:
            print(e)

    new_note = Note(body=msg.text, user=user)
    try:
        session.add(new_note)
        session.commit()
        session.refresh(new_note)
    except Exception as e:
            print(e)

    await state.update_data(body=msg.text)
    await state.clear()
    await msg.answer("Отлично, я все сохранил!")

