"""
Q-EOS Financial Management Framework
Aplicación completa (Versión 6.0 - Base de Datos Integrada)
"""
import streamlit as st
import pandas as pd
from core.margen import calcular_precio
from core.modelo_economico import LineaNegocio, PresupuestoOperaciones
from core.balances import ActivoNoCorriente, ActivoCorriente, PatrimonioNeto, PasivoNoCorriente, PasivoCorriente, Balance
from core.diagnostico import Diagnostico
from core.control import Desviacion
import database

st.set_page_config(page_title="Q-EOS Financial Framework", page_icon="🏛️", layout="wide")

# Inicializamos la DB por si acaso no está creada
database.inicializar_db()

GLOSARIO = {
    "ROE (Rentabilidad Financiera)": "Mide el beneficio que obtienen los accionistas por cada euro invertido en la empresa.",
    "ROA (Rentabilidad Económica)": "Mide la eficiencia de los activos de la empresa para generar beneficios.",
    "Fondo de Maniobra": "Representa los recursos financieros a largo plazo que financian el activo corriente.",
    "BAIT": "Beneficio Antes de Intereses e Impuestos.",
    "Liquidez General": "Capacidad de la empresa para hacer frente a sus deudas a corto plazo.",
    "Capital Circulante": "Recursos para financiar el ciclo de explotación.",
    "Desviación Presupuestaria": "Diferencia entre los datos reales y los presupuestos.",
    "Umbral de Rentabilidad": "Nivel mínimo de ventas para cubrir todos los costes."
}

st.sidebar.title("🏛️ Q-EOS")
st.sidebar.markdown("Sistema de Gestión Financiera")
st.sidebar.divider()

menu = st.sidebar.radio(
    "Selecciona un módulo:",
    ["🏠 Inicio / Dashboard", "1. Margen y Precios", "2. Modelo Económico", "3. Tesorería", "4. Balance Previsional", "5. Diagnóstico", "6. Control de Gestión", "7. Glosario Financiero", "8. Simulación Directiva"]
)

# --- PÁGINA 0: DASHBOARD ---
if menu == "🏠 Inicio / Dashboard":
    st.title("🏛️ Q-EOS Financial Management Framework")
    st.markdown("### Bienvenido a tu Sistema de Gestión Financiera")
    st.write("Esta aplicación te permite planificar, analizar y controlar la situación económica de tu empresa paso a paso.")
    st.divider()
    st.markdown("### 📊 Resumen Ejecutivo (Ejemplo)")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Ventas Totales", "150.000 €", delta="+12%")
    c2.metric("Margen Bruto", "45.000 €", delta="+5%")
    c3.metric("Resultado Neto", "15.000 €", delta="-2%")
    c4.metric("Liquidez", "1.85", delta="Saludable")
    st.divider()
    st.markdown("### 📚 Guía de Módulos")
    col1, col2 = st.columns(2)
    with col1:
        st.info("**1. Margen y Precios**\nCalcula el precio de venta ideal.")
        st.info("**2. Modelo Económico**\nEstima cuánto vas a ganar o perder.")
        st.info("**3. Tesorería**\nControla el flujo de caja.")
    with col2:
        st.success("**4. Balance Previsional**\nComprueba que tus cuentas cuadran.")
        st.success("**5. Diagnóstico**\nAnaliza ratios clave como el ROE y el ROA.")
        st.success("**6. Control de Gestión**\nCompara lo previsto con lo real.")

# --- PÁGINA 1: MARGEN ---
elif menu == "1. Margen y Precios":
    st.title("💶 Gestión del Margen")
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
            linea = LineaNegocio(nombre=str(row["Nombre"]), ventas=safe_float(row["Ventas (€)"]), margen_pct=safe_float(row["Margen (%)"]), cargas_estructura=safe_float(row["Cargas (€)"]))
            p.add(linea)
        
        st.session_state.resultado_presupuesto = p.cerrar()

    if "resultado_presupuesto" in st.session_state:
        res = st.session_state.resultado_presupuesto
        
        st.markdown("### Resultados")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Ventas", f"{res.ventas_totales:,.2f} €")
        c2.metric("Margen Bruto", f"{res.margen_bruto_total:,.2f} €")
        c3.metric("Cargas", f"{res.cargas_totales:,.2f} €")
        c4.metric("Resultado", f"{res.resultado_total:,.2f} €")
        
        st.bar_chart(pd.DataFrame({"Euros": [res.margen_bruto_total, res.cargas_totales, res.resultado_total]}, index=["Margen", "Cargas", "Resultado"]))
        
        st.divider()
        st.markdown("### 💾 Guardar en Base de Datos")
        nombre_presupuesto = st.text_input("Nombre para este presupuesto:", "Presupuesto Ejemplo")
        
        if st.button("Guardar Presupuesto"):
            database.guardar_presupuesto(
                nombre=nombre_presupuesto, 
                ventas=res.ventas_totales, 
                margen=res.margen_bruto_total, 
                cargas=res.cargas_totales
            )
            st.success("¡Presupuesto guardado en la base de datos con éxito!")
            st.rerun()

    st.divider()
    st.markdown("### 📂 Historial de Presupuestos Guardados")
    
    df_historial = database.obtener_presupuestos()
    
    if not df_historial.empty:
        st.dataframe(df_historial, width="stretch")
        
        st.markdown("#### Cargar un presupuesto guardado")
        opciones = df_historial.apply(lambda x: f"ID {x['id']}: {x['nombre']} ({x['fecha'][:10]})", axis=1).tolist()
        seleccion = st.selectbox("Selecciona un presupuesto para cargar en la tabla:", opciones)
        
        if st.button("Cargar Presupuesto Seleccionado"):
            id_seleccionado = int(seleccion.split(":")[0].replace("ID ", ""))
            fila = df_historial[df_historial["id"] == id_seleccionado].iloc[0]
            
            st.session_state.lineas_data = pd.DataFrame([
                {"Nombre": fila["nombre"], "Ventas (€)": fila["ventas"], "Margen (%)": (fila["margen"]/fila["ventas"]*100) if fila["ventas"]>0 else 0, "Cargas (€)": fila["cargas"]}
            ])
            st.success(f"Presupuesto '{fila['nombre']}' cargado en la tabla superior.")
            st.rerun()
            
    else:
        st.info("Aún no hay presupuestos guardados en la base de datos.")

# --- PÁGINA 3: TESORERÍA ---
elif menu == "3. Tesorería":
    st.title("💧 Presupuesto de Tesorería")
    c1, c2 = st.columns(2)
    saldo = c1.number_input("Saldo inicial (€)", value=20000.0)
    desfase = c2.number_input("Desfase de cobros (€)", value=-5000.0)
    if st.button("Calcular"):
        st.write(f"Saldo final previsto: **{saldo + desfase:,.2f} €**")

# --- PÁGINA 4: BALANCE PREVISIONAL ---
elif menu == "4. Balance Previsional":
    st.title("⚖️ Balance Previsional")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### ACTIVO")
        inm = st.number_input("Inmovilizado (€)", value=100000.0)
        amort = st.number_input("Amortización (€)", value=10000.0)
        exist = st.number_input("Existencias (€)", value=10000.0)
        clientes = st.number_input("Clientes (€)", value=20000.0)
        tesoreria = st.number_input("Caja (€)", value=30000.0)
        anc = ActivoNoCorriente(inmovilizado_material=inm, amortizacion_acumulada=amort)
        ac = ActivoCorriente(existencias=exist, clientes=clientes, tesoreria=tesoreria)
    with col2:
        st.markdown("#### PASIVO Y PN")
        capital = st.number_input("Capital (€)", value=80000.0)
        reservas = st.number_input("Reservas (€)", value=20000.0)
        resultado = st.number_input("Resultado (€)", value=10000.0)
        deuda_lp = st.number_input("Deuda LP (€)", value=20000.0)
        proveedores = st.number_input("Proveedores (€)", value=20000.0)
        pn = PatrimonioNeto(capital=capital, reservas=reservas, resultado_ejercicio=resultado)
        pnc = PasivoNoCorriente(deuda_largo_plazo=deuda_lp)
        pc = PasivoCorriente(proveedores=proveedores)
    if st.button("Comprobar Balance"):
        balance = Balance(nombre="Balance", activo_no_corriente=anc, activo_corriente=ac, patrimonio_neto=pn, pasivo_no_corriente=pnc, pasivo_corriente=pc, tolerancia=1000000.0)
        c1, c2, c3 = st.columns(3)
        c1.metric("Activo", f"{balance.total_activo:,.2f} €")
        c2.metric("Pasivo + PN", f"{balance.total_pasivo_mas_pn:,.2f} €")
        c3.metric("Descuadre", f"{balance.descuadre:,.2f} €")
        if abs(balance.descuadre) < 0.01: st.success("✅ El balance cuadra.")
        else: st.warning("⚠️ El balance no cuadra.")

# --- PÁGINA 5: DIAGNÓSTICO ---
elif menu == "5. Diagnóstico":
    st.title("🩺 Diagnóstico")
    c1, c2, c3 = st.columns(3)
    ventas = c1.number_input("Ventas (€)", value=150000.0)
    resultado = c2.number_input("Resultado (€)", value=10000.0)
    bait = c3.number_input("BAIT (€)", value=12000.0)
    c1, c2 = st.columns(2)
    activo = c1.number_input("Activo (€)", value=150000.0)
    pn = c2.number_input("PN (€)", value=110000.0)
    if st.button("Calcular Diagnóstico"):
        diag = Diagnostico(ventas=ventas, resultado_neto=resultado, bait=bait, activo_total=activo, patrimonio_neto=pn, pasivo_total=activo-pn, activo_corriente=60000, pasivo_corriente=20000, gastos_financieros=2000, cargas_fijas=30000, margen_contribucion_pct=40)
        c1, c2, c3 = st.columns(3)
        c1.metric("ROA", f"{diag.roa*100:.2f} %")
        c2.metric("ROE", f"{diag.roe*100:.2f} %")
        c3.metric("Liquidez", f"{diag.liquidez_general:.2f}")
        if diag.roe > 0.10: st.success("🟢 Empresa saludable")
        elif diag.roe > 0: st.warning("🟡 Rentabilidad mejorable")
        else: st.error("🔴 Pérdidas")

# --- PÁGINA 6: CONTROL DE GESTIÓN ---
elif menu == "6. Control de Gestión":
    st.title("🎛️ Control de Gestión")
    if "control_data" not in st.session_state:
        st.session_state.control_data = pd.DataFrame([
            {"Concepto": "Ventas", "Tipo": "Ingreso", "Presupuesto (€)": 100000.0, "Real (€)": 95000.0},
            {"Concepto": "Resultado", "Tipo": "Margen", "Presupuesto (€)": 20000.0, "Real (€)": 18000.0},
            {"Concepto": "Cargas", "Tipo": "Coste", "Presupuesto (€)": 15000.0, "Real (€)": 16000.0}
        ])
    edited_control = st.data_editor(st.session_state.control_data, num_rows="dynamic", width="stretch")
    if st.button("Analizar Desviaciones"):
        resultados = []
        for _, row in edited_control.iterrows():
            c = str(row["Concepto"])
            t = str(row["Tipo"]).lower()
            p = float(row["Presupuesto (€)"]) if not pd.isna(row["Presupuesto (€)"]) else 0.0
            r = float(row["Real (€)"]) if not pd.isna(row["Real (€)"]) else 0.0
            if t in ["ingreso", "margen", "coste"]:
                d = Desviacion(c, r, p, t)
                col = "🟢" if d.es_favorable else "🔴"
                resultados.append({"Concepto": c, "Presupuesto": f"{p:,.2f} €", "Real": f"{r:,.2f} €", "Desviación": f"{d.importe:,.2f} €", "Evaluación": f"{col} {'FAVORABLE' if d.es_favorable else 'DESFAVORABLE'}"})
        if resultados:
            df_resultados = pd.DataFrame(resultados)
            st.dataframe(df_resultados, width="stretch")
            excel_data_control = pd.ExcelWriter("control.xlsx", engine="openpyxl")
            df_resultados.to_excel(excel_data_control, index=False, sheet_name="Desviaciones")
            excel_data_control.close()
            with open("control.xlsx", "rb") as f:
                st.download_button("⬇️ Descargar Informe de Desviaciones en Excel", data=f, file_name="control_gestion.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# --- PÁGINA 7: GLOSARIO ---
elif menu == "7. Glosario Financiero":
    st.title("📚 Glosario Financiero")
    st.markdown("### Buscador de términos")
    busqueda = st.text_input("Escribe una palabra para buscar:", "")
    terminos_filtrados = {k: v for k, v in GLOSARIO.items() if busqueda.lower() in k.lower() or busqueda.lower() in v.lower()}
    if busqueda:
        if terminos_filtrados:
            for termino, definicion in terminos_filtrados.items():
                st.info(f"**{termino}**\n\n{definicion}")
        else:
            st.warning("No se han encontrado términos.")
    else:
        for termino, definicion in GLOSARIO.items():
            with st.expander(termino):
                st.write(definicion)

# --- PÁGINA 8: SIMULACIÓN DIRECTIVA ---
elif menu == "8. Simulación Directiva":
    st.title("🎮 Simulación Directiva (¿Qué pasaría si...?)")
    c1, c2, c3 = st.columns(3)
    base_ventas = c1.number_input("Ventas Base (€)", value=150000.0)
    base_margen = c2.number_input("Margen Base (%)", value=30.0)
    base_cargas = c3.number_input("Cargas Base (€)", value=30000.0)
    st.divider()
    delta_ventas = st.slider("Variación en Ventas (%)", min_value=-50, max_value=50, value=0)
    delta_margen = st.slider("Variación en Margen (puntos)", min_value=-20, max_value=20, value=0)
    delta_cargas = st.slider("Variación en Cargas (%)", min_value=-30, max_value=50, value=0)
    
    margen_bruto_base = base_ventas * (base_margen / 100)
    resultado_base = margen_bruto_base - base_cargas
    
    sim_ventas = base_ventas * (1 + delta_ventas / 100)
    sim_margen = base_margen + delta_margen
    sim_margen_bruto = sim_ventas * (sim_margen / 100)
    sim_cargas = base_cargas * (1 + delta_cargas / 100)
    sim_resultado = sim_margen_bruto - sim_cargas
    
    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 🔵 Escenario Base")
        st.metric("Resultado Base", f"{resultado_base:,.2f} €")
    with c2:
        st.markdown("#### 🟢 Escenario Simulado")
        st.metric("Resultado Simulado", f"{sim_resultado:,.2f} €", delta=f"{sim_resultado - resultado_base:,.2f} € vs Base")
        
    if sim_resultado > resultado_base: st.success("¡Buena decisión! El resultado mejora.")
    elif sim_resultado == resultado_base: st.info("Las decisiones no alteran el resultado.")
    else: st.warning("Cuidado: Estas decisiones reducen el beneficio.")