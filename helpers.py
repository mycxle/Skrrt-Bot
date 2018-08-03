import pyrebase
import numbers
from datetime import datetime
import time

def db_get(db, s, is_list=False, get_items=False):
	nodes = s.split("/")
	n = db.child(nodes[0])
	for i in range(1, len(nodes)):
		n = n.child(nodes[i])
	if is_list == True:
		if not get_items:
			l = list(n.get().val().values())
			l.remove("123")
			return(l)
		else:
			l = list(n.get().val().values())
			l.remove("123")
			return(l)
	return(int(n.get().val()))

def db_set(db, s, val):
	nodes = s.split("/")
	n = db.child(nodes[0])
	for i in range(1, len(nodes)-1):
		n = n.child(nodes[i])
	print("node-1 : " + nodes[-1] + ", strVAL : " + str(val))
	n.update({nodes[-1]:str(val)})
	return val

def db_add(db, s, val):
	nodes = s.split("/")
	n = db.child(nodes[0])
	for i in range(1, len(nodes)):
		n = n.child(nodes[i])
	n.push(str(val))
	return str(val)

def db_remove(db, s, lst, index):
	val = lst[index]
	key = None

	items = db_get(db, s, is_list=True, get_items=True)
	for i in items:
		if i[1] == val:
			print("found the item!")
			key = i[0]
			break
	nodes = s.split("/")
	n = db.child(nodes[0])
	for i in range(1, len(nodes)):
		n = n.child(nodes[i])
	n.child(key).remove()

	return val

def is_bool(val):
	if int(val) in {0, 1}:
		return True
	else:
		return False

def is_pos(val):
	if int(val) > 0:
		return True
	else:
		return False

def is_int(val):
	return isinstance(val, numbers.Integral)

def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset