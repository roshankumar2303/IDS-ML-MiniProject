import win32pdh
import time


def get_performance_attributes(
    object, counter, instance=None, inum=-1, format=win32pdh.PDH_FMT_LONG, machine=None
):
    # NOTE: Many counters require 2 samples to give accurate results,
    # including "% Processor Time" (as by definition, at any instant, a
    # thread's CPU usage is either 0 or 100).  To read counters like this,
    # you should copy this function, but keep the counter open, and call
    # CollectQueryData() each time you need to know.
    # See http://support.microsoft.com/default.aspx?scid=kb;EN-US;q262938
    # and http://msdn.microsoft.com/library/en-us/dnperfmo/html/perfmonpt2.asp
    # My older explanation for this was that the "AddCounter" process forced
    # the CPU to 100%, but the above makes more sense :)
    if len(instance) == 0:
        x, y = win32pdh.EnumObjectItems(None, None, object, win32pdh.PERF_DETAIL_WIZARD)
        if len(y) != 0:
            instance = y[0]
        else:
            instance = "_Total"
    path = win32pdh.MakeCounterPath((machine, object, instance, None, inum, counter))
    hq = win32pdh.OpenQuery()
    try:
        hc = win32pdh.AddCounter(hq, path)
        try:
            win32pdh.CollectQueryData(hq)
            time.sleep(1)
            win32pdh.CollectQueryData(hq)
            type, val = win32pdh.GetFormattedCounterValue(hc, format)
            return val
        finally:
            win32pdh.RemoveCounter(hc)
    finally:
        win32pdh.CloseQuery(hq)


# items, instances = win32pdh.EnumObjectItems(None, None, "Network Interface", win32pdh.PERF_DETAIL_WIZARD)
# items = win32pdh.EnumObjects(None, None, win32pdh.PERF_DETAIL_WIZARD)
# print(items)
# print("\n")
# print(instances)
