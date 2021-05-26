import pandas as pd
import numpy as np
import os
import cv2


def add_to_dataset(f):
    image = cv2.imread(f,cv2.IMREAD_GRAYSCALE)
    img=~image
    if img is not None:
        ret,thresh=cv2.threshold(img,127,255,cv2.THRESH_BINARY)
        ctrs,ret=cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        cnt=sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])
        w=int(28)
        h=int(28)
        maxi=0
        for c in cnt:
            x,y,w,h=cv2.boundingRect(c)
            maxi=max(w*h,maxi)
            if maxi==w*h:
                x_max=x
                y_max=y
                w_max=w
                h_max=h
        im_crop= thresh[y_max:y_max+h_max+10, x_max:x_max+w_max+10]
        im_resize = cv2.resize(im_crop,(28,28))
        im_resize=np.reshape(im_resize,(784,1))
    return im_resize
#cv2.imwrite('save.jpg',bw)

def create_csv(l):
    data=[]
    folders=['0','1','2','3','4','5','6','7','8','9','-','+','times','div','A','b','X','y']
    typedir=0
    for directory in folders:
        j=0
        directory="data/"+directory+"/"
        for filename in os.listdir(directory):
            if filename.endswith(".jpg"):
                f=os.path.join(directory,filename)
                feat=add_to_dataset(f)
                feat=np.append(feat,typedir)
                data.append(feat)
                j+=1
            if j>l-1:
                break
        typedir+=1
    df = pd.DataFrame(data)
    df.to_csv('dataset.csv',index=False)
length_ele=4100
create_csv(length_ele)
    
