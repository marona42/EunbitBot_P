#coding=utf-8
#export PYTHONIOENCODING=utf-8
#여러 플랫폼에서 사용 가능한 하나의 봇
#아이디어: 단답형이 아닌 대화형의 경우 클래스를 만들고 그 인스턴스가 각각 하나의 대화를 담당하게 하기.
#TODO: 코어의 return을 str로 하지 않고 그것을 불러온 모듈의 출력을 호출시켜서 결과내기.

#import pymysql
import sys #for argument

import asyncio #essential to hosting bot
import threading #not using for now

import potato
import charactercore 
import connectioncore 

def ready_bot(arguments):
	"""sys arguments!"""
	potato.set_nm(False) 	#default: noisy mode=off
	if "-n" in arguments[1:] or "--noisy" in arguments[1:]: potato.set_nm(True)
	if potato.get_nm(): print("central ready_bot()")
	
def start_bot(tasks):
	"""run async loop with tasks list"""
	platforms=asyncio.gather(*tasks,loop=loop)
	loop.run_until_complete(platforms)

loop = asyncio.get_event_loop()
potato.set_loop(loop)