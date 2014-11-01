__author__ = 'Calvin'
import inspect
import timeit


from inspect import currentframe, getframeinfo

# frameinfo = getframeinfo(currentframe())
#
# print frameinfo.filename, frameinfo.lineno

import math

class PerformanceTest(object):

    def __init__(self, repeat, number, *func_args, **func_kwargs):
        self._repeat = repeat
        self._number = number
        self._func_args = func_args
        self._func_kwargs = func_kwargs

    def __call__(self, func):
        src = inspect.getsource(func)
        self._func_src = src[src.index('\n'):]
        self._func_name = func.__name__
        print self._func_src

        call = "{0}(*{1}, **{2})".format(self._func_name, self._func_args, self._func_kwargs)
        print call
        self._timer = timeit.Timer(stmt=call, setup=self._func_src)
        trials = self._timer.repeat(self._repeat, self._number)

        time_avg_seconds = sum(trials) / len(trials)
        order = math.log10(time_avg_seconds)

        # Convert into reasonable time units
        if -6 < order < -3:
            time_units = 'us'
            factor = 1000000
        elif -3 <= order < -1:
            time_units = 'ms'
            factor = 1000.
        elif -1 <= order:
            time_units = 's'
            factor = 1

        time_avg = time_avg_seconds * factor
        print "Average time ({1}): {0:.3f} {1}".format(time_avg, time_units)

        return func

@PerformanceTest(3, 100, l=10)
def mytest(l):
    out = []
    for i in xrange(l):
        out.append(i*i)
    return out


@PerformanceTest(3, 100, 1000)
def mytest2(l):
    out = 0
    for i in xrange(l):
        out += i * i
    return out

