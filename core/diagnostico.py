"""
Q-EOS Financial Management Framework
Módulo: core.diagnostico
"""
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP

def _round(value: float, decimals: int = 4) -> float:
    quant = Decimal(10) ** -decimals
    return float(Decimal(str(value)).quantize(quant, rounding=ROUND_HALF_UP))

@dataclass(frozen=True)
class Diagnostico:
    ventas: float
    resultado_neto: float
    bait: float
    activo_total: float
    patrimonio_neto: float
    pasivo_total: float
    activo_corriente: float
    pasivo_corriente: float
    gastos_financieros: float
    cargas_fijas: float
    margen_contribucion_pct: float

    @property
    def roa(self) -> float:
        return _round(self.bait / self.activo_total) if self.activo_total else 0.0

    @property
    def roe(self) -> float:
        return _round(self.resultado_neto / self.patrimonio_neto) if self.patrimonio_neto else 0.0

    @property
    def liquidez_general(self) -> float:
        return _round(self.activo_corriente / self.pasivo_corriente) if self.pasivo_corriente else 0.0

    @property
    def endeudamiento(self) -> float:
        return _round(self.pasivo_total / self.activo_total) if self.activo_total else 0.0
