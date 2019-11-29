# -*- coding: utf-8 -*-
"""
    Simulated Brownian Diffusion Inside of a Capillary
    ==================================================
    This is almost exactly as the Simulate Brownian, but particles only move in 1 D

    :copyright:  Aquiles Carattino <aquiles@uetke.com>
    :license: GPLv3, see LICENSE for more details
"""
import numpy as np


class SimBrownian:
    """
    :param tuple camera_size: number of pixels in the x and y direction
    :return: generated an image with specified noise and particles displaced accordingly
    """
    #: Number of particles per frame
    num_particles = 10
    #: Diffusion coefficient um^2/s
    dif_coef = 2
    dif_coef_2 = 0  # For a second population of particles. Set to 0 if only one population
    #: Magnification of the microscope
    magnification = 30
    #: In real space, um
    pixel_size = 5
    #: Numerical aperture of the objective, used to estimate PSF
    NA = 1
    #: um, used to estimate PSF
    wavelength = .500
    #: Peak intensity for a particle
    signal = 300
    #: Background noise
    #: TODO: Needs to be implemented
    noise = 0
    #: Time step in the simulation. Should be set to the acquisition rate if used for a camera, seconds
    time_step = 0.03

    #: Number of pixels used to calculate the PSF of the particle
    kernel_size = 5

    #: Number of frames will be accumulated in order to speed up simulations
    #: (they will be an infinite loop). Set to 0 in order to avoid accumulating frames
    frames_to_accumulate = 0

    #: Drift to add to the brownian motion
    drift = 0

    def __init__(self, camera_size: tuple = (1000, 50), movie_length=10000):
        # camera and monitor parameters
        self.camera_size = np.array(camera_size)
        self.localization = np.zeros(shape=(self.num_particles, 2))
        self.real_space_size = self.camera_size*self.pixel_size/self.magnification
        self.real_space_margin = self.kernel_size*self.pixel_size/self.magnification
        self.localization = np.random.uniform([0, 0], self.real_space_size[1], size=(self.num_particles, 2))
        self.localization[:, 0] = self.camera_size[1]/2
        self.next_random_step()
        self.psf_width = self.magnification * self.wavelength/(2*self.NA)/self.pixel_size  # In pixels
        self.current_frame = 0
        self.movie_length = movie_length
        self.i = 0

        if self.frames_to_accumulate:
            self.frames = np.zeros((camera_size[0], camera_size[1], self.frames_to_accumulate), dtype=np.int16)

    def resize_view(self, camera_size):
        """SimulateBrownian.resizeView() adjusts the coordinates of the moving particles such that they
        fit into the desired framesize of the simulated dummycamera"""
        # self.camera_size = np.array(camera_size)
        pass

    def next_random_step(self):
        if not self.dif_coef_2:
            dr = np.sqrt(self.time_step)*np.random.normal(loc=0.0, scale=np.sqrt(self.dif_coef), size=(self.num_particles, 2))
            dr[:, 0] = 0
            dr[:, 1] += self.drift
        else:
            dr_1 = np.sqrt(self.time_step) * np.random.normal(loc=0.0, scale=np.sqrt(self.dif_coef),
                                                              size=(int(self.num_particles/2), 2))
            dr_2 = np.sqrt(self.time_step) * np.random.normal(loc=0.0, scale=np.sqrt(self.dif_coef_2),
                                                              size=(int(self.num_particles/2), 2))
            dr = np.vstack((dr_1, dr_2))
        self.localization += dr
        rem_x = np.mod(self.localization[:,0]-self.real_space_margin, self.real_space_size[0]-2*self.real_space_margin)+self.real_space_margin
        rem_y = np.mod(self.localization[:,1]-self.real_space_margin, self.real_space_size[1]-2*self.real_space_margin)+self.real_space_margin
        self.localization[:,0] = rem_x
        self.localization[:,1] = rem_y

    def gen_image(self):
        """
        :return: generated image with specified noise and particles position
        """
        if self.current_frame < self.frames_to_accumulate or not self.frames_to_accumulate:
            self.next_random_step()
            img = np.zeros(self.camera_size)
            x = np.arange(-self.kernel_size, self.kernel_size+1)
            y = np.arange(-self.kernel_size, self.kernel_size+1)
            xx, yy = np.meshgrid(x, y)
            positions = self.localization*self.magnification/self.pixel_size  # In units of pixels (with sub-px accuracy)
            for p in positions:
                p_x = p[0]-int(p[0])
                p_y = p[1]-int(p[1])
                pix_x = int(p[0])
                pix_y = int(p[1])
                s_img = 1 / (np.sqrt(2 * np.pi)*self.psf_width) * np.exp(-((xx - p_x) ** 2 + (yy - p_y) ** 2)/(2*self.psf_width**2))
                img[pix_x-self.kernel_size:pix_x+self.kernel_size+1, pix_y-self.kernel_size:pix_y+self.kernel_size+1] += s_img
            if self.frames_to_accumulate:
                self.frames[:, :, self.current_frame] = img*self.signal
                self.current_frame += 1
                return self.frames[:, :, self.current_frame-1]
            return img*self.signal
        else:
            curr_frame = self.current_frame % (2*self.frames_to_accumulate-1)
            self.current_frame += 1
            if 2*self.frames_to_accumulate > curr_frame >= self.frames_to_accumulate:
                curr_frame = (curr_frame + 1) % self.frames_to_accumulate
                return self.frames[:,:,-curr_frame]
            else:
                curr_frame = curr_frame % self.frames_to_accumulate
                return self.frames[:, :, curr_frame]

    def __next__(self):
        self.i += 1
        if self.i > self.movie_length:
            raise StopIteration()

        self.next_random_step()
        return self.gen_image()

    def __iter__(self):
        return self

    def __len__(self):
        return self.movie_length

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    sb = SimBrownian()
    img = sb.gen_image()
    plt.imshow(img)
    plt.show()
    sb.next_random_step()
    img2= sb.gen_image()
    plt.imshow(img2)
    plt.show()
