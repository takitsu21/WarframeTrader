import requests, os

def get_JWT():
    session = requests.Session()
    response = session.get('https://warframe.market/')
    return session.cookies.get_dict()

# %matplotlib inline
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import numpy as np
fig = plt.figure()
ax = plt.axes()

x = np.linspace(0, 1000, 100)
ax.plot(x, np.sin(x))
plt.show()

