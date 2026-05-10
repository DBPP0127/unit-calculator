import streamlit as st

# 모바일 화면 최적화 설정
st.set_page_config(page_title="유닛 계산기", layout="centered")

st.title("📈 유닛 계산기 (최종본)")
st.caption("리스크 관리 및 유닛 사이징 도구")

# --- 입력 섹션 ---
st.header("정보 입력")

# 1. 총 트레이딩 자금
total_capital = st.number_input("1. 총 트레이딩 자금 (원)", value=10000000, step=1000000)

# 2. 리스크 노출 비율 (%)
risk_percent = st.number_input("2. 리스크 노출 비율 (%)", value=1.0, step=0.1, format="%.1f")

# 4. ATR 입력
atr_value = st.number_input("4. ATR (변동폭)", value=10209, step=100)

# 6. 매수가 입력
buy_price = st.number_input("6. 매수가 (원)", value=276500, step=500)

# 7. 손절계수 입력 (기본값 2)
stop_loss_multiplier = st.number_input("7. 손절계수 (N값)", value=2.0, step=0.5)

# --- 계산 로직 섹션 ---

# 3. 리스크 노출 금액 = 1 * 2
risk_exposure_amount = total_capital * (risk_percent / 100)

# 5. 유닛 계산 = 3 / 4 (소수점 버림)
unit_count = int(risk_exposure_amount // atr_value) if atr_value > 0 else 0

# 8. 손절가 계산 = 6 - (7 * 4)
stop_loss_price = buy_price - (stop_loss_multiplier * atr_value)

# 9. 매수가 대비 손절률 = (8 - 6) / 6
stop_loss_rate = ((stop_loss_price - buy_price) / buy_price) * 100 if buy_price > 0 else 0

# 10. 손절 금액 = (8 - 6) * 5
actual_stop_loss_amount = (stop_loss_price - buy_price) * unit_count

# 11. 총 투자금액 = 6 * 5
total_investment_amount = buy_price * unit_count

# 12. 손절 시 총 손실율 = 10 / 1
total_loss_rate = (actual_stop_loss_amount / total_capital) * 100 if total_capital > 0 else 0

# --- 결과 출력 섹션 ---
st.divider()
st.header("계산 결과")

# 주요 수치 강조
st.success(f"**5. 최종 매수 유닛: {unit_count} 주**")

col1, col2 = st.columns(2)

with col1:
    st.info(f"**3. 리스크 노출 금액**\n\n{int(risk_exposure_amount):,} 원")
    st.metric("11. 총 투자금액", f"{int(total_investment_amount):,} 원")
    st.metric("12. 총 자산 대비 손실율", f"{total_loss_rate:.2f}%")

with col2:
    st.error(f"**8. 최종 손절가**\n\n{int(stop_loss_price):,} 원")
    st.metric("9. 매수가 대비 손절률", f"{stop_loss_rate:.2f}%")
    st.metric("10. 예상 손절 금액", f"{int(abs(actual_stop_loss_amount)):,} 원")

# 하단 정보 안내
st.sidebar.markdown(f"""
### 📊 적용된 로직
1. **리스크 금액**: 자산의 {risk_percent}%
2. **유닛**: 리스크금액 / ATR
3. **손절라인**: 매수가 - ({stop_loss_multiplier} x ATR)
4. **총 손실율**: 손절 시 전체 자산 대비 삭감 비율
""")