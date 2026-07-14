import streamlit as st
import json
import random
from datetime import datetime, timedelta
import hashlib
import requests

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="GlobalBridge AI",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    .stApp { background: #FDF6E9; font-family: 'Inter', sans-serif; max-width: 480px; margin: 0 auto; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .stDeployButton {display: none !important;}
    .stButton > button { background: #E85D2B !important; color: white !important; border: none !important;
        border-radius: 12px !important; padding: 14px 28px !important; font-size: 16px !important;
        font-weight: 500 !important; width: 100% !important; }
    .stButton > button:hover { background: #C44A1F !important; }
    .stButton > button[kind="secondary"] { background: white !important; color: #E85D2B !important;
        border: 2px solid #E85D2B !important; }
    .card { background: white; border: 1px solid #E8E0D4; border-radius: 16px; padding: 20px; margin-bottom: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06); }
    .tag { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; margin-right: 8px; }
    .tag-primary { background: rgba(232,93,43,0.12); color: #E85D2B; }
    .tag-green { background: rgba(27,107,79,0.12); color: #1B6B4F; }
    .tag-teal { background: rgba(38,70,83,0.12); color: #264653; }
    .tag-gold { background: rgba(233,196,106,0.2); color: #B8860B; }
    .tag-purple { background: rgba(138,43,226,0.12); color: #8A2BE2; }
    .progress-track { height: 8px; background: #E8E0D4; border-radius: 4px; overflow: hidden; }
    .progress-fill { height: 100%; background: #E85D2B; border-radius: 4px; transition: width 0.6s; }
    .progress-fill.green { background: #1B6B4F; }
    .explanation-box { padding: 12px 16px; border-radius: 12px; margin-top: 12px; font-size: 14px;
        background: rgba(27,107,79,0.08); color: #1B6B4F; line-height: 1.5; }
    .sw-card { background: white; border: 1px solid #E8E0D4; border-radius: 16px; padding: 16px; margin-bottom: 10px; }
    .opp-highlight { background: #E85D2B; border-radius: 16px; padding: 20px; color: white; margin-bottom: 16px; }
    .profile-header { text-align: center; padding: 24px 0; }
    .profile-avatar { width: 80px; height: 80px; border-radius: 50%;
        background: linear-gradient(135deg, #E85D2B 0%, #F4A261 100%); margin: 0 auto 12px;
        display: flex; align-items: center; justify-content: center; color: white; font-size: 32px; font-weight: 700; }
    .achievement-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
    .achievement-card { background: white; border: 1px solid #E8E0D4; border-radius: 16px; padding: 16px; text-align: center; }
    .difficulty-basic { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600;
        text-transform: uppercase; background: rgba(27,107,79,0.1); color: #1B6B4F; }
    .difficulty-intermediate { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600;
        text-transform: uppercase; background: rgba(233,196,106,0.2); color: #B8860B; }
    .difficulty-advanced { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600;
        text-transform: uppercase; background: rgba(232,93,43,0.1); color: #E85D2B; }
    .timeline { position: relative; padding-left: 40px; }
    .timeline::before { content: ''; position: absolute; left: 15px; top: 0; bottom: 0; width: 3px; background: #E8E0D4; }
    .timeline-step { position: relative; margin-bottom: 16px; }
    .timeline-dot { position: absolute; left: -33px; width: 24px; height: 24px; border-radius: 50%; background: #999;
        border: 3px solid #FDF6E9; display: flex; align-items: center; justify-content: center;
        font-size: 12px; color: white; font-weight: 700; z-index: 2; }
    .timeline-dot.completed { background: #1B6B4F; }
    .timeline-dot.current { background: #E85D2B; box-shadow: 0 0 0 4px rgba(232,93,43,0.2); }
    .stTextInput > div > div > input { border-radius: 12px !important; border: 1px solid #E8E0D4 !important;
        padding: 12px 16px !important; font-size: 15px !important; }
    .stTextInput > div > div > input:focus { border-color: #E85D2B !important;
        box-shadow: 0 0 0 2px rgba(232,93,43,0.1) !important; }
    div[data-testid="stForm"] { border: none !important; padding: 0 !important; }
    .lesson-content h2 { font-size: 20px; font-weight: 700; margin: 20px 0 12px; color: #1a1a1a; }
    .lesson-content h3 { font-size: 17px; font-weight: 600; margin: 20px 0 10px; color: #1a1a1a; }
    .lesson-content p { font-size: 15px; line-height: 1.7; color: #666; margin-bottom: 16px; }
    .lesson-content ul { margin-left: 20px; margin-bottom: 16px; }
    .lesson-content li { font-size: 15px; line-height: 1.7; color: #666; margin-bottom: 8px; }
    .lesson-content strong { color: #1a1a1a; }
    .example-box { background: #F5F0E8; border: 1px solid #E8E0D4; border-radius: 12px; padding: 16px; margin: 16px 0; }
    .example-box .label { font-size: 12px; font-weight: 600; color: #E85D2B; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; }
    .example-box pre { background: transparent; padding: 0; margin: 0; font-family: 'SF Mono', Monaco, monospace; font-size: 13px; color: #1a1a1a; }
    .lesson-content table { width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 14px; }
    .lesson-content th { background: #F5F0E8; padding: 10px; border: 1px solid #E8E0D4; text-align: left; font-weight: 600; }
    .lesson-content td { padding: 10px; border: 1px solid #E8E0D4; }
    .lesson-content code { background: rgba(0,0,0,0.05); padding: 2px 6px; border-radius: 4px; font-family: 'SF Mono', Monaco, monospace; font-size: 13px; }
</style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE INIT ====================
def init_session():
    defaults = {
        'screen': 'auth',
        'user': None,
        'is_guest': False,
        'current_question': 0,
        'answers': [],
        'assessment_results': None,
        'chat_history': [{'role': 'bot', 'text': "Hey there! 👋 I am GlobalBridge, your AI study buddy. I can help with WAEC, JAMB, coding, career advice, or any subject. What are we learning today?"}],
        'course_progress': {},
        'bookmarks': set(),
        'current_course': None,
        'current_lesson': 0,
        'filter_category': 'all',
        'opp_filter': 'all',
        'search_query': '',
        'show_explanation': False,
        'selected_option': None,
        'notifications_enabled': False,
        'reminder_time': '08:00',
        'daily_goal_completed': 1,
        'streak': 7,
        'points': 1240,
        'users': {},
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session()

# ==================== DATA ====================
DIAGNOSTIC_QUESTIONS = [
    {"id": 1, "subject": "Mathematics", "difficulty": "basic", "question": "What is the value of x in: 2x + 6 = 14?", "options": ["x = 3", "x = 4", "x = 5", "x = 7"], "correct": 1, "explanation": "Subtract 6: 2x = 8. Divide by 2: x = 4."},
    {"id": 2, "subject": "Mathematics", "difficulty": "basic", "question": "Simplify: 3/4 + 1/2", "options": ["4/6", "5/4", "1", "1/4"], "correct": 1, "explanation": "Convert 1/2 to 2/4. Then 3/4 + 2/4 = 5/4 = 1.25"},
    {"id": 3, "subject": "Mathematics", "difficulty": "intermediate", "question": "Factor: x² - 5x + 6", "options": ["(x-2)(x-3)", "(x+2)(x+3)", "(x-1)(x-6)", "(x+1)(x-6)"], "correct": 0, "explanation": "Need numbers that multiply to 6 and add to -5: -2 and -3."},
    {"id": 4, "subject": "Mathematics", "difficulty": "intermediate", "question": "In a right triangle, if a = 3 and b = 4, find c.", "options": ["5", "6", "7", "25"], "correct": 0, "explanation": "Pythagorean theorem: c² = 3² + 4² = 9 + 16 = 25. c = 5."},
    {"id": 5, "subject": "Mathematics", "difficulty": "advanced", "question": "If log₂(x) = 5, what is x?", "options": ["10", "25", "32", "64"], "correct": 2, "explanation": "log₂(x) = 5 means 2⁵ = x. 2⁵ = 32."},
    {"id": 6, "subject": "Physics", "difficulty": "basic", "question": "What is the SI unit of force?", "options": ["Watt", "Joule", "Newton", "Pascal"], "correct": 2, "explanation": "The Newton (N) is the SI unit of force."},
    {"id": 7, "subject": "Physics", "difficulty": "basic", "question": "Which of these is a scalar quantity?", "options": ["Velocity", "Force", "Speed", "Acceleration"], "correct": 2, "explanation": "Speed has magnitude only. Velocity, force, and acceleration are vectors."},
    {"id": 8, "subject": "Physics", "difficulty": "intermediate", "question": "A car accelerates from rest at 2 m/s² for 5s. Final velocity?", "options": ["5 m/s", "10 m/s", "12 m/s", "25 m/s"], "correct": 1, "explanation": "v = u + at = 0 + (2 × 5) = 10 m/s."},
    {"id": 9, "subject": "Physics", "difficulty": "intermediate", "question": "What is the resistance of a 240V, 60W bulb?", "options": ["4 ohms", "960 ohms", "14400 ohms", "240 ohms"], "correct": 1, "explanation": "P = V²/R → R = V²/P = 240²/60 = 57600/60 = 960 ohms."},
    {"id": 10, "subject": "Physics", "difficulty": "advanced", "question": "A 2kg mass moving at 3 m/s collides with a stationary 1kg mass. If they stick together, what is their final velocity?", "options": ["1 m/s", "2 m/s", "3 m/s", "6 m/s"], "correct": 1, "explanation": "Conservation of momentum: (2×3) + (1×0) = (2+1)v → 6 = 3v → v = 2 m/s."},
    {"id": 11, "subject": "Chemistry", "difficulty": "basic", "question": "What is the chemical formula for water?", "options": ["HO", "H₂O", "H₂O₂", "OH"], "correct": 1, "explanation": "Water is H₂O — two hydrogen atoms and one oxygen atom."},
    {"id": 12, "subject": "Chemistry", "difficulty": "intermediate", "question": "How many moles are in 36g of water (H=1, O=16)?", "options": ["1", "2", "3", "4"], "correct": 1, "explanation": "Molar mass of H₂O = 2(1) + 16 = 18 g/mol. Moles = 36/18 = 2."},
    {"id": 13, "subject": "Chemistry", "difficulty": "advanced", "question": "In the reaction 2H₂ + O₂ → 2H₂O, what is the limiting reagent if you have 4 moles of H₂ and 3 moles of O₂?", "options": ["H₂", "O₂", "Neither", "Both"], "correct": 0, "explanation": "4 moles H₂ needs 2 moles O₂. You have 3 moles O₂ (excess). H₂ runs out first."},
    {"id": 14, "subject": "Biology", "difficulty": "basic", "question": "What is the powerhouse of the cell?", "options": ["Nucleus", "Ribosome", "Mitochondria", "Chloroplast"], "correct": 2, "explanation": "Mitochondria produce ATP through cellular respiration."},
    {"id": 15, "subject": "Biology", "difficulty": "intermediate", "question": "During photosynthesis, what gas is released as a byproduct?", "options": ["CO₂", "O₂", "N₂", "H₂"], "correct": 1, "explanation": "Plants release oxygen (O₂) as a byproduct of photosynthesis."},
    {"id": 16, "subject": "Biology", "difficulty": "advanced", "question": "In Mendelian genetics, if a heterozygous tall plant (Tt) is crossed with a homozygous short plant (tt), what percentage of offspring will be tall?", "options": ["0%", "25%", "50%", "75%"], "correct": 2, "explanation": "Tt × tt produces Tt, Tt, tt, tt. 50% tall (Tt), 50% short (tt)."},
    {"id": 17, "subject": "English", "difficulty": "basic", "question": "Choose the correct sentence:", "options": ["She do not like apples.", "She does not likes apples.", "She does not like apples.", "She not like apples."], "correct": 2, "explanation": "Third person singular uses 'does not' + base verb."},
    {"id": 18, "subject": "English", "difficulty": "intermediate", "question": "Identify the literary device: 'The wind whispered through the trees.'", "options": ["Simile", "Metaphor", "Personification", "Hyperbole"], "correct": 2, "explanation": "Personification gives human qualities (whispering) to non-human things."},
    {"id": 19, "subject": "Economics", "difficulty": "basic", "question": "What happens to demand when price increases (ceteris paribus)?", "options": ["Demand increases", "Demand decreases", "No change", "Supply increases"], "correct": 1, "explanation": "Law of demand: as price rises, quantity demanded falls."},
    {"id": 20, "subject": "Economics", "difficulty": "intermediate", "question": "If GDP is $500 billion and population is 50 million, what is GDP per capita?", "options": ["$100", "$1,000", "$10,000", "$100,000"], "correct": 2, "explanation": "GDP per capita = GDP / Population = $500,000,000,000 / 50,000,000 = $10,000."},
]

COURSES = [
    {"id": "math-waec", "name": "WAEC Mathematics Mastery", "subject": "Mathematics", "category": "progress africa", "lessons": 42, "hours": 18, "progress": 68, "completed": 29, "level": "Senior Secondary", "color": "primary"},
    {"id": "physics-jamb", "name": "JAMB Physics Prep", "subject": "Physics", "category": "progress africa", "lessons": 36, "hours": 12, "progress": 42, "completed": 15, "level": "Senior Secondary", "color": "green"},
    {"id": "english-waec", "name": "WAEC English Language", "subject": "English", "category": "africa", "lessons": 50, "hours": 24, "progress": 0, "completed": 0, "level": "Senior Secondary", "color": "teal"},
    {"id": "python-begin", "name": "Python for Beginners", "subject": "Coding", "category": "international coding", "lessons": 45, "hours": 30, "progress": 0, "completed": 0, "level": "All levels", "color": "teal"},
    {"id": "sat-prep", "name": "SAT Preparation Course", "subject": "Career", "category": "international", "lessons": 20, "hours": 8, "progress": 0, "completed": 0, "level": "International", "color": "gold"},
    {"id": "biology-waec", "name": "WAEC Biology", "subject": "Biology", "category": "africa", "lessons": 38, "hours": 16, "progress": 0, "completed": 0, "level": "Senior Secondary", "color": "green"},
    {"id": "chem-jamb", "name": "JAMB Chemistry", "subject": "Chemistry", "category": "africa", "lessons": 40, "hours": 18, "progress": 0, "completed": 0, "level": "Senior Secondary", "color": "primary"},
    {"id": "web-dev", "name": "Web Development Fundamentals", "subject": "Coding", "category": "international coding", "lessons": 30, "hours": 22, "progress": 0, "completed": 0, "level": "All levels", "color": "teal"},
    {"id": "econ-waec", "name": "WAEC Economics", "subject": "Economics", "category": "africa", "lessons": 35, "hours": 15, "progress": 0, "completed": 0, "level": "Senior Secondary", "color": "gold"},
    {"id": "gov-waec", "name": "WAEC Government", "subject": "Government", "category": "africa", "lessons": 32, "hours": 14, "progress": 0, "completed": 0, "level": "Senior Secondary", "color": "purple"},
]

OPPORTUNITIES = [
    {"id": 1, "name": "MTN Foundation Scholarship", "type": "scholarship", "org": "MTN", "location": "Nigeria", "deadline": "Aug 30", "desc": "Full scholarship for STEM students in Nigerian universities."},
    {"id": 2, "name": "ALX Africa Software Engineering", "type": "program", "org": "ALX", "location": "Remote", "deadline": "Rolling", "desc": "12-month fully-funded software engineering program."},
    {"id": 3, "name": "Mastercard Foundation Scholars", "type": "scholarship", "org": "Mastercard", "location": "Multiple", "deadline": "Oct 15", "desc": "Full scholarships at partner universities across Africa."},
    {"id": 4, "name": "Google Africa Developer Scholarship", "type": "program", "org": "Google", "location": "Online", "deadline": "Open now", "desc": "Free access to Pluralsight courses and Google certification."},
    {"id": 5, "name": "UN Youth Volunteer Program", "type": "internship", "org": "UN", "location": "Global", "deadline": "Sep 1", "desc": "Volunteer opportunities with UN agencies worldwide."},
    {"id": 6, "name": "Andela Learning Community", "type": "program", "org": "Andela", "location": "Africa", "deadline": "Rolling", "desc": "Community-driven tech learning with mentorship."},
    {"id": 7, "name": "Chevening Scholarship", "type": "scholarship", "org": "UK Gov", "location": "UK", "deadline": "Nov 1", "desc": "Full UK Masters scholarship for future leaders."},
    {"id": 8, "name": "Flutterwave Internship", "type": "internship", "org": "Flutterwave", "location": "Lagos/Remote", "deadline": "Aug 15", "desc": "Paid internship in fintech engineering and product."},
]

TUTOR_RESPONSES = {
    "explain photosynthesis": "Photosynthesis is how plants make their food! 🌱\n\n**The process:**\n1. Plants absorb sunlight through chlorophyll\n2. They take in CO₂ from the air and water from roots\n3. Using light energy, they convert these into **glucose** and **oxygen**\n\n**Equation:** 6CO₂ + 6H₂O + light → C₆H₁₂O₆ + 6O₂\n\nThink of leaves as tiny solar panels!",
    "solve x squared plus 5x plus 6": "Let us solve step by step! 🧮\n\n**Step 1:** Factor the quadratic\nNeed two numbers that multiply to 6 and add to 5: **2 and 3**\n\n**Step 2:** Write the factors\n(x + 2)(x + 3) = 0\n\n**Step 3:** Solve each factor\nx + 2 = 0 → **x = -2**\nx + 3 = 0 → **x = -3**\n\n**Answer: x = -2 or x = -3**",
    "jamb study plan": "Here is your 12-week JAMB mastery plan! 📚\n\n**Weeks 1-4: Foundation**\n• Review all topics in your 4 subjects\n• 2 hours daily, focus on weak areas\n• Complete 1 past paper per week\n\n**Weeks 5-8: Practice**\n• Past questions (10 years minimum)\n• Timed practice tests (3 hours, exam conditions)\n• Note recurring question patterns\n\n**Weeks 9-10: Intense Revision**\n• Mock exams under real conditions\n• Review ALL mistakes in an error notebook\n• Focus on speed and accuracy\n\n**Weeks 11-12: Final Prep**\n• Light revision only — no new topics!\n• Rest, sleep well, build confidence\n• Exam strategy: attempt easy questions first",
    "python for-loop": "A for loop in Python lets you repeat code for each item! 🐍\n\n**Example 1: Print each fruit**\n```python\nfruits = ['apple', 'banana', 'cherry']\nfor fruit in fruits:\n    print(fruit)\n```\n\n**Example 2: Using range()**\n```python\nfor i in range(5):\n    print(i)  # Prints 0, 1, 2, 3, 4\n```\n\n**Key idea:** The loop variable takes each value one at a time.",
}

CURRICULUM = {
    "math-waec": {
        "title": "Number Systems & Surds",
        "subtitle": "WAEC Mathematics Mastery · Lesson 1 of 42",
        "content": """
        <h2>1. Number Systems</h2>
        <p>In WAEC Mathematics, you need to master different number types. <strong>Natural numbers</strong> are counting numbers (1, 2, 3...). <strong>Integers</strong> include negatives (...-2, -1, 0, 1, 2...). <strong>Rational numbers</strong> can be expressed as fractions p/q where q ≠ 0.</p>
        <div class="example-box">
            <div class="label">WAEC Past Question (2019)</div>
            <p><strong>Express 0.75 as a fraction in its lowest terms.</strong></p>
            <p>Solution: 0.75 = 75/100 = <strong>3/4</strong></p>
        </div>
        <h2>2. Surds</h2>
        <p>A <strong>surd</strong> is an irrational number expressed as a root. Common WAEC surd rules:</p>
        <ul>
            <li>√a × √b = √(ab)</li>
            <li>√a / √b = √(a/b)</li>
            <li>√(a²) = |a|</li>
            <li>To rationalize 1/√a, multiply by √a/√a</li>
        </ul>
        <div class="example-box">
            <div class="label">Worked Example</div>
            <p><strong>Simplify: √50 + √18 - √8</strong></p>
            <p>√50 = √(25×2) = 5√2<br>√18 = √(9×2) = 3√2<br>√8 = √(4×2) = 2√2<br><strong>Answer: 5√2 + 3√2 - 2√2 = 6√2</strong></p>
        </div>
        <h2>3. JAMB Tip</h2>
        <p>JAMB often tests surd rationalization in word problems. Always look for perfect square factors first!</p>
        """
    },
    "physics-jamb": {
        "title": "Kinematics — Motion in a Straight Line",
        "subtitle": "JAMB Physics Prep · Lesson 1 of 36",
        "content": """
        <h2>1. Definitions</h2>
        <p><strong>Displacement</strong> is distance in a specified direction (vector). <strong>Distance</strong> is the total path length (scalar). <strong>Velocity</strong> is rate of change of displacement. <strong>Acceleration</strong> is rate of change of velocity.</p>
        <h2>2. Equations of Motion (JAMB Essential)</h2>
        <p>For uniform acceleration, these five equations are tested every year:</p>
        <ul>
            <li><strong>v = u + at</strong> — velocity after time t</li>
            <li><strong>s = ut + ½at²</strong> — displacement</li>
            <li><strong>v² = u² + 2as</strong> — velocity without time</li>
            <li><strong>s = ½(u + v)t</strong> — average velocity</li>
            <li><strong>s = vt - ½at²</strong> — displacement from final velocity</li>
        </ul>
        <div class="example-box">
            <div class="label">JAMB Past Question (2022)</div>
            <p><strong>A car starts from rest and accelerates uniformly at 2 m/s² for 10 seconds. Calculate the distance traveled.</strong></p>
            <p>Given: u = 0, a = 2 m/s², t = 10s<br>Using s = ut + ½at²<br>s = 0 + ½(2)(10)² = 100 meters<br><strong>Answer: 100 m</strong></p>
        </div>
        <h2>3. Graphs of Motion</h2>
        <p>JAMB loves graph questions. Remember: <strong>the gradient of a displacement-time graph = velocity</strong>, and <strong>the gradient of a velocity-time graph = acceleration</strong>. The area under a velocity-time graph gives displacement.</p>
        """
    },
    "english-waec": {
        "title": "Comprehension & Summary Writing",
        "subtitle": "WAEC English Language · Lesson 1 of 50",
        "content": """
        <h2>1. Comprehension Strategy</h2>
        <p>WAEC comprehension passages test your ability to understand, interpret, and evaluate written text. Follow this proven approach:</p>
        <ul>
            <li><strong>Skim first:</strong> Read the passage quickly to get the main idea</li>
            <li><strong>Read questions:</strong> Know what you are looking for before detailed reading</li>
            <li><strong>Scan for answers:</strong> Go back to the text with specific questions in mind</li>
            <li><strong>Check context:</strong> Ensure your answer fits the surrounding text</li>
        </ul>
        <h2>2. Types of Comprehension Questions</h2>
        <ul>
            <li><strong>Literal:</strong> Direct facts from the text ("What time did...?")</li>
            <li><strong>Inferential:</strong> Reading between the lines ("What does the writer imply...?")</li>
            <li><strong>Evaluative:</strong> Judging the text ("Do you agree that...?")</li>
            <li><strong>Vocabulary:</strong> Word meaning in context</li>
        </ul>
        <div class="example-box">
            <div class="label">Practice Question</div>
            <p><strong>Passage:</strong> "The politician's speech was full of sound and fury, signifying nothing."</p>
            <p><strong>Question:</strong> What does the writer suggest about the politician's speech?</p>
            <p><strong>Answer:</strong> The speech was loud and impressive-sounding but lacked real substance or meaning. (Allusion to Shakespeare's Macbeth)</p>
        </div>
        <h2>3. Summary Writing (WAEC Section B)</h2>
        <p>You must summarize a passage in a specified number of words (usually 60-80). Key rules:</p>
        <ul>
            <li>Use your own words — do NOT copy phrases</li>
            <li>Include ONLY the main points (usually 5-6 points)</li>
            <li>Write in continuous prose, not bullet points</li>
            <li>Stay within the word limit (penalties apply)</li>
        </ul>
        """
    },
    "biology-waec": {
        "title": "Cell Structure & Function",
        "subtitle": "WAEC Biology · Lesson 1 of 38",
        "content": """
        <h2>1. The Cell Theory</h2>
        <p>All living organisms are made of cells. The cell is the basic unit of life. All cells come from pre-existing cells. This is the foundation of WAEC Biology.</p>
        <h2>2. Plant vs Animal Cells (WAEC Favorite)</h2>
        <table>
            <tr><th>Feature</th><th>Plant Cell</th><th>Animal Cell</th></tr>
            <tr><td>Cell wall</td><td>Present (cellulose)</td><td>Absent</td></tr>
            <tr><td>Chloroplasts</td><td>Present</td><td>Absent</td></tr>
            <tr><td>Vacuole</td><td>Large, central</td><td>Small, temporary</td></tr>
            <tr><td>Shape</td><td>Fixed, rectangular</td><td>Irregular, round</td></tr>
        </table>
        <h2>3. Cell Organelles</h2>
        <ul>
            <li><strong>Nucleus:</strong> Controls cell activities, contains DNA</li>
            <li><strong>Mitochondria:</strong> Site of respiration, produces ATP</li>
            <li><strong>Ribosomes:</strong> Protein synthesis</li>
            <li><strong>Golgi body:</strong> Packaging and secretion of proteins</li>
            <li><strong>Endoplasmic reticulum:</strong> Transport network</li>
        </ul>
        <div class="example-box">
            <div class="label">WAEC Past Question (2021)</div>
            <p><strong>State two differences between a plant cell and an animal cell.</strong></p>
            <p>1. Plant cells have a cellulose cell wall; animal cells do not.<br>2. Plant cells have chloroplasts for photosynthesis; animal cells do not.</p>
        </div>
        """
    },
    "chem-jamb": {
        "title": "Atomic Structure & the Periodic Table",
        "subtitle": "JAMB Chemistry · Lesson 1 of 40",
        "content": """
        <h2>1. Atomic Structure</h2>
        <p>An atom consists of <strong>protons</strong> (positive, in nucleus), <strong>neurons</strong> (neutral, in nucleus), and <strong>electrons</strong> (negative, orbiting nucleus). The atomic number = number of protons. Mass number = protons + neutrons.</p>
        <h2>2. Electronic Configuration</h2>
        <p>JAMB tests this heavily. Electrons fill shells in order: 2, 8, 8, 18...</p>
        <div class="example-box">
            <div class="label">Worked Examples</div>
            <p><strong>Chlorine (atomic number 17):</strong> 2, 8, 7</p>
            <p><strong>Calcium (atomic number 20):</strong> 2, 8, 8, 2</p>
            <p><strong>Iron (atomic number 26):</strong> 2, 8, 14, 2</p>
        </div>
        <h2>3. Periodic Trends</h2>
        <ul>
            <li><strong>Across a period (left to right):</strong> Atomic radius decreases, electronegativity increases, metallic character decreases</li>
            <li><strong>Down a group:</strong> Atomic radius increases, electronegativity decreases, metallic character increases</li>
        </ul>
        <h2>4. Types of Bonds</h2>
        <ul>
            <li><strong>Ionic:</strong> Transfer of electrons (metal + non-metal), e.g., NaCl</li>
            <li><strong>Covalent:</strong> Sharing of electrons (non-metal + non-metal), e.g., H₂O</li>
            <li><strong>Metallic:</strong> Sea of delocalized electrons in metals</li>
            <li><strong>Dative:</strong> One atom donates both electrons, e.g., NH₄⁺</li>
        </ul>
        """
    },
    "python-begin": {
        "title": "Introduction to Python",
        "subtitle": "Python for Beginners · Lesson 1 of 45",
        "content": """
        <h2>1. What is Python?</h2>
        <p>Python is a high-level, interpreted programming language known for its readability. It is used in web development, data science, AI, automation, and more. Major companies using Python include Google, Netflix, and Instagram.</p>
        <h2>2. Your First Program</h2>
        <p>Every programmer starts with "Hello, World!"</p>
        <div class="example-box">
            <div class="label">Code</div>
            <pre>print("Hello, World!")</pre>
            <div class="label" style="margin-top:12px;">Output</div>
            <p>Hello, World!</p>
        </div>
        <h2>3. Variables and Data Types</h2>
        <ul>
            <li><strong>int:</strong> Whole numbers — age = 17</li>
            <li><strong>float:</strong> Decimal numbers — height = 1.75</li>
            <li><strong>str:</strong> Text — name = "Amara"</li>
            <li><strong>bool:</strong> True/False — passed = True</li>
            <li><strong>list:</strong> Ordered collection — scores = [85, 90, 78]</li>
        </ul>
        <h2>4. Basic Operators</h2>
        <table>
            <tr><th>Operator</th><th>Meaning</th><th>Example</th></tr>
            <tr><td>+</td><td>Addition</td><td>5 + 3 = 8</td></tr>
            <tr><td>-</td><td>Subtraction</td><td>5 - 3 = 2</td></tr>
            <tr><td>*</td><td>Multiplication</td><td>5 * 3 = 15</td></tr>
            <tr><td>/</td><td>Division</td><td>5 / 2 = 2.5</td></tr>
            <tr><td>//</td><td>Floor division</td><td>5 // 2 = 2</td></tr>
            <tr><td>%</td><td>Modulo</td><td>5 % 2 = 1</td></tr>
            <tr><td>**</td><td>Exponent</td><td>2 ** 3 = 8</td></tr>
        </table>
        """
    },
    "econ-waec": {
        "title": "Introduction to Economics",
        "subtitle": "WAEC Economics · Lesson 1 of 35",
        "content": """
        <h2>1. Definition of Economics</h2>
        <p>Economics is the social science that studies how individuals, businesses, governments, and societies make choices about allocating limited resources to satisfy unlimited wants. <strong>Scarcity</strong> is the fundamental economic problem.</p>
        <h2>2. Branches of Economics</h2>
        <ul>
            <li><strong>Microeconomics:</strong> Studies individual units — consumers, firms, markets</li>
            <li><strong>Macroeconomics:</strong> Studies the economy as a whole — GDP, inflation, unemployment</li>
        </ul>
        <h2>3. Basic Economic Concepts</h2>
        <ul>
            <li><strong>Wants:</strong> Desires that can be satisfied by consuming goods/services</li>
            <li><strong>Needs:</strong> Essential requirements for survival (food, shelter, clothing)</li>
            <li><strong>Scarcity:</strong> Limited resources vs unlimited wants</li>
            <li><strong>Choice:</strong> Selecting the best alternative given scarcity</li>
            <li><strong>Opportunity Cost:</strong> The next best alternative foregone</li>
        </ul>
        <div class="example-box">
            <div class="label">Worked Example</div>
            <p><strong>A student has ₦5000 and must choose between buying a textbook (₦3000) or attending a tutorial (₦4000). What is the opportunity cost of choosing the tutorial?</strong></p>
            <p>The opportunity cost is the textbook — it is the next best alternative that was given up.</p>
        </div>
        <h2>4. Factors of Production (WAEC Essential)</h2>
        <table>
            <tr><th>Factor</th><th>Reward</th><th>Example</th></tr>
            <tr><td>Land</td><td>Rent</td><td>Farmland, oil reserves</td></tr>
            <tr><td>Labour</td><td>Wages/Salary</td><td>Teachers, doctors</td></tr>
            <tr><td>Capital</td><td>Interest</td><td>Machinery, computers</td></tr>
            <tr><td>Entrepreneur</td><td>Profit</td><td>Business owner</td></tr>
        </table>
        """
    },
}

# ==================== HELPER FUNCTIONS ====================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_initials(name):
    parts = name.split()
    return ''.join(p[0] for p in parts[:2]).upper()

def navigate_to(screen):
    st.session_state.screen = screen
    st.rerun()

def get_user_name():
    if st.session_state.user:
        return st.session_state.user.get('name', 'User')
    return 'Guest'

def get_user_initials():
    if st.session_state.user:
        return st.session_state.user.get('initials', 'GU')
    return 'GU'

def get_user_level():
    if st.session_state.user:
        return st.session_state.user.get('level', 'Senior Secondary')
    return 'Senior Secondary'

def get_user_location():
    if st.session_state.user:
        return st.session_state.user.get('location', 'Nigeria')
    return 'Nigeria'

# ==================== SCREEN: AUTH ====================
def render_auth():
    st.markdown("""
    <div style="text-align:center; padding: 40px 0 20px;">
        <div style="display:flex; align-items:center; justify-content:center; gap:10px; margin-bottom:24px;">
            <div style="width:40px; height:40px; background:#E85D2B; border-radius:50%; display:flex; align-items:center; justify-content:center; color:white; font-size:20px;">🎓</div>
            <div style="font-size:22px; font-weight:700; color:#1a1a1a;">GlobalBridge AI</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Sign In", "Sign Up"])
    
    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="you@example.com")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submitted = st.form_submit_button("Sign In", use_container_width=True)
            
            if submitted:
                if email and password:
                    users = st.session_state.get('users', {})
                    if email in users and users[email]['password'] == hash_password(password):
                        st.session_state.user = users[email]
                        st.session_state.is_guest = False
                        st.success(f"Welcome back, {users[email]['name']}!")
                        navigate_to('onboarding')
                    else:
                        # Demo: create user on first login
                        name = email.split('@')[0].replace('.', ' ').replace('_', ' ').title()
                        user = {
                            'email': email,
                            'name': name,
                            'initials': name[:2].upper() if len(name) >= 2 else 'GU',
                            'location': 'Nigeria',
                            'level': 'Senior Secondary',
                            'password': hash_password(password),
                            'is_guest': False
                        }
                        users[email] = user
                        st.session_state.users = users
                        st.session_state.user = user
                        st.session_state.is_guest = False
                        st.success(f"Welcome, {name}!")
                        navigate_to('onboarding')
                else:
                    st.error("Please enter email and password")
    
    with tab2:
        with st.form("signup_form"):
            name = st.text_input("Full Name", placeholder="Your full name")
            email = st.text_input("Email", placeholder="you@example.com", key="signup_email")
            password = st.text_input("Password", type="password", placeholder="Create a password (min 6 chars)", key="signup_password")
            level = st.text_input("Education Level", placeholder="e.g. Senior Secondary")
            location = st.text_input("Location", placeholder="e.g. Lagos, Nigeria")
            submitted = st.form_submit_button("Create Account", use_container_width=True)
            
            if submitted:
                if not name or not email or not password:
                    st.error("Please fill in all required fields")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters")
                else:
                    user = {
                        'email': email,
                        'name': name,
                        'initials': get_initials(name),
                        'location': location or 'Nigeria',
                        'level': level or 'Senior Secondary',
                        'password': hash_password(password),
                        'is_guest': False
                    }
                    users = st.session_state.get('users', {})
                    users[email] = user
                    st.session_state.users = users
                    st.session_state.user = user
                    st.session_state.is_guest = False
                    st.success(f"Welcome, {name}!")
                    navigate_to('onboarding')
    
    if st.button("Continue as Guest", type="secondary", use_container_width=True):
        st.session_state.user = None
        st.session_state.is_guest = True
        st.info("Continuing as guest. Sign up later to save progress!")
        navigate_to('onboarding')

# ==================== SCREEN: ONBOARDING ====================
def render_onboarding():
    st.markdown("""
    <div style="text-align:center; padding: 20px;">
        <div style="display:flex; align-items:center; justify-content:center; gap:10px; margin-bottom:16px;">
            <div style="width:40px; height:40px; background:#E85D2B; border-radius:50%; display:flex; align-items:center; justify-content:center; color:white; font-size:20px;">🎓</div>
            <div style="font-size:22px; font-weight:700; color:#1a1a1a;">GlobalBridge AI</div>
        </div>
        <svg viewBox="0 0 400 200" style="width:100%; max-width:360px; margin:16px 0;">
            <rect width="400" height="200" rx="16" fill="#FDF6E9"/>
            <ellipse cx="200" cy="180" rx="140" ry="15" fill="#E8D5B5" opacity="0.4"/>
            <rect x="100" y="120" width="200" height="40" rx="6" fill="#C4956A"/>
            <rect x="110" y="110" width="180" height="10" rx="3" fill="#A67B5B"/>
            <circle cx="150" cy="80" r="25" fill="#D4A574"/><rect x="135" y="100" width="30" height="30" rx="4" fill="#E85D2B"/>
            <circle cx="250" cy="75" r="22" fill="#C4956A"/><rect x="238" y="93" width="24" height="28" rx="4" fill="#2A9D8F"/>
            <circle cx="200" cy="70" r="24" fill="#E9C46A"/><rect x="185" y="90" width="30" height="28" rx="4" fill="#1B6B4F"/>
            <rect x="120" y="155" width="20" height="12" rx="2" fill="#1B6B4F" opacity="0.5"/>
            <rect x="150" y="158" width="16" height="10" rx="2" fill="#E85D2B" opacity="0.5"/>
            <rect x="240" y="156" width="18" height="12" rx="2" fill="#2A9D8F" opacity="0.5"/>
        </svg>
        <h1 style="font-size:28px; font-weight:700; margin-bottom:12px; color:#1a1a1a;">Learn without limits</h1>
        <p style="font-size:16px; color:#666; line-height:1.6; max-width:320px; margin:0 auto 24px;">AI-powered education that works offline. Personalized for WAEC, JAMB, coding, and global careers.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div style='text-align:center;'><div style='width:8px; height:8px; background:#E85D2B; border-radius:50%; display:inline-block;'></div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div style='text-align:center;'><div style='width:8px; height:8px; background:#E8E0D4; border-radius:50%; display:inline-block;'></div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div style='text-align:center;'><div style='width:8px; height:8px; background:#E8E0D4; border-radius:50%; display:inline-block;'></div></div>", unsafe_allow_html=True)
    
    if st.button("Start my learning journey", use_container_width=True):
        st.session_state.current_question = 0
        st.session_state.answers = []
        st.session_state.show_explanation = False
        st.session_state.selected_option = None
        navigate_to('diagnostic')
    
    if st.button("Skip for now", type="secondary", use_container_width=True):
        navigate_to('home')

# ==================== SCREEN: DIAGNOSTIC ====================
def render_diagnostic():
    q_idx = st.session_state.current_question
    
    if q_idx >= len(DIAGNOSTIC_QUESTIONS):
        calculate_results()
        navigate_to('results')
        return
    
    q = DIAGNOSTIC_QUESTIONS[q_idx]
    pct = int((q_idx / len(DIAGNOSTIC_QUESTIONS)) * 100)
    
    st.markdown(f"""
    <div style="padding: 24px 0 16px; text-align:center;">
        <h1 style="font-size:24px; font-weight:700; margin-bottom:6px;">Skill Assessment</h1>
        <p style="font-size:14px; color:#666;">Answer questions so we can build your perfect learning path</p>
    </div>
    <div style="padding: 0 0 16px;">
        <div style="display:flex; justify-content:space-between; font-size:13px; color:#666; margin-bottom:6px;">
            <span>Question {q_idx + 1} of {len(DIAGNOSTIC_QUESTIONS)}</span>
            <span>{pct}%</span>
        </div>
        <div class="progress-track"><div class="progress-fill" style="width:{pct}%"></div></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="card">
        <div style="font-size:12px; color:#E85D2B; font-weight:600; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:8px;">
            {q['subject']} <span class="difficulty-{q['difficulty']}">{q['difficulty']}</span>
        </div>
        <div style="font-size:17px; font-weight:600; line-height:1.5; margin-bottom:20px;">{q['question']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    letters = ['A', 'B', 'C', 'D']
    
    if not st.session_state.show_explanation:
        for i, opt in enumerate(q['options']):
            if st.button(f"{letters[i]}. {opt}", key=f"opt_{q_idx}_{i}", use_container_width=True):
                st.session_state.selected_option = i
                st.session_state.answers.append({
                    'subject': q['subject'],
                    'difficulty': q['difficulty'],
                    'correct': i == q['correct']
                })
                st.session_state.show_explanation = True
                st.rerun()
    else:
        selected = st.session_state.selected_option
        correct = q['correct']
        
        for i, opt in enumerate(q['options']):
            if i == correct:
                st.success(f"✓ {letters[i]}. {opt}")
            elif i == selected and i != correct:
                st.error(f"✗ {letters[i]}. {opt}")
            else:
                st.markdown(f"<div style='padding:10px; color:#999;'>{letters[i]}. {opt}</div>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="explanation-box">
            <strong>Explanation:</strong> {q['explanation']}
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Next question →", use_container_width=True):
            st.session_state.current_question += 1
            st.session_state.show_explanation = False
            st.session_state.selected_option = None
            st.rerun()

def calculate_results():
    subjects = {}
    total_correct = 0
    
    for a in st.session_state.answers:
        if a['subject'] not in subjects:
            subjects[a['subject']] = {'correct': 0, 'total': 0}
        subjects[a['subject']]['total'] += 1
        if a['correct']:
            subjects[a['subject']]['correct'] += 1
            total_correct += 1
    
    subject_scores = {sub: int((s['correct'] / s['total']) * 100) for sub, s in subjects.items()}
    sorted_scores = sorted(subject_scores.items(), key=lambda x: x[1], reverse=True)
    
    st.session_state.assessment_results = {
        'total_score': int((total_correct / len(st.session_state.answers)) * 100),
        'subject_scores': subject_scores,
        'strengths': [s for s in sorted_scores if s[1] >= 60],
        'weaknesses': [s for s in sorted_scores if s[1] < 60],
    }

# ==================== API INTEGRATIONS ====================
import time

if 'api_cache' not in st.session_state:
    st.session_state.api_cache = {}

def cached_api_call(key, fetch_func, ttl_seconds=300):
    cache = st.session_state.api_cache
    now = time.time()
    if key in cache and (now - cache[key]['timestamp']) < ttl_seconds:
        return cache[key]['data']
    try:
        data = fetch_func()
        cache[key] = {'data': data, 'timestamp': now}
        return data
    except Exception as e:
        return cache.get(key, {}).get('data', None)

def fetch_khan_academy_topics():
    url = 'https://www.khanacademy.org/api/v1/topictree'
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            data = r.json()
            subjects = []
            for child in data.get('children', [])[:8]:
                subjects.append({
                    'title': child.get('title', ''),
                    'description': child.get('description', '')[:200],
                    'url': 'https://www.khanacademy.org' + child.get('url', ''),
                    'children_count': len(child.get('children', []))
                })
            return subjects
    except:
        pass
    return []

def search_open_library(query, limit=8):
    url = f'https://openlibrary.org/search.json?q={requests.utils.quote(query)}&limit={limit}'
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            books = []
            for doc in r.json().get('docs', [])[:limit]:
                books.append({
                    'title': doc.get('title', 'Unknown'),
                    'author': ', '.join(doc.get('author_name', ['Unknown'])[:2]),
                    'year': doc.get('first_publish_year', 'N/A'),
                    'pages': doc.get('number_of_pages_median', 'N/A'),
                    'cover_id': doc.get('cover_i', None),
                    'key': doc.get('key', ''),
                    'subjects': doc.get('subject', [])[:3]
                })
            return books
    except:
        pass
    return []

def get_open_library_cover(cover_id, size='M'):
    if cover_id:
        return f'https://covers.openlibrary.org/b/id/{cover_id}-{size}.jpg'
    return None

def fetch_nasa_apod():
    url = 'https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY'
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return None

def fetch_nasa_images(query='education', count=6):
    url = f'https://images-api.nasa.gov/search?q={requests.utils.quote(query)}&media_type=image'
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            items = r.json().get('collection', {}).get('items', [])[:count]
            return [{
                'title': item.get('data', [{}])[0].get('title', ''),
                'description': item.get('data', [{}])[0].get('description', '')[:200],
                'image_url': item.get('links', [{}])[0].get('href', ''),
            } for item in items]
    except:
        pass
    return []

def fetch_random_quote():
    url = 'https://api.quotable.io/random?tags=education|inspirational|success|wisdom'
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            d = r.json()
            return {'text': d.get('content', ''), 'author': d.get('author', '')}
    except:
        pass
    fallback = [
        {'text': 'Education is the most powerful weapon which you can use to change the world.', 'author': 'Nelson Mandela'},
        {'text': 'The beautiful thing about learning is that no one can take it away from you.', 'author': 'B.B. King'},
        {'text': 'Success is the sum of small efforts, repeated day in and day out.', 'author': 'Robert Collier'},
        {'text': 'The future belongs to those who believe in the beauty of their dreams.', 'author': 'Eleanor Roosevelt'},
    ]
    return random.choice(fallback)

def search_wikipedia(query, limit=3):
    search_url = f'https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={requests.utils.quote(query)}&format=json&srlimit={limit}'
    try:
        r = requests.get(search_url, timeout=10)
        if r.status_code == 200:
            results = r.json().get('query', {}).get('search', [])
            return [{
                'title': res.get('title', ''),
                'snippet': res.get('snippet', '').replace('<span class=\"searchmatch\">', '').replace('</span>', ''),
            } for res in results]
    except:
        pass
    return []

def get_wikipedia_summary(page_title):
    url = f'https://en.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(page_title.replace(" ", "_"))}'
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            d = r.json()
            return {
                'title': d.get('title', ''),
                'extract': d.get('extract', ''),
                'thumbnail': d.get('thumbnail', {}).get('source', ''),
                'url': d.get('content_urls', {}).get('desktop', {}).get('page', '')
            }
    except:
        pass
    return None

def search_github_repos(topic='python', language='python', count=6):
    url = f'https://api.github.com/search/repositories?q=topic:{topic}+language:{language}&sort=stars&order=desc&per_page={count}'
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            repos = r.json().get('items', [])
            return [{
                'name': repo.get('name', ''),
                'description': (repo.get('description') or '')[:150],
                'stars': repo.get('stargazers_count', 0),
                'language': repo.get('language', ''),
                'url': repo.get('html_url', ''),
                'topics': repo.get('topics', [])[:4]
            } for repo in repos]
    except:
        pass
    return []

def fetch_fcc_superblocks():
    return [
        {'id': 'responsive-web-design', 'name': 'Responsive Web Design', 'cert': 'Certificate', 'lessons': 300, 'icon': '🌐'},
        {'id': 'javascript-algorithms-and-data-structures', 'name': 'JavaScript Algorithms & Data Structures', 'cert': 'Certificate', 'lessons': 300, 'icon': '📜'},
        {'id': 'front-end-development-libraries', 'name': 'Front End Development Libraries', 'cert': 'Certificate', 'lessons': 200, 'icon': '⚛️'},
        {'id': 'data-visualization', 'name': 'Data Visualization', 'cert': 'Certificate', 'lessons': 150, 'icon': '📊'},
        {'id': 'relational-database', 'name': 'Relational Database', 'cert': 'Certificate', 'lessons': 200, 'icon': '🗄️'},
        {'id': 'back-end-development-and-apis', 'name': 'Back End Development & APIs', 'cert': 'Certificate', 'lessons': 200, 'icon': '🔌'},
        {'id': 'quality-assurance', 'name': 'Quality Assurance', 'cert': 'Certificate', 'lessons': 150, 'icon': '✅'},
        {'id': 'scientific-computing-with-python', 'name': 'Scientific Computing with Python', 'cert': 'Certificate', 'lessons': 200, 'icon': '🐍'},
        {'id': 'data-analysis-with-python', 'name': 'Data Analysis with Python', 'cert': 'Certificate', 'lessons': 150, 'icon': '📈'},
        {'id': 'machine-learning-with-python', 'name': 'Machine Learning with Python', 'cert': 'Certificate', 'lessons': 200, 'icon': '🤖'},
    ]

W3SCHOOLS_COURSES = [
    {'title': 'HTML Tutorial', 'url': 'https://www.w3schools.com/html/', 'category': 'Web', 'level': 'Beginner', 'icon': '📄'},
    {'title': 'CSS Tutorial', 'url': 'https://www.w3schools.com/css/', 'category': 'Web', 'level': 'Beginner', 'icon': '🎨'},
    {'title': 'JavaScript Tutorial', 'url': 'https://www.w3schools.com/js/', 'category': 'Web', 'level': 'Beginner', 'icon': '📜'},
    {'title': 'Python Tutorial', 'url': 'https://www.w3schools.com/python/', 'category': 'Programming', 'level': 'Beginner', 'icon': '🐍'},
    {'title': 'SQL Tutorial', 'url': 'https://www.w3schools.com/sql/', 'category': 'Database', 'level': 'Beginner', 'icon': '🗄️'},
    {'title': 'PHP Tutorial', 'url': 'https://www.w3schools.com/php/', 'category': 'Web', 'level': 'Beginner', 'icon': '🐘'},
    {'title': 'Java Tutorial', 'url': 'https://www.w3schools.com/java/', 'category': 'Programming', 'level': 'Beginner', 'icon': '☕'},
    {'title': 'C++ Tutorial', 'url': 'https://www.w3schools.com/cpp/', 'category': 'Programming', 'level': 'Beginner', 'icon': '⚡'},
    {'title': 'Bootstrap Tutorial', 'url': 'https://www.w3schools.com/bootstrap/', 'category': 'Web', 'level': 'Beginner', 'icon': '🅱️'},
    {'title': 'React Tutorial', 'url': 'https://www.w3schools.com/react/', 'category': 'Web', 'level': 'Intermediate', 'icon': '⚛️'},
    {'title': 'Node.js Tutorial', 'url': 'https://www.w3schools.com/nodejs/', 'category': 'Web', 'level': 'Intermediate', 'icon': '🟢'},
    {'title': 'Git Tutorial', 'url': 'https://www.w3schools.com/git/', 'category': 'Tools', 'level': 'Beginner', 'icon': '🌿'},
]

GEEKSFORGEEKS_COURSES = [
    {'title': 'Data Structures & Algorithms', 'url': 'https://www.geeksforgeeks.org/data-structures/', 'category': 'CS', 'level': 'All Levels', 'icon': '🧮'},
    {'title': 'Python Programming', 'url': 'https://www.geeksforgeeks.org/python-programming-language/', 'category': 'Programming', 'level': 'All Levels', 'icon': '🐍'},
    {'title': 'Java Programming', 'url': 'https://www.geeksforgeeks.org/java/', 'category': 'Programming', 'level': 'All Levels', 'icon': '☕'},
    {'title': 'C++ Programming', 'url': 'https://www.geeksforgeeks.org/c-plus-plus/', 'category': 'Programming', 'level': 'All Levels', 'icon': '⚡'},
    {'title': 'Web Development', 'url': 'https://www.geeksforgeeks.org/web-development/', 'category': 'Web', 'level': 'All Levels', 'icon': '🌐'},
    {'title': 'Machine Learning', 'url': 'https://www.geeksforgeeks.org/machine-learning/', 'category': 'AI', 'level': 'Advanced', 'icon': '🤖'},
    {'title': 'Operating Systems', 'url': 'https://www.geeksforgeeks.org/operating-systems/', 'category': 'CS', 'level': 'Intermediate', 'icon': '💻'},
    {'title': 'DBMS', 'url': 'https://www.geeksforgeeks.org/dbms/', 'category': 'Database', 'level': 'Intermediate', 'icon': '🗄️'},
    {'title': 'Computer Networks', 'url': 'https://www.geeksforgeeks.org/computer-network-tutorials/', 'category': 'CS', 'level': 'Intermediate', 'icon': '🌐'},
    {'title': 'Aptitude & Reasoning', 'url': 'https://www.geeksforgeeks.org/aptitude-gq/', 'category': 'Career', 'level': 'All Levels', 'icon': '🧠'},
]

# ==================== SCREEN: RESOURCES HUB ====================
def render_resources_hub():
    st.markdown('''
    <div style="padding: 20px 0 16px;">
        <h1 style="font-size:24px; font-weight:700; margin-bottom:4px;">&#128218; Resources Hub</h1>
        <p style="font-size:14px; color:#666;">Free courses, books, and learning materials from top platforms</p>
    </div>
    ''', unsafe_allow_html=True)
    
    tabs = st.tabs(['&#127760; freeCodeCamp', '&#128214; W3Schools', '&#129518; GeeksforGeeks', '&#127891; Khan Academy', '&#128218; Open Library', '&#128640; NASA', '&#128187; GitHub'])
    
    with tabs[0]:
        st.markdown('<h3 style="font-size:16px; font-weight:600; margin:12px 0;">freeCodeCamp Certifications</h3>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:13px; color:#666; margin-bottom:16px;">100% free, project-based coding certifications.</p>', unsafe_allow_html=True)
        for course in fetch_fcc_superblocks():
            st.markdown(f'''
            <div class="card" style="margin-bottom:10px;">
                <div style="display:flex; align-items:center; gap:12px;">
                    <div style="font-size:28px;">{course['icon']}</div>
                    <div>
                        <div style="font-size:15px; font-weight:600;">{course['name']}</div>
                        <div style="font-size:12px; color:#666;">{course['lessons']}+ lessons &#183; {course['cert']}</div>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            fcc_url = f'https://www.freecodecamp.org/learn/{course["id"]}'
            if st.button(f"Start {course['name']}", key=f"fcc_{course['id']}", use_container_width=True):
                st.info(f'&#128279; Opening: {fcc_url}')
    
    with tabs[1]:
        st.markdown('<h3 style="font-size:16px; font-weight:600; margin:12px 0;">W3Schools Tutorials</h3>', unsafe_allow_html=True)
        w3_cats = list(set(c['category'] for c in W3SCHOOLS_COURSES))
        sel_cat = st.selectbox('Filter', ['All'] + w3_cats, key='w3_filter')
        filtered = W3SCHOOLS_COURSES if sel_cat == 'All' else [c for c in W3SCHOOLS_COURSES if c['category'] == sel_cat]
        for course in filtered:
            lc = '#1B6B4F' if course['level'] == 'Beginner' else '#B8860B'
            st.markdown(f'''
            <div class="card" style="margin-bottom:10px;">
                <div style="display:flex; align-items:center; gap:12px;">
                    <div style="font-size:28px;">{course['icon']}</div>
                    <div>
                        <div style="font-size:15px; font-weight:600;">{course['title']}</div>
                        <div style="font-size:12px; color:#666;">{course['category']} &#183; <span style="color:{lc};">{course['level']}</span></div>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            if st.button(f"Open {course['title']}", key=f"w3_{course['title'][:15]}", use_container_width=True):
                st.info(f'&#128279; {course["url"]}')
    
    with tabs[2]:
        st.markdown('<h3 style="font-size:16px; font-weight:600; margin:12px 0;">GeeksforGeeks Tutorials</h3>', unsafe_allow_html=True)
        gfg_cats = list(set(c['category'] for c in GEEKSFORGEEKS_COURSES))
        sel_gfg = st.selectbox('Filter', ['All'] + gfg_cats, key='gfg_filter')
        filtered = GEEKSFORGEEKS_COURSES if sel_gfg == 'All' else [c for c in GEEKSFORGEEKS_COURSES if c['category'] == sel_gfg]
        for course in filtered:
            lc = {'Beginner': '#1B6B4F', 'Intermediate': '#B8860B', 'Advanced': '#E85D2B', 'All Levels': '#264653'}.get(course['level'], '#666')
            st.markdown(f'''
            <div class="card" style="margin-bottom:10px;">
                <div style="display:flex; align-items:center; gap:12px;">
                    <div style="font-size:28px;">{course['icon']}</div>
                    <div>
                        <div style="font-size:15px; font-weight:600;">{course['title']}</div>
                        <div style="font-size:12px; color:#666;">{course['category']} &#183; <span style="color:{lc};">{course['level']}</span></div>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            if st.button(f"Read {course['title'][:25]}", key=f"gfg_{course['title'][:15]}", use_container_width=True):
                st.info(f'&#128279; {course["url"]}')
    
    with tabs[3]:
        st.markdown('<h3 style="font-size:16px; font-weight:600; margin:12px 0;">Khan Academy Subjects</h3>', unsafe_allow_html=True)
        with st.spinner('Loading...'):
            khan = cached_api_call('khan_topics', fetch_khan_academy_topics, 600)
        if khan:
            for topic in khan:
                st.markdown(f'''
                <div class="card" style="margin-bottom:10px;">
                    <div style="font-size:15px; font-weight:600;">{topic['title']}</div>
                    <div style="font-size:13px; color:#666;">{topic['description']}</div>
                    <div style="font-size:12px; color:#E85D2B;">{topic['children_count']} sub-topics</div>
                </div>
                ''', unsafe_allow_html=True)
                if st.button(f"Explore {topic['title'][:20]}", key=f"khan_{topic['title'][:15]}", use_container_width=True):
                    st.info(f'&#128279; {topic["url"]}')
        else:
            for topic in [
                {'title': 'Mathematics', 'desc': 'Arithmetic, Algebra, Geometry, Calculus', 'url': 'https://www.khanacademy.org/math', 'icon': '&#128290;'},
                {'title': 'Science', 'desc': 'Physics, Chemistry, Biology, Astronomy', 'url': 'https://www.khanacademy.org/science', 'icon': '&#128300;'},
                {'title': 'Economics', 'desc': 'Micro, Macro, Finance', 'url': 'https://www.khanacademy.org/economics-finance-domain', 'icon': '&#128176;'},
                {'title': 'Computing', 'desc': 'CS, Programming, Web', 'url': 'https://www.khanacademy.org/computing', 'icon': '&#128187;'},
            ]:
                st.markdown(f'''
                <div class="card" style="margin-bottom:10px;">
                    <div style="display:flex; align-items:center; gap:12px;">
                        <div style="font-size:28px;">{topic['icon']}</div>
                        <div>
                            <div style="font-size:15px; font-weight:600;">{topic['title']}</div>
                            <div style="font-size:13px; color:#666;">{topic['desc']}</div>
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
                if st.button(f"Visit {topic['title']}", key=f"kfb_{topic['title'][:10]}", use_container_width=True):
                    st.info(f'&#128279; {topic["url"]}')
    
    with tabs[4]:
        st.markdown('<h3 style="font-size:16px; font-weight:600; margin:12px 0;">Open Library &#8212; Free Books</h3>', unsafe_allow_html=True)
        search_query = st.text_input('Search books...', placeholder='e.g. Python programming, Physics', key='book_search')
        if search_query:
            with st.spinner('Searching...'):
                books = cached_api_call(f'ol_{search_query}', lambda: search_open_library(search_query), 300)
            if books:
                st.markdown(f"<div style='font-size:13px; color:#666; margin-bottom:12px;'>Found {len(books)} results</div>", unsafe_allow_html=True)
                for book in books:
                    cover = get_open_library_cover(book['cover_id'], 'M')
                    subjects = ', '.join(book['subjects'][:2]) if book['subjects'] else ''
                    c1, c2 = st.columns([1, 3])
                    with c1:
                        if cover:
                            st.image(cover, width=100)
                        else:
                            st.markdown('<div style="width:100px;height:140px;background:#E8E0D4;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:30px;">&#128214;</div>', unsafe_allow_html=True)
                    with c2:
                        st.markdown(f"<div style='font-size:15px;font-weight:600;'>{book['title']}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div style='font-size:13px;color:#666;'>by {book['author']}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div style='font-size:12px;color:#999;'>&#128197; {book['year']} &#183; &#128209; {book['pages']} pages</div>", unsafe_allow_html=True)
                        st.markdown(f"<div style='font-size:11px;color:#E85D2B;'>{subjects}</div>", unsafe_allow_html=True)
                        if st.button('View Book', key=f"book_{book['key']}"):
                            st.info(f'&#128279; https://openlibrary.org{book["key"]}')
                    st.markdown("<hr style='border:none;border-top:1px solid #E8E0D4;margin:12px 0;'>", unsafe_allow_html=True)
            else:
                st.info('No books found.')
        else:
            st.markdown("<h4 style='font-size:14px;font-weight:600;margin:16px 0 12px;'>Try searching for: Python, Physics, Mathematics, History</h4>", unsafe_allow_html=True)
    
    with tabs[5]:
        st.markdown('<h3 style="font-size:16px; font-weight:600; margin:12px 0;">NASA Educational Resources</h3>', unsafe_allow_html=True)
        with st.spinner('Loading NASA APOD...'):
            apod = cached_api_call('nasa_apod', fetch_nasa_apod, 3600)
        if apod:
            st.markdown(f"<div style='font-size:15px;font-weight:600;margin-bottom:8px;'>&#127756; {apod.get('title', '')}</div>", unsafe_allow_html=True)
            if apod.get('media_type') == 'image':
                st.image(apod.get('url', ''), use_column_width=True)
            with st.expander('Learn more'):
                st.write(apod.get('explanation', ''))
                st.caption(f"Date: {apod.get('date', '')} | NASA")
        
        st.markdown("<h4 style='font-size:14px;font-weight:600;margin:20px 0 12px;'>NASA Image Gallery</h4>", unsafe_allow_html=True)
        nasa_q = st.text_input('Search NASA images', placeholder='earth, mars, galaxy', key='nasa_search')
        query = nasa_q or 'education'
        with st.spinner('Searching...'):
            images = cached_api_call(f'nasa_{query}', lambda: fetch_nasa_images(query, 6), 600)
        if images:
            icols = st.columns(2)
            for i, img in enumerate(images):
                with icols[i % 2]:
                    if img.get('image_url'):
                        st.image(img['image_url'], use_column_width=True)
                    st.markdown(f"<div style='font-size:12px;font-weight:500;'>{img['title'][:60]}</div>", unsafe_allow_html=True)
    
    with tabs[6]:
        st.markdown('<h3 style="font-size:16px; font-weight:600; margin:12px 0;">GitHub Learning Repositories</h3>', unsafe_allow_html=True)
        lang = st.selectbox('Language', ['python', 'javascript', 'java', 'cpp', 'go', 'rust'], key='gh_lang')
        topic = st.selectbox('Topic', ['tutorial', 'learning', 'beginner', 'education'], key='gh_topic')
        with st.spinner('Searching GitHub...'):
            repos = cached_api_call(f'gh_{lang}_{topic}', lambda: search_github_repos(topic, lang, 8), 600)
        if repos:
            for repo in repos:
                stars = f"{repo['stars'] // 1000}k" if repo['stars'] >= 1000 else str(repo['stars'])
                st.markdown(f'''
                <div class="card" style="margin-bottom:10px;">
                    <div style="font-size:15px;font-weight:600;">&#128193; {repo['name']}</div>
                    <div style="font-size:13px;color:#666;margin:4px 0;">{repo['description']}</div>
                    <div style="font-size:12px;color:#666;">&#11088; {stars} &#183; &#128308; {repo['language']}</div>
                </div>
                ''', unsafe_allow_html=True)
                if st.button(f"View {repo['name']}", key=f"gh_{repo['name'][:15]}", use_container_width=True):
                    st.info(f'&#128279; {repo["url"]}')
        else:
            st.info('No repositories found.')

# ==================== ENHANCED HOME ====================
def render_home_enhanced():
    name = get_user_name()
    
    quote = cached_api_call('daily_quote', fetch_random_quote, ttl_seconds=3600)
    if quote:
        st.markdown(f'''
        <div style="background:linear-gradient(135deg, #264653 0%, #2A9D8F 100%); border-radius:16px; padding:16px 20px; margin-bottom:16px; color:white;">
            <div style="font-size:14px; font-style:italic; line-height:1.6; margin-bottom:8px;">&quot;{quote['text']}&quot;</div>
            <div style="font-size:12px; opacity:0.8; text-align:right;">&#8212; {quote['author']}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown(f'''
    <div style="padding: 8px 0 16px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
            <div>
                <div style="font-size:13px; color:#666;">Welcome back,</div>
                <div style="font-size:20px; font-weight:700; color:#1a1a1a;">{name}</div>
            </div>
            <div style="display:flex; gap:8px;">
                <div style="text-align:center; padding:8px 12px; background:white; border-radius:12px; border:1px solid #E8E0D4;">
                    <div style="font-size:18px;">&#128293;</div>
                    <div style="font-size:12px; font-weight:700;">{st.session_state.streak}</div>
                </div>
                <div style="text-align:center; padding:8px 12px; background:white; border-radius:12px; border:1px solid #E8E0D4;">
                    <div style="font-size:18px;">&#11088;</div>
                    <div style="font-size:12px; font-weight:700;">{st.session_state.points}</div>
                </div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown(f'''
    <div class="card" style="margin-bottom:16px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
            <div style="font-size:15px; font-weight:600;">Daily Goal</div>
            <div style="font-size:13px; color:#666;">{st.session_state.daily_goal_completed}/3 lessons</div>
        </div>
        <div class="progress-track"><div class="progress-fill" style="width:{(st.session_state.daily_goal_completed/3)*100}%"></div></div>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('<h3 style="font-size:16px; font-weight:600; margin:20px 0 12px;">Quick Actions</h3>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button('&#129302; AI Tutor', use_container_width=True):
            navigate_to('tutor')
    with col2:
        if st.button('&#128218; Resources', use_container_width=True):
            navigate_to('resources')
    with col3:
        if st.button('&#127758; Opportunities', use_container_width=True):
            navigate_to('opportunities')
    
    in_progress = [c for c in COURSES if c['progress'] > 0 and c['progress'] < 100]
    if in_progress:
        st.markdown('<h3 style="font-size:16px; font-weight:600; margin:20px 0 12px;">Continue Learning</h3>', unsafe_allow_html=True)
        for course in in_progress[:2]:
            color_map = {'primary': '#E85D2B', 'green': '#1B6B4F', 'teal': '#264653', 'gold': '#B8860B', 'purple': '#8A2BE2'}
            bar_color = color_map.get(course['color'], '#E85D2B')
            st.markdown(f'''
            <div class="card">
                <div style="display:flex; justify-content:space-between; align-items:start; margin-bottom:8px;">
                    <div>
                        <div style="font-size:15px; font-weight:600; margin-bottom:4px;">{course['name']}</div>
                        <div style="font-size:12px; color:#666;">{course['completed']} of {course['lessons']} lessons</div>
                    </div>
                    <div style="font-size:20px;">&#9654;</div>
                </div>
                <div class="progress-track"><div class="progress-fill" style="width:{course['progress']}%; background:{bar_color};"></div></div>
            </div>
            ''', unsafe_allow_html=True)
            if st.button(f"Resume {course['name']}", key=f"resume_{course['id']}", use_container_width=True):
                st.session_state.current_course = course['id']
                st.session_state.current_lesson = course['completed']
                navigate_to('course_detail')
    
    st.markdown('<h3 style="font-size:16px; font-weight:600; margin:20px 0 12px;">Recommended for You</h3>', unsafe_allow_html=True)
    recommended = [c for c in COURSES if c['progress'] == 0][:3]
    for course in recommended:
        tag_color = {'primary': 'tag-primary', 'green': 'tag-green', 'teal': 'tag-teal', 'gold': 'tag-gold', 'purple': 'tag-purple'}
        tag_class = tag_color.get(course['color'], 'tag-primary')
        st.markdown(f'''
        <div class="card">
            <div style="display:flex; justify-content:space-between; align-items:start; margin-bottom:8px;">
                <div>
                    <div class="tag {tag_class}">{course['subject']}</div>
                    <div style="font-size:15px; font-weight:600; margin-top:8px;">{course['name']}</div>
                </div>
            </div>
            <div style="font-size:13px; color:#666; margin-bottom:12px;">{course['lessons']} lessons &#183; {course['hours']} hours &#183; {course['level']}</div>
        </div>
        ''', unsafe_allow_html=True)
        if st.button(f"Start {course['name']}", key=f"start_{course['id']}", use_container_width=True):
            st.session_state.current_course = course['id']
            st.session_state.current_lesson = 0
            navigate_to('course_detail')
    
    st.markdown('<h3 style="font-size:16px; font-weight:600; margin:20px 0 12px;">Featured Opportunity</h3>', unsafe_allow_html=True)
    opp = OPPORTUNITIES[1]
    st.markdown(f'''
    <div class="opp-highlight">
        <div style="font-size:12px; font-weight:600; opacity:0.8; margin-bottom:4px;">{opp['type'].upper()}</div>
        <div style="font-size:17px; font-weight:700; margin-bottom:8px;">{opp['name']}</div>
        <div style="font-size:13px; opacity:0.9; margin-bottom:12px;">{opp['desc']}</div>
        <div style="font-size:12px; opacity:0.8;">&#128205; {opp['location']} &#183; Deadline: {opp['deadline']}</div>
    </div>
    ''', unsafe_allow_html=True)
    if st.button('View All Opportunities', type='secondary', use_container_width=True):
        navigate_to('opportunities')

# ==================== ENHANCED TUTOR ====================
def render_tutor_enhanced():
    st.markdown('''
    <div style="padding: 20px 0 16px;">
        <h1 style="font-size:24px; font-weight:700; margin-bottom:4px;">&#129302; AI Tutor</h1>
        <p style="font-size:14px; color:#666;">Ask anything &#8212; WAEC, JAMB, coding, career advice</p>
    </div>
    ''', unsafe_allow_html=True)
    
    wiki_query = st.text_input('&#128269; Quick Wikipedia Search', placeholder='Search any topic...', key='wiki_search')
    if wiki_query:
        with st.spinner('Searching Wikipedia...'):
            wiki_results = cached_api_call(f'wiki_{wiki_query}', lambda: search_wikipedia(wiki_query, 3), 300)
        if wiki_results:
            st.markdown('<h4 style="font-size:14px; font-weight:600; margin:12px 0;">Wikipedia Results</h4>', unsafe_allow_html=True)
            for result in wiki_results:
                with st.expander(result['title']):
                    st.write(result['snippet'])
                    summary = get_wikipedia_summary(result['title'])
                    if summary:
                        st.write(summary.get('extract', ''))
                        if summary.get('url'):
                            st.info(f"&#128279; {summary['url']}")
    
    st.markdown("<hr style='border:none; border-top:1px solid #E8E0D4; margin:20px 0;'>", unsafe_allow_html=True)
    
    st.markdown("<div style='font-size:13px; color:#666; margin-bottom:8px;'>Quick questions:</div>", unsafe_allow_html=True)
    quick_prompts = ['Explain photosynthesis', 'Solve x squared plus 5x plus 6', 'JAMB study plan', 'Python for-loop']
    cols = st.columns(2)
    for i, prompt in enumerate(quick_prompts):
        with cols[i % 2]:
            if st.button(prompt, key=f'quick_{i}', use_container_width=True):
                process_tutor_message(prompt)
                st.rerun()
    
    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        if msg['role'] == 'bot':
            st.markdown(f'''
            <div style="display:flex; gap:10px; margin-bottom:12px;">
                <div style="width:32px; height:32px; background:#E85D2B; border-radius:50%; display:flex; align-items:center; justify-content:center; color:white; font-size:14px; flex-shrink:0;">&#127891;</div>
                <div style="background:white; border:1px solid #E8E0D4; border-radius:12px; padding:12px 16px; font-size:14px; line-height:1.6; max-width:85%;">
                    {msg['text'].replace(chr(10), '<br>')}
                </div>
            </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown(f'''
            <div style="display:flex; justify-content:flex-end; margin-bottom:12px;">
                <div style="background:#E85D2B; color:white; border-radius:12px; padding:12px 16px; font-size:14px; line-height:1.6; max-width:85%;">
                    {msg['text']}
                </div>
            </div>
            ''', unsafe_allow_html=True)
    
    with st.form('tutor_form', clear_on_submit=True):
        user_msg = st.text_input('Ask me anything...', placeholder='e.g. How do I factor quadratic equations?', key='tutor_input')
        submitted = st.form_submit_button('Send', use_container_width=True)
        if submitted and user_msg:
            process_tutor_message(user_msg)
            st.rerun()

# ==================== ENHANCED BOTTOM NAV ====================
def render_bottom_nav_enhanced():
    screens = [
        ('home', '&#127968;', 'Home'),
        ('courses', '&#128218;', 'Courses'),
        ('resources', '&#128214;', 'Resources'),
        ('tutor', '&#129302;', 'Tutor'),
        ('profile', '&#128100;', 'Profile'),
    ]
    current = st.session_state.screen
    cols = st.columns(5)
    for i, (screen, icon, label) in enumerate(screens):
        with cols[i]:
            if st.button(f'{icon}\n{label}', key=f'nav_{screen}', use_container_width=True):
                if screen == 'courses':
                    st.session_state.filter_category = 'all'
                navigate_to(screen)

# ==================== MAIN APP ====================
def main():
    screen = st.session_state.screen
    if screen == 'auth':
        render_auth()
    elif screen == 'onboarding':
        render_onboarding()
    elif screen == 'diagnostic':
        render_diagnostic()
    elif screen == 'results':
        render_results()
    elif screen == 'home':
        render_home_enhanced()
        render_bottom_nav_enhanced()
    elif screen == 'courses':
        render_courses()
        render_bottom_nav_enhanced()
    elif screen == 'course_detail':
        render_course_detail()
        st.markdown("<div style='height:80px;'></div>", unsafe_allow_html=True)
        render_bottom_nav_enhanced()
    elif screen == 'resources':
        render_resources_hub()
        render_bottom_nav_enhanced()
    elif screen == 'tutor':
        render_tutor_enhanced()
        render_bottom_nav_enhanced()
    elif screen == 'opportunities':
        render_opportunities()
        render_bottom_nav_enhanced()
    elif screen == 'profile':
        render_profile()
        render_bottom_nav_enhanced()
    else:
        render_home_enhanced()
        render_bottom_nav_enhanced()

if __name__ == '__main__':
    main()