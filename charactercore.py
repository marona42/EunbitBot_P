import os #for know path
import sys #for call this module
import json #for messaging & monolog

"""고유기능을 처리하는 모듈로, _(이름) 메소드들을 제외한 메소드들은 각 플랫폼을 통해 실행할 수 있고, !목록으로 그 종류를 확인할 수 있습니다.
	_(메소드)의 경우, 각 기능에 간접적으로 쓰이는 메소드로, !목록 에는 안 뜨지만, 그 기능들 중간중간에 쓰입니다."""


def _목록(): return [x for x in dir(core) if not x.startswith('_') and callable(getattr(core,x))]#dir 그냥 쓰면 내부 변수까지 가져와요 callable이 호출 가능한 메소드들 목록
def _o목록(): return [x[1:] for x in dir(core) if x.startswith('o') and callable(getattr(core,x))]#예전 string 반환하는 형식의 함수들 목록 (결과값 앞에 o 없음!)
def _몰랑(): return random.choice(["",""]) #모르는 명령어 반응
def o목록(message):
	"""제가 지원하는 기능들을 알려줘요."""
	return ', '.join(_목록()) +" 같은게 있어요!"
def o도움(message):
	"""각 기능들의 docstring을 읽어서 말해줘요. 그러니까 쉽게 말해서 그 기능이 뭘 하는지 알려줘요."""
	texts=message['text'].split()
	if len(texts)==1: return "도움말이 필요한 기능을 뒤에 붙여주세요."
	elif texts[1] not in _목록(): return texts[1]+_몰랑()
	elif getattr(core,texts[1]).__doc__ is None: return "" #모르는 명령어 반응
	else: return getattr(core,texts[1]).__doc__
	
async def 십초(message,caller):
	"""caller 호출형 기능 샘플: 10초뒤에 다시 한번 알려줘요."""
	texts=message['text'].split()
	await caller.out_message(caller.message_d['channel'],"10초뒤 다시 알려줄게요.")
	await timecore.set_alarm(s=10)
	await caller.out_message(caller.message_d['channel'],"10초 끝!")
async def 출력(message,caller):
	"""caller 호출형 기능: 샘플"""
	await caller.out_message(caller.message_d['channel'],">_<")
	
	
core = sys.modules[__name__]

if __name__ == "__main__":
	print("봇 인격모듈")
	