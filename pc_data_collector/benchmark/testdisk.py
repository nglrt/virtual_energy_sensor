#!/usr/bin/env python

import time, math, os, tempfile

def humanize_bytes(bytes, precision=1):
    """Return a humanized string representation of a number of bytes.

    Assumes `from __future__ import division`.

    >>> humanize_bytes(1)
    '1 byte'
    >>> humanize_bytes(1024)
    '1.0 kB'
    >>> humanize_bytes(1024*123)
    '123.0 kB'
    >>> humanize_bytes(1024*12342)
    '12.1 MB'
    >>> humanize_bytes(1024*12342,2)
    '12.05 MB'
    >>> humanize_bytes(1024*1234,2)
    '1.21 MB'
    >>> humanize_bytes(1024*1234*1111,2)
    '1.31 GB'
    >>> humanize_bytes(1024*1234*1111,1)
    '1.3 GB'
    """
    abbrevs = (
        (1<<50L, 'PB'),
        (1<<40L, 'TB'),
        (1<<30L, 'GB'),
        (1<<20L, 'MB'),
        (1<<10L, 'kB'),
        (1, 'bytes')
    )
    if bytes == 1:
        return '1 byte'
    for factor, suffix in abbrevs:
        if bytes >= factor:
            break
    return '%.*f %s' % (precision, bytes / factor, suffix)

def rated_write_to_file(fileobject, rate, interval):
    """rate:byte/sec, interval:sec"""
    
    blocks_per_sec = rate/102400
    block_freq = 1.0/ blocks_per_sec

    bu = bytearray(b'\x00' * 102400)
    
    start = time.time()
    
    print "Block freq is %s" % block_freq    
    
    while time.time() - start < interval:
        fileobject.write(bu)
        time.sleep(block_freq)
        
    fileobject.flush()
        

def rated_read_to_file(fileobject, rate, interval):
    """rate: byte/sec, interval: sec"""
    blocks_per_sec = rate/102400
    block_freq = 1.0/ blocks_per_sec

    start = time.time()    
    
    fileobject.seek(0)    
    
    while time.time() - start < interval:
        
        data = fileobject.read(102400)
        time.sleep(block_freq)


def run_single_benchmark(rate, interval):
    with tempfile.NamedTemporaryFile('wb+') as foo:
        start = time.time()
        rated_write_to_file(foo, rate, interval)
        end = time.time()
        
        foo.seek(0)
    
        start = time.time()
        rated_read_to_file(foo, rate, interval)
        end = time.time()
    
        print "Writing timme ------------------>  " + str(end - start)
        print "Reading time ------------------->  " + str(end - start)
        print "File size    ------------------->  " + humanize_bytes(foo.tell()) 
    

def run_benchmark():
    run_single_benchmark(1000*1000, 10) # 1 MByte
    run_single_benchmark(10*1000*1000, 10) # 10 MByte
    run_single_benchmark(20*1000*1000, 10) # 20 MByte
    run_single_benchmark(40*1000*1000, 10) # 40 MByte
    run_single_benchmark(80*1000*1000, 10) # 80 MByte
    run_single_benchmark(160*1000*1000, 40) # 160 MByte
    
    print "done"
    
if __name__=="__main__":
    run_benchmark()