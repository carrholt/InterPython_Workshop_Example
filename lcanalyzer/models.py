"""Module containing models representing lightcurves.

The Model layer is responsible for the 'business logic' part of the software.

The lightcurves are saved in a table (2D array) where each row corresponds to a single observation.
Depending on the dataset (LSST or Kepler), a table can contain observations of a single or several 
objects, in a single or different bands.
"""

import pandas as pd

def load_dataset(filename):
    """Load a table from CSV file.    
    :param filename: The name of the .csv file to load
    :returns: pd.DataFrame with the data from the file.
    """
    return pd.read_csv(filename)


def mean_mag(data,mag_col):
    """Calculate the mean magnitude of a lightcurve.
    :param data: pf.DataFrame with observed magnitudes for a single source.
    :param mag_col: a string with the name of the columns for calculating the mean.
    :returns: A float with mean value of the column.
    """
    return data[mag_col].mean()


def max_mag(data,mag_col):
    """Calculate the max magnitude of a lightcurve.
    :param data: pd.DataFrame with observed magnitudes for a single source.
    :param mag_col: a string with the name of the column for calculating the max value.
    :returns: The max value of the column.
    """
    return data[mag_col].max()


def min_mag(data,mag_col):
    """Calculate the min magnitude of a lightcurve.
    :param data: pd.DataFrame with observed magnitudes for a single source.
    :param mag_col: a string with the name of the column for calculating the min value.
    :returns: The min value of the column.
    """
    return data[mag_col].min()

def calc_stats(lc, bands, mag_col):
    """Calculate max, mean and min values for all bands of a lightcurve.
    :param lc: pd.DataFrame with observed magnitudes for a single source.
    :param bands: a list of all magnitude bands.
    :param mag_col: a string with the name of the column for calculating the min value.
    :returns: The max, mean, and min values of the column for all bands.
    """
    stats = {}
    for b in bands:
        stat = {}
        stat["max"] = max_mag(lc[b], mag_col)
        stat["mean"] = mean_mag(lc[b], mag_col)
        stat["min"] = min_mag(lc[b], mag_col)
        stats[b] = stat
    return pd.DataFrame.from_records(stats)

def normalize_lc(df,mag_col):
    """ Normalize a single lightcurve.
    :param df: pd.DataFrame with observed magnitudes for a single source.
    :param mag_col: a string with the name of the column for normalizing.
    :returns: Normalized lightcurve.
    """
    min = min_mag(df,mag_col)
    max = max_mag((df-min),mag_col)
    lc = (df[mag_col]-min)/max
    lc = lc.fillna(0)
    return lc