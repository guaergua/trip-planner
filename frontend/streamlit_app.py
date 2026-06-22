import streamlit as st
import pandas as pd
import numpy as np
import time
import json
from datetime import datetime
import requests  # 用于获取在线音乐流
import base64

# ------------------------------
# 1. 页面设置
# ------------------------------
st.set_page_config(
    page_title="✨ 多功能仪表盘",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------
# 2. 自定义 CSS（包含本地背景图片与毛玻璃效果）
# ------------------------------
st.markdown("""
<style>
/* 整体背景：本地图片 + 渐变色 + 噪点纹理 */
.stApp::before {
    content: "";
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background-image: url("../assets/background.avif");   /* 本地图片路径 */
    background-size: cover;
    background-position: center;
    opacity: 0.12;               /* 透明度，让文字更清晰 */
    z-index: -1;
    pointer-events: none;
}
.stApp {
    background-image: 
        linear-gradient(135deg, #e8ecef 0%, #c9d6dc 100%),
        url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
    background-blend-mode: overlay;
    background-size: cover, 200px 200px;
    background-repeat: no-repeat, repeat;
}

/* 主内容区半透明毛玻璃卡片 */
.block-container {
    background-color: rgba(255, 255, 255, 0.72) !important;
    backdrop-filter: blur(4px);
    border-radius: 12px;
    padding: 1.8rem 2.2rem !important;
    margin-left: 3rem !important;
    margin-right: 3rem !important;
    max-width: 1200px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.08);
}

/* 标题美化 */
h1, h2, h3 {
    color: #1a2332 !important;
    font-weight: 600 !important;
}

/* 侧边栏透明化 */
.css-1d391kg, .css-12oz5g7 {
    background-color: rgba(255, 255, 255, 0.5) !important;
}

/* 按钮圆润 */
.stButton button {
    border-radius: 24px !important;
    border: none;
    padding: 0.4rem 1.2rem;
    background: #f0f2f6;
    transition: all 0.2s;
}
.stButton button:hover {
    background: #d1d9e0;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# ------------------------------
# 3. 侧边栏导航
# ------------------------------
st.sidebar.title("📌 导航")
page = st.sidebar.radio(
    "选择页面",
    ["首页", "关于我们", "数据分析", "数据可视化", "数据表格", "🎵 音乐电台", "💬 聊天室"]
)

# 侧边栏附加信息
st.sidebar.markdown("---")
st.sidebar.info("使用本地背景图片\n路径: `assets/background.avif`")

# ------------------------------
# 4. 各页面内容
# ------------------------------

# 4.0 公共：如果当前页不是聊天室，则显示时间和欢迎
if page != "💬 聊天室":
    st.title(f"✨ {page}")
    st.caption(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# 4.1 首页
if page == "首页":
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("访问者", "1,234", "+12%")
    with col2:
        st.metric("活跃项目", "56", "↑3")
    with col3:
        st.metric("数据总量", "82.7 GB", "↓2%")
    
    st.markdown("### 📊 快速概览")
    # 模拟折线图
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['销售额', '用户数', '转化率']
    )
    st.line_chart(chart_data)

# 4.2 关于我们
elif page == "关于我们":
    st.markdown("""
    **团队简介**  
    我们是一支热爱数据与技术的团队，致力于打造美观且实用的数据分析工具。  
    - **核心成员**：张三（数据工程师）、李四（全栈开发）、王五（UI设计）  
    - **联系方式**：contact@example.com  
    - **技术栈**：Streamlit, Python, Plotly, Pandas  
    """)
    st.image("https://via.placeholder.com/800x200?text=About+Us+Banner", use_column_width=True)

# 4.3 数据分析
elif page == "数据分析":
    uploaded_file = st.file_uploader("上传 CSV 文件进行数据分析", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df)
        if st.button("显示基本统计"):
            st.write(df.describe())
        if st.button("显示缺失值"):
            st.write(df.isnull().sum())
    else:
        st.info("请上传一个 CSV 文件开始分析。")

# 4.4 数据可视化
elif page == "数据可视化":
    st.markdown("### 📈 示例图表")
    df = pd.DataFrame(
        np.random.randn(100, 3),
        columns=['指标A', '指标B', '指标C']
    )
    option = st.selectbox("选择图表类型", ["散点图", "柱状图", "面积图"])
    if option == "散点图":
        st.scatter_chart(df)
    elif option == "柱状图":
        st.bar_chart(df)
    else:
        st.area_chart(df)

# 4.5 数据表格
elif page == "数据表格":
    st.markdown("### 📋 示例数据表（可排序、筛选）")
    data = {
        "城市": ["北京", "上海", "广州", "深圳", "杭州"],
        "GDP (亿元)": [36102, 38155, 25019, 27670, 15373],
        "人口 (万)": [2189, 2428, 1530, 1756, 1036],
        "增速 (%)": [5.2, 4.8, 3.9, 4.2, 6.1]
    }
    df = pd.DataFrame(data)
    st.data_editor(df, use_container_width=True)   # 可编辑表格

# 4.6 音乐电台
elif page == "🎵 音乐电台":
    st.title("🎵 音乐电台")
    st.caption("在线音乐列表（来源：freemusicarchive.org）")

    # 预设几首免费音乐（均为公开可用链接）
    playlist = [
        {"name": "Ambient Piano", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"},
        {"name": "Relaxing Guitar", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3"},
        {"name": "Electronic Beat", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3"},
        {"name": "Jazz Vibes", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3"},
        {"name": "Chill Out", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3"}
    ]

    # 将播放列表保存到 session_state
    if "playlist" not in st.session_state:
        st.session_state.playlist = playlist
        st.session_state.current_track = 0
        st.session_state.playing = False
        st.session_state.player_key = 0   # 用于强制刷新音频组件

    col1, col2, col3 = st.columns([1,4,1])
    with col2:
        track_info = st.session_state.playlist[st.session_state.current_track]
        st.markdown(f"### 🎧 正在播放: **{track_info['name']}**")
        # 音频播放器
        audio_html = f"""
        <audio id="audio-player" controls autoplay style="width:100%;">
            <source src="{track_info['url']}" type="audio/mpeg">
            您的浏览器不支持音频播放。
        </audio>
        <script>
            var audio = document.getElementById('audio-player');
            // 控制播放状态
        </script>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
        # 控制按钮
        btn_col1, btn_col2, btn_col3 = st.columns(3)
        with btn_col1:
            if st.button("⏮ 上一首"):
                st.session_state.current_track = (st.session_state.current_track - 1) % len(st.session_state.playlist)
                st.rerun()
        with btn_col2:
            if st.button("⏯ 播放/暂停"):
                # 由于 HTML audio 无法直接通过 Streamlit 控制，所以使用 rerun 重置
                st.session_state.playing = not st.session_state.playing
                st.rerun()
        with btn_col3:
            if st.button("⏭ 下一首"):
                st.session_state.current_track = (st.session_state.current_track + 1) % len(st.session_state.playlist)
                st.rerun()

    # 显示完整播放列表
    st.markdown("---")
    st.markdown("📋 **播放列表**")
    for i, track in enumerate(st.session_state.playlist):
        if i == st.session_state.current_track:
            st.markdown(f"- **▶ {track['name']}** (当前)")
        else:
            st.markdown(f"- {track['name']}")

# 4.7 聊天室
elif page == "💬 聊天室":
    st.title("💬 聊天室")
    st.caption("模拟聊天界面（仅本地存储）")

    # 初始化聊天记录
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "你好！我是智能助手，有什么可以帮你的？"}
        ]

    # 显示聊天记录
    for msg in st.session_state.messages:
        if msg["role"] == "assistant":
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(msg["content"])
        else:
            with st.chat_message("user", avatar="👤"):
                st.markdown(msg["content"])

    # 输入框
    prompt = st.chat_input("输入你的消息...")
    if prompt:
        # 添加用户消息
        st.session_state.messages.append({"role": "user", "content": prompt})
        # 模拟回复
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("思考中..."):
                time.sleep(1.2)
                reply = f"收到你的消息: “{prompt}”\n\n这是一个模拟回复，实际可接入 AI 接口。"
                st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

# ------------------------------
# 5. 页脚
# ------------------------------
st.sidebar.markdown("---")
st.sidebar.success("❤️ 使用 Streamlit 构建 | 🎯 版本 1.0")