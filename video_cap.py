import cv2
import numpy as n
import time
import matplotlib.pyplot as plt
import os

def downscale(frameg,dec=10):
    width = int(frameg.shape[1] / float(dec))
    height = int(frameg.shape[0] / float(dec))
    dim = (width, height)
    # resize image and normalize
    resc=n.array(cv2.resize(frameg, dim, interpolation = cv2.INTER_AREA),dtype=n.float32)
    resc=resc/n.sqrt(n.mean(resc**2.0))
    return(resc)

def start_cap(hist_len=300,
              dname="vs",
              logfile="vs/cam.log",
              image_quality=30,
              max_fps=5,
              thresh=10.0):

    os.system("mkdir -p %s"%(dname))
    f=open(logfile,"w")
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), image_quality]
    video_capture = cv2.VideoCapture(1)
    # Check success
    if not video_capture.isOpened():
        raise Exception("Could not open video device")
    # Set properties. Each returns === True on success (i.e. correct resolution)
    video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    fi=0
    sd_hist=n.zeros(hist_len)
    sd_hist[:]=n.nan
    noise_floor = 1.0
    prev_cap_t = time.time()
    min_dt = 1.0/max_fps
    while True:
        t0=time.time()
        # Read picture. ret === True on success
        ret, frame = video_capture.read()

        # downscale to denoise a bit
        frameg = downscale(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
        
        if fi > 0:
            diff=n.sum(n.abs(frameg-prev_frame)**2.0)
            #            plt.imshow(frameg-prev_frame)
            #           plt.colorbar()
            #          plt.show()
            if fi == 1:
                cv2.imshow("frame",frame)
                cv2.imshow("det",frameg-prev_frame)                
                key=cv2.waitKey(10)
  
                       
            sd_hist[fi%hist_len]=diff
            noise_floor = n.nanmedian(sd_hist)
            noise_std = n.nanmean(n.abs(sd_hist-noise_floor))
            
            if n.abs(diff - noise_floor) > thresh*noise_std and ( (t0-prev_cap_t) > min_dt ) and fi > hist_len:
                t_event=time.time()
                prev_cap_t=t_event
                val=n.abs(diff - noise_floor)/noise_std
                print("detection %1.2f val %1.2f"%(t_event,val))
                cv2.imshow("frame",frame)
                cv2.imshow("det",frameg-prev_frame)                
                key=cv2.waitKey(100)
                f.write("%f detection %1.2f noise_floor %1.2f noise_std %1.2f\n"%(time.time(),n.abs(diff-noise_floor)/noise_std,noise_floor,noise_std))
                cv2.imwrite("vs/test-%1.2f.jpg"%(t_event),frame,encode_param)

                
  #              plt.plot(sd_hist)
   #             plt.show()
        prev_frame=frameg
        fi+=1
        t1=time.time()
        if fi%10 == 0 and fi > 0:
            print("%f fps %1.2f noise_floor %1.2f noise_std %1.6f\n"%(time.time(),1.0/(t1-t0),noise_floor,noise_std))
        

    video_capture.release()

start_cap()
