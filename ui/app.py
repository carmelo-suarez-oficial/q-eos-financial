"""
Q-EOS Financial Management Framework
Aplicación principal unificada
"""
import streamlit as st
import pandas as pd
from core.margen import calcular_precio
from core.modelo_economico import LineaNegocio, PresupuestoOperaciones
from core.tesoreria import desde_modelo_economico

st.set_page_config(page_title="Q-EOS Financial Framework", page_icon="🏛️", layout="wide")

st.sidebar.title("🏛️ Q-EOS")
st.sidebar.markdown("Sistema de Gestión Financiera")

# Menú de navegación en la barra lateral
menu = st.sidebar.radio(
    "Selecciona un módulo:",
    ["1. Margen y Precios", "2. Modelo Económico", "3. Tesorería"]
)

# --- PÁGINA 1: MARGEN ---
if menu == "1. Margen y Precios":
    st.title("💶 Gestión del Margen")
    st.caption("Calcula el precio de venta a partir del coste y el margen objetivo.")
    
    c1, c2, c3 = st.columns(3)
    pcsi = c1.number_input("Coste sin IVA (€)", min_value=0.01, value=1750.0)
    mg = c2.number_input("Margen (%)", min_value=0.0, max_value=99.99, value=30.0)
    iva = c3.number_input("IVA (%)", min_value=0.0, value=21.0)
    
    if st.button("Calcular Precio"):
        r = calcular_precio(pcsi, mg, iva)
        c1, c2, c3 = st.columns(3)
        c1.metric("PVsi (sin IVA)", f"{r.precio_venta_sin_iva:,.2f} €")
        c2.metric("PVP (con IVA)", f"{r.precio_venta_con_iva:,.2f} €")
        c3.metric("Margen Real", f"{r.margen_real_pct:.2f} %")

# --- PÁGINA 2: MODELO ECONÓMICO ---
elif menu == "2. Modelo Económico":
    st.title("📊 Presupuesto de Operaciones")
    st.caption("Calcula el resultado previsional de tu negocio.")
    
    c1, c2, c3 = st.columns(3)
    ventas = c1.number_input("Ventas previstas (€)", min_value=0.0, value=100000.0)
    margen = c2.number_input("Margen sobre ventas (%)", min_value=0.0, value=30.0)
    cargas = c3.number_input("Cargas totales (€)", min_value=0.0, value=25000.0)
    
    if st.button("Calcular Resultado"):
        linea = LineaNegocio("Línea 1", ventas, margen, cargas)
        st.success(f"Resultado estimado: **{linea.resultado:,.2f} €**")
        st.write(f"Margen bruto: {linea.margen_bruto:,.2f} €")

# --- PÁGINA 3: TESORERÍA ---
elif menu == "3. Tesorería":
    st.title("💧 Presupuesto de Tesorería")
    st.caption("Analiza el flujo de caja de tu empresa.")
    
    c1, c2 = st.columns(2)
    saldo = c1.number_input("Saldo inicial en caja (€)", min_value=0.0, value=20000.0)
    desfase = c2.number_input("Desfase de cobros (€)", value=-5000.0)
    
    if st.button("Calcular Flujo de Caja"):
        st.info("Simulación simple de tesorería")
        st.write(f"El saldo final previsto es: **{saldo + desfase:,.2f} €**")
