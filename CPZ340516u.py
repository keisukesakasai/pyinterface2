
import pyinterface


class InvalidChRangeError(Exception):
    pass


class InvalidCurrentRange(Exception):
    pass


class InvalidSamplingModeError(Exception):
    pass


class cpz340816u(object):

    def __init__(self, dev=0):
        self.dev = dev
        self.bname = 3405
        self.driver = pyinterface.open(self.bname, self.dev)
        self.initialize()


    def initialize(self):
        self.driver.initialize()
        return

    
    def set_output(self, onoff=0):
        onoff_eff = [0, 1]

        if onoff in onoff_eff: pass
        else:
            msg = 'Onoff must be 0 or 1 absolutelly'
            msg += 'while {0} is given.'.format(onoff)
            raise InvalidOnOffError(msg)
        
        self.driver._da_onoff(onoff=onoff)
        

    def set_Irange(self, mode='DA_0_100mV'):
        mode_eff = ['DA_0_1mV', 'DA_0_100mV']

        if mode in mode_eff: pass
        else:
            msg = 'Samplinge range is DA_0_1mV or DA_0_100mV '
            msg += 'while {0} is given.'.format(mode)

        self.driver.set_sampling_range(mode=mode)
        return


    def query_Irange(self):
        self.driver.get_samplinge_range()


    def set_current(self, current=0.0, ch=0):
        ch = 'ch{0}'.format(ch+1)
        ch_lim_initial = 1
        ch_lim_final = 8
        cur_lim_initial = 0.0
        cur_lim_final = 100.0
        ch_eff = ['ch{}'.format(i) for i in range(ch_lim_initial, ch_lim_final+1)]

        if ch in ch_eff: pass
        else:
            msg = 'Ch range is in ch{0} - ch{1}'.format(ch_lim_initial, ch_lim_final)
            msg += 'while {0} is given'.format(ch)
            raise InvalidChRange(msg)

        if cur_lim_initial <= abs(current) <= cur_lim_filna:
            self.driver.output_da_sim(ch, current)
        else:
            msg = 'Current must be in {0}[mA] - {1}[V].'.format(cur_lim_initial, cur_lim_final)
            msg += 'while {0}[mA] is given.'.format(current)
            raise InvalidCurrentError(msg)
        return
        

    def finalize(self):
        self.driver.finalize()
        return
