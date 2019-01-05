keys={
	#YOUR TOKENS HERE OR
}
#
def get_key(keyname):
		if keyname in keys:
			return keys[keyname]
		else: raise KeyError("There is no key named '" +keyname+"' !")
	#SIMPLE EXAMPLE with using PLAIN dict. STRONGLY RECOMMAND to handle with sure security. 