import streamlit as st
import requests
import json
import base64
import os
from datetime import datetime

# ==================== 新增1：历史攻略记录初始化 ====================
if "history" not in st.session_state:
    st.session_state.history = []

# ---------- 处理背景图片 ----------
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
img_path = os.path.join(project_root, "assets", "background.avif")

if os.path.exists(img_path):
    with open(img_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()
    img_url = f"data:image/avif;base64,{img_b64}"
else:
    img_url = "data:image/avif;base64,"  # 空图片，不显示

# ---------- 自定义 CSS ----------
st.markdown(f"""
<style>
.stApp {{
    background: transparent !important;
}}
.stApp::before {{
    content: "";
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background-image: url("{img_url}");
    background-size: cover;
    background-position: center;
    opacity: 0.15;
    z-index: -1;
    pointer-events: none;
}}
</style>
""", unsafe_allow_html=True)

# ========== 页面标题 ==========
st.markdown("## 旅行攻略生成器")
st.markdown("填好下面几个信息，让 AI 帮你规划行程。")

# ========== 后端 URL 配置 ==========
backend_url = "http://localhost:8000"  
# 可改为实际的 ngrok 地址，如 "https://abc123.ngrok.io"

# ========== 输入表单 ==========
with st.form("trip_form"):
    col1, col2 = st.columns([3, 2])
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
    submitted = st.form_submit_button("开始生成攻略", use_container_width=True)

# ==================== 新增2：显示目的地天气（在表单下方，提交前显示） ====================
if destination:
    try:
        weather_url = f"https://wttr.in/{destination}?format=%C+%t"
        resp = requests.get(weather_url, timeout=5)
        if resp.status_code == 200:
            weather = resp.text.strip()
            st.info(f"📍 {destination} 当前天气：{weather}")
        else:
            st.info(f"📍 无法获取 {destination} 的天气")
    except:
        st.info(f"📍 天气服务暂时不可用")

# ========== 处理提交 ==========
if submitted:
    if not destination.strip():
        st.warning("请输入目的地")
    else:
        with st.spinner("正在生成，请稍等……（可能需要十几秒）"):
            try:
                payload = {
                    "destination": destination.strip(),
                    "days": int(days),
                    "preferences": preferences.strip()
                }
                response = requests.post(
                    f"{backend_url}/generate_trip",
                    json=payload,
                    timeout=90
                )
                if response.status_code == 200:
                    data = response.json()
                    plan = data.get("plan", data.get("result", ""))
                    # 展示结果
                    st.markdown(f"""
                    <div class="result-box">
                        <h4 style="margin-top:0; font-size:1.1em;">为您生成的攻略</h4>
                        {plan}
                    </div>
                    """, unsafe_allow_html=True)

                    # ==================== 新增3：下载攻略按钮 ====================
                    if plan:
                        st.download_button(
                            label="📥 下载攻略",
                            data=plan.encode("utf-8"),
                            file_name=f"{destination.strip()}_攻略.md",
                            mime="text/markdown",
                            use_container_width=True
                        )

                    # ==================== 新增4：将本次结果存入历史记录 ====================
                    st.session_state.history.append({
                        "time": datetime.now().strftime("%H:%M"),
                        "destination": destination.strip(),
                        "plan": plan
                    })
                else:
                    st.error(f"服务器返回了错误（状态码 {response.status_code}）")
                    st.info("可能是后端模型超时或请求格式不对，请尝试刷新后重试。")
            except requests.exceptions.ConnectionError:
                st.error("无法连接到后端服务，请确认后端是否已启动，或者检查输入的地址。")
            except Exception as e:
                st.error(f"发生意外错误：{e}")
else:
    st.markdown("---")
    st.caption("填写左侧信息，点击「开始生成攻略」即可。")

# ==================== 新增5：展示历史攻略记录（放在页脚之前） ====================
if st.session_state.history:
    with st.expander("📋 历史攻略记录（点击展开）", expanded=False):
        for i, h in enumerate(st.session_state.history):
            st.markdown(f"**🕒 {h['time']} · {h['destination']}**")
            # 只显示前200字避免页面过长
            st.caption(h['plan'][:200] + ("..." if len(h['plan']) > 200 else ""))
            st.divider()

# === 页脚 ====
st.markdown("---")
st.markdown(
    "<small style='color: #666;'>本工具使用 AI 生成内容，请结合实际情况调整行程。</small>",
    unsafe_allow_html=True
)