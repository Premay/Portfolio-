import streamlit as st
import json
import random
from datetime import datetime, timedelta
import hashlib

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


# ==================== SCREEN: RESULTS ====================
def render_results():
    results = st.session_state.assessment_results
    if not results:
        navigate_to('home')
        return

    st.markdown(f"""
    <div style="text-align:center; padding: 24px 0 16px;">
        <div style="width:80px; height:80px; background:linear-gradient(135deg, #1B6B4F 0%, #2A9D8F 100%); border-radius:50%; margin:0 auto 16px; display:flex; align-items:center; justify-content:center; color:white; font-size:28px; font-weight:700;">
            {results['total_score']}%
        </div>
        <h1 style="font-size:24px; font-weight:700; margin-bottom:8px;">Assessment Complete!</h1>
        <p style="font-size:15px; color:#666; max-width:320px; margin:0 auto;">Here is how you performed across subjects</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h3 style='font-size:16px; font-weight:600; margin:20px 0 12px;'>Subject Breakdown</h3>", unsafe_allow_html=True)

    for subject, score in results['subject_scores'].items():
        color = '#1B6B4F' if score >= 60 else '#E85D2B'
        st.markdown(f"""
        <div class="card" style="margin-bottom:10px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <span style="font-size:15px; font-weight:600;">{subject}</span>
                <span style="font-size:14px; font-weight:700; color:{color};">{score}%</span>
            </div>
            <div class="progress-track"><div class="progress-fill" style="width:{score}%; background:{color};"></div></div>
        </div>
        """, unsafe_allow_html=True)

    if results['strengths']:
        st.markdown("<h3 style='font-size:16px; font-weight:600; margin:20px 0 12px; color:#1B6B4F;'>Your Strengths</h3>", unsafe_allow_html=True)
        for sub, score in results['strengths']:
            st.markdown(f"<div class='tag tag-green'>{sub} ({score}%)</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    if results['weaknesses']:
        st.markdown("<h3 style='font-size:16px; font-weight:600; margin:20px 0 12px; color:#E85D2B;'>Areas to Improve</h3>", unsafe_allow_html=True)
        for sub, score in results['weaknesses']:
            st.markdown(f"<div class='tag tag-primary'>{sub} ({score}%)</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="explanation-box" style="margin-bottom:20px;">
        <strong>Tip:</strong> We have personalized your course recommendations based on these results. Focus on your weak areas while maintaining your strengths!
    </div>
    """, unsafe_allow_html=True)

    if st.button("Go to Dashboard", use_container_width=True):
        navigate_to('home')

# ==================== BOTTOM NAV ====================
def render_bottom_nav():
    screens = [
        ('home', '🏠', 'Home'),
        ('courses', '📚', 'Courses'),
        ('tutor', '🤖', 'Tutor'),
        ('opportunities', '🌍', 'Opps'),
        ('profile', '👤', 'Profile'),
    ]

    current = st.session_state.screen
    cols = st.columns(5)

    for i, (screen, icon, label) in enumerate(screens):
        with cols[i]:
            active = current == screen
            bg = '#E85D2B' if active else 'transparent'
            color = 'white' if active else '#666'

            if st.button(f"{icon}\n{label}", key=f"nav_{screen}", use_container_width=True):
                if screen == 'courses':
                    st.session_state.filter_category = 'all'
                navigate_to(screen)

# ==================== SCREEN: HOME ====================
def render_home():
    name = get_user_name()

    st.markdown(f"""
    <div style="padding: 20px 0 16px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
            <div>
                <div style="font-size:13px; color:#666;">Welcome back,</div>
                <div style="font-size:20px; font-weight:700; color:#1a1a1a;">{name}</div>
            </div>
            <div style="display:flex; gap:8px;">
                <div style="text-align:center; padding:8px 12px; background:white; border-radius:12px; border:1px solid #E8E0D4;">
                    <div style="font-size:18px;">🔥</div>
                    <div style="font-size:12px; font-weight:700;">{st.session_state.streak}</div>
                </div>
                <div style="text-align:center; padding:8px 12px; background:white; border-radius:12px; border:1px solid #E8E0D4;">
                    <div style="font-size:18px;">⭐</div>
                    <div style="font-size:12px; font-weight:700;">{st.session_state.points}</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Daily goal
    st.markdown(f"""
    <div class="card" style="margin-bottom:16px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
            <div style="font-size:15px; font-weight:600;">Daily Goal</div>
            <div style="font-size:13px; color:#666;">{st.session_state.daily_goal_completed}/3 lessons</div>
        </div>
        <div class="progress-track"><div class="progress-fill" style="width:{(st.session_state.daily_goal_completed/3)*100}%"></div></div>
    </div>
    """, unsafe_allow_html=True)

    # Continue Learning
    in_progress = [c for c in COURSES if c['progress'] > 0 and c['progress'] < 100]
    if in_progress:
        st.markdown("<h3 style='font-size:16px; font-weight:600; margin:20px 0 12px;'>Continue Learning</h3>", unsafe_allow_html=True)
        for course in in_progress[:2]:
            color_map = {'primary': '#E85D2B', 'green': '#1B6B4F', 'teal': '#264653', 'gold': '#B8860B', 'purple': '#8A2BE2'}
            bar_color = color_map.get(course['color'], '#E85D2B')

            st.markdown(f"""
            <div class="card" style="cursor:pointer;" onclick="">
                <div style="display:flex; justify-content:space-between; align-items:start; margin-bottom:8px;">
                    <div>
                        <div style="font-size:15px; font-weight:600; margin-bottom:4px;">{course['name']}</div>
                        <div style="font-size:12px; color:#666;">{course['completed']} of {course['lessons']} lessons</div>
                    </div>
                    <div style="font-size:20px;">▶</div>
                </div>
                <div class="progress-track"><div class="progress-fill" style="width:{course['progress']}%; background:{bar_color};"></div></div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Resume {course['name']}", key=f"resume_{course['id']}", use_container_width=True):
                st.session_state.current_course = course['id']
                st.session_state.current_lesson = course['completed']
                navigate_to('course_detail')

    # Recommended Courses
    st.markdown("<h3 style='font-size:16px; font-weight:600; margin:20px 0 12px;'>Recommended for You</h3>", unsafe_allow_html=True)

    recommended = [c for c in COURSES if c['progress'] == 0][:3]
    for course in recommended:
        tag_color = {'primary': 'tag-primary', 'green': 'tag-green', 'teal': 'tag-teal', 'gold': 'tag-gold', 'purple': 'tag-purple'}
        tag_class = tag_color.get(course['color'], 'tag-primary')

        st.markdown(f"""
        <div class="card">
            <div style="display:flex; justify-content:space-between; align-items:start; margin-bottom:8px;">
                <div>
                    <div class="tag {tag_class}">{course['subject']}</div>
                    <div style="font-size:15px; font-weight:600; margin-top:8px;">{course['name']}</div>
                </div>
            </div>
            <div style="font-size:13px; color:#666; margin-bottom:12px;">{course['lessons']} lessons · {course['hours']} hours · {course['level']}</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"Start {course['name']}", key=f"start_{course['id']}", use_container_width=True):
            st.session_state.current_course = course['id']
            st.session_state.current_lesson = 0
            navigate_to('course_detail')

    # Quick Actions
    st.markdown("<h3 style='font-size:16px; font-weight:600; margin:20px 0 12px;'>Quick Actions</h3>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🤖 AI Tutor", use_container_width=True):
            navigate_to('tutor')
    with col2:
        if st.button("🌍 Opportunities", use_container_width=True):
            navigate_to('opportunities')

    # Featured Opportunity
    st.markdown("<h3 style='font-size:16px; font-weight:600; margin:20px 0 12px;'>Featured Opportunity</h3>", unsafe_allow_html=True)
    opp = OPPORTUNITIES[1]  # ALX
    st.markdown(f"""
    <div class="opp-highlight">
        <div style="font-size:12px; font-weight:600; opacity:0.8; margin-bottom:4px;">{opp['type'].upper()}</div>
        <div style="font-size:17px; font-weight:700; margin-bottom:8px;">{opp['name']}</div>
        <div style="font-size:13px; opacity:0.9; margin-bottom:12px;">{opp['desc']}</div>
        <div style="font-size:12px; opacity:0.8;">📍 {opp['location']} · Deadline: {opp['deadline']}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("View All Opportunities", type="secondary", use_container_width=True):
        navigate_to('opportunities')

# ==================== SCREEN: COURSES ====================
def render_courses():
    st.markdown("""
    <div style="padding: 20px 0 16px;">
        <h1 style="font-size:24px; font-weight:700; margin-bottom:4px;">Courses</h1>
        <p style="font-size:14px; color:#666;">Explore subjects tailored for you</p>
    </div>
    """, unsafe_allow_html=True)

    # Search
    search = st.text_input("Search courses...", placeholder="Type to search...", key="course_search")
    st.session_state.search_query = search

    # Category filter
    categories = {
        'all': 'All Courses',
        'progress africa': 'In Progress',
        'africa': 'WAEC / JAMB',
        'international coding': 'Coding',
        'international': 'International',
    }

    cols = st.columns(len(categories))
    for i, (cat_key, cat_label) in enumerate(categories.items()):
        with cols[i]:
            active = st.session_state.filter_category == cat_key
            if st.button(cat_label, key=f"cat_{cat_key}", use_container_width=True, 
                        type="primary" if active else "secondary"):
                st.session_state.filter_category = cat_key
                st.rerun()

    # Filter courses
    filtered = COURSES
    if st.session_state.filter_category != 'all':
        filtered = [c for c in COURSES if c['category'] == st.session_state.filter_category]
    if search:
        filtered = [c for c in filtered if search.lower() in c['name'].lower() or search.lower() in c['subject'].lower()]

    for course in filtered:
        tag_color = {'primary': 'tag-primary', 'green': 'tag-green', 'teal': 'tag-teal', 'gold': 'tag-gold', 'purple': 'tag-purple'}
        tag_class = tag_color.get(course['color'], 'tag-primary')
        progress_text = f"{course['progress']}% complete" if course['progress'] > 0 else "Not started"

        st.markdown(f"""
        <div class="card">
            <div style="display:flex; justify-content:space-between; align-items:start; margin-bottom:8px;">
                <div>
                    <div class="tag {tag_class}">{course['subject']}</div>
                    <div style="font-size:15px; font-weight:600; margin-top:8px;">{course['name']}</div>
                </div>
                <div style="font-size:12px; color:#666;">{progress_text}</div>
            </div>
            <div style="font-size:13px; color:#666; margin-bottom:12px;">{course['lessons']} lessons · {course['hours']} hours · {course['level']}</div>
            <div class="progress-track" style="margin-bottom:12px;"><div class="progress-fill" style="width:{course['progress']}%"></div></div>
        </div>
        """, unsafe_allow_html=True)

        btn_label = "Continue" if course['progress'] > 0 else "Start Course"
        if st.button(btn_label, key=f"course_btn_{course['id']}", use_container_width=True):
            st.session_state.current_course = course['id']
            st.session_state.current_lesson = course['completed']
            navigate_to('course_detail')

# ==================== SCREEN: COURSE DETAIL ====================
def render_course_detail():
    course_id = st.session_state.current_course
    if not course_id or course_id not in CURRICULUM:
        st.error("Course not found")
        if st.button("Back to Courses", use_container_width=True):
            navigate_to('courses')
        return

    course = next((c for c in COURSES if c['id'] == course_id), None)
    lesson = CURRICULUM[course_id]
    lesson_num = st.session_state.current_lesson + 1

    st.markdown(f"""
    <div style="padding: 16px 0;">
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:12px;">
            <div style="font-size:20px; cursor:pointer;" onclick="">←</div>
            <div style="font-size:14px; color:#666;">{course['name']}</div>
        </div>
        <div class="progress-track" style="margin-bottom:16px;"><div class="progress-fill" style="width:{course['progress']}%"></div></div>
        <div style="font-size:12px; color:#666; margin-bottom:8px;">{lesson['subtitle']}</div>
        <h1 style="font-size:22px; font-weight:700; margin-bottom:16px;">{lesson['title']}</h1>
    </div>
    """, unsafe_allow_html=True)

    # Lesson content
    st.markdown(f"<div class='lesson-content'>{lesson['content']}</div>", unsafe_allow_html=True)

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Previous Lesson", use_container_width=True, disabled=lesson_num <= 1):
            st.session_state.current_lesson -= 1
            st.rerun()
    with col2:
        if st.button("Next Lesson →", use_container_width=True):
            st.session_state.current_lesson += 1
            # Update progress
            if course:
                new_completed = min(st.session_state.current_lesson + 1, course['lessons'])
                course['completed'] = new_completed
                course['progress'] = int((new_completed / course['lessons']) * 100)
                # Award points
                st.session_state.points += 10
            st.rerun()

    # Bookmark
    if st.button("🔖 Bookmark this lesson", use_container_width=True):
        st.session_state.bookmarks.add(course_id)
        st.success("Lesson bookmarked!")

    # Ask AI Tutor about this lesson
    if st.button("🤖 Ask AI Tutor about this topic", use_container_width=True):
        st.session_state.tutor_context = lesson['title']
        navigate_to('tutor')

# ==================== SCREEN: AI TUTOR ====================
def render_tutor():
    st.markdown("""
    <div style="padding: 20px 0 16px;">
        <h1 style="font-size:24px; font-weight:700; margin-bottom:4px;">🤖 AI Tutor</h1>
        <p style="font-size:14px; color:#666;">Ask anything — WAEC, JAMB, coding, career advice</p>
    </div>
    """, unsafe_allow_html=True)

    # Quick prompts
    st.markdown("<div style='font-size:13px; color:#666; margin-bottom:8px;'>Quick questions:</div>", unsafe_allow_html=True)

    quick_prompts = [
        "Explain photosynthesis",
        "Solve x squared plus 5x plus 6",
        "JAMB study plan",
        "Python for-loop",
    ]

    cols = st.columns(2)
    for i, prompt in enumerate(quick_prompts):
        with cols[i % 2]:
            if st.button(prompt, key=f"quick_{i}", use_container_width=True):
                process_tutor_message(prompt)
                st.rerun()

    # Chat history
    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)

    for msg in st.session_state.chat_history:
        if msg['role'] == 'bot':
            st.markdown(f"""
            <div style="display:flex; gap:10px; margin-bottom:12px;">
                <div style="width:32px; height:32px; background:#E85D2B; border-radius:50%; display:flex; align-items:center; justify-content:center; color:white; font-size:14px; flex-shrink:0;">🎓</div>
                <div style="background:white; border:1px solid #E8E0D4; border-radius:12px; padding:12px 16px; font-size:14px; line-height:1.6; max-width:85%;">
                    {msg['text'].replace(chr(10), '<br>')}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="display:flex; justify-content:flex-end; margin-bottom:12px;">
                <div style="background:#E85D2B; color:white; border-radius:12px; padding:12px 16px; font-size:14px; line-height:1.6; max-width:85%;">
                    {msg['text']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Input
    with st.form("tutor_form", clear_on_submit=True):
        user_msg = st.text_input("Ask me anything...", placeholder="e.g. How do I factor quadratic equations?", key="tutor_input")
        submitted = st.form_submit_button("Send", use_container_width=True)

        if submitted and user_msg:
            process_tutor_message(user_msg)
            st.rerun()

def process_tutor_message(message):
    st.session_state.chat_history.append({'role': 'user', 'text': message})

    # Simple keyword-based responses
    msg_lower = message.lower()
    response = None

    for key, resp in TUTOR_RESPONSES.items():
        if key in msg_lower:
            response = resp
            break

    if not response:
        # Generate contextual response
        if any(w in msg_lower for w in ['math', 'mathematics', 'algebra', 'equation']):
            response = "I can help with math! Try asking about factoring, quadratic equations, or logarithms. For WAEC/JAMB, focus on surds, simultaneous equations, and calculus basics."
        elif any(w in msg_lower for w in ['physics', 'force', 'motion', 'energy']):
            response = "Physics is all about understanding principles! For JAMB, master kinematics (equations of motion), waves, and electromagnetism. Would you like a specific topic explained?"
        elif any(w in msg_lower for w in ['chemistry', 'atom', 'mole', 'reaction']):
            response = "Chemistry covers atomic structure, bonding, and stoichiometry. For WAEC, organic chemistry and electrolysis are high-yield topics. What would you like to explore?"
        elif any(w in msg_lower for w in ['english', 'grammar', 'essay', 'comprehension']):
            response = "For WAEC English, practice summary writing (stick to the word limit!) and comprehension strategies. For essays, plan your points before writing. Need specific help?"
        elif any(w in msg_lower for w in ['code', 'python', 'programming', 'developer']):
            response = "Python is great for beginners! Start with variables, loops, and functions. I can explain any concept with examples. What coding topic interests you?"
        elif any(w in msg_lower for w in ['career', 'job', 'university', 'scholarship']):
            response = "I can help with career planning! Check the Opportunities tab for scholarships and internships. For university applications, focus on your personal statement and references."
        elif any(w in msg_lower for w in ['waec', 'ssce', 'senior']):
            response = "WAEC preparation tip: Focus on past questions from the last 10 years. Pay special attention to recurring question types. Practice under timed conditions. Which subject?"
        elif any(w in msg_lower for w in ['jamb', 'utme']):
            response = "JAMB strategy: Use the syllabus as your guide. Practice CBT simulations. In the exam, answer easy questions first to build confidence. Need a study plan?"
        else:
            response = "That is a great question! I am here to help with WAEC, JAMB, coding, career advice, and any subject. Could you share more details so I can give you the best answer?"

    st.session_state.chat_history.append({'role': 'bot', 'text': response})
    st.session_state.points += 5

# ==================== SCREEN: OPPORTUNITIES ====================
def render_opportunities():
    st.markdown("""
    <div style="padding: 20px 0 16px;">
        <h1 style="font-size:24px; font-weight:700; margin-bottom:4px;">🌍 Opportunities</h1>
        <p style="font-size:14px; color:#666;">Scholarships, programs, and internships</p>
    </div>
    """, unsafe_allow_html=True)

    # Filter
    opp_types = {'all': 'All', 'scholarship': 'Scholarships', 'program': 'Programs', 'internship': 'Internships'}
    cols = st.columns(len(opp_types))
    for i, (type_key, type_label) in enumerate(opp_types.items()):
        with cols[i]:
            active = st.session_state.opp_filter == type_key
            if st.button(type_label, key=f"opp_filter_{type_key}", use_container_width=True,
                        type="primary" if active else "secondary"):
                st.session_state.opp_filter = type_key
                st.rerun()

    filtered = OPPORTUNITIES
    if st.session_state.opp_filter != 'all':
        filtered = [o for o in OPPORTUNITIES if o['type'] == st.session_state.opp_filter]

    for opp in filtered:
        type_colors = {'scholarship': 'tag-gold', 'program': 'tag-teal', 'internship': 'tag-purple'}
        tag_class = type_colors.get(opp['type'], 'tag-primary')

        st.markdown(f"""
        <div class="card">
            <div style="display:flex; justify-content:space-between; align-items:start; margin-bottom:8px;">
                <div>
                    <div class="tag {tag_class}">{opp['type'].upper()}</div>
                    <div style="font-size:15px; font-weight:600; margin-top:8px;">{opp['name']}</div>
                </div>
            </div>
            <div style="font-size:13px; color:#666; margin-bottom:8px;">{opp['desc']}</div>
            <div style="display:flex; gap:12px; font-size:12px; color:#666;">
                <span>🏢 {opp['org']}</span>
                <span>📍 {opp['location']}</span>
                <span>📅 {opp['deadline']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"Learn More", key=f"opp_btn_{opp['id']}", use_container_width=True):
            st.info(f"Visit {opp['org']} website to apply for {opp['name']}. Deadline: {opp['deadline']}")

# ==================== SCREEN: PROFILE ====================
def render_profile():
    name = get_user_name()
    initials = get_user_initials()
    level = get_user_level()
    location = get_user_location()

    st.markdown(f"""
    <div class="profile-header">
        <div class="profile-avatar">{initials}</div>
        <div style="font-size:20px; font-weight:700;">{name}</div>
        <div style="font-size:14px; color:#666;">{level} · {location}</div>
    </div>
    """, unsafe_allow_html=True)

    # Stats
    st.markdown(f"""
    <div class="achievement-grid" style="margin-bottom:20px;">
        <div class="achievement-card">
            <div style="font-size:24px; margin-bottom:4px;">🔥</div>
            <div style="font-size:20px; font-weight:700;">{st.session_state.streak}</div>
            <div style="font-size:12px; color:#666;">Day Streak</div>
        </div>
        <div class="achievement-card">
            <div style="font-size:24px; margin-bottom:4px;">⭐</div>
            <div style="font-size:20px; font-weight:700;">{st.session_state.points}</div>
            <div style="font-size:12px; color:#666;">Points</div>
        </div>
        <div class="achievement-card">
            <div style="font-size:24px; margin-bottom:4px;">📚</div>
            <div style="font-size:20px; font-weight:700;">{sum(1 for c in COURSES if c['progress'] > 0)}</div>
            <div style="font-size:12px; color:#666;">Courses</div>
        </div>
        <div class="achievement-card">
            <div style="font-size:24px; margin-bottom:4px;">🏆</div>
            <div style="font-size:20px; font-weight:700;">3</div>
            <div style="font-size:12px; color:#666;">Badges</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Settings
    st.markdown("<h3 style='font-size:16px; font-weight:600; margin:20px 0 12px;'>Settings</h3>", unsafe_allow_html=True)

    st.session_state.notifications_enabled = st.toggle("Push Notifications", value=st.session_state.notifications_enabled)
    st.session_state.reminder_time = st.text_input("Daily Reminder Time", value=st.session_state.reminder_time)

    # Bookmarks
    if st.session_state.bookmarks:
        st.markdown("<h3 style='font-size:16px; font-weight:600; margin:20px 0 12px;'>Bookmarked Lessons</h3>", unsafe_allow_html=True)
        for bm in list(st.session_state.bookmarks)[:5]:
            course = next((c for c in COURSES if c['id'] == bm), None)
            if course:
                st.markdown(f"<div class='card' style='padding:12px 16px;'><div style='font-size:14px; font-weight:500;'>{course['name']}</div></div>", unsafe_allow_html=True)

    # Assessment results
    if st.session_state.assessment_results:
        st.markdown("<h3 style='font-size:16px; font-weight:600; margin:20px 0 12px;'>Assessment Results</h3>", unsafe_allow_html=True)
        st.markdown(f"<div class='card'><div style='font-size:14px;'>Overall Score: <strong>{st.session_state.assessment_results['total_score']}%</strong></div></div>", unsafe_allow_html=True)

    # Logout
    st.markdown("<div style='margin-top:24px;'></div>", unsafe_allow_html=True)
    if st.button("🚪 Log Out", type="secondary", use_container_width=True):
        st.session_state.user = None
        st.session_state.is_guest = False
        navigate_to('auth')

    if st.button("🔄 Retake Assessment", use_container_width=True):
        st.session_state.current_question = 0
        st.session_state.answers = []
        st.session_state.assessment_results = None
        st.session_state.show_explanation = False
        st.session_state.selected_option = None
        navigate_to('diagnostic')

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
        render_home()
        render_bottom_nav()
    elif screen == 'courses':
        render_courses()
        render_bottom_nav()
    elif screen == 'course_detail':
        render_course_detail()
        st.markdown("<div style='height:80px;'></div>", unsafe_allow_html=True)
        render_bottom_nav()
    elif screen == 'tutor':
        render_tutor()
        render_bottom_nav()
    elif screen == 'opportunities':
        render_opportunities()
        render_bottom_nav()
    elif screen == 'profile':
        render_profile()
        render_bottom_nav()
    else:
        render_home()
        render_bottom_nav()

if __name__ == "__main__":
    main()
