from __future__ import print_function
import multiprocessing
import subprocess
import os
from time import gmtime, strftime
from datetime import datetime
import MySQLdb as my
def pinger( job_q, results_q ):
    DEVNULL = open(os.devnull,'w')
    while True:
        ip = job_q.get()
        if ip is None: break

        try:
            subprocess.check_call(['ping','-c1',ip],
                                  stdout=DEVNULL)
            results_q.put(ip)
        except:
            pass

if __name__ == '__main__':
    pool_size = 255

    jobs = multiprocessing.Queue()
    results = multiprocessing.Queue()

    pool = [ multiprocessing.Process(target=pinger, args=(jobs,results))
             for i in range(pool_size) ]

    for p in pool:
        p.start()

    for i in range(1,109):
        jobs.put('10.45.33.{0}'.format(i))
   
    
    for p in pool:
        jobs.put(None)

    for p in pool:
        p.join()
    output = " "
    a = str(datetime.now())[:19]
    output +=a
    output += " "
    while not results.empty():
        ip = results.get()
        ip += " "
        output +=ip
    db = my.connect(host="localhost",
                user="root",
                passwd="mysqleptp",
                db="KLUIOT"
                )

    cursor = db.cursor()
    id = "LIB6"
    number_of_rows = cursor.execute('''insert into iptable (labno,online) VALUES(%s,%s)''',(id,output))
    db.commit()   # you need to call commit() method to save
    # your changes to the database
    
    
    db.close()
