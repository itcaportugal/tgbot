# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""Simple inline keyboard bot with multiple CallbackQueryHandlers.
This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined as callback query handler. Then, those functions are
passed to the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot that uses inline keyboard that has multiple CallbackQueryHandlers arranged in a
ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line to stop the bot.
"""
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from telegram.ext import (
    Updater,
    Filters,
    MessageHandler,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
)
TOKEN = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Stages
FIRST, SECOND = range(2)
# Callback data
REUNIOES, TWO, PRESENCIAIS, ONLINE, REGRAS, TELEFONE = range(6)


def start(update: Update, context: CallbackContext) -> int:
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).
    keyboard = [
        [
            InlineKeyboardButton("Reuniões \uE235", callback_data=str(REUNIOES)),
            InlineKeyboardButton("Diretrizes \uE235", callback_data=str(REGRAS)),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    update.message.reply_text("""Olá! Eu sou o bot de Cocaína Anónimos e estou aqui para te ajudar.

Por agora posso ajudar-te a encontrar reuniões e a ver as diretrizes do grupo.

Carrega num dos Botões que encontras em baixo para selecionares uma opção.

No futuro vou fazer também o seguinte por ti:

- Mostrar-te os nossos passos.
- Mostrar-te as nossas tradições.
- Etc..

Estou em constante desenvolvimento, como tal lembra-te de mim e chama-me frequentemente com o comando:

/ajuda
""", reply_markup=reply_markup)
    # Tell ConversationHandler that we're in state `FIRST` now
    return FIRST


def start_over(update: Update, context: CallbackContext) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    # Get CallbackQuery from Update
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Reuniões \uE235", callback_data=str(REUNIOES)),
            InlineKeyboardButton("Diretrizes \uE235", callback_data=str(REGRAS)),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Instead of sending a new message, edit the message that
    # originated the CallbackQuery. This gives the feeling of an
    # interactive menu.
    query.edit_message_text(text="""Olá! Eu sou o bot de Cocaína Anónimos e estou aqui para te ajudar.

Por agora posso ajudar-te a encontrar reuniões e a ver as diretrizes do grupo.

Carrega num dos Botões que encontras em baixo para selecionares uma opção.

No futuro vou fazer também o seguinte por ti:

- Mostrar-te os nossos passos.
- Mostrar-te as nossas tradições.
- Etc..

Estou em constante desenvolvimento, como tal lembra-te de mim e chama-me frequentemente com o comando:

/ajuda
""", reply_markup=reply_markup)
    return FIRST


def reunioes(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Presenciais \uE235", callback_data=str(PRESENCIAIS)),
            InlineKeyboardButton("Online \uE235", callback_data=str(ONLINE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Qual é o tipo de reuniões que desejas consultar?", reply_markup=reply_markup
    )
    return FIRST

def regras(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Voltar ao início! \uE235", callback_data=str(REUNIOES)),
            InlineKeyboardButton("Terminar \uE235", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="""
    Diretrizes sugeridas para o grupo Telegram.
Comunicar informações sobre C.A., e oferecer esperança e conforto aos membros com pouco ou nenhum acesso às reuniões, por meio da partilha de experiências, força e esperança entre os membros.
C.A. é uma irmandade de aditos/alcoolicos que compartilham a sua experiência, força e esperança a fim de resolver seus problemas comuns.
C.A. não é aliado a nenhuma seita, denominação, entidade política, organização ou instituição; não se envolve em qualquer controvérsia; nem endossa nem se opõe a qualquer causa.
- O foco principal é compartilhar nossa própria experiência pessoal, força e esperança.
- Os participantes devem ser membros de C.A..
- Tudo o que é dito no Grupo deve ser mantido em sigilo.
- Breves citações de Literatura Aprovada são permitidas.
- O uso ou menção a literatura externa é desencorajado.
- C.A. é um programa espiritual, que não se baseia em nenhuma forma particular de religião. Não vamos frustrar nosso propósito entrando em discussões a respeito de crenças religiosas específicas.
- Postagens relacionadas com recuperação apenas, mensagens pessoais devem ser compartilhadas por mensagem privada
- Considere o tamanho da postagem ... alguns participantes têm dados limitados.
Cada membro é responsável por manter o grupo focado na recuperação e na discussão de tópicos relacionados com C.A..
    """, reply_markup=reply_markup
    )
    return SECOND

def two(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data=str(REUNIOES)),
            InlineKeyboardButton("3", callback_data=str(PRESENCIAIS)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Second CallbackQueryHandler, Choose a route", reply_markup=reply_markup
    )
    return FIRST


def presenciais(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Voltar ao início! \uE235", callback_data=str(REUNIOES)),
            InlineKeyboardButton("Terminar \uE235", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(parse_mode=ParseMode.HTML,
        text="""
<b>SEGUNDA-FEIRA 19h00 às 20h15</b>
Grupo Aceitar é viver
CAMPOLIDE
Igreja de Santo António de Campolide
Travessa Estêvão Pinto
1070-373 Lisboa
<i>*Reunião aberta a não-adictos</i>

<b>TERÇA-FEIRA 19h30 às 20h30</b>
Grupo Livro Azul
CAMPOLIDE
Igreja de Santo António de Campolide
Travessa Estêvão Pinto
1070-373 Lisboa

<b>QUARTA-FEIRA 19H45 às 20H45</b>
Grupo C.A. Em Casa
ALMADA
Centro Cultural e Juvenil de Santo Amaro
Casa Amarela
Estrada dos Álamos
2810-260 Laranjeiro
<i>*Esta reunião não se realiza aos feriados</i>

<b>SÁBADO 19h30 às 20h30</b>
Grupo As Lágrimas ficaram no passado
PAREDE
Junta de Freguesia de Parede
R. José Relvas 84
2775-221 Parede
<i>*Reunião aberta a não-adictos no último sábado de cada mês</i>
""", reply_markup=reply_markup
    )
    # Transfer to conversation state `SECOND`
    return SECOND


def online(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Voltar ao início! \uE235", callback_data=str(REUNIOES)),
            InlineKeyboardButton("Terminar \uE235", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="""

- Domingo - Grupo Acredita é possivel
  19h 00m (reunião aberta* - último domingo do mês)

- Segunda - Grupo Esperança Fé Coragem
  20h 00m (reunião aberta* na terceira semana do mês)

- Terça - Grupo Resulta se trabalhamos para isso
  19h 00m (reunião aberta* - última terça-feira do mês)

- Quarta - Grupo Ação e Oração
  20h 30m

- Quinta - Grupo Renascer Online
  21h 00m

- Sexta - Grupo 12
  21h 00m

- Sábado - Grupo Sábado à noite com CA
  21h 00m (reunião aberta* - primeiro sábado do mês)

Dados de acesso às reuniões Zoom
https://zoom.us/j/xxxxxxxxxx

ID da reunião: xxx xxx xxx
Senha: ca
""", disable_web_page_preview=True, reply_markup=reply_markup
    )
    return SECOND

def end(update: Update, context: CallbackContext) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="""Até já!
E não te esqueças... se precisares de mim basta escreveres:
/ajuda
""")
    return ConversationHandler.END

def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('ajuda', start)],
        states={
            FIRST: [
                CallbackQueryHandler(reunioes, pattern='^' + str(REUNIOES) + '$'),
                CallbackQueryHandler(end, pattern='^' + str(TWO) + '$'),
                CallbackQueryHandler(presenciais, pattern='^' + str(PRESENCIAIS) + '$'),
                CallbackQueryHandler(online, pattern='^' + str(ONLINE) + '$'),
                CallbackQueryHandler(regras, pattern='^' + str(REGRAS) + '$'),
            ],
            SECOND: [
                CallbackQueryHandler(start_over, pattern='^' + str(REUNIOES) + '$'),
                CallbackQueryHandler(end, pattern='^' + str(TWO) + '$'),
            ],
        },
        # fallbacks=[CommandHandler('start', start)],
        fallbacks=[MessageHandler(Filters.command, start)],
    )

    # Add ConversationHandler to dispatcher that will be used for handling updates
    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
