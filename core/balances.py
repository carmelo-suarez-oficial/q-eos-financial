"""
Q-EOS Financial Management Framework
Módulo: core.balances
"""
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP

def _round(value: float, decimals: int = 2) -> float:
    quant = Decimal(10) ** -decimals
    return float(Decimal(str(value)).quantize(quant, rounding=ROUND_HALF_UP))

@dataclass(frozen=True)
class ActivoNoCorriente:
    inmovilizado_material: float = 0.0
    amortizacion_acumulada: float = 0.0
    @property
    def total(self) -> float:
        return _round(self.inmovilizado_material - self.amortizacion_acumulada)

@dataclass(frozen=True)
class ActivoCorriente:
    existencias: float = 0.0
    clientes: float = 0.0
    tesoreria: float = 0.0
    @property
    def total(self) -> float:
        return _round(self.existencias + self.clientes + self.tesoreria)

@dataclass(frozen=True)
class PatrimonioNeto:
    capital: float = 0.0
    reservas: float = 0.0
    resultado_ejercicio: float = 0.0
    @property
    def total(self) -> float:
        return _round(self.capital + self.reservas + self.resultado_ejercicio)

@dataclass(frozen=True)
class PasivoNoCorriente:
    deuda_largo_plazo: float = 0.0
    @property
    def total(self) -> float:
        return _round(self.deuda_largo_plazo)

@dataclass(frozen=True)
class PasivoCorriente:
    proveedores: float = 0.0
    deuda_corto_plazo: float = 0.0
    @property
    def total(self) -> float:
        return _round(self.proveedores + self.deuda_corto_plazo)

@dataclass(frozen=True)
class Balance:
    nombre: str
    activo_no_corriente: ActivoNoCorriente
    activo_corriente: ActivoCorriente
    patrimonio_neto: PatrimonioNeto
    pasivo_no_corriente: PasivoNoCorriente
    pasivo_corriente: PasivoCorriente
    tolerancia: float = 0.01

    @property
    def total_activo(self) -> float:
        return _round(self.activo_no_corriente.total + self.activo_corriente.total)

    @property
    def total_pasivo_mas_pn(self) -> float:
        return _round(self.pasivo_no_corriente.total + self.pasivo_corriente.total + self.patrimonio_neto.total)

    @property
    def descuadre(self) -> float:
        return _round(self.total_activo - self.total_pasivo_mas_pn)

    @property
    def fondo_maniobra(self) -> float:
        return _round(self.activo_corriente.total - self.pasivo_corriente.total)
