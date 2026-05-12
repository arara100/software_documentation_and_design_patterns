from infrastructure.di_container import DIContainer


_container = None


def get_container() -> DIContainer:
    """Lazy DI container to avoid early initialization order issues."""
    global _container
    if _container is None:
        _container = DIContainer()
    return _container
