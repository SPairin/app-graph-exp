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
    if c2 != c:
        fig.add_trace(go.Scatter(
            x=[x_min, x_max],
            y=[c2, c2],
            mode='lines',
            name=f'เส้นกำกับ Graph 2 (y = {c2})',
            line=dict(color='orange', dash='dash', width=1.5)
        ))

# ---------------------------------------------------------
# Annotations ชี้ตำแหน่งสำคัญบนกราฟ
# ---------------------------------------------------------
# คำนวณทิศทางการเติบโต dy/dx = α · β · ln(a) · a^(β(x-h))
growth_rate = alpha * beta * np.log(a) if a > 0 else 0

if show_annotations:
    # Annotation จุดตัดแกน Y
    if x_min <= 0 <= x_max:
        fig.add_annotation(
            x=0,
            y=y_intercept,
            text=f"📍 จุดตัดแกน Y: (0, {y_intercept:.2f})",
            showarrow=True,
            arrowhead=2,
            arrowcolor="purple",
            ax=55,
            ay=-40,
            bgcolor="rgba(255, 255, 255, 0.9)",
            bordercolor="purple",
            borderwidth=1
        )
    
    # Annotation เส้นกำกับแนวนอน y = c
    fig.add_annotation(
        x=x_max,
        y=c,
        text=f" Horizontal Asymptote: y = {c}",
        showarrow=False,
        xanchor="right",
        yanchor="bottom" if alpha >= 0 else "top",
        font=dict(color="crimson", size=12),
        bgcolor="rgba(255, 230, 230, 0.85)"
    )

    # Annotation บอกประเภทกราฟ
    if np.isclose(growth_rate, 0):
        behavior_text = "🔵 Constant Line (ฟังก์ชันคงตัว)"
    elif growth_rate > 0:
        behavior_text = "📈 Exponential Growth (ฟังก์ชันเพิ่ม)"
    else:
        behavior_text = "📉 Exponential Decay (ฟังก์ชันลด)"

    mid_x = (x_min + x_max) / 2
    mid_y = eval_exponential(mid_x, alpha, a, beta, h, c)

    fig.add_annotation(
        x=mid_x,
        y=mid_y,
        text=f"<b>{behavior_text}</b>",
        showarrow=True,
        arrowhead=1,
        arrowcolor="#1f77b4",
        ax=0,
        ay=-45,
        bgcolor="rgba(240, 248, 255, 0.9)",
        bordercolor="#1f77b4",
        font=dict(size=12, color="#1f77b4")
    )

# ปรับ Layout & Graph Titles
fig.update_layout(
    title=dict(text=f"<b>{custom_title}</b>", font=dict(size=18)),
    xaxis_title=custom_xlabel,
    yaxis_title=custom_ylabel,
    hovermode="x unified",
    template="plotly_white",
    height=600,
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, bgcolor="rgba(255, 255, 255, 0.75)"),
    dragmode="pan"
)

# ---------------------------------------------------------
# 4. การแสดงผลบนหน้าจอ (Main Layout)
# ---------------------------------------------------------
col_graph, col_info = st.columns([3, 2])

with col_graph:
    st.plotly_chart(fig, use_container_width=True)
    st.info("""
    💡 **วิธี Zoom & Control มุมมอง:**
    - **Zoom In / Zoom Out:** หมุน Scroll Wheel ของเมาส์ หรือใช้เครื่องมือ Zoom บนมุมขวาของกราฟ
    - **Pan (ลากขยับมุมมอง):** คลิกเมาส์ค้างแล้วลากไปมาได้อย่างอิสระ
    - **Reset View:** ดับเบิ้ลคลิกบนพื้นที่กราฟเพื่อกลับสุ่มุมมองเริ่มต้น
    """)

with col_info:
    st.subheader("🔍 วิเคราะห์พฤติกรรมทางคณิตศาสตร์")
    
    # วิเคราะห์ฟังก์ชันเพิ่ม / ฟังก์ชันลด
    if np.isclose(growth_rate, 0):
        st.info("🔵 **ชนิดฟังก์ชัน:** ฟังก์ชันคงตัว (Constant Function)")
    elif growth_rate > 0:
        st.success("🟢 **ชนิดฟังก์ชัน:** ฟังก์ชันเพิ่ม (Strictly Increasing)")
    else:
        st.warning("🟠 **ชนิดฟังก์ชัน:** ฟังก์ชันลด (Strictly Decreasing)")

    st.markdown("---")
    st.markdown("### 📌 สรุปคุณสมบัติของ $y = \\alpha a^{\\beta(x-h)} + c$")
    
    # Range Calculation
    if alpha > 0:
        range_str = f"({c}, +\\infty)"
    elif alpha < 0:
        range_str = f"(-\\infty, {c})"
    else:
        range_str = f"\\{{{c}\\}}"
        
    st.write(f"- **โดเมน (Domain):** $(-\\infty, +\\infty)$")
    st.write(f"- **เรนจ์ (Range):** ${range_str}$")
    st.write(f"- **เส้นกำกับแนวนอน (Horizontal Asymptote):** $y = {c}$")
    st.write(f"- **จุดตัดแกน Y (Y-intercept):** $(0, {y_intercept:.4f})$")

    st.markdown("---")
    st.markdown("### ♾️ พฤติกรรมลิมิตเมื่อ $x \\to \\pm\\infty$")
    
    exp_dir = beta * np.log(a) if a > 0 else 0
    if exp_dir > 0:
        lim_pos_x = "+∞" if alpha > 0 else ("-∞" if alpha < 0 else f"{c}")
        lim_neg_x = f"{c}"
    elif exp_dir < 0:
        lim_pos_x = f"{c}"
        lim_neg_x = "+∞" if alpha > 0 else ("-∞" if alpha < 0 else f"{c}")
    else:
        lim_pos_x = f"{alpha + c}"
        lim_neg_x = f"{alpha + c}"

    st.latex(r"\lim_{x \to +\infty} y = " + lim_pos_x)
    st.latex(r"\lim_{x \to -\infty} y = " + lim_neg_x)

# ---------------------------------------------------------
# 5. แท็บรายละเอียดเพิ่มเติม
# ---------------------------------------------------------
st.divider()
tab1, tab2, tab3 = st.tabs(["🧮 คำนวณค่าพิกัด (X ➔ Y)", "📋 ตารางค่า (X, Y)", "📚 อธิบายหน้าที่ของแต่ละพารามิเตอร์"])

with tab1:
    st.subheader("คำนวณค่า Y จากค่า X ที่กำหนด")
    col_in, col_out = st.columns(2)
    with col_in:
        test_x = st.number_input("ป้อนค่า X:", value=1.0, step=0.5)
    with col_out:
        test_y = eval_exponential(test_x, alpha, a, beta, h, c)
        st.metric(label=f"ค่า Y ของ Graph 1 ที่ X = {test_x}", value=f"{test_y:.6f}")
        if compare_mode:
            test_y2 = eval_exponential(test_x, alpha2, a2, beta2, h2, c2)
            st.metric(label=f"ค่า Y ของ Graph 2 ที่ X = {test_x}", value=f"{test_y2:.6f}")

with tab2:
    st.subheader("ตารางพิกัด (X, Y)")
    sample_x = np.linspace(x_min, x_max, 21)
    sample_y = eval_exponential(sample_x, alpha, a, beta, h, c)
    df_data = {"X": sample_x, "Y (Graph 1)": sample_y}
    if compare_mode:
        df_data["Y (Graph 2)"] = eval_exponential(sample_x, alpha2, a2, beta2, h2, c2)
    df = pd.DataFrame(df_data)
    st.dataframe(df.style.format("{:.4f}"), use_container_width=True)

with tab3:
    st.markdown(r"""
    ### 📚 รายละเอียดพารามิเตอร์ในสมการ $y = \alpha a^{\beta(x - h)} + c$

    1. **สัมประสิทธิ์ $\alpha$ (Vertical Stretch / Reflection):**
       - **$\alpha > 0$:** กราฟวางตัวอยู่ **เหนือ** เส้นกำกับ $y = c$ (เรนจ์คือ $(c, +\infty)$)
       - **$\alpha < 0$:** กราฟจะถูกสะท้อนแนวตั้งลงมาอยู่ **ใต้** เส้นกำกับ $y = c$ (เรนจ์คือ $(-\infty, c)$)
       - ค่า $|\alpha|$ ยิ่งมาก กราฟจะยืดชันขึ้นในแนวตั้ง

    2. **ฐาน $a$ (Base Value):**
       - ต้องเป็นจำนวนจริงบวก และ $a \neq 1$
       - หาก $a > 1$: ฐานมีลักษณะเติบโต (Growth Base)
       - หาก $0 < a < 1$: ฐานมีลักษณะถดถอย (Decay Base)

    3. **ตัวคูณกำลัง $\beta$ (Horizontal Scaling / Direction):**
       - ควบคุมอัตราความชันแนวนอน
       - **$\beta > 0$:** รักษาทิศทางเดิมของแกน X
       - **$\beta < 0$:** เกิดการสะท้อนแนวนอน (Horizontal Reflection) เปลี่ยนพฤติกรรมจาก Growth เป็น Decay หรือ Decay เป็น Growth

    4. **การเลื่อนแนวนอน $h$ (Horizontal Shift):**
       - เลื่อนกราฟไปทางขวาเมื่อ $h > 0$ และเลื่อนไปทางซ้ายเมื่อ $h < 0$

    5. **การเลื่อนแนวตั้งและเส้นกำกับ $c$ (Vertical Shift & Horizontal Asymptote):**
       - เส้นตรง **$y = c$** คือเส้นกำกับแนวนอนที่กราฟจะเฉียดเข้าใกล้เรื่อยๆ เมื่อ $x \to \infty$ หรือ $x \to -\infty$
    """)
