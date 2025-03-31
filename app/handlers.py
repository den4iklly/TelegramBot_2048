import json

from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import game_2048

import app.keyboards as kb

router = Router()


class GameStates(StatesGroup):
    playing = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет! Это бот для игры 2048\nЧтобы начать напишите /play', reply_markup=kb.main)


@router.message(F.text.in_(['left', 'right', 'up', 'down']))
async def cmd_direction(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == GameStates.playing:
        data = await state.get_data()
        game_message = data.get("game_message")
        values = data.get("values")
        values, changed = game_2048.MoveTiles(message.text, values)
        if changed:
            values = game_2048.AddTile(values, 1)
            await game_message.edit_text('Карта 2048', reply_markup=kb.create_kb_2048(values))
        if not game_2048.CanMove(values):
            await message.answer("Поражение!")
            await state.set_data(None)
            await state.set_state(None)
        if game_2048.CheckWin(values):
            await message.answer("Победа!")
            await state.set_data(None)
            await state.set_state(None)
        await message.delete()
    else:
        await message.answer("Напишите /play чтобы начать игру")


@router.message(Command("new"))
async def cmd_new(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == GameStates.playing:
        await state.update_data(game_message=None, values=None)
        await state.set_state(None)
        await cmd_play(message, state)
    else:
        await message.answer("У вас нет начатой игры\nЕсли хотите начать, напишите /play")


@router.message(Command("play"))
async def cmd_play(message: Message, state: FSMContext):

    current_state = await state.get_state()

    if current_state == GameStates.playing:
        await message.answer("У вас уже есть начатая игра\nЕсли хотите начать новую, напишите /new")

    else:
        await state.set_state(GameStates.playing)
        values = game_2048.CreateMap([4, 4])
        values = game_2048.AddTile(values, 2)

        game_message = await message.answer('Карта 2048', reply_markup=kb.create_kb_2048(values))

        await state.update_data(game_message=game_message, values=values)
