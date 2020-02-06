
if __name__ == "__main__":

    import time
    from xray import XRay

    class Person:

        def update(self):
            age = 0
            while True:
                time.sleep(10)
                age += 1


    xray = XRay(period=5)
    xray.monitor_function(Person.update, lambda l: print(l))
    xray.start()

    person = Person()
    person.update()

