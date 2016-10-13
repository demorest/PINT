# __init__.py for PINT models/ directory
"""This module contains implementations of pulsar timing models.
"""
# Import the main timing model classes
from .timing_model import TimingModel, generate_timing_model

# Import all standard model components here.  Note, this is necessary
# for model components that we want available to model_builder.
from . import astrometry, dispersion_model, spindown, solar_system_shapiro, \
        frequency_dependent, jump, glitch, \
        pulsar_binary, binary_bt, binary_dd, binary_ell1

from .model_builder import get_model

# Define a standard basic model
StandardTimingModel = generate_timing_model("StandardTimingModel",
        (astrometry.AstrometryEquatorial, 
            spindown.Spindown, 
            dispersion_model.Dispersion, 
            solar_system_shapiro.SolarSystemShapiro))
