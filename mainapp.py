import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd

# ---------------------------------------------------------
# 1. การตั้งค่าหน้าเว็บ (Page Configuration)
# ---------------------------------------------------------
st.set_page_config(
    page_title="การศึกษาพฤติกรรมกราฟ y = α · a^(β(x-h)) + c",
    page_icon="📈",
    layout="wide"
)

st.title("📈 การศึกษาพฤติกรรมของกราฟเอ็กซ์โพเนนเชียล")
st.latex(r"y = \alpha \cdot a^{\beta(x - h)} + c")

st.markdown("""
เว็บแอปพลิเคชันนี้ออกแบบมาเพื่อศึกษาพฤติกรรมและการเปลี่ยนแปลงของกราฟเอ็กซ์โพเนนเชียลตามสมการ 
**$y = \\alpha a^{\\beta(x - h)} + c$** ท่านสามารถปรับเปลี่ยนค่าพารามิเตอร์ $\\alpha, a, \\beta, h, c$ บนแถบด้านข้าง
เพื่อดูการเปลี่ยนแปลงของกราฟ เส้นกำกับ จุดตัดแกน และพฤติกรรมลิมิตได้แบบเรียลไทม์
""")

# ---------------------------------------------------------
# 2. แถบควบคุมพารามิเตอร์ (Sidebar)
# ---------------------------------------------------------
st.sidebar.header("⚙️ กำหนดพารามิเตอร์สมการ")
st.sidebar.latex(r"y = \alpha \cdot a^{\beta(x - h)} + c")

st.sidebar.subheader("📌 พารามิเตอร์ Graph 1")

# ตัวเลือกการกำหนดฐาน a
base_option = st.sidebar.radio("เลือกประเภทฐาน a:", ["กำหนดค่า a เอง", "ฐานธรรมชาติ e (a ≈ 2.71828)"])
if base_option == "ฐานธรรมชาติ e (a ≈ 2.71828)":
    a = np.e
else:
    a = st.sidebar.number_input("ฐาน a (a > 0, a ≠ 1):", value=2.0, min_value=0.0001, step=0.1)

if a == 1.0:
    st.sidebar.warning("⚠️ ถ้า a = 1 สมการจะกลายเป็นเส้นตรง y = α + c (ไม่ใช่ฟังก์ชันเอ็กซ์โพเนนเชียล)")

alpha = st.sidebar.number_input("สัมประสิทธิ์ α (Alpha - ยืด/สะท้อนแนวตั้ง):", value=1.0, step=0.5)
beta = st.sidebar.number_input("ตัวคูณกำลัง β (Beta - ยืด/สะท้อนแนวนอน):", value=1.0, step=0.1)
h = st.sidebar.number_input("การเลื่อนแนวนอน h (Horizontal Shift):", value=0.0, step=0.5)
c = st.sidebar.number_input("การเลื่อนแนวตั้ง c (Vertical Shift / เส้นกำกับ):", value=0.0, step=0.5)

# โหมดเปรียบเทียบกราฟ 2
compare_mode = st.sidebar.checkbox("🔄 เปิดโหมดเปรียบเทียบกับ Graph 2")
if compare_mode:
    st.sidebar.subheader("📌 พารามิเตอร์ Graph 2")
    base_option2 = st.sidebar.radio("เลือกประเภทฐาน a2:", ["กำหนดค่า a2 เอง", "ฐานธรรมชาติ e (a2 ≈ 2.71828)"], key="base2")
    if base_option2 == "ฐานธรรมชาติ e (a2 ≈ 2.71828)":
        a2 = np.e
    else:
        a2 = st.sidebar.number_input("ฐาน a2:", value=0.5, min_value=0.0001, step=0.1, key="a2_val")
        
    alpha2 = st.sidebar.number_input("สัมประสิทธิ์ α2:", value=1.0, step=0.5, key="alpha2")
    beta2 = st.sidebar.number_input("ตัวคูณกำลัง β2:", value=1.0, step=0.1, key="beta2")
    h2 = st.sidebar.number_input("การเลื่อนแนวนอน h2:", value=0.0, step=0.5, key="h2")
    c2 = st.sidebar.number_input("การเลื่อนแนวตั้ง c2:", value=0.0, step=0.5, key="c2")

st.sidebar.subheader("🔍 ขอบเขตแกน X")
x_min = st.sidebar.number_input("X Min", value=-5.0, step=1.0)
x_max = st.sidebar.number_input("X Max", value=5.0, step=1.0)
if x_min >= x_max:
    st.sidebar.error("❌ ค่า X Min ต้องน้อยกว่า X Max")

# ส่วนปรับแต่ง Labels
st.sidebar.subheader("🏷️ ปรับแต่ง Labels บนกราฟ")
custom_title = st.sidebar.text_input("ชื่อหัวเรื่องกราฟ (Graph Title Label):", value="กราฟแสดงฟังก์ชัน y = α · a^(β(x - h)) + c")
custom_xlabel = st.sidebar.text_input("Label แกน X (X-Axis Label):", value="แกน x")
custom_ylabel = st.sidebar.text_input("Label แกน Y (Y-Axis Label):", value="แกน y")

show_annotations = st.sidebar.checkbox("📌 แสดง Annotations ชี้บอกจุดสำคัญ", value=True)
show_data_labels = st.sidebar.checkbox("🔢 แสดง Data Labels พิกัดจุดบนกราฟ", value=False)

# ---------------------------------------------------------
# 3. ฟังก์ชันคำนวณ และการสร้างกราฟ Plotly
# ---------------------------------------------------------
def eval_exponential(x, alpha_val, a_val, beta_val, h_val, c_val):
    return alpha_val * (a_val ** (beta_val * (x - h_val))) + c_val

x_vals = np.linspace(x_min, x_max, 800)
y_vals = eval_exponential(x_vals, alpha, a, beta, h, c)

fig = go.Figure()

# 1. เส้นกำกับแนวนอน Horizontal Asymptote (y = c)
fig.add_trace(go.Scatter(
    x=[x_min, x_max],
    y=[c, c],
    mode='lines',
    name=f'เส้นกำกับ Horizontal Asymptote (y = {c})',
    line=dict(color='crimson', dash='dash', width=2)
))

# 2. เส้นกราฟหลัก (Graph 1)
a_disp = "e" if np.isclose(a, np.e) else f"{round(a, 2)}"
eq_label = f"y = {alpha} · ({a_disp})^({beta}(x - {h})) + {c}"

fig.add_trace(go.Scatter(
    x=x_vals,
    y=y_vals,
    mode='lines',
    name=f'Graph 1: {eq_label}',
    line=dict(color='#1f77b4', width=3),
    hovertemplate='<b>x</b>: %{x:.3f}<br><b>y</b>: %{y:.3f}<extra></extra>'
))

# 3. Data Labels (พิกัดจุดบนเส้นกราฟ)
if show_data_labels:
    sample_x = np.linspace(x_min, x_max, 9)
    sample_y = eval_exponential(sample_x, alpha, a, beta, h, c)
    text_labels = [f"({x:.1f}, {y:.1f})" for x, y in zip(sample_x, sample_y)]
    
    fig.add_trace(go.Scatter(
        x=sample_x,
        y=sample_y,
        mode='markers+text',
        name='Data Labels',
        marker=dict(color='#1f77b4', size=8),
        text=text_labels,
        textposition="top center",
        textfont=dict(size=10, color="darkblue")
    ))

# 4. จุดตัดแกน Y (x = 0)
y_intercept = eval_exponential(0, alpha, a, beta, h, c)
if x_min <= 0 <= x_max:
    fig.add_trace(go.Scatter(
        x=[0],
        y=[y_intercept],
        mode='markers',
        name=f'จุดตัดแกน Y (0, {y_intercept:.2f})',
        marker=dict(color='purple', size=11, symbol='circle')
    ))

# 5. กราฟเปรียบเทียบ (Graph 2)
if compare_mode:
    y_vals2 = eval_exponential(x_vals, alpha2, a2, beta2, h2, c2)
    a2_disp = "e" if np.isclose(a2, np.e) else f"{round(a2, 2)}"
    eq_label2 = f"y = {alpha2} · ({a2_disp})^({beta2}(x - {h2})) + {c2}"
    
    fig.add_trace(go.Scatter(
        x=x_vals,
        y=y_vals2,
        mode='lines',
        name=f'Graph 2: {eq_label2}',
        line=dict(color='#ff7f0e', width=3, dash='dot'),
        hovertemplate='<b>x</b>: %{x:.3f}<br><b>y</b>: %{y:.3f}<extra></extra>'
    ))
    if c
