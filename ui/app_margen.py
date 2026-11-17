"""
Q-EOS Financial Management Framework
Interfaz Visual: Módulo de Margen y Fijación de Precios
"""
import streamlit as st
import pandas as pd
from core.margen import calcular_precio

st.set_page_config(page_title="Q-EOS · Margen", page_icon="💶", layout="wide")
st.title("💶 Q-EOS · Gestión del Margen y Fijación de Precios")
st.caption("Unidad 1 · Conceptos previos — Plan de Gestión")

st.subheader("Calculadora de precio de venta")
col1, col2, col3 = st.columns(3)

with col1:
    pcsi = st.number_input("Precio de coste sin IVA (PCsi)", min_value=0.01, value=1750.0, step=10.0)
with col2:
    mg = st.number_input("Margen sobre venta neta (%)", min_value=0.0, max_value=99.99, value=30.0, step=0.25)
with col3:
    iva = st.number_input("IVA repercutido (%)", min_value=0.0, max_value=50.0, value=21.0, step=1.0)

if st.button("Calcular Precio"):
    try:
        r = calcular_precio(pcsi, mg, iva)
        
        st.success("Cálculo realizado correctamente")
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Coeficiente (CR)", f"{r.coeficiente_relacion:.6f}")
        c2.metric("PVsi (sin IVA)", f"{r.precio_venta_sin_iva:,.2f} €")
        c3.metric("PVP (con IVA)", f"{r.precio_venta_con_iva:,.2f} €")
        c4.metric("Margen real", f"{r.margen_real_pct:.2f} %")
        
        st.divider()
        st.markdown("### Desglose")
        df = pd.DataFrame([r.to_dict()]).T
        df.columns = ["Valor"]
        st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"Error: {e}")
