from multiprocessing import Process
import mmap
import contextlib
import time
import os, cv2
import numpy as np


def writer(share_file_name, img_shape):
    idx = 0
    
    img_size = np.prod(img_shape)
    
    with contextlib.closing(mmap.mmap(-1, img_size, tagname=share_file_name, access=mmap.ACCESS_WRITE)) as mem:    
        # writer 
        while True:
            # load data (from image or video)
            im = cv2.imread("{}.png".format(idx%3))
            byte_content = im.tobytes()
            print('{} Write data to share memory! length:{}'.format(idx, len(byte_content)))
            
            # write to share memory
            mem.seek(0)
            mem.write(byte_content)
            mem.flush()
            
            # take a rest
            time.sleep(5)
            idx += 1


if __name__ == '__main__':
    share_file_tmp = "tmp"
    
    img_shape = (257, 257, 3)
    
    p_writer = Process(target=writer, args=(share_file_tmp, img_shape))
    p_writer.start()
    p_writer.join()
    
    
    
    


