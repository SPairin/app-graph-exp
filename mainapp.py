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
# 2. แถบควบคุมพารามิเตอร์ (Sidebar)
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

st.sidebar.subheader("🔍 ขอบเขตแกน X บนกราฟ")
x_min = st.sidebar.number_input("X Min", value=-10.0, step=1.0)
x_max = st.sidebar.number_input("X Max", value=10.0, step=1.0)
if x_min >= x_max:
    st.sidebar.error("❌ ค่า X Min ต้องน้อยกว่า X Max")

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

# เส้นกำกับแนวนอน (Horizontal Asymptote y = c)
fig.add_trace(go.Scatter(
    x=[x_min, x_max],
    y=[c, c],
    mode='lines',
    name=f'เส้นกำกับ Horizontal Asymptote (y = {c})',
    line=dict(color='crimson', dash='dash', width=2)
))

# เส้นกราฟหลัก (Graph 1)
eq_label = f"f(x) = {a} · {round(b, 2) if 'ทั่วไป' in mode else 'e'}^{'(' + str(k) + ')' if 'ฐาน e' in mode else ''}(x - {h}) + {c}"
fig.add_trace(go.Scatter(
    x=x_vals,
    y=y_vals,
    mode='lines',
    name=f'Graph 1: {eq_label}',
    line=dict(color='#1f77b4', width=3),
    hovertemplate='<b>X</b>: %{x:.3f}<br><b>Y</b>: %{y:.3f}<extra></extra>'
))

# จุดตัดแกน Y (x = 0)
y_intercept = eval_exponential(0, a, b, h, c, k)
if x_min <= 0 <= x_max:
    fig.add_trace(go.Scatter(
        x=[0],
        y=[y_intercept],
        mode='markers+text',
        name='จุดตัดแกน Y',
        marker=dict(color='purple', size=10, symbol='circle'),
        text=[f"  (0, {y_intercept:.2f})"],
        textposition="top right"
    ))

# วาด Graph 2 หากเปิดโหมดเปรียบเทียบ
if compare_mode:
    y_vals2 = eval_exponential(x_vals, a2, b2, h2, c2, k2)
    fig.add_trace(go.Scatter(
        x=x_vals,
        y=y_vals2,
        mode='lines',
        name='Graph 2 (เปรียบเทียบ)',
        line=dict(color='#ff7f0e', width=3, dash='dot'),
        hovertemplate='<b>X</b>: %{x:.3f}<br><b>Y</b>: %{y:.3f}<extra></extra>'
    ))
    if c2 != c:
        fig.add_trace(go.Scatter(
            x=[x_min, x_max],
            y=[c2, c2],
            mode='lines',
            name=f'เส้นกำกับ Graph 2 (y = {c2})',
            line=dict(color='orange', dash='dash', width=1.5)
        ))

# ปรับ Layout และเปิดใช้งาน Zoom/Pan
fig.update_layout(
    title="📊 กราฟแสดงฟังก์ชันเอ็กซ์โพเนนเชียล (ลาก Pan / Scroll Zoom ได้อิสระ)",
    xaxis_title="แกน X",
    yaxis_title="แกน Y",
    hovermode="x unified",
    template="plotly_white",
    height=580,
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
    dragmode="pan"  # ตั้งค่าเริ่มต้นให้ใช้เมาส์ลากเลื่อนกราฟได้ทันที
)

# ---------------------------------------------------------
# 4. การแสดงผลบนหน้าจอ (Main Layout)
# ---------------------------------------------------------
col_graph, col_info = st.columns([3, 2])

with col_graph:
    st.plotly_chart(fig, use_container_width=True)
    st.info("""
    💡 **วิธี Zoom และควบคุมมุมมองกราฟ:**
    - **Zoom In / Zoom Out:** หมุน Scroll Wheel ของเมาส์ หรือใช้เครื่องมือรูปแว่นขยายที่มุมขวาบนของกราฟ
    - **Pan (ลากขยับกราฟ):** คลิกเมาส์ค้างบนกราฟแล้วลากไปมา
    - **Reset View:** ดับเบิ้ลคลิกบนพื้นที่กราฟเพื่อรีเซ็ตมุมมองกลับมาค่าเริ่มต้น
    """)

with col_info:
    st.subheader("🔍 วิเคราะห์พฤติกรรมของกราฟ")
    
    # คำนวณลักษณะของกราฟ (ฟังก์ชันเพิ่ม / ฟังก์ชันลด)
    if "ทั่วไป" in mode:
        is_increasing = (b > 1 and a > 0) or (0 < b < 1 and a < 0)
        is_growth_shape = (b > 1)
    else:
        is_increasing = (k > 0 and a > 0) or (k < 0 and a < 0)
        is_growth_shape = (k > 0)

    # แสดงป้ายเตือนลักษณะกราฟ
    if is_increasing:
        st.success("🟢 **ชนิดกราฟ:** ฟังก์ชันเพิ่ม (Strictly Increasing)")
    else:
        st.warning("🟠 **ชนิดกราฟ:** ฟังก์ชันลด (Strictly Decreasing)")

    st.markdown("---")
    st.markdown("### 📌 สรุปคุณสมบัติทางคณิตศาสตร์")
    
    # Domain & Range
    range_str = f"({c}, +\\infty)" if a > 0 else f"(-\\infty, {c})"
    
    st.write(f"- **โดเมน (Domain):** $(-\\infty, +\\infty)$ หรือ จำนวนจริงทั้งหมด")
    st.write(f"- **เรนจ์ (Range):** ${range_str}$")
    st.write(f"- **เส้นกำกับแนวนอน (Horizontal Asymptote):** เส้นตรง $y = {c}$")
    st.write(f"- **จุดตัดแกน Y (Y-intercept):** $(0, {y_intercept:.4f})$")

    st.markdown("---")
    st.markdown("### ♾️ พฤติกรรมเมื่อ $x \\to \\pm\\infty$ (Limit Behaviors)")
    
    if "ทั่วไป" in mode:
        if b > 1:
            lim_pos = "+∞" if a > 0 else "-∞"
            lim_neg = f"{c}"
        else:
            lim_pos = f"{c}"
            lim_neg = "+∞" if a > 0 else "-∞"
    else:
        if k > 0:
            lim_pos = "+∞" if a > 0 else "-∞"
            lim_neg = f"{c}"
        else:
            lim_pos = f"{c}"
            lim_neg = "+∞" if a > 0 else "-∞"

    st.latex(r"\lim_{x \to +\infty} f(x) = " + lim_pos)
    st.latex(r"\lim_{x \to -\infty} f(x) = " + lim_neg)

# ---------------------------------------------------------
# 5. แท็บความรู้และเครื่องมือเพิ่มเติม
# ---------------------------------------------------------
st.divider()
tab1, tab2, tab3 = st.tabs(["🧮 เครื่องมือคำนวณจุดพิกัด", "📋 ตารางค่า (X, Y)", "📚 คำอธิบายทฤษฎีพฤติกรรมกราฟ"])

with tab1:
    st.subheader("ทดลองป้อนค่า X เพื่อคำนวณหาค่า Y")
    col_in, col_out = st.columns(2)
    with col_in:
        test_x = st.number_input("ป้อนค่า X:", value=1.0, step=0.5)
    with col_out:
        test_y = eval_exponential(test_x, a, b, h, c, k)
        st.metric(label=f"ค่า Y ของ Graph 1 ที่ X = {test_x}", value=f"{test_y:.6f}")
        if compare_mode:
            test_y2 = eval_exponential(test_x, a2, b2, h2, c2, k2)
            st.metric(label=f"ค่า Y ของ Graph 2 ที่ X = {test_x}", value=f"{test_y2:.6f}")

with tab2:
    st.subheader("ตารางแสดงพิกัดค่า (X, Y)")
    sample_x = np.linspace(x_min, x_max, 21)
    sample_y = eval_exponential(sample_x, a, b, h, c, k)
    
    df_data = {"X": sample_x, "Y (Graph 1)": sample_y}
    if compare_mode:
        df_data["Y (Graph 2)"] = eval_exponential(sample_x, a2, b2, h2, c2, k2)
    
    df = pd.DataFrame(df_data)
    st.dataframe(df.style.format("{:.4f}"), use_container_width=True)

with tab3:
    st.markdown("""
    ### 📚 รายละเอียดพฤติกรรมของกราฟเอ็กซ์โพเนนเชียล $f(x) = a \\cdot b^{x - h} + c$

    1. **พฤติกรรมของฐาน $b$ (Base Value):**
       - **เมื่อ $b > 1$:** กราฟมีลักษณะแบบ **Exponential Growth** (ค่า Y พุ่งขึ้นอย่างรวดเร็วเมื่อ X เพิ่มขึ้น)
       - **เมื่อ $0 < b < 1$:** กราฟมีลักษณะแบบ **Exponential Decay** (ค่า Y ลดลงอย่างรวดเร็วและค่อยๆ ลู่เข้าหาเส้นกำกับ)
       - *หมายเหตุ:* ฐาน $b$ ต้องเป็นจำนวนจริงบวก และไม่เท่ากับ 1

    2. **เส้นกำกับแนวนอน $y = c$ (Horizontal Asymptote):**
       - เส้นตรง $y = c$ คือขอบเขตที่กราฟจะเฉียดเข้าใกล้เรื่อยๆ แต่ไม่มีวันแตะหรือตัดเส้นนี้
       - การเปลี่ยนค่า $c$ คือการ **ย้ายกราฟขึ้น-ลง** ในแนวตั้ง

    3. **ผลของค่าสัมประสิทธิ์ $a$ (Vertical Scaling & Reflection):**
       - **ถ้า $a > 0$:** กราฟจะวางตัวอยู่ **เหนือ** เส้นกำกับ $y = c$
       - **ถ้า $a < 0$:** กราฟจะถูก **สะท้อนข้ามเส้นกำกับ (Reflected)** มาอยู่ด้านล่าง
       - ยิ่ง $|a|$ มีค่ามาก กราฟจะยิ่งยืดตัวชันขึ้นในแนวตั้งเร็วขึ้น

    4. **การเลื่อนขนานแนวนอน $h$ (Horizontal Shift):**
       - ค่า $h$ ทำให้กราฟเลื่อนไปทางขวา ($h > 0$) หรือทางซ้าย ($h < 0$) โดยรูปทรงคงเดิม
    """)
