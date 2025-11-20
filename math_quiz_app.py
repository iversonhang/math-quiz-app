import streamlit as st
import random
from datetime import date, datetime
import sqlite3
import hashlib
import pandas as pd

# --- CONFIGURATION ---
st.set_page_config(page_title="香港小五/小六數學挑戰站 (無限版)", page_icon="🧮")

# --- DATABASE FUNCTIONS ---

def get_db_connection():
    conn = sqlite3.connect('math_data.db', check_same_thread=False)
    return conn

def init_db():
    """Initialize the database with users and scores tables."""
    conn = get_db_connection()
    c = conn.cursor()
    # User table
    c.execute('CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, password TEXT)')
    # Score history table
    c.execute('''CREATE TABLE IF NOT EXISTS scores
                 (username TEXT, topic TEXT, score INTEGER, total INTEGER, 
                  percentage REAL, timestamp TEXT)''')
    conn.commit()
    conn.close()

def make_hashes(password):
    """Create a secure hash of the password."""
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    """Check if the entered password matches the stored hash."""
    if make_hashes(password) == hashed_text:
        return True
    return False

def add_user(username, password):
    """Add a new user to the database."""
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users(username, password) VALUES (?,?)', 
                  (username, make_hashes(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False # Username already exists
    finally:
        conn.close()

def login_user(username, password):
    """Verify login credentials."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    data = c.fetchall()
    conn.close()
    
    if data:
        if check_hashes(password, data[0][1]):
            return True
    return False

def save_score_to_db(username, topic, score, total):
    """Save the quiz result to history."""
    conn = get_db_connection()
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    percentage = round((score / total) * 100, 1)
    c.execute('INSERT INTO scores(username, topic, score, total, percentage, timestamp) VALUES (?,?,?,?,?,?)', 
              (username, topic, score, total, percentage, timestamp))
    conn.commit()
    conn.close()

def get_user_history(username):
    """Retrieve score history for a user."""
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT topic, score, total, percentage, timestamp FROM scores WHERE username = ? ORDER BY timestamp DESC", conn, params=(username,))
    conn.close()
    return df

# --- QUESTION GENERATORS (Same as before) ---

def generate_algebra_question():
    q_type = random.choice(["equation_solve", "substitution", "expression"])
    if q_type == "equation_solve":
        a = random.randint(2, 9)
        ans = random.randint(2, 12)
        b = random.randint(1, 20)
        c = a * ans + b
        var = random.choice(['x', 'y', 'a', 'm'])
        question = f"解方程： ${a}{var} + {b} = {c}$"
        correct = str(ans)
        options = [str(ans), str(ans+1), str(ans-1), str(ans*2)]
        explanation = f"${a}{var} = {c} - {b} = {c-b}$，所以 ${var} = {c-b} \div {a} = {ans}$。"
    elif q_type == "substitution":
        n = random.randint(2, 10)
        a = random.randint(2, 5)
        b = random.randint(1, 10)
        var = random.choice(['x', 'y', 'k'])
        correct_val = a * n - b
        question = f"如果 ${var} = {n}$，求 ${a}{var} - {b}$ 的值。"
        correct = str(correct_val)
        options = [str(correct_val), str(correct_val+a), str(correct_val-b), str(a*n+b)]
        explanation = f"代入 ${var}={n}$： ${a}({n}) - {b} = {a*n} - {b} = {correct_val}$。"
    else:
        n = random.randint(2, 10)
        var = random.choice(['y', 'n', 'x'])
        op_text = random.choice(["減去", "加上", "乘以", "除以"])
        if op_text == "減去":
            question = f"下列哪個代數式表示「從 {var} 減去 {n}」？"
            correct = f"{var} - {n}"
            options = [f"{var} - {n}", f"{n} - {var}", f"{var} / {n}", f"{n}{var}"]
        elif op_text == "加上":
            question = f"下列哪個代數式表示「{var} 加上 {n}」？"
            correct = f"{var} + {n}"
            options = [f"{var} + {n}", f"{var} - {n}", f"{var} / {n}", f"{n}{var}"]
        else:
            question = f"下列哪個代數式表示「{n} 乘以 {var}」？"
            correct = f"{n}{var}"
            options = [f"{n}{var}", f"{var} + {n}", f"{var} / {n}", f"{var} - {n}"]
        explanation = "根據題意直接寫出代數式。"
    random.shuffle(options)
    return {"topic": "代數", "question": question, "options": options, "answer": correct, "explanation": explanation}

def generate_geometry_question():
    q_type = random.choice(["triangle_area", "square_area", "cube_vol", "direction"])
    if q_type == "triangle_area":
        b = random.randint(4, 20)
        h = random.randint(4, 20)
        if b % 2 != 0 and h % 2 != 0: b += 1
        area = int(0.5 * b * h)
        question = f"計算底為 ${b}\\text{{ cm}}$，高為 ${h}\\text{{ cm}}$ 的三角形面積。"
        correct = f"{area} cm²"
        options = [f"{area} cm²", f"{b*h} cm²", f"{area+10} cm²", f"{b+h} cm²"]
        explanation = f"面積 = (底 × 高) / 2 = ({b} × {h}) / 2 = {area}。"
    elif q_type == "cube_vol":
        s = random.randint(2, 10)
        vol = s ** 3
        question = f"邊長為 ${s}\\text{{ cm}}$ 的正方體，體積是多少？"
        correct = f"{vol} cm³"
        options = [f"{vol} cm³", f"{s*s} cm³", f"{s*4} cm³", f"{vol*2} cm³"]
        explanation = f"體積 = 邊長 × 邊長 × 邊長 = {s} × {s} × {s} = {vol}。"
    elif q_type == "direction":
        turns = random.choice([("90°", "東"), ("180°", "南"), ("270°", "西"), ("135°", "東南"), ("225°", "西南")])
        deg, direct = turns
        question = f"如果你面向北方，順時針轉 ${deg}$，你會面向哪個方向？"
        correct = direct
        options = list(set(["東", "南", "西", "北", "東南", "東北", "西南", "西北"]))
        random.shuffle(options)
        options = options[:3]
        if correct not in options: options[0] = correct
        explanation = f"從北方順時針轉 ${deg}$ 指向{direct}。"
    else:
        s = random.randint(2, 15)
        area = s * s
        question = f"正方形的邊長是 ${s}\\text{{ m}}$，它的面積是多少？"
        correct = f"{area} m²"
        options = [f"{area} m²", f"{s*4} m²", f"{s*2} m²", f"{area+5} m²"]
        explanation = f"正方形面積 = 邊長 × 邊長 = {s} × {s} = {area}。"
    random.shuffle(options)
    return {"topic": "幾何", "question": question, "options": options, "answer": correct, "explanation": explanation}

def generate_number_question():
    q_type = random.choice(["percentage", "hcf", "lcm", "decimal_mult"])
    if q_type == "percentage":
        num = random.choice([1, 2, 3, 4])
        den = random.choice([5, 10, 20, 25, 50])
        val = (num / den) * 100
        question = f"把 $\\frac{{{num}}}{{{den}}}$ 化為百分數。"
        correct = f"{int(val)}%"
        options = [f"{int(val)}%", f"{int(val/2)}%", f"{int(val*2)}%", f"{num*10}%"]
        explanation = f"${num} \div {den} = {num/den} = {int(val)}\%$。"
    elif q_type == "hcf":
        a = random.randint(2, 9) * random.randint(1, 4)
        b = random.randint(2, 9) * random.randint(1, 4)
        x, y = a, b
        while y: x, y = y, x % y
        hcf = x
        question = f"求 ${a}$ 和 ${b}$ 的 H.C.F (最大公因數)。"
        correct = str(hcf)
        options = list(set([str(hcf), str(random.randint(1, 10)), str(random.randint(1, 10)), str(1)]))
        if len(options) < 4: options.append(str(hcf+1))
        options = options[:4]
        if str(hcf) not in options: options[0] = str(hcf)
        explanation = f"找出能同時整除 {a} 和 {b} 的最大整數。"
    elif q_type == "lcm":
        a = random.randint(2, 8)
        b = random.randint(2, 8)
        x, y = a, b
        while y: x, y = y, x % y
        lcm = int((a * b) / x)
        question = f"求 ${a}$ 和 ${b}$ 的 L.C.M (最小公倍數)。"
        correct = str(lcm)
        options = [str(lcm), str(a*b), str(lcm*2), str(lcm+1)]
        explanation = f"{a} 和 {b} 的公倍數中最小的一個是 {lcm}。"
    else:
        a = random.randint(1, 9) / 10
        b = random.randint(2, 9)
        ans = round(a * b, 2)
        question = f"計算： ${a} \\times {b}$"
        correct = str(ans)
        options = [str(ans), str(ans*10), str(ans/10), str(round(ans+0.1, 2))]
        explanation = "直接相乘，注意小數點位置。"
    random.shuffle(options)
    return {"topic": "數範疇", "question": question, "options": options, "answer": correct, "explanation": explanation}

def generate_data_question():
    n1 = random.randint(10, 50)
    n2 = random.randint(10, 50)
    n3 = random.randint(10, 50)
    current_sum = n1 + n2 + n3
    remainder = current_sum % 3
    if remainder != 0:
        n3 += (3 - remainder)
    avg = int((n1 + n2 + n3) / 3)
    question = f"求這組數的平均數 (Average)： ${n1}, {n2}, {n3}$"
    correct = str(avg)
    options = [str(avg), str(avg+5), str(avg-2), str(n1+n2+n3)]
    random.shuffle(options)
    explanation = f"總和 = {n1+n2+n3}。平均數 = {n1+n2+n3} ÷ 3 = {avg}。"
    return {"topic": "數據處理", "question": question, "options": options, "answer": correct, "explanation": explanation}

def get_dynamic_questions(topic_filter="每日挑戰"):
    questions = []
    num_questions = 10
    
    if topic_filter == "每日挑戰":
        today_seed = date.today().toordinal()
        random.seed(today_seed)
    else:
        random.seed()

    for i in range(num_questions):
        if topic_filter == "每日挑戰":
            q_topic = random.choice(["代數", "幾何", "數範疇", "數據處理"])
        else:
            q_topic = topic_filter

        if q_topic == "代數": q = generate_algebra_question()
        elif q_topic == "幾何": q = generate_geometry_question()
        elif q_topic == "數範疇": q = generate_number_question()
        elif q_topic == "數據處理": q = generate_data_question()
        else: q = generate_number_question()
        q['id'] = i
        questions.append(q)
    return questions

# --- MAIN APP UI ---

def main():
    # Ensure DB tables exist
    init_db()

    # Session State for Login
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = ''

    # --- AUTHENTICATION LOGIC ---
    if not st.session_state.logged_in:
        st.title("🎓 香港小五/小六數學挑戰站")
        
        tab1, tab2 = st.tabs(["登入 (Login)", "註冊 (Sign Up)"])
        
        with tab1:
            st.subheader("歡迎回來！")
            login_user_input = st.text_input("用戶名", key="login_user")
            login_pass_input = st.text_input("密碼", type='password', key="login_pass")
            if st.button("登入"):
                if login_user(login_user_input, login_pass_input):
                    st.session_state.logged_in = True
                    st.session_state.username = login_user_input
                    st.success(f"歡迎 {login_user_input}！")
                    st.rerun()
                else:
                    st.error("用戶名或密碼錯誤")

        with tab2:
            st.subheader("建立新帳戶")
            new_user = st.text_input("設定用戶名", key="new_user")
            new_pass = st.text_input("設定密碼", type='password', key="new_pass")
            if st.button("註冊"):
                if new_user and new_pass:
                    if add_user(new_user, new_pass):
                        st.success("帳戶建立成功！請切換到「登入」頁面。")
                    else:
                        st.warning("該用戶名已被使用，請選擇另一個。")
                else:
                    st.warning("請輸入用戶名和密碼")
        return  # Stop here if not logged in

    # --- LOGGED IN INTERFACE ---
    
    # Sidebar
    st.sidebar.title(f"👤 {st.session_state.username}")
    
    app_mode = st.sidebar.radio("導航", ["開始練習", "我的成績記錄"])
    
    if st.sidebar.button("登出"):
        st.session_state.logged_in = False
        st.session_state.username = ''
        st.rerun()

    # --- QUIZ SECTION ---
    if app_mode == "開始練習":
        topics = ["每日挑戰", "代數", "幾何", "數範疇", "數據處理"]
        selected_topic = st.sidebar.selectbox("選擇主題", topics)
        
        st.title(f"香港小五/小六數學 - {selected_topic}")
        
        if selected_topic == "每日挑戰":
            st.info(f"📅 **日期: {date.today()}** | 今天的題目已生成。")
            session_key = f"dyn_quiz_{date.today()}"
        else:
            st.info(f"📝 正在練習 **{selected_topic}**。")
            # Unique session ID for practice modes
            if 'practice_session_id' not in st.session_state:
                st.session_state.practice_session_id = random.randint(1, 10000)
            session_key = f"dyn_quiz_{selected_topic}_{st.session_state.practice_session_id}"
        
        # Load or Generate Questions
        if session_key not in st.session_state:
            st.session_state[session_key] = get_dynamic_questions(selected_topic)
            st.session_state.user_answers = {}
            st.session_state.submitted = False

        quiz_questions = st.session_state[session_key]

        with st.form("quiz_form"):
            user_answers = {}
            for idx, q in enumerate(quiz_questions):
                st.subheader(f"題目 {idx+1} ({q['topic']}) : {q['question']}")
                answer = st.radio("選擇答案:", q['options'], key=f"{session_key}_q_{q['id']}", index=None)
                user_answers[q['id']] = answer
                st.markdown("---")
                
            submitted = st.form_submit_button("提交答案")
            
            if submitted:
                st.session_state.user_answers = user_answers
                st.session_state.submitted = True

        if st.session_state.get('submitted'):
            score = 0
            total = len(quiz_questions)
            st.markdown("## 📊 成績單")
            
            for idx, q in enumerate(quiz_questions):
                user_ans = st.session_state.user_answers.get(q['id'])
                correct_ans = q['answer']
                if user_ans == correct_ans:
                    score += 1
                    st.success(f"**題目 {idx+1}: 答對了！**")
                else:
                    st.error(f"**題目 {idx+1}: 答錯了。**")
                    st.write(f"你的答案: {user_ans}")
                    st.write(f"正確答案: **{correct_ans}**")
                    st.info(f"💡 解釋: {q['explanation']}")
                st.markdown("---")
                
            percentage = (score / total) * 100
            st.metric(label="最終得分", value=f"{score}/{total}", delta=f"{percentage}%")
            
            # SAVE SCORE TO DATABASE
            # Check if we already saved this specific session to avoid duplicates on re-render
            save_key = f"saved_{session_key}"
            if save_key not in st.session_state:
                save_score_to_db(st.session_state.username, selected_topic, score, total)
                st.session_state[save_key] = True
                st.toast("成績已保存到記錄！", icon="💾")

            if st.button("重試 / 生成新題目"):
                del st.session_state[session_key]
                if selected_topic != "每日挑戰":
                    st.session_state.practice_session_id = random.randint(1, 10000)
                st.rerun()

    # --- HISTORY SECTION ---
    elif app_mode == "我的成績記錄":
        st.title("📜 我的成績記錄")
        
        df = get_user_history(st.session_state.username)
        
        if not df.empty:
            # Calculate stats
            avg_score = df['percentage'].mean()
            total_quizzes = len(df)
            
            col1, col2 = st.columns(2)
            col1.metric("總練習次數", total_quizzes)
            col2.metric("平均得分", f"{avg_score:.1f}%")
            
            st.subheader("詳細記錄")
            # Rename columns for better display
            df.columns = ["主題", "得分", "總分", "百分比", "日期時間"]
            st.dataframe(df, use_container_width=True)
            
            # Simple chart
            st.subheader("進步趨勢")
            st.line_chart(df, x="日期時間", y="百分比")
        else:
            st.info("暫無練習記錄。快去「開始練習」挑戰一下吧！")

if __name__ == "__main__":
    main()
