"""RAM gate: wait until free physical RAM >= 1.4 GB (max ~30 min). Import gate.wait() or run as script."""
import ctypes, time


class MS(ctypes.Structure):
    _fields_ = [('dwLength', ctypes.c_ulong), ('dwMemoryLoad', ctypes.c_ulong), ('ullTotalPhys', ctypes.c_ulonglong),
                ('ullAvailPhys', ctypes.c_ulonglong), ('ullTotalPageFile', ctypes.c_ulonglong),
                ('ullAvailPageFile', ctypes.c_ulonglong), ('ullTotalVirtual', ctypes.c_ulonglong),
                ('ullAvailVirtual', ctypes.c_ulonglong), ('ullAvailExtendedVirtual', ctypes.c_ulonglong)]


def free_gb():
    m = MS(); m.dwLength = ctypes.sizeof(MS)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
    return m.ullAvailPhys / 2**30


def wait(need=1.4, tries=180):
    for _ in range(tries):
        g = free_gb()
        if g >= need:
            return g
        time.sleep(10)
    raise SystemExit(f'RAM_TIMEOUT {free_gb():.2f}')


if __name__ == '__main__':
    print(f'RAM_OK {wait():.2f}')
