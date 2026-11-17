"""
Pruebas de validación de los módulos del Q-EOS.
"""
import pytest
from core.margen import calcular_precio, coeficiente_relacion
from core.modelo_economico import LineaNegocio, ResultadoPrevisional
from core.balances import ActivoCorriente, ActivoNoCorriente, Balance, PatrimonioNeto, PasivoCorriente, PasivoNoCorriente

def test_calculo_margen_ejemplo_manual():
    # Manual: PCsi 1750, Mg 30% -> PVsi 2500
    r = calcular_precio(precio_coste=1750.0, margen_pct=30.0, iva_pct=0.0)
    assert r.precio_venta_sin_iva == 2500.0
    assert r.importe_margen == 750.0

def test_modelo_economico_basico():
    linea = LineaNegocio("A", ventas=100_000, margen_pct=30, cargas_estructura=20_000)
    assert linea.margen_bruto == 30_000.0
    assert linea.resultado == 10_000.0

def test_balance_cuadra():
    b = Balance(
        nombre="Test",
        activo_no_corriente=ActivoNoCorriente(inmovilizado_material=50_000),
        activo_corriente=ActivoCorriente(tesoreria=50_000),
        patrimonio_neto=PatrimonioNeto(capital=80_000, resultado_ejercicio=20_000),
        pasivo_no_corriente=PasivoNoCorriente(deuda_largo_plazo=0),
        pasivo_corriente=PasivoCorriente(proveedores=0)
    )
    assert b.total_activo == 100_000.0
    assert b.descuadre == 0.0
