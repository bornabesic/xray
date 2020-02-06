
import sys
import threading
import time
import gc
from collections import defaultdict

class XRay(threading.Thread):

    def __init__(self, period=10):
        super().__init__(daemon=True)

        self.threads_and_functions = defaultdict(lambda: defaultdict(list))
        self.period = period
        self.running = True

    def get_function_from_frame(self, current_frame):
        fs = list(filter(lambda ref: hasattr(ref, "__code__") and ref.__code__ is current_frame.f_code, gc.get_referrers(current_frame.f_code)))
        return fs[0] if fs else None

    def get_scope(self, thread, function):
        found = False
        current_frame = sys._current_frames()[thread.ident]
        while current_frame is not None:
            current_function = self.get_function_from_frame(current_frame)
            if current_function is function:
                found = True
                break
            current_frame = current_frame.f_back

        if found:
            return current_frame

    def monitor_function(self, function, callback, parent_thread=None):
        if parent_thread is None:
            parent_thread = threading.main_thread()
        self.threads_and_functions[parent_thread][function].append(callback)

    def tick(self):
        for thread, functions_and_callbacks in self.threads_and_functions.items():
            for function, callbacks in functions_and_callbacks.items():
                frame = self.get_scope(thread, function)
                if frame is not None:
                    for callback in callbacks:
                        callback(frame.f_locals)

    def run(self):
        while self.running:
            self.tick()
            time.sleep(self.period)

    def stop():
        self.running = False

