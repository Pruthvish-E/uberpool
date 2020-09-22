#sudo fuser -n tcp -k 14231
#14231 14232 14233 14235
import numpy as np
from numpy.linalg import norm



import threading 
import socket 

# import thread module 
from _thread import *

# global variable x 

buffcount=0
d={}



cdb = []
pdb = []

def create_consumer(username, source, destination, seats):
    cdb.append([username, source, destination, seats])

def remove_consumer(username):
    for i in cdb:
        if(i[0] == username):
            cdb.remove(i)

def create_producer(username, source, destination, seats):
    pdb.append([username, source, destination, seats])

def remove_producer(username):
    for i in pdb:
        if(i[0] == username):
            pdb.remove(i)

# create_consumer("c1", (0,0), (2,2), 1)
# create_consumer("c2", (2,0), (2,2), 1)
# create_consumer("c3", (0,2), (2,2), 1)
# create_producer("p1", (0,0), (2,2), 4)
# create_producer("p2", (3,0), (3,1), 1)
# print(cdb)
# print(pdb)


def get_consumer_details(username):
    for i in cdb:
        if username in i:
           s = 'customer name:- '+username+' source:- '+str(i[1][0])+','+str(i[1][1])+' destination:- '+str(i[2][0])+','+str(i[2][1])+' needed seats:- '+str(i[3])
           return s
    return ''


def get_producer_details(username):
    for i in pdb:
        if username in i:
           s = 'driver name:- '+username+' source:- '+str(i[1][0])+','+str(i[1][1])+' destination:- '+str(i[2][0])+','+str(i[2][1])+' seats:- '+str(i[3])
           return s
    return ''




def mapper(pdb, cdb):
    order = {}
    # add booked/not booked bit
    for c in cdb:
        c.append(0)

    # for consumer book a producer if there are seats
    for prod in pdb:
        order[prod[0]] = []
        remain = prod[3]
        #print("producer", prod[0], remain)
        for c in cdb:
            if(c[4] == 1):
                continue
            #print(prod[0], c[0], cdb, remain)
            if(c[3] > remain):
                continue
            order[prod[0]].append([c[0]])
            remain -= c[3]
            c[4] = 1
    return order

# mapper(pdb, cdb)








def server_to_client(cs,buff): 
	# local host IP '127.0.0.1' 



	# message you send to server 
	#message = "shaurya says geeksforgeeks"
	while True: 
		global buffcount	
		if(buffcount==1):
			

	# Define the port on which you want to connect 
			
			#print("aqcuring")
			buff.acquire()
			#print("opening")
			
			f = open("mail.txt", "r")
			message=f.read()
			port = 14231
			if(message[0:6]!="logout"):
				a=message.split(' ')
			
				email = a[1]
				#print("email:- ",email)
				filename=email+".txt"
				print(a)
				# b=a[3:]
				# string='*'
				# x=a[0]+"  "+a[2]+"\n"+string.join(b)
				role = a[7]
				print("role:- ",role)
				print(a)
				print(email,(int(a[2]),int(a[3])),(int(a[4]),int(a[5])),int(a[6]))
				if(role == "driver"):
					create_producer(email,(int(a[2]),int(a[3])),(int(a[4]),int(a[5])),int(a[6]))					
				else:
					create_consumer(email,(int(a[2]),int(a[3])),(int(a[4]),int(a[5])),int(a[6]))


				schedule = mapper(pdb,cdb)
				print("schedule:- ",schedule)
				

				q=open(filename,"w")
				x = ''
				if(role == "driver"):
					x+='Order to collect Customers:-\n\t\t'
					customers = schedule[email]
					for i in customers:
						x+='\n'+get_consumer_details(i[0])+'\n'
						w = open(i[0]+'.txt',"w")
						w.write('Your assigned driver:-\n\t\t'+'\n'+get_producer_details(email)+'\n')
						w.close()
					#print("#################  X:- ",x)
				else:
					x+='Your assigned driver:-\n\t\t'
					for i in schedule.keys():
						if (email in schedule[i]):
							x+='\n'+get_producer_details(i)+'\n'
							w = open(i+'.txt','a+')
							w.write('\n'+get_producer_details(i)+'\n')
							w.close()
							#print("#################  X:- ",x)
							break



				q.write(x)
				q.close()
				f.close()
				buffcount=0
				buff.release()

				global d

				if((email in d) and (d[email][0]!=-1)):
					host=d[email][0]

					s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
					s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

		# connect to server on local computer 
					s.connect((host,port)) 
				
				
			# message sent to server 
					#print("sending")
					buff.acquire()
					y=open(filename,"r")
					contentfile=y.read()
					y.close()
					buff.release()
					s.send(contentfile.encode('ascii')) 
					#print("sent")
					s.close()
			else:

				buffcount=0
				buff.release()
				s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
				s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		# connect to server on local computer 
				host=message[6:]
				#print(host)
				s.connect((host,port)) 
				
				
			# message sent to server 
				#print("sending")
				lgout="logout"
				s.send(lgout.encode('ascii')) 
				#print("sent")
				s.close()

			# messaga received from server 
			#data = s.recv(1024) 

			# print the received message 
			# here it would be a reverse of sent message 
			#print('Received from the server :',str(data.decode('ascii'))) 

			# ask the client whether he wants to continue 
			

		# close the connection 
					


# thread fuction 
def threaded(c,buff,cs,addr): 
	dflag=0

	global d

	for email,ip in d.items():
	    if ip[0] == addr:
	        fromemail=email

	add=fromemail
	print("fromemail:- ",fromemail)
	global buffcount
	while True: 
		#print(buffcount, "in Thread")
		if(buffcount==0):
			buff.acquire()
			f = open("mail.txt", "w")
			#print("hi")
		# reverse the given string from client 
			while(True):
				data = c.recv(1024) 
				data1=str(data.decode('ascii'))
				#print(data1)
				
				if not data: 
					dflag=1
					#print('Bye') 
					
					# lock released on exit 
					cs.release() 
					break

				if(data1!="logout"):
					final=add+' '+data1
					print("final:- ",final)
					f.write(final)
					#print("wrote")
					

				else:
					data1=data1+addr
					f.write(data1)
					d[fromemail][0]=-1
					buffcount=0
									
				
				
			
			if(data1=="logout"):
				buffcount=0
			else:
				buffcount=1
			#print("Buffer",buffcount)	
					
			f.close()
			buff.release()	
				
		if(dflag):
			break
		sleep(5)
	

		# send back reversed string to client 
		#c.send(data) 

	# connection closed 
	c.close() 

def client_to_server(cs,buff): 
	host = "" 

	# reverse a port on your computer 
	# in our case it is 12345 but it 
	# can be anything 
	port = 14232
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((host, port)) 
	print("Socket binded to port : ", port) 

	# put the socket into listening mode 
	s.listen(5) 
	#print("socket is listening") 

	# a forever loop until client wants to exit 
	while True: 

		# establish connection with client 
		c, addr = s.accept() 

		# lock acquired by client 
		cs.acquire() 
		print('Connected to :', addr[0], ':', addr[1],'\n') 

		# Start a new thread and return its identifier 
		start_new_thread(threaded, (c,buff,cs,addr[0],)) 
	s.close() 

def thlogin(c,cs,addr):
	

	while(True):

		data=c.recv(1024)
		data1=str(data.decode('ascii'))

		if not data:
			#print("Wrong")
			cs.release()
			break

		field=data1.split()
		tryemail=field[0]
		trypass=field[1]

		global d

		if tryemail in d:
			if (d[tryemail][1]==trypass):
				d[tryemail][0]=addr
				q=open(tryemail+".txt","r")
				msg="1"+q.read()
				#print(msg)
				q.close()
				c.send(msg.encode('ascii'))


			else:
				c.send("0".encode('ascii'))

		else:
			c.send("0".encode('ascii'))

	c.close()


def threg(c,reg):

	while(True):

		msg=c.recv(1024)
		msg=str(msg.decode('ascii'))

		if not msg:
			#print("Wrong")
			reg.release()
			break

		l=msg.split("*")
		email=l[0]
		star="*"
		password=star.join(l[1:])
		global d
		if email not in d:
			d[email]=["",password]
			q=open(email+".txt","a+")
			q.close()
			msg="Confirmed"
			c.send(msg.encode('ascii'))
		else:
			msd="Not there"
			c.send(msg.encode('ascii'))
	c.close()



def authenticate(cs):
	host = "" 

	# reverse a port on your computer 
	# in our case it is 12345 but it 
	# can be anything 
	port = 14235
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((host, port)) 
	print("Main socket binded to port: ", port) 

	# put the socket into listening mode 
	s.listen(5) 
	print("Main socket is listening\n") 

	# a forever loop until client wants to exit  

		# establish connection with client 
	while(True):
		c, addr = s.accept() 

		# lock acquired by client 
		cs.acquire() 
		print('Connected to :', addr[0], ':', addr[1],'\n') 

		# Start a new thread and return its identifier 
		start_new_thread(thlogin, (c,cs,addr[0],)) 
	s.close() 






def registration(reg):
	host = "" 

	# reverse a port on your computer 
	# in our case it is 12345 but it 
	# can be anything 
	port = 14233
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((host, port)) 
	print("Main socket binded to port: ", port) 

	# put the socket into listening mode 
	s.listen(5) 
	print("Main socket is listening \n") 

	# a forever loop until client wants to exit  

		# establish connection with client 
	while(True):
		c, addr = s.accept() 

		# lock acquired by client 
		reg.acquire() 
		print('Connected to :', addr[0], ':', addr[1],'\n') 

		# Start a new thread and return its identifier 
		start_new_thread(threg, (c,reg,)) 
	s.close()






def main_task(): 
	global x 
	# setting global variable x as 0 
	x = 0

	# creating a lock 
	
	cs = threading.Lock() 
	buff = threading.Lock() 
	reg= threading.Lock()

	# creating threads 
	t1 = threading.Thread(target=client_to_server, args=(cs,buff,)) 
	t2 = threading.Thread(target=server_to_client, args=(cs,buff,))
	t3 = threading.Thread(target=authenticate, args=(cs,)) 
	t4 = threading.Thread(target=registration, args=(reg,)) 
	# start threads 
	t4.start()
	t3.start()
	t1.start() 
	t2.start() 


	# wait until threads finish their job 
	t4.join()
	t3.join()
	t1.join() 
	t2.join() 

if __name__ == "__main__": 
	main_task() 
		 

