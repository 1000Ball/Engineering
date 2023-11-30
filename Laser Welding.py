import numpy as np
from thermostate import Q_
'''A working guide for settings on the laser welding machine. Reference values might need
to be tweaked in the future.'''

#--------------------------------------------------------------------------------------------

class Laser_Weld:
    '''A class for calculating setting to use on the laser welding machine'''
    def __init__(self, material):
        self.reference = {'aluminum': {'density': Q_(2.7, 'g/cm^3'),
                                       'melt point': Q_(660.3, 'degC'),
                                       'c_p': Q_(0.96, 'J/(g*K)'),
                                       'c_p Latent': Q_(399, 'kJ/kg')},
                          'becu': {'density': Q_(0.298, 'lb/in^3'),
                                   'melt point': Q_(1150, 'degC'),
                                   'c_p': Q_(0.376812, 'J/(g*degC)'),
                                   'c_p Latent': Q_(215, 'kJ/kg')},
                          'steel': {'density': Q_(7.8, 'g/cm^3'),
                                   'melt point': Q_(1370, 'degC'),
                                   'c_p': Q_(0.47, 'J/(g*degC)'),
                                   'c_p Latent': Q_(1380, 'kJ/kg')},
                          'moldmax': {'density': Q_(8.36, 'g/cm^3'),
                                   'melt point': Q_(870, 'degC'),
                                   'c_p': Q_(0.41, 'J/(g*degC)'),
                                   'c_p Latent': Q_(206, 'kJ/kg')}}
        self.voltage = Q_(450, 'V')
        self.props = self.reference[material.lower()]
        self.density = self.props['density']
        self.melt_point = self.props['melt point']
        self.c_p = self.props['c_p']
        self.c_p_Latent = self.props['c_p Latent']

#--------------------------------------------------------------------------------------------

    def settings(self, wire_D, spot_size, duration):
        '''Assuming wire size is in inches, spot size in mm, duration in ms. Call room temp 20 degC'''
        self.wire_D = Q_(wire_D, 'in')
        self.spot_size = Q_(spot_size, 'mm')
        self.duration = Q_(duration, 'ms')
        room_temp = Q_(20, 'degC')

        up_to_melt = ((self.c_p * (self.melt_point - room_temp) * self.density * self.vol_used()) / self.duration).to('W')
        melt = ((self.c_p_Latent * self.density * self.vol_used()) / self.duration).to('W')
        welded_power = (up_to_melt + melt).to('W')

        return (f'"Average pulse power" should be set to a number around {welded_power}')
    
#--------------------------------------------------------------------------------------------
    
    def vol_used(self):
        '''Calculates approximate volume hit by laser spot'''
        return (np.pi * (self.wire_D/2)**2 * (self.spot_size/2)).to('mm^3')
    
#--------------------------------------------------------------------------------------------

if __name__ == '__main__':
    Aluminum = Laser_Weld('Aluminum')
    Steel = Laser_Weld('Steel')
    BeCu = Laser_Weld('BeCu')
    MoldMax = Laser_Weld('MoldMax')
