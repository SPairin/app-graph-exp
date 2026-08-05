import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

# Set Streamlit page configuration
st.set_page_config(page_title="Exponential Function Explorer", layout="wide")

st.title("Interactive Exponential Function Explorer")
st.write(
    "Explore the behavior of the general exponential graph "
    "$y = a \\cdot e^{k \\cdot x} + c$ by adjusting the coefficients below."
)

# Sidebar sliders for parameters
st.sidebar.header("Coefficient Controls")

a = st.sidebar.slider(
    "Coefficient a (Amplitude / Vertical Scale)",
    min_value=-10.0,
    max_value=10.0,
    value=2.0,
    step=0.1,
    help="Controls vertical stretching/compression and vertical reflection."
)

k = st.sidebar.slider(
    "Coefficient k (Growth/Decay Rate)",
    min_value=-5.0,
    max_value=5.0,
    value=1.5,
    step=0.1,
    help="Positive k gives growth; negative k gives decay."
)

c = st.sidebar.slider(
    "Vertical Shift c (Horizontal Asymptote)",
    min_value=-10.0,
    max_value=10.0,
    value=5.0,
    step=0.5,
    help="Shifts the graph vertically and sets the horizontal asymptote y = c."
)

# Compute values for plotting
x = np.linspace(-3, 3, 400)
y = a * np.exp(k * x) + c

# Calculate y-intercept
y_intercept = a + c

# Create Matplotlib Figure
fig, ax = plt.subplots(figsize=(10, 5))

# Plot the exponential curve
ax.plot(
    x, y, 
    label=f"$y = {a:.1f} \\cdot e^{{{k:.1f}x}} + {c:.1f}$", 
    color="#1f77b4", 
    linewidth=2.5
)

# Plot Horizontal Asymptote
ax.axhline(
    y=c, 
    color="gray", 
    linestyle="--", 
    alpha=0.7, 
    label=f"Asymptote (y = {c:.1f})"
)

# Plot Y-intercept point
ax.plot(
    0, y_intercept, 
    "ro", 
    markersize=8, 
    label=f"y-intercept (0, {y_intercept:.1f})"
)

# Set axis limits and styling
ax.set_xlim(-3, 3)

# Dynamic y-limits calculation
y_sample = [a * np.exp(k * -3) + c, a * np.exp(k * 3) + c, y_intercept, c]
y_min, y_max = min(y_sample), max(y_sample)
padding = max(abs(y_max - y_min) * 0.2, 5.0)
ax.set_ylim(max(y_min - padding, -30), min(y_max + padding, 50))

ax.set_xlabel("x", fontsize=12)
ax.set_ylabel("y", fontsize=12)
ax.set_title(f"Graph of $y = {a:.1f} \\cdot e^{{{k:.1f} \\cdot x}} + {c:.1f}$", fontsize=14)
ax.grid(True, linestyle=":", alpha=0.6)
ax.legend(loc="upper left")

# Display the plot
st.pyplot(fig)

# Parameter Summary Box
st.code(
    f"Function Parameters:\na = {a:.1f}\nk = {k:.1f}\nc = {c:.1f}",
    language="text"
)

# Dynamic Analysis and Insights
st.subheader("Graph Behavior Analysis")

analysis = []

if k > 0 and a > 0:
    analysis.append("📈 **Exponential Growth**: As $x$ increases, $y$ grows rapidly toward $+\\infty$.")
elif k < 0 and a > 0:
    analysis.append("📉 **Exponential Decay**: As $x$ increases, $y$ approaches the asymptote $y = c$.")
elif k > 0 and a < 0:
    analysis.append("📉 **Inverted Growth**: Vertically reflected ($a < 0$). $y$ decreases toward $-\\infty$.")
elif k < 0 and a < 0:
    analysis.append("📈 **Inverted Decay**: Vertically reflected ($a < 0$). $y$ increases toward $y = c$ from below.")
elif k == 0 or a == 0:
    analysis.append("➡️ **Constant Line**: The graph is a flat horizontal line $y = " + f"{y_intercept:.1f}" + "$.")

analysis.append(f"🏁 **Horizontal Asymptote**: $y = {c:.1f}$ (the line the graph approaches as $x \\to \\pm\\infty$).")
analysis.append(f"📍 **y-intercept**: $(0, {y_intercept:.1f})$ computed from $a \\cdot e^0 + c = {a:.1f} + {c:.1f}$.")

for item in analysis:
    st.markdown(f"- {item}")
