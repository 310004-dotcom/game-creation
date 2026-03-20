import streamlit as st
import random

# 設定網頁標題和配置
st.set_page_config(page_title="賽博龐克文字冒險", layout="centered")

# 賽博龐克主題 CSS
st.markdown("""
<style>
body {
    background-color: #0a0a0a;
    color: #00ff00;
    font-family: 'Courier New', monospace;
}
.stButton>button {
    background-color: #ff0080;
    color: white;
    border: 2px solid #00ff00;
    border-radius: 5px;
}
.stTextInput>div>input {
    background-color: #1a1a1a;
    color: #00ff00;
    border: 1px solid #00ff00;
}
.stSuccess {
    background-color: #004400;
    color: #00ff00;
}
.stError {
    background-color: #440000;
    color: #ff0000;
}
.stInfo {
    background-color: #004444;
    color: #00ffff;
}
</style>
""", unsafe_allow_html=True)

st.title("🕶️ 賽博龐克文字冒險")

# 初始化遊戲狀態
if 'hp' not in st.session_state:
    st.session_state.hp = 100
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'scene' not in st.session_state:
    st.session_state.scene = "你醒來在霓虹燈閃爍的賽博龐克城市街道上。空氣中瀰漫著電子煙和機油的味道。周圍是高聳的摩天大樓，螢幕上閃爍著廣告。你的 HP 是 100。你準備好開始冒險了嗎？"
if 'inventory' not in st.session_state:
    st.session_state.inventory = []
if 'game_over' not in st.session_state:
    st.session_state.game_over = False

# 顯示狀態
st.subheader("狀態")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("HP", st.session_state.hp)
with col2:
    st.metric("分數", st.session_state.score)
with col3:
    st.write("物品:", ", ".join(st.session_state.inventory) if st.session_state.inventory else "無")

# 顯示當前場景
st.subheader("當前場景")
st.write(st.session_state.scene)

# 簡單 AI 回應邏輯 (毒舌酸民風格)
def generate_response(action):
    action = action.lower()
    responses = {
        "探索": [
            "哦，看看這傢伙居然敢探索？小心別被自己的影子嚇到，菜鳥！HP -5",
            "探索？哈，你以為這是遊樂園嗎？這裡是地獄！但算你運氣好，找到一個隨機寶箱！獲得護盾模組。",
            "探索個屁，你在幹嘛？浪費時間！HP -10"
        ],
        "戰鬥": [
            "戰鬥？就你這小身板？被揍得鼻青臉腫，HP -20",
            "哇，英雄上場！結果被電暈槍電到，HP -15，但你撿到敵人的錢包，分數 +10",
            "戰鬥？你連拳頭都握不好！HP -30"
        ],
        "休息": [
            "休息？在這鬼地方休息？你是來度假的嗎？HP +10，但分數 -5，因為你太懶了",
            "休息一下，恢復精神。HP +20",
            "休息？哈，你以為這是飯店嗎？HP +5"
        ],
        "default": [
            "你在說什麼鬼話？我聽不懂！HP -5",
            "隨機事件：你踩到地雷！HP -25",
            "隨機寶箱出現！獲得能量飲料，HP +15"
        ]
    }

    if "探索" in action:
        response = random.choice(responses["探索"])
    elif "戰鬥" in action or "打" in action:
        response = random.choice(responses["戰鬥"])
    elif "休息" in action or "睡" in action:
        response = random.choice(responses["休息"])
    else:
        response = random.choice(responses["default"])

    return response

# 隨機意外事件（增加不可預測性）
def trigger_random_event():
    events = [
        ("電網故障撞斷你的能量核心！HP -10", -10, 0, None),
        ("幸運！你撿到遺失的加密晶片，分數 +15", 0, 15, None),
        ("無人機空投治療包，HP +20", 20, 0, None),
        ("遇到街頭黑客埋伏，HP -20", -20, 0, None),
        ("霓虹煙霧彈爆開，HP -5，下一回合傷害減半（TODO）", -5, 0, None)
    ]
    event_text, hp_delta, score_delta, item = random.choice(events)
    return event_text, hp_delta, score_delta, item

# 道具效果定義
item_effects = {
    "能量飲料": {"hp": 30, "score": 5, "msg": "你喝下能量飲料，HP +30，分數 +5！"},
    "護盾模組": {"hp": 0, "score": 15, "msg": "你啟動護盾模組，暫時防禦提升（未來可能減少傷害）。分數 +15！"},
    "增強藥劑": {"hp": 50, "score": 10, "msg": "你注入增強藥劑，HP +50，分數 +10！"},
}

def use_item(item):
    if item not in item_effects:
        return "無效道具，無法使用。"
    effect = item_effects[item]
    st.session_state.hp += effect["hp"]
    st.session_state.score += effect["score"]
    # HP 上限 150
    st.session_state.hp = min(st.session_state.hp, 150)
    return effect["msg"]

# 處理玩家輸入
if not st.session_state.game_over:
    action = st.text_input("輸入你的行動（例如：探索街道、戰鬥敵人、休息）", key="action_input")
    if st.button("執行行動"):
        if action:
            response = generate_response(action)
            st.session_state.scene = f"你決定：{action}\n\nAI 回應：{response}"

            # 更新狀態（行動結果）
            if "HP -" in response:
                hp_loss = int(response.split("HP -")[1].split()[0])
                st.session_state.hp -= hp_loss
            elif "HP +" in response:
                hp_gain = int(response.split("HP +")[1].split()[0])
                st.session_state.hp += hp_gain
            if "分數 +" in response:
                score_gain = int(response.split("分數 +")[1].split()[0])
                st.session_state.score += score_gain
            elif "分數 -" in response:
                score_loss = int(response.split("分數 -")[1].split()[0])
                st.session_state.score -= score_loss
            if "獲得" in response and "物品" in response:
                item = "神秘物品"
                st.session_state.inventory.append(item)
            if "獲得能量飲料" in response:
                st.session_state.inventory.append("能量飲料")

            # 隨機意外事件機率 (25%)
            if random.random() < 0.25:
                event_text, event_hp, event_score, event_item = trigger_random_event()
                st.session_state.scene += f"\n\n意外事件：{event_text}"
                st.info(f"⚡ 意外事件發生：{event_text}")
                if event_hp != 0:
                    st.session_state.hp += event_hp
                if event_score != 0:
                    st.session_state.score += event_score
                if event_item:
                    st.session_state.inventory.append(event_item)


            # 檢查遊戲結束
            if st.session_state.hp <= 0:
                st.session_state.game_over = True
                st.session_state.scene += "\n\n遊戲結束！你輸了，菜鳥！"
                st.error("遊戲結束！你輸了，菜鳥！")
            else:
                # 視覺回饋
                if st.session_state.hp < 50:
                    st.warning("小心，你的 HP 很低了！")
                elif "寶箱" in response:
                    st.success("🎉 隨機寶箱！")
        else:
            st.warning("請輸入行動！")
else:
    if st.button("重新開始"):
        st.session_state.hp = 100
        st.session_state.score = 0
        st.session_state.scene = "你醒來在霓虹燈閃爍的賽博龐克城市街道上。空氣中瀰漫著電子煙和機油的味道。周圍是高聳的摩天大樓，螢幕上閃爍著廣告。你的 HP 是 100。你準備好開始冒險了嗎？"
        st.session_state.inventory = []
        st.session_state.game_over = False
        st.rerun()

st.info("💡 輸入行動來繼續冒險。記住，HP 歸零就輸了！")
