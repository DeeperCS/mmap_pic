from multiprocessing import Process
import mmap
import contextlib
import time
import os, cv2
import numpy as np

def reader(share_file, img_shape):
    img_size = np.prod(img_shape)
    
    # reader 
    while True:
        with contextlib.closing(mmap.mmap(-1, img_size, tagname=share_file, access=mmap.ACCESS_READ)) as mem:
            # read data 
            share_data = mem.read(img_size)  
            
            # convert, reshape and save to image
            img = np.frombuffer(share_data, dtype=np.uint8).reshape(img_shape)
            cv2.imwrite("received.png", img)
            print("saved to img")

        time.sleep(5)


if __name__ == '__main__':
    share_file_tmp = "tmp"
    img_shape = (257, 257, 3)
    
    p_reader = Process(target=reader, args=(share_file_tmp, img_shape))
    p_reader.start()
    p_reader.join()