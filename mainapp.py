import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd

# ---------------------------------------------------------
# 1. การตั้งค่าหน้าเว็บ (Page Configuration)
# ---------------------------------------------------------
st.set_page_config(
    page_title="การศึกษาพฤติกรรมของกราฟเอ็กซ์โพเนนเชียล",
    page_icon="📈",
    layout="wide"
)

st.title("📈 การศึกษาพฤติกรรมของกราฟเอ็กซ์โพเนนเชียล (Exponential Graph Explorer)")
st.markdown("""
เว็บแอปพลิเคชันนี้ออกแบบมาเพื่อศึกษาพฤติกรรมและการเปลี่ยนแปลงของฟังก์ชันเอ็กซ์โพเนนเชียล 
""")

# ---------------------------------------------------------
# 2. แถบควบคุมพารามิเตอร์ และ Labels (Sidebar)
# ---------------------------------------------------------
st.sidebar.header("⚙️ ตั้งค่าพารามิเตอร์ของฟังก์ชัน")

# เลือกรูปแบบสมการ
mode = st.sidebar.radio(
    "เลือกรูปแบบสมการ:",
    ["รูปแบบฐานทั่วไป: f(x) = a · b^(x - h) + c", "รูปแบบฐาน e (Natural): f(x) = a · e^(k(x - h)) + c"]
)

st.sidebar.subheader("📌 กำหนดค่าสำหรับ Graph 1")

if "ทั่วไป" in mode:
    a = st.sidebar.number_input("ค่าสัมประสิทธิ์ a (การสะท้อน/ปรับความยืด)", value=1.0, step=0.5)
    b = st.sidebar.number_input("ฐาน b (b > 0, b ≠ 1)", value=2.0, min_value=0.001, step=0.1)
    if b == 1.0:
        st.sidebar.warning("⚠️ กรณี b = 1 กราฟจะเป็นเส้นตรง y = a + c (ไม่ใช่ฟังก์ชันเอ็กซ์โพเนนเชียล)")
    h = st.sidebar.number_input("การเลื่อนขนานแนวนอน h", value=0.0, step=0.5)
    c = st.sidebar.number_input("การเลื่อนขนานแนวตั้ง c (เส้นกำกับ)", value=0.0, step=0.5)
    k = 1.0
else:
    a = st.sidebar.number_input("ค่าสัมประสิทธิ์ a", value=1.0, step=0.5)
    k = st.sidebar.number_input("อัตราการเติบโต k (Growth/Decay Rate)", value=1.0, step=0.1)
    h = st.sidebar.number_input("การเลื่อนขนานแนวนอน h", value=0.0, step=0.5)
    c = st.sidebar.number_input("การเลื่อนขนานแนวตั้ง c (เส้นกำกับ)", value=0.0, step=0.5)
    b = np.e

# โหมดเปรียบเทียบกราฟ
compare_mode = st.sidebar.checkbox("🔄 เปิดโหมดเปรียบเทียบกับ Graph 2")
if compare_mode:
    st.sidebar.subheader("📌 กำหนดค่าสำหรับ Graph 2")
    if "ทั่วไป" in mode:
        a2 = st.sidebar.number_input("a2", value=1.0, step=0.5, key="a2")
        b2 = st.sidebar.number_input("b2", value=0.5, min_value=0.001, step=0.1, key="b2")
        h2 = st.sidebar.number_input("h2", value=0.0, step=0.5, key="h2")
        c2 = st.sidebar.number_input("c2", value=0.0, step=0.5, key="c2")
        k2 = 1.0
    else:
        a2 = st.sidebar.number_input("a2", value=1.0, step=0.5, key="a2")
        k2 = st.sidebar.number_input("k2", value=-1.0, step=0.1, key="k2")
        h2 = st.sidebar.number_input("h2", value=0.0, step=0.5, key="h2")
        c2 = st.sidebar.number_input("c2", value=0.0, step=0.5, key="c2")
        b2 = np.e

st.sidebar.subheader("🔍 ขอบเขตแกน X")
x_min = st.sidebar.number_input("X Min", value=-5.0, step=1.0)
x_max = st.sidebar.number_input("X Max", value=5.0, step=1.0)
if x_min >= x_max:
    st.sidebar.error("❌ ค่า X Min ต้องน้อยกว่า X Max")

# ---------------------------------------------------------
# ส่วนจัดการ Custom Labels & Display Options
# ---------------------------------------------------------
st.sidebar.subheader("🏷️ ปรับแต่ง Labels & ข้อความบนกราฟ")
custom_title = st.sidebar.text_input("ชื่อหัวเรื่องกราฟ (Graph Title Label):", value="กราฟแสดงฟังก์ชันเอ็กซ์โพเนนเชียล")
custom_xlabel = st.sidebar.text_input("Label แกน X (X-Axis Label):", value="ตัวแปรต้น (x)")
custom_ylabel = st.sidebar.text_input("Label แกน Y (Y-Axis Label):", value="ค่าฟังก์ชัน f(x)")

show_annotations = st.sidebar.checkbox("📌 แสดงข้อความชี้บอกจุดสำคัญบนกราฟ (Annotations)", value=True)
show_data_labels = st.sidebar.checkbox("🔢 แสดง Data Labels (ตัวเลขพิกัดจุดบนกราฟ)", value=False)

# ---------------------------------------------------------
# 3. ฟังก์ชันคำนวณ และสร้างกราฟ Plotly
# ---------------------------------------------------------
def eval_exponential(x, a_val, b_val, h_val, c_val, k_val=1.0):
    if "ทั่วไป" in mode:
        return a_val * (b_val ** (x - h_val)) + c_val
    else:
        return a_val * np.exp(k_val * (x - h_val)) + c_val

x_vals = np.linspace(x_min, x_max, 800)
y_vals = eval_exponential(x_vals, a, b, h, c, k)

fig = go.Figure()

# 1. เส้นกำกับแนวนอน (Horizontal Asymptote y = c)
fig.add_trace(go.Scatter(
    x=[x_min, x_max],
    y=[c, c],
    mode='lines',
    name=f'เส้นกำกับ Asymptote (y = {c})',
    line=dict(color='crimson', dash='dash', width=2)
))

# 2. เส้นกราฟหลัก (Graph 1)
if "ทั่วไป" in mode:
    eq_label = f"f(x) = {a} · ({round(b, 2)})^{{(x - {h})}} + {c}"
else:
    eq_label = f"f(x) = {a} · e^{{{k}(x - {h})}} + {c}"

fig.add_trace(go.Scatter(
    x=x_vals,
    y=y_vals,
    mode='lines',
    name=f'Graph 1: {eq_label}',
    line=dict(color='#1f77b4', width=3),
    hovertemplate='<b>X Label</b>: %{x:.3f}<br><b>Y Label</b>: %{y:.3f}<extra></extra>'
))

# 3. Data Labels (แสดงพิกัดบนเส้นกราฟ หากเปิดใช้งาน)
if show_data_labels:
    sample_x = np.linspace(x_min, x_max, 9)
    sample_y = eval_exponential(sample_x, a, b, h, c, k)
    text_labels = [f"({x:.1f}, {y:.1f})" for x, y in zip(sample_x, sample_y)]
    
    fig.add_trace(go.Scatter(
        x=sample_x,
        y=sample_y,
        mode='markers+text',
        name='Data Labels (พิกัด)',
        marker=dict(color='#1f77b4', size=8),
        text=text_labels,
        textposition="top center",
        textfont=dict(size=10, color="darkblue")
    ))

# 4. จุดตัดแกน Y (Y-intercept)
y_intercept = eval_exponential(0, a, b, h, c, k)
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
    y_vals2 = eval_exponential(x_vals, a2, b2, h2, c2, k2)
    fig.add_trace(go.Scatter(
        x=x_vals,
        y=y_vals2,
        mode='lines',
        name='Graph 2 (เปรียบเทียบ)',
        line=dict(color='#ff7f0e', width=3, dash='dot'),
        hovertemplate='<b>X Label</b>: %{x:.3f}<br><b>Y Label</b>: %{y:.3f}<extra></extra>'
    ))
    if c2 != c:
        fig.add_trace(go.Scatter(
            x=[x_min, x_max],
            y=[c2, c2],
            mode='lines',
            name=f'เส้นกำกับ Graph 2 (y = {c2})',
            line=dict(color='orange', dash='dash', width=1.5)
        ))

# ---------------------------------------------------------
# เพิ่ม Annotations ชี้บอกตำแหน่งบนกราฟ (ถ้าเปิดสวิตช์)
# ---------------------------------------------------------
if show_annotations:
    # Annotation จุดตัดแกน Y
    if x_min <= 0 <= x_max:
        fig.add_annotation(
            x=0,
            y=y_intercept,
            text=f"📍 จุดตัดแกน Y: (0, {y_intercept:.2f})",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="purple",
            ax=50,
            ay=-40,
            bgcolor="rgba(255, 255, 255, 0.85)",
            bordercolor="purple",
            borderwidth=1,
            font=dict(size=12)
        )
    
    # Annotation Label บนเส้นกำกับแนวนอน
    fig.add_annotation(
        x=x_max,
        y=c,
        text=f" Horizontal Asymptote: y = {c}",
        showarrow=False,
        xanchor="right",
        yanchor="bottom" if a > 0 else "top",
        font=dict(color="crimson", size=12, family="Arial Bold"),
        bgcolor="rgba(255, 230, 230, 0.8)"
    )

    # Annotation Label บอกประเภทพฤติกรรมกราฟ
    is_increasing = (b > 1 and a > 0) or (0 < b < 1 and a < 0) if "ทั่วไป" in mode else (k > 0 and a > 0) or (k < 0 and a < 0)
    behavior_text = "📈 Exponential Growth (ฟังก์ชันเพิ่ม)" if is_increasing else "📉 Exponential Decay (ฟังก์ชันลด)"
    
    mid_x = (x_min + x_max) / 2
    mid_y = eval_exponential(mid_x, a, b, h, c, k)
    
    fig.add_annotation(
        x=mid_x,
        y=mid_y,
        text=f"<b>{behavior_text}</b>",
        showarrow=True,
        arrowhead=1,
        arrowcolor="#1f77b4",
        ax=0,
        ay=-50,
        bgcolor="rgba(240, 248, 255, 0.9)",
        bordercolor="#1f77b4",
        borderwidth=1.5,
        font=dict(size=12, color="#1f77b4")
    )

# ปรับ แต่ง Layout & Axis Labels
fig.update_layout(
    title=dict(
        text=f"<b>{custom_title}</b>",
        font=dict(size=18)
    ),
    xaxis_title=custom_xlabel,
    yaxis_title=custom_ylabel,
    hovermode="x unified",
    template="plotly_white",
    height=600,
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, bgcolor="rgba(255, 255, 255, 0.7)"),
    dragmode="pan"
)

# ---------------------------------------------------------
# 4. การแสดงผลบนหน้าจอ (Main Layout)
# ---------------------------------------------------------
col_graph, col_info = st.columns([3, 2])

with col_graph:
    st.plotly_chart(fig, use_container_width=True)
    st.info("""
    💡 **คำแนะนำการโต้ตอบกับกราฟ:**
    - **Zoom In / Zoom Out:** หมุน Scroll Wheel ของเมาส์
    - **Pan (ลากขยับมุมมอง):** คลิกเมาส์ค้างบนพื้นที่กราฟแล้วลาก
    - **Toggle Labels:** เปิด/ปิด Data Labels หรือ Annotations ได้ที่แถบด้านข้าง (Sidebar)
    """)

with col_info:
    st.subheader("🔍 วิเคราะห์พฤติกรรมของกราฟ")
    
    is_increasing = (b > 1 and a > 0) or (0 < b < 1 and a < 0) if "ทั่วไป" in mode else (k > 0 and a > 0) or (k < 0 and a < 0)

    if is_increasing:
        st.success("🟢 **ชนิดกราฟ:** ฟังก์ชันเพิ่ม (Strictly Increasing)")
    else:
        st.warning("🟠 **ชนิดกราฟ:** ฟังก์ชันลด (Strictly Decreasing)")

    st.markdown("---")
    st.markdown("### 📌 สรุปคุณสมบัติทางคณิตศาสตร์")
    
    range_str = f"({c}, +\\infty)" if a > 0 else f"(-\\infty, {c})"
    
    st.write(f"- **โดเมน (Domain):** $(-\\infty, +\\infty)$")
    st.write(f"- **เรนจ์ (Range):** ${range_str}$")
    st.write(f"- **เส้นกำกับแนวนอน (Horizontal Asymptote):** $y = {c}$")
    st.write(f"- **จุดตัดแกน Y (Y-intercept):** $(0, {y_intercept:.4f})$")

    st.markdown("---")
    st.markdown("### ♾️ พฤติกรรมเมื่อ $x \\to \\pm\\infty$")
    
    if "ทั่วไป" in mode:
        lim_pos = ("+∞" if a > 0 else "-∞") if b > 1 else f"{c}"
        lim_neg = f"{c}" if b > 1 else ("+∞" if a > 0 else "-∞")
    else:
        lim_pos = ("+∞" if a > 0 else "-∞") if k > 0 else f"{c}"
        lim_neg = f"{c}" if k > 0 else ("+∞" if a > 0 else "-∞")

    st.latex(r"\lim_{x \to +\infty} f(x) = " + lim_pos)
    st.latex(r"\lim_{x \to -\infty} f(x) = " + lim_neg)

# ---------------------------------------------------------
# 5. แท็บความรู้และเครื่องมือเพิ่มเติม
# ---------------------------------------------------------
st.divider()
tab1, tab2, tab3 = st.tabs(["🧮 เครื่องมือคำนวณพิกัด", "📋 ตารางค่า (X, Y)", "📚 ทฤษฎีและพฤติกรรมกราฟ"])

with tab1:
    st.subheader("ทดลองป้อนค่า X เพื่อคำนวณหาค่า Y")
    col_in, col_out = st.columns(2)
    with col_in:
        test_x = st.number_input("ป้อนค่า X:", value=1.0, step=0.5)
    with col_out:
        test_y = eval_exponential(test_x, a, b, h, c, k)
        st.metric(label=f"ค่า Y ของ Graph 1 ที่ X = {test_x}", value=f"{test_y:.6f}")

with tab2:
    st.subheader("ตารางแสดงพิกัดค่า (X, Y)")
    sample_x = np.linspace(x_min, x_max, 21)
    sample_y = eval_exponential(sample_x, a, b, h, c, k)
    df = pd.DataFrame({"X": sample_x, "Y (Graph 1)": sample_y})
    st.dataframe(df.style.format("{:.4f}"), use_container_width=True)

with tab3:
    st.markdown("""
    ### 📚 รายละเอียดพฤติกรรมของกราฟเอ็กซ์โพเนนเชียล $f(x) = a \\cdot b^{x - h} + c$

    1. **พฤติกรรมของฐาน $b$ (Base Value):**
       - **เมื่อ $b > 1$:** กราฟมีลักษณะแบบ **Exponential Growth** 
       - **เมื่อ $0 < b < 1$:** กราฟมีลักษณะแบบ **Exponential Decay**

    2. **เส้นกำกับแนวนอน $y = c$ (Horizontal Asymptote):**
       - เส้นตรง $y = c$ คือขอบเขตที่กราฟจะเฉียดเข้าใกล้เรื่อยๆ แต่ไม่ตัดเส้นนี้

    3. **ผลของค่าสัมประสิทธิ์ $a$ (Vertical Scaling & Reflection):**
       - **ถ้า $a > 0$:** กราฟอยู่เหนือเส้นกำกับ $y = c$
       - **ถ้า $a < 0$:** กราฟจะถูกสะท้อนลงมาอยู่ด้านล่างเส้นกำกับ
    """)
