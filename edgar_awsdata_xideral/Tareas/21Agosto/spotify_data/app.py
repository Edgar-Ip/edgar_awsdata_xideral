import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==============================
# Configuración inicial
# ==============================
st.set_page_config(page_title="Spotify Dashboard", layout="wide")

st.title("🎵 Dashboard de Análisis Spotify")

# Sidebar: cargar archivo CSV
st.sidebar.title("Datos")
file = st.sidebar.file_uploader("Sube tu archivo CSV de Spotify", type=["csv"])

if file is None:
    st.warning("⚠️ Sube un archivo CSV para continuar.")
    st.stop()

# Leer datos
df = pd.read_csv(file)

# ==============================
# KPIs
# ==============================
total_songs = df.shape[0]
liked_ratio = df['liked'].mean() * 100
avg_danceability = df['danceability'].mean()
avg_energy = df['energy'].mean()
avg_duration_min = (df['duration_ms'].mean()) / 60000

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.metric("Total canciones", total_songs)
with c2:
    st.metric("% Canciones gustadas", f"{liked_ratio:.2f}%")
with c3:
    st.metric("Danceability promedio", f"{avg_danceability:.2f}")
with c4:
    st.metric("Energy promedio", f"{avg_energy:.2f}")
with c5:
    st.metric("Duración promedio", f"{avg_duration_min:.2f} min")

st.markdown("----")

# ==============================
# Visualizaciones
# ==============================
cols = st.columns(2)

# --- Distribución liked ---
with cols[0]:
    st.subheader("Distribución de canciones gustadas")
    fig, ax = plt.subplots(figsize=(6,4))
    df['liked'].value_counts().plot(kind='bar', ax=ax, color=['salmon','skyblue'])
    ax.set_xlabel("Liked (0 = No, 1 = Sí)")
    ax.set_ylabel("Cantidad")
    st.pyplot(fig)

# --- Modo mayor vs menor ---
with cols[1]:
    st.subheader("Proporción de modo (Mayor vs Menor)")
    fig, ax = plt.subplots(figsize=(5,5))
    df['mode'].value_counts().plot.pie(
        autopct='%1.1f%%',
        labels=['Menor (0)', 'Mayor (1)'],
        colors=['lightcoral', 'lightgreen'],
        ax=ax
    )
    ax.set_ylabel("")
    st.pyplot(fig)

st.markdown("---")

# --- Danceability ---
st.subheader("Distribución de Danceability")
fig, ax = plt.subplots(figsize=(8,4))
sns.histplot(df['danceability'], bins=20, kde=True, color="green", ax=ax)
ax.set_xlabel("Danceability")
ax.set_ylabel("Frecuencia")
st.pyplot(fig)

st.markdown("---")

# --- Correlaciones ---
st.subheader("Mapa de calor de correlaciones")
fig, ax = plt.subplots(figsize=(6,4))
corr = df[['danceability','energy','valence','tempo','duration_ms']].corr()
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
st.pyplot(fig)

st.markdown("✅ Dashboard generado con Streamlit 🚀")
