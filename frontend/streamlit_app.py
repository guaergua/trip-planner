import streamlit as st
import requests
import json
from datetime import datetime

# ========== 页面设置 ==========
st.set_page_config(
    page_title="AI 旅游攻略",
    page_icon="✈️",       # 允许 favicon 用 emoji，但界面上不用 emoji 做图标
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========== 自定义 CSS：背景有噪点 + 微弱渐变，避免紫色/靛蓝 ==========
st.markdown(
    """
    <style>
    /* 整个页面的背景：浅灰白到淡蓝绿的渐变，叠加噪点纹理（SVG 点阵） */
    .stApp {
        background-image: 
            linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%),
            url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
        background-blend-mode: overlay;
        background-size: cover, 200px 200px;   /* 噪声纹理重复 */
        background-repeat: no-repeat, repeat;
    }
    /* 去掉 Streamlit 默认的居中效果，内容区靠左 */
    .block-container {
        padding-left: 3rem !important;
        padding-right: 3rem !important;
        max-width: 960px;
        margin-left: 0;
        margin-right: auto;
    }
    /* 输入框、按钮等不做居中，保持默认左对齐 */
    .stTextInput, .stTextArea, .stNumberInput, .stButton {
        text-align: left;
    }
    /* 避免任何 emoji 作为功能图标，用纯文字 */
    /* 自定义结果卡片（非卡片布局，只是一段带背景的文本框） */
    .result-box {
        background: rgba(255,255,255,0.8);
        border-left: 4px solid #4a90d9;
        padding: 1rem;
        border-radius: 4px;
        margin-top: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ========== 页面标题（不用 Hero，用简单的 H2） ==========
st.markdown("## 旅行攻略生成器")
st.markdown("填好下面几个信息，让 AI 帮你规划行程。")

# ========== 后端 URL 配置（允许用户修改，但默认都是 localhost） ==========
with st.sidebar:
    st.markdown("**后端服务地址**")
    backend_url = st.text_input(
        "API 地址",
        value="http://localhost:8000",
        help="如果后端部署在其他地方，请修改这里"
    )

# ========== 输入表单 ==========
with st.form("trip_form"):
    col1, col2 = st.columns([3, 2])  # 不等宽，避免完美对称
    with col1:
        destination = st.text_input("你想去哪里？", placeholder="例如：北京、东京、巴黎")
    with col2:
        days = st.number_input("玩几天？", min_value=1, max_value=30, value=3, step=1)

    st.markdown("---")
    preferences = st.text_area(
        "有什么特别的喜好或要求吗？",
        placeholder="喜欢美食、历史景点、或者带孩子出行等",
        height=120
    )
    # 提交按钮（不用 emoji，用纯文字）
    submitted = st.form_submit_button("开始生成攻略", use_container_width=True)

# ========== 处理提交 ==========
if submitted:
    if not destination.strip():
        st.warning("请输入目的地")
    else:
        # 显示加载状态（自带 Streamlit spinner）
        with st.spinner("正在生成，请稍等……（可能需要十几秒）"):
            try:
                payload = {
                    "destination": destination.strip(),
                    "days": int(days),
                    "preferences": preferences.strip()
                }
                # 调用后端
                response = requests.post(
                    f"{backend_url}/generate_trip",
                    json=payload,
                    timeout=90  # 大模型可能较慢
                )
                if response.status_code == 200:
                    data = response.json()
                    plan = data.get("plan", data.get("result", ""))
                    # 展示结果（不用卡片布局，用带边框的文本框）
                    st.markdown(f"""
                    <div class="result-box">
                        <h4 style="margin-top:0; font-size:1.1em;">为您生成的攻略</h4>
                        {plan}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error(f"服务器返回了错误（状态码 {response.status_code}）")
                    st.info("可能是后端模型超时或请求格式不对，请尝试刷新后重试。")
            except requests.exceptions.ConnectionError:
                st.error("无法连接到后端服务，请确认后端是否已启动，或者检查输入的地址。")
            except Exception as e:
                st.error(f"发生意外错误：{e}")
else:
    # 默认展示占位提示，引导用户操作（不用 Hero，用小剂量文字）
    st.markdown("---")
    st.caption("填写左侧信息，点击「开始生成攻略」即可。")

# === 页脚：简单的版权信息（纯文本）===
st.markdown("---")
st.markdown(
    "<small style='color: #666;'>本工具使用 AI 生成内容，请结合实际情况调整行程。</small>",
    unsafe_allow_html=True
)