"""
Q-EOS Financial Management Framework
Módulo: core.margen
"""
from dataclasses import dataclass, asdict
from decimal import Decimal, ROUND_HALF_UP

class MargenError(ValueError):
    pass

def _round(value: float, decimals: int = 2) -> float:
    quant = Decimal(10) ** -decimals
    return float(Decimal(str(value)).quantize(quant, rounding=ROUND_HALF_UP))

def coeficiente_relacion(margen_pct: float) -> float:
    if margen_pct < 0 or margen_pct >= 100:
        raise MargenError("El margen debe estar entre 0 y 99.99%.")
    return 1.0 / (1.0 - margen_pct / 100.0)

@dataclass(frozen=True)
class CalculoPrecio:
    precio_coste: float
    margen_objetivo_pct: float
    coeficiente_relacion: float
    precio_venta_sin_iva: float
    iva_pct: float
    precio_venta_con_iva: float
    margen_real_pct: float
    importe_margen: float

    def to_dict(self) -> dict:
        return asdict(self)

def calcular_precio(precio_coste: float, margen_pct: float, iva_pct: float = 21.0, decimales: int = 2) -> CalculoPrecio:
    if precio_coste <= 0:
        raise MargenError("El precio de coste debe ser mayor que cero.")
    
    cr = coeficiente_relacion(margen_pct)
    pvsi = precio_coste * cr
    pvp = pvsi * (1.0 + iva_pct / 100.0)
    importe_margen = pvsi - precio_coste
    margen_real = (importe_margen / pvsi) * 100.0

    return CalculoPrecio(
        precio_coste=_round(precio_coste, decimales),
        margen_objetivo_pct=_round(margen_pct, 4),
        coeficiente_relacion=_round(cr, 9),
        precio_venta_sin_iva=_round(pvsi, decimales),
        iva_pct=_round(iva_pct, 2),
        precio_venta_con_iva=_round(pvp, decimales),
        margen_real_pct=_round(margen_real, 4),
        importe_margen=_round(importe_margen, decimales),
    )
