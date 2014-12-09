
class Event:
    def __init__(self):
        """ Create an event.

        :rtype : Event
        """
        self.handlers = set()

    def handle(self, handler):
        """ Adds a handler to the chain.

        :param handler:
        :return:
        :rtype: Event
        """
        self.handlers.add(handler)
        return self

    def unhandle(self, handler):
        """ Removes a handler from the chain.

        :param handler:
        :return:
        :rtype: Event
        :raise ValueError:
        """
        try:
            self.handlers.remove(handler)
        except:
            raise ValueError("Handler is not handling this event, so cannot unhandle it.")
        return self

    def fire(self, *args, **kargs):
        """ Fire the event.

        :param args: Positional arguments to pass to the handlers.
        :param kargs: Keyword arguments to pass to the handlers.
        """
        for handler in self.handlers:
            handler(*args, **kargs)

    def getHandlerCount(self):
        """ Returns the length of the handler chain for this event.

        :return: Length of the handler chain.
        :rtype: int
        """
        return len(self.handlers)

    __iadd__ = handle
    __isub__ = unhandle
    __call__ = fire
    __len__  = getHandlerCount

