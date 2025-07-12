from bot.plugins import music
from bot.command import Command


command = Command()
command.include_command(music.command)
