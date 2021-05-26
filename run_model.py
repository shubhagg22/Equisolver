import cv2
import numpy as np
from keras.models import load_model
from collections import defaultdict

def out_answer(image):
    model=load_model('model')
    if type(image)== type("1"):
        img=cv2.imread(image,cv2.IMREAD_GRAYSCALE)
    else:
        img=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    result=0
    train_data=[]
    fin_rect=[]
    if img is not None:
        img=~img
        ret,thresh=cv2.threshold(img,127,255,cv2.THRESH_BINARY)
        ctrs,ret=cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        cnt=sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])
        w=int(28)
        h=int(28)
        #print(len(cnt))
        rects=[]
        for c in cnt :
            x,y,w,h= cv2.boundingRect(c)
            rect=[x,y,w,h]
            if(w*h>100):
                rects.append(rect)
        #print(rects)
        bool_rect=[]
        for r in rects:
            l=[]
            for rec in rects:
                flag=0
                if rec!=r:
                    if r[0]<(rec[0]+rec[2]+10) and rec[0]<(r[0]+r[2]+10) and r[1]<(rec[1]+rec[3]+10) and rec[1]<(r[1]+r[3]+10):
                        flag=1
                    l.append(flag)
                if rec==r:
                    l.append(0)
            bool_rect.append(l)
        #print(bool_rect)
        dump_rect=[]
        for i in range(0,len(rects)):
            for j in range(0,len(rects)):
                if bool_rect[i][j]==1:
                    area1=rects[i][2]*rects[i][3]
                    area2=rects[j][2]*rects[j][3]
                    if(area1==min(area1,area2)):
                        dump_rect.append(rects[i])
        #print(len(dump_rect))
        final_rect=[i for i in rects if i not in dump_rect]
        mima=[]
        for i in final_rect:
            if len(fin_rect)==0:
                fin_rect.append([final_rect[0]])
                mima.append([final_rect[0][1],final_rect[0][3]])
                continue
            flag=0
            for j in range(len(mima)):
                if not ((i[1]<mima[j][0] and i[1]+i[3]<mima[j][0]) or (i[1]>mima[j][0]+mima[j][1] and i[1]+i[3]>mima[j][0]+mima[j][1])):
                    u=mima[j][0]
                    mima[j][0]=min(mima[j][0],i[1])
                    if mima[j][1]+u < i[3]+i[1]:
                        mima[j][1]=i[3]+i[1]-mima[j][0]
                    else:
                        mima[j][1]=mima[j][1]+u-mima[j][0]
                    fin_rect[j].append(i)
                    flag=1
                    break
            if flag==0:
                mima.append([i[1],i[1]+i[3]])
                fin_rect.append([i])
        for i in fin_rect:
            eq=[]
            for r in i:
                x=r[0]
                y=r[1]
                w=r[2]
                h=r[3]
                im_crop =thresh[y:y+h+10,x:x+w+10]
                im_resize = cv2.resize(im_crop,(28,28))
                im_resize=np.reshape(im_resize,(1,28,28))
                eq.append(im_resize)
            train_data.append(eq)
    superscript_map = {"0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶",
    "7": "⁷", "8": "⁸", "9": "⁹", "a": "ᵃ", "b": "ᵇ", "c": "ᶜ", "d": "ᵈ",
    "e": "ᵉ", "f": "ᶠ", "g": "ᵍ", "h": "ʰ", "i": "ᶦ", "j": "ʲ", "k": "ᵏ",
    "l": "ˡ", "m": "ᵐ", "n": "ⁿ", "o": "ᵒ", "p": "ᵖ", "q": "۹", "r": "ʳ",
    "s": "ˢ", "t": "ᵗ", "u": "ᵘ", "v": "ᵛ", "w": "ʷ", "x": "ˣ", "y": "ʸ",
    "z": "ᶻ", "A": "ᴬ", "B": "ᴮ", "C": "ᶜ", "D": "ᴰ", "E": "ᴱ", "F": "ᶠ",
    "G": "ᴳ", "H": "ᴴ", "I": "ᴵ", "J": "ᴶ", "K": "ᴷ", "L": "ᴸ", "M": "ᴹ",
    "N": "ᴺ", "O": "ᴼ", "P": "ᴾ", "Q": "Q", "R": "ᴿ", "S": "ˢ", "T": "ᵀ",
    "U": "ᵁ", "V": "ⱽ", "W": "ᵂ", "X": "ˣ", "Y": "ʸ", "Z": "ᶻ", "+": "⁺",
    "-": "⁻", "=": "⁼", "(": "⁽", ")": "⁾"}
    equations=[]
    for eq in range(len(train_data)):
        s=[]
        for i in range(len(train_data[eq])):
            train_data[eq][i]=np.array(train_data[eq][i])
            train_data[eq][i]=train_data[eq][i].reshape(1,28,28,1)
            result=np.argmax(model.predict(train_data[eq][i]), axis=-1)
            if(i>0 and result[0]==10 and s[-1]=="-"):
                if fin_rect[eq][i-1][0]+fin_rect[eq][i-1][2] > fin_rect[eq][i][0]:
                    s[-1]="="
                    continue
            if(i>0 and result[0]>=0 and result[0]<10 and s[-2] in ['x','y','a','b']):
                if fin_rect[eq][i-1][1]+fin_rect[eq][i-1][3]/2>=fin_rect[eq][i][1]:
                    s[-1]=str(result[0])
                    continue
            if(result[0]==1 or result[0]==10):
                tanx=fin_rect[eq][i][1]/fin_rect[eq][i][0]
                if tanx>=1 and tanx<=5.68:
                    result[0]=13
            if result[0]==17:
                s.append('y')
                s.append('1')
            elif result[0]==16:
                s.append('x')
                s.append('1')
            elif result[0]==15:
                s.append('b')
                s.append('1')
            elif result[0]==14:
                s.append('a')
                s.append('1')
            elif result[0]==10:
                s.append('-')
            elif(result[0]==11):
                s.append('+')
            elif(result[0]==12):
                s.append('*')
            elif(result[0]==13):
                s.append('/')
            elif(result[0]==0):
                s.append('0')
            elif(result[0]==1):
                s.append('1')
            elif(result[0]==2):
                s.append('2')
            elif(result[0]==3):
                s.append('3')
            elif(result[0]==4):
                s.append('4')
            elif(result[0]==5):
                s.append('5')
            elif(result[0]==6):
                s.append('6')
            elif(result[0]==7):
                s.append('7')
            elif(result[0]==8):
                s.append('8')
            elif(result[0]==9):
                s.append('9')
        equations.append(s)
    n=len(equations)
    if n==0:
        return False
    elif n==1:
        if "=" not in equations[0]:
            s=""
            for i in equations[0]:
                s+=i
            try:
                ans=eval(s)
                return(s,str(ans))
            except:
                return(s,'Falsely Recognized')
        else:
            string=""
            quadratic=False
            for i in range(len(equations[0])):
                if equations[0][i-1] in ['x','y','a','b']:
                    if equations[0][i]!="1":
                        quadratic=True
                        string+=superscript_map[equations[0][i]]
                    continue
                else:
                    string+=equations[0][i]
            if quadratic==False:
                equation=equations[0]
                var=[]
                s=""
                d=defaultdict(int)
                i=0
                flag=1
                while i<len(equation):
                    if equation[i] not in ['x','y','a','b','+','-','=']:
                        s+=equation[i]
                    else:
                        if equation[i]=="+" or equation[i]=="-":
                            if s!="":
                                try:
                                    d['c']+=flag*eval(s)
                                except:
                                    return (string,'Falsely Recognized')
                            s=equation[i]
                        elif equation[i]=="=":
                            if s!="":
                                try:
                                    d['c']+=flag*eval(s)
                                except:
                                    return (string,'Falsely Recognized')
                            s=""
                            flag=-1
                        else:
                            if s=="" and i==0:
                                s="1"
                            if s=="+":
                                s="1"
                            if s=="-":
                                s="-1"
                            if s!="":
                                try:
                                    d[equation[i]]+=flag*eval(s)
                                except:
                                    return (string,'Falsely Recognized')
                                var.append(equation[i])
                                s=""
                            i+=1
                    i+=1
                if s!="":
                    d['c']+=flag*eval(s)
                val_x=-(d['c'])/d[var[0]]
                return (string,var[0]+" = "+str(val_x))
            else:
                equation=equations[0]
                var=[]
                d=defaultdict(int)
                s=""
                i=0
                flag=1
                while i<len(equation):
                    if equation[i] not in ['x','y','a','b','+','-','=']:
                        s+=equation[i]
                    else:
                        if equation[i]=="+" or equation[i]=="-":
                            if s!="":
                                try:
                                    d['c']+=flag*eval(s)
                                except:
                                    return (string,'Falsely Recognized')
                            s=equation[i]
                        elif equation[i]=="=":
                            if s!="":
                                try:
                                    d['c']+=flag*eval(s)
                                except:
                                    return (string,'Falsely Recognized')
                            s=""
                            flag=-1
                        else:
                            c=""
                            if i<len(equation)-1:
                                if equation[i+1]=="2":
                                    c="a"
                                elif equation[i+1]=="1":
                                    c="b"
                            if s=="" and i==0:
                                s="1"
                            if s=="+":
                                s="1"
                            if s=="-":
                                s="-1"
                            if s!="":
                                try:
                                    d[c]+=flag*eval(s)
                                except:
                                    return (string,'Falsely Recognized')
                                var.append(equation[i])
                                s=""
                            i+=1
                    i+=1
                if s!="":
                    d['c']+=flag*eval(s)
                print(d)
                from cmath import sqrt as csqrt
                from math import sqrt
                D= d['b']**2-4*d['a']*d['c']
                if D<0:
                    val_x1=(-d['b']+csqrt(D))/(2*d['a'])
                    val_x2=(-d['b']-csqrt(D))/(2*d['a'])
                else:
                    val_x1=(-d['b']+sqrt(D))/(2*d['a'])
                    val_x2=(-d['b']-sqrt(D))/(2*d['a'])
                if val_x1==val_x2:
                    return (string,var[0]+" = "+str(val_x1))
                return (string,var[0]+" = "+str(val_x1)+" "+var[0]+" = "+str(val_x2))
    else:
        equ=[]
        var=[]
        string=""
        for equation in equations:
            for i in range(len(equation)):
                if equation[i-1] in ['x','y','a','b']:
                    continue
                string+=equation[i]
            string+=" "
        for equation in equations:
            d=defaultdict(int)
            s=''
            i=0
            flag=1
            while i<len(equation):
                if equation[i] not in ['x','y','a','b','+','-','=']:
                    s+=equation[i]
                else:
                    if equation[i]=="+" or equation[i]=="-":
                        if s!="":
                            try:
                                d['c']+=flag*eval(s)
                            except:
                                return (string,'Falsely Recognized')
                        s=equation[i]
                    elif equation[i]=="=":
                        if s!="":
                            try:
                                d['c']+=flag*eval(s)
                            except:
                                return (string,'Falsely Recognized')
                        s=""
                        flag=-1
                    else:
                        if s=="" and i==0:
                                s="1"
                        if s=="+":
                                s="1"
                        if s=="-":
                                s="-1"
                        if s!="":
                            try:
                                d[equation[i]]+=flag*eval(s)
                            except:
                                return (string,'Falsely Recognized')
                            var.append(equation[i])
                            s=""
                        i+=1
                i+=1
            if s!="":
                d['c']+=flag*eval(s)
            equ.append(d)
        val_y=-(equ[1][var[0]]*equ[0]['c']-equ[0][var[0]]*equ[1]['c'])/(equ[1][var[0]]*equ[0][var[1]]-equ[0][var[0]]*equ[1][var[1]])
        val_x=-(equ[0][var[1]]*val_y+equ[0]['c'])/equ[0][var[0]]
        return (string,var[0]+" = "+str(val_x)+" "+var[1]+" = "+str(val_y))

if __name__ == '__main__':
    print(out_answer('save.png'))
