from oscar.apps.shipping import repository
from . import methods

class Repository(repository.Repository):
    methods = (repository.Free(), methods.Standard(), methods.Express())