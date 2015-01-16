import socket
import time
import datetime

#sock = socket.create_connection(("10.0.19.4", 30001))
sock = socket.create_connection(("10.0.19.4", 30002))

data = 13000* "0"
def benchmark_send(conn, sleep_time = 0.001,duration_in_sec=15):
    
    start = datetime.datetime.now()
    while (datetime.datetime.now()-start).total_seconds() < duration_in_sec:
        conn.send(data)
        if sleep_time > 0:
            time.sleep(sleep_time)
        #print i
    conn.close()

def benchmark_receive(conn, sleep_time = 0.001, duration_in_sec=15):
    start = datetime.datetime.now()
    while (datetime.datetime.now()-start).total_seconds() < duration_in_sec:
        conn.recv(13000)
        if sleep_time > 0:
            time.sleep(sleep_time)
        #print i
    conn.close()  

def run_benchmark():
    timings = [0.03, 0.01, 0.005, 0.0025, 0.00125, 0.000775, 0]
    for t in timings:
        sock_send = socket.create_connection(("10.0.19.4", 30001))
        benchmark_send(sock_send, t)    
        
        sock_recv = socket.create_connection(("10.0.19.4", 30002))
        benchmark_receive(sock_recv, t)
    print "done..."
    
if __name__=="__main__":
    run_benchmark()

