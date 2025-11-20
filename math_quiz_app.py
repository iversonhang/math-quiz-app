import streamlit as st
import random
from datetime import date

# --- CONFIGURATION ---
st.set_page_config(page_title="HK Primary 5 & 6 Math Hero", page_icon="🧮")

# --- QUESTION BANK ---
# Expanded database covering HK Education Bureau Key Stage 2 Math
# Topics: Algebra, Geometry (Shape & Space), Number (Percentages, Fractions), Data Handling
QUESTION_BANK = [
    # --- ALGEBRA ---
    {
        "id": 1,
        "topic": "Algebra",
        "question": "Which of the following is an equation?",
        "options": ["3x + 5", "y - 4 = 10", "5 + 7 = 12", "x > 6"],
        "answer": "y - 4 = 10",
        "explanation": "An equation must contain an unknown variable and an equals sign."
    },
    {
        "id": 2,
        "topic": "Algebra",
        "question": "Solve for a: 3a + 4 = 19",
        "options": ["5", "6", "7", "15"],
        "answer": "5",
        "explanation": "3a = 19 - 4 -> 3a = 15 -> a = 5."
    },
    {
        "id": 3,
        "topic": "Algebra",
        "question": "If y = 6, what is the value of 2y - 3?",
        "options": ["9", "10", "12", "15"],
        "answer": "9",
        "explanation": "2(6) - 3 = 12 - 3 = 9."
    },
    {
        "id": 4,
        "topic": "Algebra",
        "question": "Solve: m / 4 = 8",
        "options": ["2", "12", "32", "4"],
        "answer": "32",
        "explanation": "Multiply both sides by 4: m = 8 * 4 = 32."
    },
    {
        "id": 5,
        "topic": "Algebra",
        "question": "Which algebraic expression represents 'subtract 5 from y'?",
        "options": ["5 - y", "y - 5", "y / 5", "5y"],
        "answer": "y - 5",
        "explanation": "Subtracting 5 from y is written as y - 5."
    },

    # --- GEOMETRY ---
    {
        "id": 6,
        "topic": "Geometry",
        "question": "Calculate the area of a triangle with base 12 cm and height 5 cm.",
        "options": ["60 cm²", "30 cm²", "34 cm²", "17 cm²"],
        "answer": "30 cm²",
        "explanation": "Area = (Base × Height) / 2 = (12 × 5) / 2 = 30."
    },
    {
        "id": 7,
        "topic": "Geometry",
        "question": "Which 3D shape has 6 square faces, 12 edges, and 8 vertices?",
        "options": ["Cuboid", "Square-based pyramid", "Cube", "Triangular prism"],
        "answer": "Cube",
        "explanation": "A cube is the only shape listed with 6 identical square faces."
    },
    {
        "id": 8,
        "topic": "Geometry",
        "question": "If you face North and turn 135° clockwise, which direction do you face?",
        "options": ["East", "South-East", "South", "North-East"],
        "answer": "South-East",
        "explanation": "90° is East. 135° is 90° + 45°, which is South-East."
    },
    {
        "id": 9,
        "topic": "Geometry",
        "question": "What is the volume of a cube with side length 4 cm?",
        "options": ["16 cm³", "64 cm³", "12 cm³", "24 cm³"],
        "answer": "64 cm³",
        "explanation": "Volume = side × side × side = 4 × 4 × 4 = 64."
    },
    {
        "id": 10,
        "topic": "Geometry",
        "question": "The diameter of a circle is 10 cm. What is its radius?",
        "options": ["5 cm", "10 cm", "20 cm", "100 cm"],
        "answer": "5 cm",
        "explanation": "Radius is half of the diameter. 10 / 2 = 5."
    },

    # --- NUMBERS & PERCENTAGES ---
    {
        "id": 11,
        "topic": "Number",
        "question": "Convert 3/5 into a percentage.",
        "options": ["30%", "50%", "60%", "75%"],
        "answer": "60%",
        "explanation": "3/5 = 6/10 = 60%."
    },
    {
        "id": 12,
        "topic": "Number",
        "question": "Calculate: 2.4 × 0.5",
        "options": ["1.2", "12", "4.8", "0.12"],
        "answer": "1.2",
        "explanation": "Multiplying by 0.5 is the same as dividing by 2."
    },
    {
        "id": 13,
        "topic": "Number",
        "question": "What is 25% of 80?",
        "options": ["25", "20", "40", "10"],
        "answer": "20",
        "explanation": "25% is 1/4. 80 divided by 4 is 20."
    },
    {
        "id": 14,
        "topic": "Number",
        "question": "Find the H.C.F (Highest Common Factor) of 12 and 18.",
        "options": ["3", "6", "12", "36"],
        "answer": "6",
        "explanation": "Factors of 12: 1,2,3,4,6,12. Factors of 18: 1,2,3,6,9,18. HCF is 6."
    },
    {
        "id": 15,
        "topic": "Number",
        "question": "A tank has 4 Liters. 500 mL is used. How much is left?",
        "options": ["3.5 L", "4.5 L", "350 mL", "399.5 L"],
        "answer": "3.5 L",
        "explanation": "4 L = 4000 mL. 4000 - 500 = 3500 mL = 3.5 L."
    },

    # --- DATA HANDLING ---
    {
        "id": 16,
        "topic": "Data Handling",
        "question": "Find the average of: 18, 25, 32",
        "options": ["20", "25", "75", "30"],
        "answer": "25",
        "explanation": "(18 + 25 + 32) / 3 = 75 / 3 = 25."
    },
    {
        "id": 17,
        "topic": "Data Handling",
        "question": "In a pie chart, what is the sum of all angles at the center?",
        "options": ["90°", "180°", "360°", "100°"],
        "answer": "360°",
        "explanation": "A full circle is 360 degrees."
    },
    {
        "id": 18,
        "topic": "Data Handling",
        "question": "The average of 3 numbers is 20. What is their sum?",
        "options": ["23", "60", "17", "40"],
        "answer": "60",
        "explanation": "Sum = Average × Count. 20 × 3 = 60."
    },
    {
        "id": 19,
        "topic": "Data Handling",
        "question": "If a bar chart shows 10 units height for 'Apple' and 1 unit = 5 people, how many people chose Apple?",
        "options": ["10", "15", "50", "2"],
        "answer": "50",
        "explanation": "10 units × 5 people/unit = 50 people."
    },
    {
        "id": 20,
        "topic": "Number",
        "question": "What is the L.C.M (Lowest Common Multiple) of 4 and 6?",
        "options": ["24", "12", "2", "10"],
        "answer": "12",
        "explanation": "Multiples of 4: 4, 8, 12... Multiples of 6: 6, 12... LCM is 12."
    }
]

# --- HELPER FUNCTIONS ---

def get_questions(topic_filter="Daily Challenge"):
    """
    Returns 10 questions.
    - If 'Daily Challenge': Seeds random with today's date so it's consistent for the day.
    - If Topic: Randomly picks 10 from that topic.
    """
    questions = []
    
    if topic_filter == "Daily Challenge":
        # Seed with today's ordinal date (integer)
        # This ensures the questions are random, but the SAME set for the whole day.
        today_seed = date.today().toordinal()
        random.seed(today_seed)
        
        # Get a copy of all questions and shuffle them consistently based on the seed
        all_qs = QUESTION_BANK.copy()
        random.shuffle(all_qs)
        
        # Pick first 10
        questions = all_qs[:10]
        
    else:
        # Topic specific - Pure random (resets on refresh)
        # Filter by topic
        topic_qs = [q for q in QUESTION_BANK if q['topic'] == topic_filter]
        
        # If we have fewer than 10 questions for a topic, return all of them
        # Otherwise, sample 10
        if len(topic_qs) <= 10:
            questions = topic_qs
        else:
            questions = random.sample(topic_qs, 10)
            
    return questions

# --- MAIN APP ---

def main():
    # Sidebar for navigation
    st.sidebar.title("🧮 Math Options")
    
    # Topic Selector
    topics = ["Daily Challenge", "Algebra", "Geometry", "Number", "Data Handling"]
    selected_topic = st.sidebar.selectbox("Choose a Topic", topics)
    
    st.title(f"Hong Kong Primary 5 & 6 Math - {selected_topic}")
    
    if selected_topic == "Daily Challenge":
        st.info(f"📅 **Date: {date.today()}** | These questions refresh automatically tomorrow!")
    else:
        st.info(f"📝 Practicing **{selected_topic}**. Refresh the page to get a new set of random questions.")

    # Initialize session state for scoring if not exists
    if 'score' not in st.session_state:
        st.session_state.score = 0
    
    # Get questions based on selection
    # We cache the quiz questions in session state so they don't reshuffle when user clicks buttons
    session_key = f"quiz_data_{selected_topic}_{date.today()}" if selected_topic == "Daily Challenge" else f"quiz_data_{selected_topic}"
    
    if session_key not in st.session_state:
        st.session_state[session_key] = get_questions(selected_topic)
        # Reset answers when topic changes/refreshes
        st.session_state.user_answers = {}
        st.session_state.submitted = False

    quiz_questions = st.session_state[session_key]

    # Display Quiz Form
    with st.form("quiz_form"):
        user_answers = {}
        for idx, q in enumerate(quiz_questions):
            st.subheader(f"Q{idx+1}: {q['question']}")
            
            # Radio button for options
            # Use a unique key for each question
            answer = st.radio(
                "Select an answer:", 
                q['options'], 
                key=f"q_{q['id']}",
                index=None # No default selection
            )
            user_answers[q['id']] = answer
            st.markdown("---")
            
        submitted = st.form_submit_button("Submit Answers")
        
        if submitted:
            st.session_state.user_answers = user_answers
            st.session_state.submitted = True

    # --- RESULTS SECTION ---
    if st.session_state.get('submitted'):
        score = 0
        total = len(quiz_questions)
        
        st.markdown("## 📊 Results")
        
        for idx, q in enumerate(quiz_questions):
            user_ans = st.session_state.user_answers.get(q['id'])
            correct_ans = q['answer']
            
            if user_ans == correct_ans:
                score += 1
                st.success(f"**Q{idx+1}: Correct!**")
            else:
                st.error(f"**Q{idx+1}: Incorrect.**")
                st.write(f"Your answer: {user_ans}")
                st.write(f"Correct answer: **{correct_ans}**")
                st.info(f"💡 Explanation: {q['explanation']}")
            
            st.markdown("---")
            
        # Final Score Calculation
        percentage = (score / total) * 100
        if percentage >= 80:
            msg = "🌟 Amazing job! You are a Math Wizard!"
        elif percentage >= 50:
            msg = "👍 Good effort! Keep practicing!"
        else:
            msg = "💪 Don't give up! Review the explanations above."
            
        st.metric(label="Final Score", value=f"{score}/{total}", delta=f"{percentage}%")
        st.write(msg)

        if st.button("Retry / New Set"):
            # Clear specific session keys to force reload
            del st.session_state[session_key]
            st.rerun()

if __name__ == "__main__":
    main()