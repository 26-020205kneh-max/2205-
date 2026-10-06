import streamlit as st

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="2205 박윤호 - 오목 게임",
    page_icon="⚫",
    layout="centered"
)

SIZE = 15

# -----------------------------
# 세션 상태 초기화
# -----------------------------
if "board" not in st.session_state:
    st.session_state.board = [[0 for _ in range(SIZE)] for _ in range(SIZE)]

if "player" not in st.session_state:
    st.session_state.player = 1

if "game_over" not in st.session_state:
    st.session_state.game_over = False

if "winner" not in st.session_state:
    st.session_state.winner = 0


# -----------------------------
# 게임 초기화
# -----------------------------
def reset_game():
    st.session_state.board = [
        [0 for _ in range(SIZE)]
        for _ in range(SIZE)
    ]

    st.session_state.player = 1
    st.session_state.game_over = False
    st.session_state.winner = 0


# -----------------------------
# 승리 확인
# -----------------------------
def check_win(row, col, player):
    directions = [
        (0, 1),    # 가로
        (1, 0),    # 세로
        (1, 1),    # 대각선 \
        (1, -1)    # 대각선 /
    ]

    for dr, dc in directions:
        count = 1

        # 한 방향
        r = row + dr
        c = col + dc

        while (
            0 <= r < SIZE
            and 0 <= c < SIZE
            and st.session_state.board[r][c] == player
        ):
            count += 1
            r += dr
            c += dc

        # 반대 방향
        r = row - dr
        c = col - dc

        while (
            0 <= r < SIZE
            and 0 <= c < SIZE
            and st.session_state.board[r][c] == player
        ):
            count += 1
            r -= dr
            c -= dc

        if count >= 5:
            return True

    return False


# -----------------------------
# 돌 놓기
# -----------------------------
def put_stone(row, col):
    if st.session_state.game_over:
        return

    # 이미 돌이 있으면 무시
    if st.session_state.board[row][col] != 0:
        return

    player = st.session_state.player

    st.session_state.board[row][col] = player

    # 승리 확인
    if check_win(row, col, player):
        st.session_state.game_over = True
        st.session_state.winner = player
        return

    # 플레이어 변경
    if player == 1:
        st.session_state.player = 2
    else:
        st.session_state.player = 1


# -----------------------------
# CSS
# -----------------------------
st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        color: #5a3518;
        font-size: 36px;
        font-weight: bold;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        color: #777;
        margin-bottom: 20px;
    }

    .board {
        background-color: #D9A85F;
        padding: 10px;
        border: 5px solid #6B421F;
        border-radius: 5px;
    }

    div.stButton > button {
        width: 100%;
        height: 42px;
        border-radius: 5px;
        border: 1px solid #6B421F;
        background-color: #E5B96A;
        color: #3E2512;
        font-size: 20px;
        font-weight: bold;
        padding: 0;
    }

    div.stButton > button:hover {
        background-color: #F0CA7C;
        border-color: #3E2512;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# 제목
# -----------------------------
st.markdown(
    '<div class="main-title">🎮 2205 박윤호</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">⚫ ⚪ 오목 게임</div>',
    unsafe_allow_html=True
)


# -----------------------------
# 게임 상태 표시
# -----------------------------
if st.session_state.game_over:

    if st.session_state.winner == 1:
        st.success("🎉 흑돌 승리!")

    else:
        st.success("🎉 백돌 승리!")

else:

    if st.session_state.player == 1:
        st.info("⚫ 흑돌 차례입니다.")
    else:
        st.info("⚪ 백돌 차례입니다.")


# -----------------------------
# 오목판
# -----------------------------
st.markdown('<div class="board">', unsafe_allow_html=True)

for row in range(SIZE):

    columns = st.columns(SIZE, gap="small")

    for col in range(SIZE):

        with columns[col]:

            value = st.session_state.board[row][col]

            if value == 1:
                text = "⚫"

            elif value == 2:
                text = "⚪"

            else:
                text = "·"

            st.button(
                text,
                key=f"cell_{row}_{col}",
                on_click=put_stone,
                args=(row, col),
                disabled=(
                    value != 0
                    or st.session_state.game_over
                )
            )

st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------
# 다시 시작 버튼
# -----------------------------
st.write("")

if st.button("🔄 게임 다시 시작"):
    reset_game()
    st.rerun()


# -----------------------------
# 게임 설명
# -----------------------------
st.divider()

st.markdown("### 🎯 게임 방법")

st.write(
    """
    - ⚫ 흑돌부터 게임을 시작합니다.
    - ⚫ → ⚪ 순서로 돌을 놓습니다.
    - 가로, 세로, 대각선 중 한 방향으로 **5개의 돌을 연속으로 놓으면 승리**합니다.
    - `🔄 게임 다시 시작` 버튼을 누르면 새로운 게임을 시작할 수 있습니다.
    """
)

st.caption("2205 박윤호 · Omok Game")
