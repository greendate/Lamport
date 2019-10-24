from multiprocessing import Process, Pipe
from os import getpid
from datetime import datetime


def local_time(counter):
    return ' (LAMPORT_TIME={}, LOCAL_TIME={})'.format(counter, datetime.now())


def calc_recv_timestamp(recv_time_stamp, counter):
    return max(recv_time_stamp, counter) + 1


def calc_recv_timestamp(recv_time_stamp, counter):
    for i in range(len(counter)):
        counter[i] = max(recv_time_stamp[i], counter[i])
    return counter


def event(pid, counter):
    counter[pid] += 1
    print('Something happened in {} !'.\
          format(pid) + local_time(counter))
    return counter


def send_message(pipe, pid, counter):
    counter[pid] += 1
    pipe.send(('Empty shell', counter))
    print('Message sent from ' + str(pid) + local_time(counter))
    return counter


def recv_message(pipe, pid, counter):
    message, timestamp = pipe.recv()
    counter[pid] += 1
    counter = calc_recv_timestamp(timestamp, counter)
    print('Message received at ' + str(pid)  + local_time(counter))
    return counter


def process_one(pipe12):
    pid = 0
    counter = [0, 0, 0]
    counter = send_message(pipe12, pid, counter)
    counter = send_message(pipe12, pid, counter)
    counter = event(pid, counter)
    counter = recv_message(pipe12, pid, counter)
    counter = event(pid, counter)
    counter = event(pid, counter)
    counter = recv_message(pipe12, pid, counter)

def process_two(pipe21, pipe23):
    pid = 1
    counter = [0, 0, 0]
    counter = recv_message(pipe21, pid, counter)
    counter = recv_message(pipe21, pid, counter)
    counter = send_message(pipe21, pid, counter)
    counter = recv_message(pipe23, pid, counter)
    counter = event(pid, counter)
    counter = send_message(pipe21, pid, counter)
    counter = send_message(pipe23, pid, counter)
    counter = send_message(pipe23, pid, counter)


def process_three(pipe32):
    pid = 2
    counter = [0, 0, 0]
    counter = send_message(pipe32, pid, counter)
    counter = recv_message(pipe32, pid, counter)
    counter = event(pid, counter)
    counter = recv_message(pipe32, pid, counter)


if __name__ == '__main__':
    p12, p21 = Pipe()
    p23, p32 = Pipe()

    process1 = Process(target=process_one,
                       args=(p12,))
    process2 = Process(target=process_two,
                       args=(p21, p23))
    process3 = Process(target=process_three,
                       args=(p32,))

    process1.start()
    process2.start()
    process3.start()

    process1.join()
    process2.join()
    process3.join()
