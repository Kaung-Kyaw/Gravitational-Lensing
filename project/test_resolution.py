from functions import * 
import numpy as np 
import matplotlib.pyplot as plt 

#creates source image and chosen coordinates
centre = 1000
slength = 2000
swidth = 2000
s = np.zeros(shape=(slength,swidth))
s[centre,centre] = 1

#blank lensed image coordinates
R = np.zeros(shape=(slength,swidth))

#chooses rc as test value
rc = 0.7

#scaling for multiplitcation, and shift of add/subtrac for coordinate change
scale = swidth/2 
shift = swidth/2

#nested loop for finding s1 and s2 with reduced coordinates
#transforms s1 and s2 back into pixel coordinates 
#matches blank R coordinates to einstien lensed source 
for i in range(swidth):
    for j in range(slength):
        r1 = (i/scale)-1
        r2 = (j/scale)-1
        s1,s2 = transform(rc,r1,r2)
        R[i,j] = s[(int((s1+1) *scale)),int((s2+1)*scale)]

#calls funciton to get properties of cricle for rc value
xc,yc,r = Get_Radius(R)
theo_r =np.sqrt(1-rc**2)
exp_r = r/swidth *2
print(f"""
theoretical r : {theo_r}
test data r: {exp_r}
diff: {round((np.abs((theo_r-exp_r)/theo_r) *100))}%""")



#creates figure for source image   
plt.figure()
plt.title("Source Image Before Gravitational Lensing")
plt.imshow(s)
#creates figure for lensed image 
plt.figure()
plt.title("Gravitationally Lensed Image")
plt.imshow(R)
#shows the graphs
plt.show()

