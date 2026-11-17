"""
Q-EOS Financial Management Framework
Módulo: core.modelo_economico
"""
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP

def _round(value: float, decimals: int = 2) -> float:
    quant = Decimal(10) ** -decimals
    return float(Decimal(str(value)).quantize(quant, rounding=ROUND_HALF_UP))

@dataclass(frozen=True)
class LineaNegocio:
    nombre: str
    ventas: float
    margen_pct: float
    cargas_estructura: float = 0.0
    cargas_financieras: float = 0.0

    @property
    def margen_bruto(self) -> float:
        return _round(self.ventas * self.margen_pct / 100.0)
        
    @property
    def cargas_totales(self) -> float:
        return _round(self.cargas_estructura + self.cargas_financieras)
        
    @property
    def resultado(self) -> float:
        return _round(self.margen_bruto - self.cargas_totales)

@dataclass(frozen=True)
class ResultadoPrevisional:
    lineas: tuple[LineaNegocio, ...]

    @property
    def ventas_totales(self) -> float:
        return _round(sum(l.ventas for l in self.lineas))

    @property
    def margen_bruto_total(self) -> float:
        return _round(sum(l.margen_bruto for l in self.lineas))

    @property
    def cargas_totales(self) -> float:
        return _round(sum(l.cargas_totales for l in self.lineas))

    @property
    def resultado_total(self) -> float:
        return _round(self.margen_bruto_total - self.cargas_totales)
