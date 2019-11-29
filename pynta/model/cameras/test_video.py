import os
import subprocess
import matplotlib.pyplot as plt
import numpy as np

from pynta.model.cameras.sim_fiber_brownian import SimBrownian

SimBrownian.num_particles = 20
SimBrownian.signal = 5000
sb = SimBrownian(camera_size=(15, 1000), movie_length=500)
files = []

fig, ax = plt.subplots(figsize=(10, 2))
fig.subplots_adjust(bottom=0, top=1, left=0, right=1)
i = 0
for img in sb:  # 50 frames
    plt.cla()
    plt.imshow(img, interpolation='nearest', cmap=plt.get_cmap('gray'))
    plt.axis('off')
    fname = 'test/_tmp%03d.png' % i
    print('Saving frame', fname)
    plt.savefig(fname)
    files.append(fname)
    i += 1

# print('Making movie animation.mpg - this may take a while')
# subprocess.call("mencoder 'mf://_tmp*.png' -mf type=png:fps=10 -ovc lavc "
#                 "-lavcopts vcodec=wmv2 -oac copy -o animation.mpg", shell=True)
#
# cleanup
# for fname in files:
#     os.remove(fname)
