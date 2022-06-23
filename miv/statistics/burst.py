import os

import matplotlib.pyplot as plt
import numpy as np

from miv.typing import SpikestampsType


def burst(spiketrains: SpikestampsType, channel: float, min_isi: float, min_len: float):
    """
    Calculates parameters critical to characterize bursting phenomenon on a single channel
    Bursting is defined as the occurence of a specified number of spikes (usually >10), with a small interspike interval (usually < 100ms) [1]_, [2]_

    Parameters
    ----------
    spikes : SpikestampsType
           Single spike-stamps
    Channel : float
       Channel to analyze
    min_isi : float
       Minimum Interspike Interval (in seconds) to be considered as bursting [standard = 0.1]
    min_len : float
       Minimum number of simultaneous spikes to be considered as bursting [standard = 10]

    Returns
    -------
    start_time: float
           The time instances when a burst starts
    burst_duration: float
           The time duration of a particular burst
    burst_len: float
            Number of spikes in a particular burst
    burst_rate: float
            firing rates corresponding to particular bursts

    ..[1] Chiappalone, Michela, et al. "Burst detection algorithms for the analysis of spatio-temporal patterns
    in cortical networks of neurons." Neurocomputing 65 (2005): 653-662.
    ..[2] Eisenman, Lawrence N., et al. "Quantification of bursting and synchrony in cultured
    hippocampal neurons." Journal of neurophysiology 114.2 (2015): 1059-1071.

    """

    spike_interval = np.diff(
        spiketrains[channel].magnitude
    )  # Calculate Inter Spike Interval (ISI)
    burst_spike = (spike_interval <= min_isi).astype(
        np.int32
    )  # Only spikes within specified min ISI are 1 otherwise 0 and are stored
    min_spikes = min_len
    burst = []  # List to store burst parameters

    for i in np.arange(
        len(burst_spike) - min_spikes
    ):  # Loop to check clusters of spikes greater than specified minimum length of burst
        t = 0
        if np.sum(burst_spike[i : i + min_spikes]) == min_spikes:
            q = 1
            while q > 0 and i + q + min_spikes <= len(burst_spike) - 1:
                if burst_spike[i + q + min_spikes - 1] == 1:
                    t = q
                    q += 1
                else:
                    q = 0

            burst.append([i, t + min_spikes])
            burst_spike[
                i : i + t + min_spikes
            ] = 0  # Zeroing counted spikes to avoid recounting
    Q = np.array(burst)

    if np.sum(Q) == 0:
        start_time = 0
        end_time = 0
        burst_duration = 0
        burst_rate = 0
        burst_len = 0
    else:
        spike = np.array(spiketrains[channel].magnitude)
        start_time = spike[Q[:, 0]]
        end_time = spike[Q[:, 0] + Q[:, 1]]
        burst_len = Q[:, 1] + 1
        burst_duration = end_time - start_time
        burst_rate = burst_len / (burst_duration)

    return start_time, burst_duration, burst_len, burst_rate
