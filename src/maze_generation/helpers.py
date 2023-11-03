from src.events.event import Event
from src.events.observer import Observer
from src.events.publisher import Publisher


class TestPublisher(Publisher):
    def attach_observer(self, observer: Observer):
        pass

    def detach_observer(self, observer: Observer):
        pass

    def dispatch_event(event: Event):
        pass



class TestObserver(Observer):
    def on_event(self, event: Event):
        pass


def dispatch_event(event: Event):
    pass