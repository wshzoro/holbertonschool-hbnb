from .reviews import api as reviews_ns
api.add_namespace(reviews_ns, path='/reviews')
