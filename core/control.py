"""
Q-EOS Financial Management Framework
Módulo: core.control
"""
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP

def _round(value: float, decimals: int = 2) -> float:
    quant = Decimal(10) ** -decimals
    return float(Decimal(str(value)).quantize(quant, rounding=ROUND_HALF_UP))

@dataclass(frozen=True)
class Desviacion:
    concepto: str
    real: float
    presupuesto: float
    tipo: str = "neutro"

    @property
    def importe(self) -> float:
        return _round(self.real - self.presupuesto)

    @property
    def es_favorable(self) -> bool:
        if self.tipo in ("ingreso", "margen"):
            return self.importe > 0
        if self.tipo == "coste":
            return self.importe < 0
        return False
