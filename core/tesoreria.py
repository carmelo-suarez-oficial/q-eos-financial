"""
Q-EOS Financial Management Framework
Módulo: core.tesoreria
"""
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP

def _round(value: float, decimals: int = 2) -> float:
    quant = Decimal(10) ** -decimals
    return float(Decimal(str(value)).quantize(quant, rounding=ROUND_HALF_UP))

@dataclass(frozen=True)
class PeriodoTesoreria:
    nombre: str
    ingresos: float = 0.0
    gastos: float = 0.0
    cobros: float = 0.0
    pagos: float = 0.0

    @property
    def flujo_neto_caja(self) -> float:
        return _round(self.cobros - self.pagos)

    @property
    def resultado_devengo(self) -> float:
        return _round(self.ingresos - self.gastos)

    @property
    def desfase_financiero(self) -> float:
        return _round(self.cobros - self.ingresos)

@dataclass(frozen=True)
class PresupuestoTesoreria:
    periodos: tuple[PeriodoTesoreria, ...]
    saldo_inicial: float
    saldo_minimo: float = 0.0

    @property
    def lineas(self):
        out = []
        saldo = self.saldo_inicial
        for p in self.periodos:
            final = _round(saldo + p.flujo_neto_caja)
            out.append((p, saldo, final))
            saldo = final
        return out

    @property
    def saldo_final(self) -> float:
        return self.lineas[-1][2]

    @property
    def alerta_liquidez(self) -> bool:
        return min(l[2] for l in self.lineas) < self.saldo_minimo
