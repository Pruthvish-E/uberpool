import numpy as np
from numpy.linalg import norm

'''
class consumer:
    def __init__(self, username, source, destination, seats):
        self.username = username
        self.source = source
        self.destination = destination
        self.seats = seats

c = consumer("foo", (1, 2), (4,6), 1)
print(c.username)
print(c.source)
'''

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




create_consumer("c1", (0,0), (2,2), 1)
create_consumer("c2", (2,0), (2,2), 1)
create_consumer("c3", (0,2), (2,2), 1)
create_producer("p1", (0,0), (2,2), 4)
create_producer("p2", (3,0), (3,1), 1)
#print(cdb)
print(pdb)

'''
# if sarr[p[3]] lies on the line then accept else reject
#if(seatarr[p[3]] > totalseats or sarr[p[3]][1] != m*sarr[p[3]][0] + c):
    #continue

def mapper(pdb, cdb):
    order = {}
    for prod in pdb:
        order[prod[0]] = list()
        remaining_seat = prod[3]
        print("producer", prod[0], remaining_seat)
        src = np.asarray(prod[1])
        dest = np.asarray(prod[2])
        #a = dest[1] - src[1]
        #b = dest[0] - src[0]
        #if(b):
            #m = a/b
            #c = src[1] - m*src[0]
            #print(m, c)
        #else:
            #c = src[0]
            #print(c)
        temp = []
        for c in cdb:
            if(not(remaining_seat)):
                break
            if(c[3] > remaining_seat):
                continue
            d = norm(np.cross(dest - src, src - c[1]))/norm(dest - src)
            #temp.append([c[0], d])
            order[prod[0]].append([c[0], d])
            cdb.remove(c)
            remaining_seat -= c[3]
            print("distance between", prod[0], "and", c[0], d)
            print(cdb)
        #temp.sort(key = lambda x : x[1])
    print(order)
'''

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

#mapper(pdb, cdb)
print(get_producer_details('p'))
print(get_consumer_details('c'))


role = "driver"
email = "p1"

schedule = mapper(pdb,cdb)
print("schedule:- ",schedule)


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

print(x)