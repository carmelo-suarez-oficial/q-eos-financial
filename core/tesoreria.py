from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from core.modelo_economico import ResultadoPrevisional

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

@dataclass(frozen=True)
class PresupuestoTesoreria:
    periodos: tuple[PeriodoTesoreria, ...]
    saldo_inicial: float
    saldo_minimo: float = 0.0

    @property
    def saldo_final(self) -> float:
        saldo = self.saldo_inicial
        for p in self.periodos:
            saldo = _round(saldo + p.flujo_neto_caja)
        return saldo

def desde_modelo_economico(resultado: ResultadoPrevisional, saldo_inicial: float, desfase_cobros: float = 0.0, desfase_pagos: float = 0.0) -> PresupuestoTesoreria:
    ingresos = resultado.ventas_totales
    gastos = _round(ingresos - resultado.resultado_total)
    cobros = _round(ingresos + desfase_cobros)
    pagos = _round(gastos + desfase_pagos)
    periodo = PeriodoTesoreria("Periodo-1", ingresos, gastos, cobros, pagos)
    return PresupuestoTesoreria((periodo,), saldo_inicial)