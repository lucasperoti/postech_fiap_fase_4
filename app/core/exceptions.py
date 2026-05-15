class DomainException(Exception):
    """Base exception for domain errors"""
    pass


class VeiculoNotFoundException(DomainException):
    pass


class VeiculoJaVendidoError(DomainException):
    pass
