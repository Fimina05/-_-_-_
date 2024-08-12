from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup  #для состояний
from aiogram.fsm.context import FSMContext

from app import keyboards as kb
import app.database.requests as rq

router = Router()

#class Register(StatesGroup):   # запрашивает данные
#     name = State()
#     age = State()
#     number = State()


@router.message(CommandStart()) # обрабатываем сообщение
async def cmd_start(message: Message):  # на вход тип сообщение
    await rq.set_user(message.from_user.id)
    await message.answer('Добро пожаловать в магазин кросовок!', reply_markup=kb.main)  # на сообщение даём ответ

    
@router.message(F.text == 'Каталог')
async def catalog(message: Message):
    await message.answer('Выберите категорию товара', reply_markup = await kb.categories())


@router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery):
    await callback.answer('Вы выбрали категорию')
    await callback.message.answer('Выберите товар по категории', 
                                  reply_markup = await kb.items(callback.data.split('_')[1]))
    

@router.callback_query(F.data.startswith('item_'))    # прописать доп клавиатуру  в keyboards
async def category(callback: CallbackQuery):
    item_data = await rq.get_item(callback.data.split('_')[1])
    await callback.answer('Вы выбрали товар')
    await callback.message.answer(f'Название: {item_data.name}\nОписание: {item_data.description}\nЦена: {item_data.price}$', 
                                  reply_markup = await kb.items(callback.data.split('_')[1]))
    

    

# @router.message(Command('help'))
# async def cmd_help(message: Message):
#      await message.answer('Вы нажали на кнопку помощи')


# @router.message(F.text == 'Каталог')
# async def catalog(message: Message):
#      await message.answer('Выберите категорию товара', reply_markup=kb.catalog)


# @router.callback_query(F.data == 't-shirt')  
# async  def t_shirt(callback:CallbackQuery):
#      await callback.answer('Вы выбрали категорию', show_alert= True)  # появляется уведомление и исчезает/появляется уведомлеие и нужно закрыть его 
#      await callback.message.answer('Вы выбрали категорию футболок')


# @router.message(Command('register'))    #запрашивает имя
# async def register(message: Message, state: FSMContext ):
#      await state.set_state(Register.name)
#      await message.answer('Введите ваше имя')


# @router.message(Register.name)      
# async def register_name(message: Message, state: FSMContext ):
#      await state.update_data(name=message.text)   # то, что прислал пользователь храниться в сообщении в поле text , сохраняем инфу
#      await state.set_state(Register.age)
#      await message.answer('Введите ваш возраст')


# @router.message(Register.age) 
# async def register_age(message: Message, state: FSMContext ):
#      await state.update_data(age=message.text)  
#      await state.set_state(Register.number)
#      await message.answer('Отправьте ваш номер телефона', reply_markup=kb.get_number)


# @router.message(Register.number, F.contact)  # добавляем F(фильтр), что бы отправить номер через нажатие кнопки
# async def register_number(message: Message, state: FSMContext):
#       await state.update_data(number=message.contact.phone_number)  
#       data = await state.get_data()    # достаём информацию
#       await message.answer(f'Ваше имя: {data["name"]}\nВаш возраст:{data["age"]}\nНомер:{data["number"]}')  # выведем информацию этому же пользователю
#       await state.clear()    # очистили состояния, чтобы пользователь мог спокойно дальше пользоваться ботом