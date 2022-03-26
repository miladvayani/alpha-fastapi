from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Generic, NamedTuple, Type, TypeVar, final
from starlette.types import Scope

T = TypeVar("T")


class ScopeRangeError(Exception):
    """Stack range error when raise if the stack is not in live
    context.

    .. highlight:: python
    .. code-block:: python

        def live_scope():
            print(LocalStack())

        with insert_scope:
            live_scope() # will print `LocalStack` instance

        live_scope() # will raise `ScopeRangeError`

    Args:
        Exception (_type_): error message.
    """

    def __init__(self, *args: object) -> None:
        self.messages = args or [
            "you can not access to bounded scope outside of request context or closed stack."
        ]
        super().__init__(*self.messages)


class StackError(Exception):
    """if stack is closed or is binded will raise this error.

    Args:
        Exception (_type_): error message.
    """

    def __init__(self, *args: object) -> None:
        self.messages = args or ["Stack is not useable."]
        super().__init__(*self.messages)


class DataStructureInterface(ABC):
    def __init__(self) -> None:
        self.__stack: list = None
        self.__scope: Scope = None

    @property
    def stack(self):
        """get current stack

        Raises:
            StackError: stack is not usable

        Returns:
            list: current stack
        """
        if self.__stack is not None:
            return self.__stack
        raise StackError()

    @property
    def scope(self):
        """get current/live scope

        Raises:
            ScopeRangeError: scope error

        Returns:
            `starlette.types.Scope`: instance of starlette scope.
        """
        if self.__scope:
            return self.__scope
        raise ScopeRangeError()

    @scope.setter
    def scope(self, value: Scope):
        self.__scope = value

    def create_scope(self, scope: Scope, stackable: bool = True):
        """Create a scope to stack for accessing in live scope context,
        whenever the scope has deleted or closed, stack will clear automatically.

        Args:
            scope (Scope): Inserted scope from middleware or context manager.
            stackable (bool, optional): specify the proxy is a stackable object or not if been `True`
            else will not consider as a stack. Defaults to True.
        """
        self.scope = scope
        if stackable:
            self.__stack = []
        else:
            self.__stack = None

    @abstractmethod
    def push(self, value: str) -> None:
        """pop the key from stack if the object is a stack

        Args:
            key (int, optional): stack key or index. Defaults to None.
        """

    @abstractmethod
    def pop(self, key: int = None) -> None:
        """push the key from stack if the object is a stack

        Args:
            key (int, optional): stack key or index. Defaults to None.
        """


class LocalStack(DataStructureInterface):
    def push(self, value: str) -> None:
        if self.scope:
            if self.stack is not None:
                self.stack.append(value)

    def pop(self, key: int = None) -> None:
        if self.scope:
            if key:
                self.stack.pop(key)
            else:
                self.stack.pop()


@final
class LocalProxy(Generic[T]):
    """LocalProxy is a proxy to wrap the primary object that will
    protect it. you can access all of attrs and methods of assigned
    scope or lookuper object but you can not declare a new attr from
    outside of code.

    .. highlight:: python
    .. code-block:: python

        stack = LocalStack()
        proxy = LocalProxy(stack, context=True)
        proxy.start(request.scope)

        proxy.ctx.scope = request.scope # True
        proxy.url == request.url # True
        proxy == request # False

    if context been `False` you cannot use ctx and you have to specify
    a lookuper to proxy.

    .. highlight:: python
    .. code-block:: python

       stack = LocalStack()
       proxy = LocalProxy(stack, context=False)
       proxy.start(request.scope, lookup=request.scope)

    Args:
        Generic (LocalStack): context to wrap that.
    """

    def __init__(
        self, ls: LocalStack, context: bool = False, stackable: bool = False
    ) -> LocalProxy:
        """This is a final class, by the way any class can not inherit from this class

        Args:
            ls (LocalStack): instance
            context (bool, optional): specifying the lookuping to modified scope.
            Defaults to False.
            stackable (bool, optional): will enable the stack from LocalStack.
            Defaults to False.

        """
        self.__connect: LocalStack = ls
        self.ctx_lookup: bool = context
        self.lookup: Type[T] = None
        self.stackable: bool = stackable

    def __call__(self, content: str) -> Any:
        self.ctx.push(content)
        return content

    def pop(self, index: int = 0):
        self.ctx.pop(key=index)

    def get_private_stack(self) -> list:
        return self.ctx.stack

    def start(self, scope: Scope, lookup: Type[T] = None):
        """create scope for context

        Args:
            scope (Scope): context scope
            lookup (Type[T], optional): context lookup. Defaults to None.
        """
        self.lookup: Type[T] = lookup
        self.ctx.create_scope(scope, self.stackable)

    def __getattr__(self, key) -> Any:
        if self.ctx_lookup:
            if self.ctx.scope:
                if self.lookup:
                    return getattr(self.lookup, key)
                else:
                    return getattr(self.ctx.scope, key)
        else:
            return super().__getattribute__(key)

    def __repr__(self) -> str:
        return f"{self.ctx}"

    @property
    def ctx(self):
        return self.__connect
