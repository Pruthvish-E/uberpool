# Import socket module 
import socket 
from datetime import datetime
from _thread import *
import threading 

print_lock = threading.Lock() 
gflag=1



# thread fuction 
def threaded(c): 
	 
	global gflag
		# data received from client 
	#print("In new thread")
	data = c.recv(1024) 
	#print("In new thread 1")
	data1=str(data.decode('ascii'))
	 


	if(data1!="logout"):	# reverse the given string from client 
		f = open("mailclient.txt", "w")
		f.write(data1)
		f.close() 
		#print('Bye') 
				
		# lock released on exit 
		print_lock.release() 
		
		# send back reversed string to client 
		#c.send(data) 

		# connection closed 
		c.close() 
	else:
		gflag=0
		print_lock.release() 
		c.close()


def server_to_client(): 
	host = "" 
	global gflag
	gflag=1
	port = 14231
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((host, port)) 
	#print("socket binded to port", port)
	# reverse a port on your computer 
	# in our case it is 12345 but it 
	# can be anything 
	s.listen(5) 
	#print("socket is listening") 

	# a forever loop until client wants to exit 
	

	while gflag: 
 

		# put the socket into listening mode 
		#print("three terminate 1")
		
		if(gflag):
		# establish connection with client 
			c, addr = s.accept() 
			#print("three terminate 2")
	
			# lock acquired by client 
			print_lock.acquire() 
			#print("three terminate 3")
			#print('Connected to :', addr[0], ':', addr[1],'\n') 

			# Start a new thread and return its identifier 
			start_new_thread(threaded, (c,)) 
			#print("three terminate 4")
	s.close() 



def client_to_server(): 
	# local host IP '127.0.0.1' 
	#host = '192.168.43.50'


	# Define the port on which you want to connect 
	port = 14232



	# message you send to server 
	
	while True: 
		print("\nEnter \n1. Search for a car \n2. Offer a ride \n3. Check Status \n4. Logout\n")
		key=input()
		if (key=="1") :
			
			host='192.168.1.5'
			print("Enter Username:")
			email = input()
			print("Enter Source:")
			source = input()
			print("Enter Destination:")
			destination = input()
			print("Enter number of seats:")
			nseats = input()
			

			s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
			s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			now=datetime.now()
			#ct=now.strftime("%d %B %Y , %H:%M:%S")

			#message2=repaddr+"*"+ct+"*"+message+"\n"

			# connect to server on local computer 
			s.connect((host,port)) 
			message = email+' '+source+' '+destination+' '+nseats+' client'

		# message sent to server 
			s.send(message.encode('ascii')) 

			key="0"
			s.close()

		elif(key=="2"):
			# q=open("mailclient.txt","r")
			# print("\n*******************************************************************************\n")
			# msg=q.readline()
			# while(msg):
			# 	mail=q.readline()
			# 	print(msg,mail,"\n")
			# 	msg=q.readline()
			# q.close()
			# print("\n*******************************************************************************\n")

			host='192.168.1.5'
			print("Enter Username:")
			email = input()
			
			print("Enter Source:")
			source = input()
			print("Enter Destination:")
			destination = input()
			print("Enter number of seats:")
			nseats = input()
			

			s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
			s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			now=datetime.now()
			#ct=now.strftime("%d %B %Y , %H:%M:%S")

			#message2=repaddr+"*"+ct+"*"+message+"\n"

			# connect to server on local computer 
			s.connect((host,port)) 
			message = email+' '+source+' '+destination+' '+nseats+' '+'driver' #

		# message sent to server 
			s.send(message.encode('ascii')) 

			key="0"
			s.close()


		elif(key == "3"):  #TODO

			q=open(email+".txt","r")
			print("\n*******************************************************************************\n")
			msg=q.readline()
			while(msg):
				#mail=q.readline()
				print(msg,"\n")
				msg=q.readline()
			q.close()
			print("\n*******************************************************************************\n")



		elif (key=="4"):
			global gflag
			gflag=0
			host='192.168.1.5'
			s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
			s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			# connect to server on local computer 
			s.connect((host,port))
			message2="logout" 


		# message sent to server 
			s.send(message2.encode('ascii')) 
			s.close()
			break

		else:
			print("Invalid Input\n")
	#print("Out")


		# message received from server 
		#data = s.recv(1024) 

		# print the received message 
		# here it would be a reverse of sent message 
		#print('Received from the server :',str(data.decode('ascii'))) 

		# ask the client whether he wants to continue 

	# close the connection 
	
	 
def login():
	server="192.168.1.5"
	port=14235
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.connect((server,port))
	print("Enter Email ID:")
	email=input()
	print("Enter Password:")
	password=input()
	tup=email+" "+password
	s.send(tup.encode('ascii'))
	data = s.recv(1024)
	data2=str(data.decode('ascii'))
	value=data2[0]
	mail=data2[1:]
	#print(mail)
	if(int(value)==1):
		q=open("mailclient.txt","w")
		q.write(mail)
		q.close()
	s.close()
	return(int(value))

def register():
	server="192.168.1.5"
	port=14233
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.connect((server,port))
	print("Enter new Email ID:")
	email=input()
	print("Enter Password:")
	password=input()
	print("Confirm Password:")
	confpass=input()

	if(password==confpass):
		finalreg=email+"*"+password
		s.send(finalreg.encode('ascii'))
		confirm=s.recv(1024)
		confirm=str(confirm.decode('ascii'))
		if(confirm=="Confirmed"):
			print("\nEmail registered successfully.\n")
			s.close()
			return(1)
		else:
			print("\nEmail already exists.\n")
			s.close()
			return(0)

	else:
		print("\nPasswords do not match.\n")
		s.close()
		return(0)







def main_task(): 
	global x 
	# setting global variable x as 0 
	x = 0

	# creating a lock 
	
	cs = threading.Lock() 
	buff = threading.Lock() 



	while(True):
		print("\nEnter\n1. Login\n2. Register\n3. Exit\n")
		l=input()
		if(l=="1"):
			auth=login()
			if(auth):
			# creating threads 
				t1 = threading.Thread(target=client_to_server) 
				t2 = threading.Thread(target=server_to_client) 

				# start threads 
				t1.start() 
				t2.start() 

				# wait until threads finish their job 
				t1.join() 
				t2.join() 

			else:
				print("\nYou are not authorised.\n")
		elif(l=="2"):
			auth1=register()
			if(auth1):
				auth=login()
				if(auth):
				# creating threads 
					t1 = threading.Thread(target=client_to_server) 
					t2 = threading.Thread(target=server_to_client) 

					# start threads 
					t1.start() 
					t2.start() 

					# wait until threads finish their job 
					t1.join() 
					t2.join()

				else:
					print("\nYou are not authorised.\n")
		elif(l=="3"):
			exit()

		else:
			print("Invalid option.\n")




if __name__ == "__main__": 
	 
	main_task()  
