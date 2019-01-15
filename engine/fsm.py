from typing import Callable, TypeVar, Set

T = TypeVar('T')


class FiniteStateMachine:

    def __init__(self, initial_state: T, transition_function: Callable, final_state: Set[T]):
        """
        Build a finite state machine.
        :param initial_state: initial state
        :param transition_function: transition function (state: T, args, kargs) -> accepted: bool, next_state: T
        :param final_state: set of final state

        if state is callable then it will be called on each accepted transition,
        """
        self._initial_state = initial_state
        self._transition_function = transition_function
        self._final_state = final_state
        self._listeners = []
        self._current_state = self._initial_state

    @property
    def state(self) -> T:
        """
        :return: current state
        """
        return self._current_state

    def __repr__(self):
        return f'state: {self._current_state}'

    @property
    def terminated(self) -> bool:
        """
        :return: True if current state is a final state
        """
        return self._current_state in self._final_state

    def reset(self):
        """
        Reinitialize FSM.
        """
        self._current_state = self._initial_state

    @property
    def listeners(self):
        """
        :return: a list of listener
        """
        return self._listeners

    def subscribe(self, listener: Callable[[T, T], None]) -> Callable:
        """
        Subscribe on state transition
        :param listener: listener function (previous, current)
        :return: an unsubscribe function
        """
        self._listeners.append(listener)
        return lambda: self._listeners.remove(listener)

    def send(self, *args, **kwargs) -> T:
        """
        Apply an event and notify listener on transition if event is accepted
        :param args:
        :param kwargs:
        :return: accepted (True of False), current state
        """
        previous_state = self._current_state

        accepted, self._current_state = self._transition_function(self._current_state, *args, **kwargs)

        if accepted:
            # notify all listener
            if self._current_state != previous_state:
                for listener in self._listeners:
                    listener(previous_state, self._current_state)

            # process current state
            if callable(self._current_state):
                self._current_state()

        return accepted, self._current_state
