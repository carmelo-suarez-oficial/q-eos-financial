"""
Q-EOS Financial Management Framework
Aplicación principal unificada (Versión 2.2 - A prueba de errores)
"""
import streamlit as st
import pandas as pd
from core.margen import calcular_precio
from core.modelo_economico import LineaNegocio, PresupuestoOperaciones

st.set_page_config(page_title="Q-EOS Financial Framework", page_icon="🏛️", layout="wide")

st.sidebar.title("🏛️ Q-EOS")
st.sidebar.markdown("Sistema de Gestión Financiera")

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
    st.caption("Añade tus líneas de negocio para calcular el resultado previsional.")
    
    st.markdown("### 1. Introduce tus líneas de negocio")
    if "lineas_data" not in st.session_state:
        st.session_state.lineas_data = pd.DataFrame([
            {"Nombre": "Producto A", "Ventas (€)": 100000.0, "Margen (%)": 30.0, "Cargas (€)": 20000.0},
            {"Nombre": "Producto B", "Ventas (€)": 50000.0, "Margen (%)": 20.0, "Cargas (€)": 10000.0}
        ])
        
    # Usamos width="stretch" para evitar los avisos amarillos
    edited_df = st.data_editor(st.session_state.lineas_data, num_rows="dynamic", width="stretch")
    
    if st.button("Calcular Resultado Previsional"):
        # Función blindada para convertir cualquier celda vacía o error en 0.0
        def safe_float(val):
            if pd.isna(val) or val is None or str(val).strip() == "":
                return 0.0
            try:
                return float(val)
            except (ValueError, TypeError):
                return 0.0

        p = PresupuestoOperaciones()
        for _, row in edited_df.iterrows():
            nombre = str(row["Nombre"]) if not pd.isna(row["Nombre"]) else "Sin nombre"
            linea = LineaNegocio(
                nombre=nombre, 
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