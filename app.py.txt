import streamlit as st

# 모바일 화면에 최적화된 레이아웃 설정
st.set_page_config(page_title="유닛 계산기", layout="centered")

st.title("📊 리스크 관리 유닛 계산기")
st.caption("터틀 트레이딩 방식의 자금 관리 도구")

# --- 입력 섹션 ---
st.header("1. 정보 입력")

# 1. 총 트레이딩 자금
total_capital = st.number_input("총 트레이딩 자금 (원)", value=10000000, step=1000000)

# 2. 리스크 노출 비율 (%)
risk_percent = st.number_input("리스크 노출 비율 (%)", value=1.0, step=0.1, format="%.1f")

# 4. ATR 입력
atr_value = st.number_input("ATR (평균 실질 변동폭)", value=10209, step=100)

# 6. 현재가 입력
current_price = st.number_input("현재가 (원)", value=276500, step=500)

# --- 계산 로직 섹션 ---

# 3. 리스크 노출 금액 = 1 * 2
risk_amount = total_capital * (risk_percent / 100)

# 5. 유닛 계산 = 3 / 4 (소수점 버림)
unit_count = int(risk_amount // atr_value) if atr_value > 0 else 0

# 7. 손절가 계산 = 6 - (2 * ATR)
stop_loss_price = current_price - (2 * atr_value)

# 8. 손절금액 = (7 - 6) * 5
# (손실액이므로 절대값 처리를 하거나 그대로 표시)
expected_loss = (stop_loss_price - current_price) * unit_count

# 9. 총 투자금액 = 6 * 5
total_investment = current_price * unit_count

# --- 결과 출력 섹션 ---
st.divider()
st.header("2. 계산 결과")

col1, col2 = st.columns(2)

with col1:
    st.metric("리스크 노출 금액", f"{int(risk_amount):,} 원")
    st.info(f"📍 **최종 유닛: {unit_count} 주**")
    st.metric("총 투자금액", f"{int(total_investment):,} 원")

with col2:
    st.error(f"손절가 (2ATR): {int(stop_loss_price):,} 원")
    st.metric("예상 손절 금액", f"{int(expected_loss):,} 원")

# 진행 가이드
st.sidebar.markdown("""
### 💡 사용 가이드
1. 자신의 **총 자산**과 감수할 **리스크(보통 1%)**를 넣으세요.
2. 해당 종목의 **ATR**을 입력하여 변동성을 반영합니다.
3. 계산된 **유닛(주식 수)**만큼만 매수하세요.
4. 가격이 **손절가**에 도달하면 미련 없이 매도합니다.
""")