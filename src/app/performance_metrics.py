import time
from win32pdh import (
    EnumObjectItems,
    MakeCounterPath,
    OpenQuery,
    AddCounter,
    CollectQueryData,
    GetFormattedCounterValue,
    RemoveCounter,
    CloseQuery,
    PDH_FMT_LONG,
    PERF_DETAIL_WIZARD,
)


def get_windows_metrics(
    object, counter, instance=None, inum=-1, format=PDH_FMT_LONG, machine=None
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
    if object == "Network Interface":
        __, network_instance = EnumObjectItems(None, None, object, PERF_DETAIL_WIZARD)
        if len(network_instance) != 0:
            instance = network_instance[0]
    path = MakeCounterPath((machine, object, instance, None, inum, counter))
    hq = OpenQuery()
    try:
        hc = AddCounter(hq, path)
        try:
            CollectQueryData(hq)
            time.sleep(1)
            CollectQueryData(hq)
            type, val = GetFormattedCounterValue(hc, format)
            return val
        finally:
            RemoveCounter(hc)
    finally:
        CloseQuery(hq)
