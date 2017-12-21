
import struct
form . import core


class InvalidChTypeError(Exception):
    pass


class InvalidChRangeError(Exception):
    pass


class InvalidVoltageError(Exception):
    pass


class pci340816_driver(core.inteface_driver):
    bit_flags_in = (
        (
            ('B0', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7'),
            ('B8', 'B9', 'B10', 'B11', 'B12', 'B13', 'B14', 'B15'),
            ('C0', 'C1', 'C2', 'C3', '', '', '', ''),
            ('', '', '', '', '', '', '', ''),
            ('', '', '', '', '', '', '', ''),
            ('', '', '', '', '', '', '', ''),
            ('RG0', 'RG1', '', '', '', '', '', ''),
            ('', '', '', '', '', '', '', ''),
            ('', '', '', '', '', '', '', ''),
            ('', '', '', '', '', '', '', ''),
            ('', '', '', '', '', '', '', ''),
            ('', '', '', '', '', '', '', ''),
            ('GATE', '', '', '', '', '', '', ''),
            ('TMR', '', 'TRG', '', '', 'SPS', '', ''),
            ('', '', '', '', '', '', '', ''),
            ('TMR', '', 'TRG', '', '', 'SPS', '', ''),
            ('', '', 'EINT', '', '', '', '', ''),
            ('', '', '', '', '', '', '', ''),
            ('MRD', '', '', '', '', '', '', 'MWR'),
            ('OFS0', 'OFS1', 'OFS2', 'OFS3', 'OFS4', 'OFS5', 'OFS6', 'OFS7'),
            ('GAIN0', 'GAIN1', 'GAIN2', 'GAIN3', 'GAIN4', 'GAIN5', 'GAIN6', 'GAIN7'),
            ('CAR0', 'CAR1', 'CAR2', 'CAR3', '', '', '', ''),
            ('TRG0', 'TRG1', 'TRG2', 'TRG3', 'TRG4', 'TRG5', 'TRG6', 'TRG7'),
            ('BID0', 'BID1', 'BID2', 'BID3', 'M/S', 'CLKOEN', 'TRGOEN', ''),
            ('', '', '', '', '', '', '', ''),
            ('', '', '', '', '', '', '', ''),
            ('', '', '', '', '', '', '', ''),
            ('AO', '', '', '', '', '', '', ''),
            ('', '', '', '', '', '', '', ''),
            ('', '', '', '', '', '', '', ''),
            ('IN1', 'IN2', '', '', '', '', '', ''),
            ('', '', '', '', '', '', '', '')
        ),
    )

    bit_flags_out = (
        (
            ('B0', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7'),
            ('B8', 'B9', 'B10', 'B11', 'B12', 'B13', 'B14', 'B15'),
            ('C0', 'C1', 'C2', 'C3', '', '', '', ''),
            ('', '', '', '', '', '', '', ''),
            ('', '', '', '', '', '', '', ''),
            ('MD0', 'MD1', '', '', '', '', '', ''),
            ('', '', '', '', '', '', '', ''),
            ('', '', '', '', '', '', '', ''),
            ('TCTRL0', 'TCTRL1', 'TCTRL2', 'TCTRL3', 'TCTRL4', 'TCTRL5', 'TCTRL6', 'TCTRL7'),
            ('TCTRL8', 'TCTRL9', 'TCTRL10', 'TCTRL11', 'TCTRL12', 'TCTRL13', 'TCTRL14', 'TCTRL15'),
            ('TCTRL16', 'TCTRL17', 'TCTRL18', 'TCTRL19', 'TCTRL20', 'TCTRL21', 'TCTRL22', 'TCTRL23'),
            ('', '', '', '', '', '', '', ''),
            ('GATE', '', '', '', '', '', '', ''),
            ('TMR', '', 'TRG', '', '', 'SPS', '', ''),
            ('', '', '', '', '', '', '', ''),
            ('TMR', '', 'TRG', '', '', 'SPS', '', ''),
            ('', '', 'EINT', '', '', '', '', ''),
            ('', '', '', '', '', '', '', ''),
            ('MRD', '', '', '', '', '', '', 'MWR'),
            ('OFS0', 'OFS1', 'OFS2', 'OFS3', 'OFS4', 'OFS5', 'OFS6', 'OFS7'),
            ('GAIN0', 'GAIN1', 'GAIN2', 'GAIN3', 'GAIN4', 'GAIN5', 'GAIN6', 'GAIN7'),
            ('CAR0', 'CAR1', 'CAR2', 'CAR3', '', '', '', ''),
            ('TRG0', 'TRG1', 'TRG2', 'TRG3', 'TRG4', 'TRG5', 'TRG6', 'TRG7'),
            ('BID0', 'BID1', 'BID2', 'BID3', 'M/S', 'CLKOEN', 'TRGOEN', ''),
            ('', '', '', '', '', '', '', ''),
            ('', '', '', '', '', '', '', ''),
            ('', '', '', '', '', '', '', ''),
            ('AO', '', '', '', '', '', '', ''),
            ('', '', '', '', '', '', '', ''),
            ('', '', '', '', '', '', '', ''),
            ('IN1', 'IN2', '', '', '', '', '', ''),
            ('', '', '', '', '', '', '', '')
        ),
    )        

    def get_board_id(self):
        bar = 0
        offset = 0x17
        size = 1

        ret = self.read(bar, offset, size)
        bid = ret.to_hex()[1]

        return bid


    def _verify_voltage(self, voltage=0):
        vol_limit = 10
        if abs(voltage) <= vol_limit: pass
        else:
            msg = 'Voltage must be in -{0}[V] - {1}[V].'.format(-vol_limit, vol_limit)
            msg += 'while {0}[V] is given.'.format(voltage)
            raise InvalidVoltageError(msg)
        return


    def _verify_ch(self, ch=''):
        ch_lim_initial = 1
        ch_lim_final = 16

        if ch.find('-') == -1:
            msg = 'Ch type must be 'chx-chy' absolutelly'
            msg += 'while {0} is given.'.format(ch)
            raise InvalidChtypeError(msg)
        
        ch_ = ch.split('-')
        if len(ch_) == 2: pass
        else :
            msg = 'Ch type must be 'chx-chy' absolutelly'
            msg += 'while {0} is given.'.format(ch)
            raise InvalidChtypeError(msg)
            
        ch_initial, ch_final = int(ch_[0]), int(ch_[1])
        if 1 <= ch_initial < ch_final <= 16: pass
        else:
            msg = 'Ch range is in ch{0} - ch{1}'.format(ch_lim_initial, ch_lim_final)
            msg = 'while ch{0} - ch{1} is given'.format(ch_initial, ch_final)
        ch = [i for i in range(ch_initial, ch_final+1)]

        return ch


    def _voltage2list(self, voltage=0):
        vol_range = 10
        res = 16
        res_int = 2**res

        if voltage == 10: bytes_v = res_int - 1
        else: int((voltage + vol_range)/(vol_range/(res_int/2)))
        bit_ = bin(bytes_v).replace('0b', '0'*(16-(len(bin(bytes_v))-2)))
        bit_list = [int(bit_[i]) for i in range(len(bit_))]
        bit_list.reverse()

        return bit_list


    def _set_sampling_config(self, mode=''):
        bar = 0
        offset = 0x05

        if mode == 'all_vout_disable': mode_ = ''
        elif mode == 'all_vout': mode = 'MD0'
        elif mode == 'all_vclear': mode = 'MD1'
        elif mode == 'all_vout_enale': mode = 'MD0 MD1'

        flags = mode_

        self.set_flag(bar, offset, flags)
        return


    def _ch2bit(self, ch=''):
        if ch == '': return b''
        else:
            ch = int(ch.replace('ch', ''))
            ch = bin(ch-1).replace('0b', '0'*(8-(len(bin(ch-1))-2)))
            bit_list = [int(ch[i]) for i in range(len(ch))]
            bit_list.reverse()

            return bit_list


    def _da_onoff(self, onoff=0):
        bar = 0
        offset = 0x1b

        if onoff = 0: onoff_ = ''
        if onoff = 1: onoff_ = 'AO'

        flags = onoff_

        self.set_flag(bar, offset, flags)
        return


    def _da_output(self, ch='', voltage=0):
        bar = 0
        size_ch = 1
        size_vol = 2
        offset_ch = 0x02
        offset_vol = 0x00

        data_ch = self._ch2bit(ch=ch)
        new_d_ch = core.list2bytes(data_ch)
        self.write(bar_ch, offset_ch, new_d_ch)

        data_vol = self.voltage2bit(voltage=voltage)
        new_d_vol = core.list2byte(data_vol)
        self.write(bar_ch, offset_vol, new_d_vol)
        return


    def _start_sampling(self):
        self._set_sampling_config(mode='all_vout')

    
    def da_output(self, ch='', voltage=0):
        bar = 0
        size = 2
        offset = 0x00

        ch = _verify_ch(ch=ch)
        voltage = _verify_voltage(voltage=voltage)
        voltage = _voltage2list(voltage=voltage)
        self._set_sampling_config(mode='all_vout_enable')
        self._da_onoff(onoff=1)
        time.sleep(0.01)
        
        for i in range(len(ch)):
            _da_output(ch=ch[i], voltage)

        self._start_sampling()
        # self._da_onoff(onoff=0)
        time.sleep(0.01)
        return


    def initialize(self):
        self._set_sampling_config('all_vout_clear')
