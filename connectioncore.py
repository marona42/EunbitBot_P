import discord
import websockets #for Slack
from slacker import Slacker	#for Slack
import socket	#for IRC
import json #for parsing slack message
from abc import * #for IOmodule_blueprint

import sys

from charactercore import core
import potato

class AlreadyConnectedError(Exception):
	def __init__(self,message):
		print(message+"는 이미 연결된 인스턴스입니다!")

class IOmodule_blueprint(metaclass=ABCMeta):		#이름 나중에 생각해서 바꾸기
	def get_connect():#생성자에 바로 연결
		raise NotImplementedError
	def get_disconnect():
		raise NotImplementedError

	def run_bot():
		raise NotImplementedError

	def set_myinfo():
		raise NotImplementedError
	def out_message(): #기본적인(간단한-RAW) 메세지 출력동작
		raise NotImplementedError

	
class Slack(IOmodule_blueprint):
	"""Slack 메신저의 I/O를 다룹니다."""
	def __init__(self):
		self.connected=False

	async def run_bot(self):								###봇 실행기
		self.ws = await websockets.connect(self.talkurl)
		while True:
			self.message_json = await self.ws.recv()

			self.message=json.loads(self.message_json,encoding='utf-8')
			if potato.get_nm() : print(self.message)
			self.message['platform']="Slack"
			if self.message.get('type')=='message' and self.message.get('text') and not self.message.get('is_im') and self.message.get('text')[0]=='!':
				self.commands=self.message.get('text').split()
				try:
					if self.commands[0][1:] in core._목록():
						if self.commands[0][1:] in core._o목록():		#o목록에 o함수들이 정리되어있음
							await self.out_message(self.message_d['channel'],getattr(core,'o'+self.commands[0][1:])(self.message_d),self.message_d) #o붙여서 호출!
						else:
							await getattr(core,self.commands[0][1:])(self.message_d,self)			#message caller 넘겨줌
					else:
						self.out_message(self.message['channel'],self.message.get('text')[0][1:]+core._몰랑())
				except Exception as e:
					self.out_message(self.message['channel'],e)
					self.out_message(self.message['channel'],"") #에러메세지 발생 알림 멘트
		
	def set_connect(self,con_token):
		
		if(self.connected):
			raise AlreadyConnectedError("Slack")
		
		self.atoken=con_token
		self.SL=Slacker(self.atoken)
		self.talker=self.SL.rtm.start()
		self.talkurl=self.talker.body['url']

		self.task = potato.get_loop().create_task(self.run_bot())
		self.connected=True
		print("Connected at Slack")
		
	def get_task(self): return self.task

	def out_message(self,channel_q,text_q):
		self.SL.chat.post_message(channel=channel_q,text=text_q,as_user=True)
	
	def out_message_heavy(self,channel_q,attachment_dict):#"""양식 있는 메세지를 만듭니다. 언젠간 쓰겠지."""
		self.SL.chat.post_message(channel=channel_q,text=None,attachments=[attachments_dict],as_user=True)

class Discord(IOmodule_blueprint,discord.Client):

	async def out_message(self,channel,text,message=None):
		await self.send_message(channel,text)

	async def on_ready(self):
		print('Connected at discord as '+ self.user.name)
	
	async def on_message(self,message):		#http://discordpy.readthedocs.io/en/latest/api.html#message
		self.message_d={'channel':message.channel,'text':message.content,'user':message.author,'platform':'discord'}
		if potato.get_nm(): print('channel :',self.message_d['channel'],'/ text :',self.message_d['text'],'/ user :',self.message_d['user'])
		if message.content.startswith('!'):
			self.commands=str(message.content).split()
			try:
				if self.commands[0][1:] in core._목록():
					if self.commands[0][1:] in core._o목록():		#o목록에 o함수들이 정리되어있음
						await self.out_message(self.message_d['channel'],getattr(core,'o'+self.commands[0][1:])(self.message_d),self.message_d) #o붙여서 호출!
					else:
						await getattr(core,self.commands[0][1:])(self.message_d,self)			#caller로 클래스를 넘겨줌
				else:
					await self.out_message(self.message_d['channel'],self.commands[0][1:]+core._몰랑())
			except Exception as e:
					await self.out_message(self.message_d['channel'],e)
					await self.out_message(self.message_d['channel'],"")#에러메세지 발생 알림 멘트
				
			#await client.send_message(message.channel, 'leave message')		#반응받기
			#msg = await client.wait_for_message(timeout=15.0, author=message.author)
