import numpy as np
import random
import matplotlib.pyplot as plt
import scipy.constants
from skimage import measure, feature, io, color, draw


#defines function for a density of galaxy clusters and returns result as float
#unless r is bigger than the maximum radius
def get_density(r: float, max_radius: float=None, f0: float = 1, a: float = 1) -> float:
    if max_radius and r > max_radius:
        return 0
    return f0 * np.exp(-r / a)

#defines probability function, returns True or False that generated number <=cluster density
#p subbed by get_density so cluster less dense as r increases
def probability(p: float) -> bool:
    rand = random.uniform(0, 1)
    return rand <= p

#defines function for finding the xc,yc, and r of Einstein Ring code learnt from online seen in pdf reference [4]
def Get_Radius(img: np.ndarray) ->tuple:
    img = feature.canny(img).astype(np.uint8)
    img[img > 0] = 255

    coordinates = np.column_stack(np.nonzero(img))

    model, inliers = measure.ransac(coordinates, measure.CircleModel,
                                    min_samples=3, residual_threshold=1,
                                    max_trials=500)
    
    return model.params

#defines function for finding s1 and s2
def transform(rc:float,r1:float,r2:float,epsilon:float=0) -> float:
    s1 = r1 - (r1*(1-epsilon)/np.sqrt((rc**2)+(r1**2)+(r2**2)))
    s2 = r2 - (r2*(1+epsilon)/np.sqrt((rc**2)+(r1**2)+(r2**2)))
    return s1,s2