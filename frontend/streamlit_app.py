import streamlit as st
import random
import time

# 设置页面标题和布局
st.set_page_config(page_title="AI 旅游攻略生成器", layout="centered")

# 页面主标题
st.title("🌍 AI 旅游攻略生成器")

# 用户输入区域
destination = st.text_input("请输入目的地", placeholder="例如：北京、东京、巴黎...")
days = st.number_input("请输入旅行天数", min_value=1, max_value=30, value=3, step=1)

# 按钮触发生成
if st.button("生成攻略"):
    # 检查目的地是否为空
    if not destination.strip():
        st.error("请输入有效的目的地！")
    else:
        # 显示加载状态（模拟请求延迟）
        with st.spinner("正在精心为您规划行程..."):
            time.sleep(1.5)  # 模拟网络请求延迟

            # ----- 伪数据生成函数 -----
            def generate_itinerary(dest, num_days):
                """
                根据目的地和天数生成每日行程（伪数据）
                参数:
                    dest: 目的地字符串
                    num_days: 旅行天数
                返回:
                    列表，每个元素是一个字典，包含 'title' 和 'description'
                """
                # 预定义一些热门目的地的景点列表
                attractions = {
                    "北京": ["天安门广场", "故宫博物院", "颐和园", "长城", "天坛", "鸟巢", "798艺术区"],
                    "东京": ["浅草寺", "东京塔", "涩谷十字路口", "秋叶原", "新宿御苑", "银座"],
                    "巴黎": ["埃菲尔铁塔", "卢浮宫", "巴黎圣母院", "凯旋门", "塞纳河畔", "香榭丽舍大街"],
                    "纽约": ["自由女神像", "时代广场", "中央公园", "帝国大厦", "大都会博物馆", "百老汇"],
                }
                # 如果目的地不在预定义列表中，使用通用模板
                if dest in attractions:
                    spots = attractions[dest].copy()
                else:
                    spots = [f"{dest}著名景点{i}" for i in range(1, 20)]

                # 打乱景点顺序，让每日行程更随机
                random.shuffle(spots)

                itinerary = []
                for day in range(1, num_days + 1):
                    # 每天分配 1-2 个景点
                    start_idx = (day - 1) * 2
                    end_idx = start_idx + 2
                    day_spots = spots[start_idx:end_idx]

                    # 如果景点不够，用“自由活动”补充
                    if not day_spots:
                        day_spots = ["自由活动"]

                    # 生成标题（如：第1天：天安门广场 & 故宫博物院）
                    title = f"第{day}天：{day_spots[0]}"
                    if len(day_spots) > 1:
                        title += f" & {day_spots[1]}"

                    # 生成描述（上午、下午、晚上建议）
                    desc = f"上午游览 {day_spots[0]}，"
                    if len(day_spots) > 1:
                        desc += f"下午前往 {day_spots[1]}。"
                    else:
                        desc += "下午自由活动。"
                    desc += "晚上可以品尝当地美食，感受夜生活。"

                    itinerary.append({"title": title, "description": desc})

                return itinerary

            # 调用伪数据函数生成行程
            itinerary = generate_itinerary(destination.strip(), days)

        # 显示成功提示
        st.success("攻略生成成功！")
        st.subheader(f"📍 {destination} {days}天行程安排")

        # 逐日显示行程，使用可折叠的 expander 组件，默认展开
        for day_plan in itinerary:
            with st.expander(f"**{day_plan['title']}**", expanded=True):
                st.write(day_plan['description'])

# 页脚信息
st.markdown("---")
st.caption("本项目使用 Streamlit 构建，数据为示例伪数据，用于演示前端交互效果。")