import numpy as np
import random
import matplotlib.pyplot as plt
import scipy.constants
from skimage import measure, feature, io, color, draw
from functions import *
from PIL import Image 

#works out and defines values from slide, including rc to use for lens equation
R_c = 70 * (10**-3)
D_s = 878
D_i = 637
D_ls = 441
sigma = 1500 * 10 ** 3
c = scipy.constants.c
pi = scipy.constants.pi
theta_E = 4 * pi * (sigma ** 2) * D_ls / (c ** 2 * D_s)
rc = R_c / (D_i * theta_E)


#outputs results of equations above (theoretical values)
print(f"""
r_c:  {round(rc,3)}
Theta_E {theta_E}
D_s: {D_s}
D_i: {D_i}
D_ls: {D_ls}
""")

#Defines properties of source image coordinate plane 
width = 2000
height = 2000
s = np.zeros(shape=(width, height))
max_radius = None

#scaling for multiplitcation
scale = width/2

#generates nested loop to centre galaxy cluster and run through probability
for x in range(width):
    for y in range(height):
        x_ = (scale - x - 1)
        y_ = (scale - y - 1)
        r = np.sqrt(x_ ** 2 + y_ ** 2)
        density = get_density(r, a=20, max_radius=max_radius)
        if probability(density):
            s[x][y] = 1

#blank lensed image coordinates
R = np.zeros(shape=(width,height))
epsilon = 0
#nested loop for finding s1 and s2 with reduced coordinates
for i in range(width):
    for j in range(height):
        r1 = (i/scale)-1
        r2 = (j/scale)-1
        s1,s2 = transform(rc,r1,r2,epsilon)
        R[i,j] = s[(int((s1+1)*scale)),int((s2+1)*scale)]

#Fetches actual Image
im = Image.open('1.jpg')
imarray = np.array(im)
imwidth = imarray.shape[0]
imheight = imarray.shape[1]


#crerates blank lensed coordinate 
lensed = np.zeros(shape=(imarray.shape[0],imarray.shape[1],3))
#new shifting and scaling
imshift = imwidth/2
#nested loop to get [-1,1] coordinates and run it through lensing equation
for i in range(imwidth):
    for j in range(imheight):
        r1 = (i/imshift) -1 
        r2 = (j/imshift)-1
        s1,s2 = transform(rc,r1,r2,epsilon)
        lensed[i,j] = imarray[(int((s1+1)*imshift)),int((s2+1)*imshift)]

#Fetches actual Image of Stars
im_star = Image.open('stars.jpg')
imarray_star = np.array(im_star)
imwidth_star = imarray_star.shape[0]
imheight_star = imarray_star.shape[1]


#crerates blank lensed coordinate 
lensed_star = np.zeros(shape=(imarray_star.shape[0],imarray_star.shape[1],3))
#new shifting and scaling
imshift_star = imwidth_star/2
#nested loop to get [-1,1] coordinates and run it through lensing equation
for i in range(imwidth_star):
    for j in range(imheight_star):
        r1 = (i/imshift_star) -1 
        r2 = (j/imshift_star)-1
        s1,s2 = transform(rc,r1,r2,epsilon)
        lensed_star[i,j] = imarray_star[(int((s1+1)*imshift_star)),int((s2+1)*imshift_star)]

#Fetches actual Image of Stars
im_cluster = Image.open('Cluster.jpg')
imarray_cluster = np.array(im_cluster)
imwidth_cluster = imarray_cluster.shape[0]
imheight_cluster = imarray_cluster.shape[1]

#crerates blank lensed coordinate 
lensed_cluster = np.zeros(shape=(imarray_cluster.shape[0],imarray_cluster.shape[1],3))
#new shifting and scaling
imshift_cluster = imwidth_cluster/2
#nested loop to get [-1,1] coordinates and run it through lensing equation
for i in range(imwidth_cluster):
    for j in range(imheight_cluster):
        r1 = (i/imshift_cluster) -1 
        r2 = (j/imshift_cluster)-1
        s1,s2 = transform(rc,r1,r2,epsilon)
        lensed_cluster[i,j] = imarray_cluster[(int((s1+1)*imshift_cluster)),int((s2+1)*imshift_cluster)]


# take radius of ring
# radius divided by number of pixels to get %
# multiply by 2 as rc exists in [-1,1] reduced coordinates
# R should be ~ 0.7 in reduced coordinates 
xc,yc,r = Get_Radius(R)
theo_r =np.sqrt(1-rc**2)
exp_r = r/width *2
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

#creates figure for actual image of single galaxy
plt.figure()
plt.title("Actual Image of Glaxy")
plt.imshow(imarray)

#creates figure for lensed image of real cluster, too bright to see so scaled down by 255
plt.figure()
plt.title("Einstein Ring of Actual Galaxy")
plt.imshow(lensed/255)

#creates figure for actual image of stars cluster
plt.figure()
plt.title("Actual Image of Star Clusters")
plt.imshow(imarray_star)

#creates figure for lensed image of real cluster, too bright to see so scaled down by 255
plt.figure()
plt.title("Einstein Ring of Stars")
plt.imshow(lensed_star/255)

#creates figure for another actual image of galaxy clusters
plt.figure()
plt.title("Actual Image of Galaxy Clusters")
plt.imshow(imarray_cluster)

#creates figure for lensed image of real cluster, too bright to see so scaled down by 255
plt.figure()
plt.title("Einstein Ring of Actual Image of Galaxy Clusters")
plt.imshow(lensed_cluster/255)

#creates figure for radiating source image
plt.show()

