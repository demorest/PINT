"""This module implements phase jumps.
"""
# phase_jump.py
# Defines PhaseJump timing model class
import numpy
import astropy.units as u
from .timing_model import TimingModel, MissingParameter
import parameter as p


class JumpDelay(TimingModel):
    """This is a class to implement phase jumps
    """
    def __init__(self):
        super(JumpDelay, self).__init__()
        # TODO: In the future we should have phase jump as well.
        self.add_param(p.maskParameter(name = 'JUMP', units='second'))
        self.delay_funcs['L1'] += [self.jump_delay,]
    def setup(self):
        super(JumpDelay, self).setup()
        self.jumps = []
        for mask_par in self.get_params_of_type('maskParameter'):
            if mask_par.startswith('JUMP'):
                self.jumps.append(mask_par)
        for j in self.jumps:
            self.make_delay_jump_deriv_funcs(j)
            
    def jump_delay(self, toas):
        """This method returns the jump delays for each toas section collected by
        jump parameters. The delay value is determined by jump parameter value
        in the unit of seconds.
        """
        jdelay = numpy.zeros(len(toas))
        for jump in self.jumps:
            jump_par = getattr(self, jump)
            mask = jump_par.select_toa_mask(toas)
            # NOTE: Currently parfile jump value has opposite sign with our
            # delay calculation.
            jdelay[mask] += -jump_par.value
        return jdelay

    def d_delay_d_jump(self, jump_par, toas):
        d_delay_d_j = numpy.zeros(len(toas))
        mask = jump_par.select_toa_mask(toas)
        d_delay_d_j[mask] = 1.0
        return d_delay_d_j

    def make_delay_jump_deriv_funcs(self, param):
        """Make jump delay derivitve
        """
        def deriv_func(toas):
            jump_p = getattr(self, param)
            return self.d_delay_d_jump(jump_p, toas)
        deriv_func.__name__ = 'd_delay_d_' + param
        setattr(self, 'd_delay_d_' + param, deriv_func)
