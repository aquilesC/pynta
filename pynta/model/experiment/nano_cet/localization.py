from multiprocessing import Queue
from time import sleep

import numpy as np
from pandas import DataFrame
from scipy.stats import stats
from trackpy.linking import Linker

from pynta.model.experiment.nano_cet.exceptions import DiameterNotDefined
from pynta.util import get_logger

try:
    import trackpy as tp
    trackpy = True
except:
    trackpy = False


def calculate_locations_image(image, publisher_queue, locations_queue, **kwargs):
    """ Calculates the positions of the particles on an image. It used the trackpy package, which may not be
    installed by default.
    """
    if not 'diameter' in kwargs:
        raise DiameterNotDefined('A diameter is mandatory for locating particles')

    diameter = kwargs['diameter']
    del kwargs['diameter']
    image = image[1]  # image[0] is the timestamp of the frame
    logger = get_logger(name=__name__)
    logger.debug('Calculating positions on image')
    if trackpy:
        logger.debug('Calculating positions with trackpy')
        locations = tp.locate(image, diameter, **kwargs)
        logger.debug('Got {} locations'.format(len(locations)))
        publisher_queue.put({'topic': 'trackpy_locations', 'data': locations})
        locations_queue.put(locations)


def add_linking_queue(data, queue):
    logger = get_logger(__name__)
    logger.debug('Adding data frame to linking queue')
    queue.put(data)


def link_queue(locations_queue, publisher_queue, links_queue, **kwargs):
    """ Links the locations of particles from a location queue.
    It is a reimplementation of the link_iter of trackpy.
    """
    logger = get_logger(name=__name__)
    logger.info('Starting to create trajectory links from queue')
    t = 0  # First frame
    search_range = kwargs['search_range']
    del kwargs['search_range']
    linker = Linker(search_range, **kwargs)
    while True:
        if not locations_queue.empty() or locations_queue.qsize()>0:
            locations = locations_queue.get()
            if isinstance(locations, str):
                logger.debug('Got string on coordinates')
                break

            coords = np.vstack((locations['x'], locations['y'])).T
            if t == 0:
                logger.debug('First set of coordinates')
                linker.init_level(coords, t)
            else:
                logger.debug('Processing frame {}'.format(t))
                linker.next_level(coords, t)
            logger.debug("Frame {0}: {1} trajectories present.".format(t, len(linker.particle_ids)))
            t += 1
            locations['particle'] = linker.particle_ids
            locations['frame'] = t
            publisher_queue.put({'topic': 'particle_links', 'data': [locations, linker.particle_ids]})
            links_queue.put(locations)
    logger.info('Stopping link queue trajectories')


def add_links_to_queue(data, queue):
    queue.put(data)


def calculate_histogram_sizes(tracks_queue, config, out_queue):
    params = config['tracking']['process']
    df = DataFrame()
    sleep(5)
    while True:
        while not tracks_queue.empty() or tracks_queue.qsize() > 0:
            data = tracks_queue.get()
            df = df.append(data)

        if len(df) % 100 == 0:
            # t1 = tp.filter_stubs(df, params['min_traj_length'])
            # print(t1.head())
            # t2 = t1[((t1['mass'] > params['min_mass']) & (t1['size'] < params['max_size']) &
            #          (t1['ecc'] < params['max_ecc']))]
            # print(t2.head())
            # t2 = t1
            # d = tp.compute_drift(t1)
            # tm = tp.subtract_drift(t2.copy(), d)
            im = tp.imsd(df, config['tracking']['process']['um_pixel'], config['camera']['fps'])
            values = []
            for pcle in im:
                data = im[pcle]
                slope, intercept, r, p, stderr = stats.linregress(np.log(data.index), np.log(data.values))
                values.append([slope, intercept])

            out_queue.put(values)

        # if len(df) > 100:
        #     break

