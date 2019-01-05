#common variables!

def set_loop(lp):
  global loop #not to use local variable
  loop=lp
def set_nm(nm):
  global noisymode
  noisymode=nm
def get_loop():
  return loop
def get_nm(): return noisymode

loop=[]
noisymode=False