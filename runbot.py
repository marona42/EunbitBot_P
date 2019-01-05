#coding=utf-8
#export PYTHONIOENCODING=utf-8
import sys

import centralcore
import faithcore
import potato

centralcore.ready_bot(sys.argv)
tasks=[]

#add tasks by init platforms connection using connectioncore

#Exampels:
#NAME_discord = centralcore.connectioncore.Discord()
#NAME_discord.task = centralcore.loop.create_task(NAME_discord.start(faithcore.get_key("YOUR KEYS NAME HERE")))
#tasks.append(NAME_discord.task)

if potato.get_nm(): print("central.start_bot()")
centralcore.start_bot(tasks)