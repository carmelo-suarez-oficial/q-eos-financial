"""
Q-EOS Financial Management Framework
Aplicación completa (Versión 3.0 - Plan de Gestión)
"""
import streamlit as st
import pandas as pd
from core.margen import calcular_precio
from core.modelo_economico import LineaNegocio, PresupuestoOperaciones
from core.balances import ActivoNoCorriente, ActivoCorriente, PatrimonioNeto, PasivoNoCorriente, PasivoCorriente, Balance
from core.diagnostico import Diagnostico

st.set_page_config(page_title="Q-EOS Financial Framework", page_icon="🏛️", layout="wide")

st.sidebar.title("🏛️ Q-EOS")
st.sidebar.markdown("Sistema de Gestión Financiera")

menu = st.sidebar.radio(
    "Selecciona un módulo:",
    ["1. Margen y Precios", "2. Modelo Económico", "3. Tesorería", "4. Balance Previsional", "5. Diagnóstico"]
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
    st.caption("Añade tus líneas de negocio para calcular el resultado previsional.")
    
    st.markdown("### 1. Introduce tus líneas de negocio")
    if "lineas_data" not in st.session_state:
        st.session_state.lineas_data = pd.DataFrame([
            {"Nombre": "Producto A", "Ventas (€)": 100000.0, "Margen (%)": 30.0, "Cargas (€)": 20000.0},
            {"Nombre": "Producto B", "Ventas (€)": 50000.0, "Margen (%)": 20.0, "Cargas (€)": 10000.0}
        ])
        
    edited_df = st.data_editor(st.session_state.lineas_data, num_rows="dynamic", width="stretch")
    
    if st.button("Calcular Resultado Previsional"):
        def safe_float(val):
            if pd.isna(val) or val is None or str(val).strip() == "": return 0.0
            try: return float(val)
            except: return 0.0

        p = PresupuestoOperaciones()
        for _, row in edited_df.iterrows():
            linea = LineaNegocio(
                nombre=str(row["Nombre"]) if not pd.isna(row["Nombre"]) else "Sin nombre", 
                ventas=safe_float(row["Ventas (€)"]), 
                margen_pct=safe_float(row["Margen (%)"]), 
                cargas_estructura=safe_float(row["Cargas (€)"])
            )
            p.add(linea)
            
        resultado = p.cerrar()
        
        st.markdown("### 2. Resultados")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Ventas Totales", f"{resultado.ventas_totales:,.2f} €")
        c2.metric("Margen Bruto", f"{resultado.margen_bruto_total:,.2f} €")
        c3.metric("Cargas Totales", f"{resultado.cargas_totales:,.2f} €")
        delta_pct = (resultado.resultado_total / resultado.ventas_totales * 100) if resultado.ventas_totales > 0 else 0
        c4.metric("Resultado", f"{resultado.resultado_total:,.2f} €", delta=f"{delta_pct:.1f}% s/ventas")
        
        st.markdown("### 3. Gráfico de Contribución")
        chart_data = pd.DataFrame({
            "Concepto": ["Margen Bruto", "Cargas", "Resultado"],
            "Euros": [resultado.margen_bruto_total, resultado.cargas_totales, resultado.resultado_total]
        })
        st.bar_chart(chart_data.set_index("Concepto"))

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

# --- PÁGINA 4: BALANCE PREVISIONAL ---
elif menu == "4. Balance Previsional":
    st.title("⚖️ Balance Previsional")
    st.caption("Comprueba la ecuación fundamental: Activo = Pasivo + Patrimonio Neto")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### ACTIVO")
        inm = st.number_input("Inmovilizado material (€)", value=100000.0)
        amort = st.number_input("Amortización acumulada (€)", value=10000.0)
        exist = st.number_input("Existencias (€)", value=10000.0)
        clientes = st.number_input("Clientes (€)", value=20000.0)
        tesoreria = st.number_input("Tesorería / Caja (€)", value=30000.0)
        
        anc = ActivoNoCorriente(inmovilizado_material=inm, amortizacion_acumulada=amort)
        ac = ActivoCorriente(existencias=exist, clientes=clientes, tesoreria=tesoreria)
        
    with col2:
        st.markdown("#### PASIVO Y PATRIMONIO NETO")
        capital = st.number_input("Capital (€)", value=80000.0)
        reservas = st.number_input("Reservas (€)", value=20000.0)
        resultado = st.number_input("Resultado del ejercicio (€)", value=10000.0)
        deuda_lp = st.number_input("Deuda a largo plazo (€)", value=20000.0)
        proveedores = st.number_input("Proveedores (€)", value=20000.0)
        
        pn = PatrimonioNeto(capital=capital, reservas=reservas, resultado_ejercicio=resultado)
        pnc = PasivoNoCorriente(deuda_largo_plazo=deuda_lp)
        pc = PasivoCorriente(proveedores=proveedores)
        
    if st.button("Calcular y Comprobar Balance"):
        balance = Balance(
            nombre="Balance Previsional", 
            activo_no_corriente=anc, activo_corriente=ac, 
            patrimonio_neto=pn, pasivo_no_corriente=pnc, pasivo_corriente=pc,
            tolerancia=1000000.0 # Tolerancia alta para permitir visualización
        )
        
        st.markdown("### Resultados del Balance")
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Activo", f"{balance.total_activo:,.2f} €")
        c2.metric("Total Pasivo + PN", f"{balance.total_pasivo_mas_pn:,.2f} €")
        c3.metric("Descuadre", f"{balance.descuadre:,.2f} €")
        
        if abs(balance.descuadre) < 0.01:
            st.success("✅ El balance cuadra perfectamente.")
        else:
            st.warning("⚠️ El balance no cuadra. Revisa las partidas.")
            
        st.info(f"El Fondo de Maniobra es: **{balance.fondo_maniobra:,.2f} €**")

# --- PÁGINA 5: DIAGNÓSTICO ---
elif menu == "5. Diagnóstico":
    st.title("🩺 Diagnóstico Económico-Financiero")
    st.caption("Analiza la rentabilidad y la viabilidad de la empresa.")
    
    st.markdown("### 1. Datos para el análisis")
    c1, c2, c3 = st.columns(3)
    ventas = c1.number_input("Ventas Totales (€)", value=150000.0)
    resultado = c2.number_input("Resultado Neto (€)", value=10000.0)
    bait = c3.number_input("BAIT (Beneficio antes de intereses e impuestos)", value=12000.0)
    
    c1, c2 = st.columns(2)
    activo = c1.number_input("Activo Total (€)", value=150000.0)
    pn = c2.number_input("Patrimonio Neto (€)", value=110000.0)
    
    if st.button("Calcular Diagnóstico"):
        # Creamos un objeto de diagnóstico básico
        diag = Diagnostico(
            ventas=ventas, resultado_neto=resultado, bait=bait,
            activo_total=activo, patrimonio_neto=pn, pasivo_total=activo-pn,
            activo_corriente=60000, pasivo_corriente=20000,
            gastos_financieros=2000, cargas_fijas=30000, margen_contribucion_pct=40
        )
        
        st.markdown("### 2. Ratios Clave")
        c1, c2, c3 = st.columns(3)
        c1.metric("ROA (Rentabilidad Económica)", f"{diag.roa*100:.2f} %")
        c2.metric("ROE (Rentabilidad Financiera)", f"{diag.roe*100:.2f} %")
        c3.metric("Liquidez General", f"{diag.liquidez_general:.2f}")
        
        st.markdown("### 3. Semáforo de Viabilidad")
        if diag.roe > 0.10:
            st.success("🟢 Empresa saludable (ROE > 10%)")
        elif diag.roe > 0:
            st.warning("🟡 Rentabilidad positiva pero mejorable")
        else:
            st.error("🔴 Pérdidas: La empresa destruye valor")