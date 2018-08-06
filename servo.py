import microbit

class SERVO:
    def __init__(self, pin, min_us, max_us,frequency=50):
        
        self._pin=pin
        self._max=max_us
        self._min=min_us
        self._period=1000000//frequency
        self._pin.set_analog_period_microseconds(self._period)

    def _pulse(self, period, snooze=None):

        if period<0:
            period=-period
        else:
            period=max(min(period,self._max),self._min)
            
        duty=round((period * 1023 ) / self._period)
        self._pin.write_analog(duty)

        if snooze is not None:
            microbit.sleep(int(snooze))
            self.off()
            
    def off(self):
        
        self._pin.write_digital(0)

    def angle(self, dwell=None):

        raise NotImplementedError

    def speed(self,percent=0):

        raise NotImplementedError


class AngularServo(SERVO):

    def __init__(self, pin, min_us=500, max_us=2200, ms_per_degree=3,
                 max_angle=180,frequency=50):

        self._speed=ms_per_degree
        self._at_angle=0
        self._mid=min_us+((max_us-min_us)//2)
        super().__init__(pin, min_us, max_us, frequency)
        self._pulse(self._mid,600)
        self._half_max=max_angle//2
        
    def angle(self, dwell=None):

        if dwell is None:
            return self._at_angle

        if self._speed is None:
            move_time=None
        else:
            move_time=abs(dwell - self._at_angle) * self._speed

        if dwell == 0:
            period=self._mid 
        elif dwell < 0:
            period=self._mid + ((self._mid - self._min) * dwell/self._half_max)
        else:
            period=self._mid + ((self._max - self._mid) * dwell/self._half_max)

        self._pulse(period, move_time)

        if dwell<0:
            dwell=max(dwell,-self._half_max)
        else:
            dwell=min(dwell,self._half_max)

        self._at_angle=dwell


class ContinuousServo(SERVO):

    def __init__(self,pin ,min_us=400 ,stop_us=1500 ,max_us=2200 ,
                 frequency=50):

        self._stop=stop_us
        
        super().__init__(pin, min_us,max_us, frequency)
        
    def speed(self,percent=0):

        if percent==0:
            period=self._stop
        elif percent<0:
            period=round(self._stop + \
                         ((self._stop - self._min) * percent / 100))
        else:
            period=round(self._stop + \
                         ((self._max - self._stop) * percent / 100))

        self._pulse(period,None)
