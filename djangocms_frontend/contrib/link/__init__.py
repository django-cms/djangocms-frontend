class FormsSite:
    @property
    def urls(self):
        from .urls import urls

        return urls


site = FormsSite()

__all__ = ["site"]
