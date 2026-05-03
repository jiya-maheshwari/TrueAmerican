import streamlit as st
import random
from datetime import datetime

st.set_page_config(page_title="True American – Desi Edition", page_icon="🇮🇳", layout="wide")

# ─────────────────────────────────────────────────────────────────────────────
# STATE
# ─────────────────────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "players": {},
        "teams": {},
        "card_log": [],
        "current_card": None,
        "logged_in_email": None,
        "logged_in_name": None,
        "logged_in_team": None,
        "card_revealed": False,
        "card_result": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─────────────────────────────────────────────────────────────────────────────
# CARD DECK
# reward  = spaces moved forward on PASS (always >= 1, you always move on a pass)
# penalty = drink punishment on FAIL ONLY — no movement on fail ever
#
# Easy   → reward 1, penalty "1 sip"
# Medium → reward 2, penalty "3 sips"
# Hard   → reward 3, penalty "finish your drink"
# ─────────────────────────────────────────────────────────────────────────────
CARDS = {

    # ── TRIVIA ────────────────────────────────────────────────────────────────
    "trivia": [
        # BOLLYWOOD — Easy (reward 1)
        {"q": "Which film had the song 'Ek Do Teen'?", "a": "Tezaab (1988)", "reward": 1, "penalty": "1 sip"},
        {"q": "Which year did DDLJ release?", "a": "1995", "reward": 1, "penalty": "1 sip"},
        {"q": "Who directed 3 Idiots?", "a": "Rajkumar Hirani", "reward": 1, "penalty": "1 sip"},
        {"q": "Who played Poo in K3G?", "a": "Kareena Kapoor Khan", "reward": 1, "penalty": "1 sip"},
        {"q": "Which film had 'Mogambo Khush Hua'?", "a": "Mr. India (1987)", "reward": 1, "penalty": "1 sip"},
        {"q": "Which film had the song 'Chaiyya Chaiyya'?", "a": "Dil Se (1998)", "reward": 1, "penalty": "1 sip"},
        {"q": "Who is known as 'Bhai' in Bollywood?", "a": "Salman Khan", "reward": 1, "penalty": "1 sip"},
        {"q": "Name the villain in Sholay.", "a": "Gabbar Singh", "reward": 1, "penalty": "1 sip"},
        {"q": "Who played Rancho in 3 Idiots?", "a": "Aamir Khan", "reward": 1, "penalty": "1 sip"},
        {"q": "Who sang 'Tum Hi Ho'?", "a": "Arijit Singh", "reward": 1, "penalty": "1 sip"},
        {"q": "Who played Aman in Kal Ho Na Ho?", "a": "Shah Rukh Khan", "reward": 1, "penalty": "1 sip"},
        {"q": "Who directed Gully Boy?", "a": "Zoya Akhtar", "reward": 1, "penalty": "1 sip"},
        {"q": "Which film had the song 'Kuch Kuch Hota Hai'?", "a": "Kuch Kuch Hota Hai", "reward": 1, "penalty": "1 sip"},
        {"q": "Which cricketer is known as 'The Wall'?", "a": "Rahul Dravid", "reward": 1, "penalty": "1 sip"},
        {"q": "What does IPL stand for?", "a": "Indian Premier League", "reward": 1, "penalty": "1 sip"},
        {"q": "Who is the Nightingale of India?", "a": "Lata Mangeshkar", "reward": 1, "penalty": "1 sip"},
        {"q": "Which actress is called 'Desi Girl'?", "a": "Priyanka Chopra", "reward": 1, "penalty": "1 sip"},
        {"q": "Name India's first prime minister.", "a": "Jawaharlal Nehru", "reward": 1, "penalty": "1 sip"},
        {"q": "Who built the Taj Mahal?", "a": "Shah Jahan", "reward": 1, "penalty": "1 sip"},
        {"q": "Which Indian city is the Silicon Valley of India?", "a": "Bengaluru", "reward": 1, "penalty": "1 sip"},
        {"q": "Which Indian state is called God's Own Country?", "a": "Kerala", "reward": 1, "penalty": "1 sip"},
        {"q": "In which city is the Gateway of India?", "a": "Mumbai", "reward": 1, "penalty": "1 sip"},
        {"q": "Who wrote India's national anthem?", "a": "Rabindranath Tagore", "reward": 1, "penalty": "1 sip"},
        {"q": "What is India's national animal?", "a": "Bengal Tiger", "reward": 1, "penalty": "1 sip"},
        {"q": "Which year did India gain independence?", "a": "1947", "reward": 1, "penalty": "1 sip"},
        {"q": "What does DDLJ stand for?", "a": "Dilwale Dulhania Le Jayenge", "reward": 1, "penalty": "1 sip"},
        {"q": "Which film started Hrithik Roshan's career?", "a": "Kaho Naa... Pyaar Hai (2000)", "reward": 1, "penalty": "1 sip"},
        {"q": "Which Bollywood film is based on the 1983 Cricket World Cup?", "a": "83 (2021)", "reward": 1, "penalty": "1 sip"},
        {"q": "What does 'jugaad' mean?", "a": "A clever improvised fix", "reward": 1, "penalty": "1 sip"},
        {"q": "Which Indian festival is the festival of lights?", "a": "Diwali", "reward": 1, "penalty": "1 sip"},
        {"q": "Who directed Dangal?", "a": "Nitesh Tiwari", "reward": 1, "penalty": "1 sip"},
        {"q": "Which city is India's film industry capital?", "a": "Mumbai", "reward": 1, "penalty": "1 sip"},
        {"q": "Which film featured the character Circuit?", "a": "Munna Bhai MBBS", "reward": 1, "penalty": "1 sip"},

        # BOLLYWOOD / INDIA — Medium (reward 2)
        {"q": "Which AR Rahman song won an Oscar?", "a": "Jai Ho (Slumdog Millionaire)", "reward": 2, "penalty": "3 sips"},
        {"q": "Who was the first Indian to win an individual Olympic gold?", "a": "Abhinav Bindra, 2008", "reward": 2, "penalty": "3 sips"},
        {"q": "Which film was India's first Oscar nomination — in 1958?", "a": "Mother India", "reward": 2, "penalty": "3 sips"},
        {"q": "Which state produces the most tea in India?", "a": "Assam", "reward": 2, "penalty": "3 sips"},
        {"q": "Which Indian state has the longest coastline?", "a": "Gujarat", "reward": 2, "penalty": "3 sips"},
        {"q": "Who was PM of India during the 1971 war?", "a": "Indira Gandhi", "reward": 2, "penalty": "3 sips"},
        {"q": "Which freedom fighter was called Netaji?", "a": "Subhas Chandra Bose", "reward": 2, "penalty": "3 sips"},
        {"q": "What was the name of India's first satellite?", "a": "Aryabhata (1975)", "reward": 2, "penalty": "3 sips"},
        {"q": "Who composed the Sholay soundtrack?", "a": "R.D. Burman", "reward": 2, "penalty": "3 sips"},
        {"q": "Which year did Sachin score his 100th international century?", "a": "2012", "reward": 2, "penalty": "3 sips"},
        {"q": "What is the highest civilian award in India?", "a": "Bharat Ratna", "reward": 2, "penalty": "3 sips"},
        {"q": "Who was the first woman to win an Olympic medal for India?", "a": "Karnam Malleswari, 2000", "reward": 2, "penalty": "3 sips"},
        {"q": "Which Indian classical dance originates from Tamil Nadu?", "a": "Bharatanatyam", "reward": 2, "penalty": "3 sips"},
        {"q": "Which Bollywood film had SRK, Kajol AND Rani Mukherjee?", "a": "Kuch Kuch Hota Hai", "reward": 2, "penalty": "3 sips"},
        {"q": "Which freedom fighter said 'Give me blood and I will give you freedom'?", "a": "Subhas Chandra Bose", "reward": 2, "penalty": "3 sips"},

        # BOLLYWOOD / INDIA — Hard (reward 3)
        {"q": "Which year did India first win the Cricket World Cup?", "a": "1983", "reward": 3, "penalty": "finish your drink"},
        {"q": "Name the composer behind Dil Chahta Hai's soundtrack.", "a": "Shankar-Ehsaan-Loy", "reward": 3, "penalty": "finish your drink"},
        {"q": "Which Bollywood film starred both Amitabh Bachchan and Rekha opposite each other?", "a": "Silsila (1981)", "reward": 3, "penalty": "finish your drink"},
        {"q": "Name the PM of India who declared the Emergency in 1975.", "a": "Indira Gandhi", "reward": 3, "penalty": "finish your drink"},
        {"q": "How many states does India have?", "a": "28 states and 8 Union Territories", "reward": 3, "penalty": "finish your drink"},

        # GEN Z / US STUDENT — Easy (reward 1)
        {"q": "What does 'no cap' mean?", "a": "No lie / for real", "reward": 1, "penalty": "1 sip"},
        {"q": "What is a situationship?", "a": "A romantic relationship with no official label", "reward": 1, "penalty": "1 sip"},
        {"q": "What does 'slay' mean in Gen Z slang?", "a": "To do something exceptionally well", "reward": 1, "penalty": "1 sip"},
        {"q": "What is doom scrolling?", "a": "Endlessly scrolling through bad news or social media", "reward": 1, "penalty": "1 sip"},
        {"q": "What does 'touch grass' mean?", "a": "Go outside / get off the internet", "reward": 1, "penalty": "1 sip"},
        {"q": "What does 'ghosting' mean?", "a": "Cutting off contact with someone without explanation", "reward": 1, "penalty": "1 sip"},
        {"q": "What is 'the ick'?", "a": "A sudden turn-off/disgust toward someone you liked", "reward": 1, "penalty": "1 sip"},
        {"q": "What does OPT stand for?", "a": "Optional Practical Training", "reward": 1, "penalty": "1 sip"},
        {"q": "What does FAFSA stand for?", "a": "Free Application for Federal Student Aid", "reward": 1, "penalty": "1 sip"},
        {"q": "What is Spotify Wrapped?", "a": "Spotify's annual summary of your most-listened music", "reward": 1, "penalty": "1 sip"},
        {"q": "What does 'lowkey' mean?", "a": "Secretly / subtly", "reward": 1, "penalty": "1 sip"},
        {"q": "What is a red flag in dating context?", "a": "A warning sign that someone may be bad for you", "reward": 1, "penalty": "1 sip"},
        {"q": "What does 'it's giving' mean?", "a": "It has the vibe of / it looks like", "reward": 1, "penalty": "1 sip"},
        {"q": "What is a finsta?", "a": "A fake/private secondary Instagram account", "reward": 1, "penalty": "1 sip"},
        {"q": "What does STEM stand for?", "a": "Science, Technology, Engineering, Mathematics", "reward": 1, "penalty": "1 sip"},
        {"q": "What does 'understood the assignment' mean?", "a": "Someone did exactly what was needed, perfectly", "reward": 1, "penalty": "1 sip"},
        {"q": "What does 'rizz' mean?", "a": "Natural charm / ability to attract people", "reward": 1, "penalty": "1 sip"},
        {"q": "What is 'gatekeeping'?", "a": "Keeping something exclusive / not sharing with others", "reward": 1, "penalty": "1 sip"},
        {"q": "What is a 404 error?", "a": "Page not found", "reward": 1, "penalty": "1 sip"},
        {"q": "What does 'chronically online' mean?", "a": "Out of touch with real life from too much internet", "reward": 1, "penalty": "1 sip"},
        {"q": "What is ChatGPT made by?", "a": "OpenAI", "reward": 1, "penalty": "1 sip"},
        {"q": "What does 'main character energy' mean?", "a": "Acting like you're the confident protagonist of your own life", "reward": 1, "penalty": "1 sip"},
        {"q": "What app do most US college students use to pay each other back?", "a": "Venmo", "reward": 1, "penalty": "1 sip"},
        {"q": "Which company owns Instagram and WhatsApp?", "a": "Meta", "reward": 1, "penalty": "1 sip"},
        {"q": "What is the Duolingo owl's name?", "a": "Duo", "reward": 1, "penalty": "1 sip"},
        {"q": "What does 'delulu' mean in Gen Z slang?", "a": "Delusional — out of touch with reality about a situation", "reward": 1, "penalty": "1 sip"},
        {"q": "What does 'rent free' mean — as in living in someone's head?", "a": "They can't stop thinking about you", "reward": 1, "penalty": "1 sip"},
        {"q": "What does 'era' mean as Gen Z uses it — e.g. villain era?", "a": "A phase or period you're currently in", "reward": 1, "penalty": "1 sip"},
        {"q": "What does 'ate and left no crumbs' mean?", "a": "Did something perfectly, left nothing to criticise", "reward": 1, "penalty": "1 sip"},
        {"q": "What does 'NPC' mean as an insult?", "a": "Someone who is robotic / has no personality of their own", "reward": 1, "penalty": "1 sip"},

        # GEN Z / US STUDENT — Medium (reward 2)
        {"q": "What does the H-1B visa allow?", "a": "Work in the US in a specialty occupation", "reward": 2, "penalty": "3 sips"},
        {"q": "What is the cap on H-1B visas per year?", "a": "65,000 regular + 20,000 master's cap", "reward": 2, "penalty": "3 sips"},
        {"q": "What does DOGE stand for in the US government?", "a": "Department of Government Efficiency", "reward": 2, "penalty": "3 sips"},
        {"q": "Which president was impeached twice?", "a": "Donald Trump", "reward": 2, "penalty": "3 sips"},
        {"q": "What does APR stand for on a credit card?", "a": "Annual Percentage Rate", "reward": 2, "penalty": "3 sips"},
        {"q": "What is the federal minimum wage in the US?", "a": "$7.25/hour", "reward": 2, "penalty": "3 sips"},
        {"q": "What does the Bechdel Test check for in a film?", "a": "Whether 2+ women talk to each other about something other than a man", "reward": 2, "penalty": "3 sips"},
        {"q": "Which Indian-origin person is CEO of Google?", "a": "Sundar Pichai", "reward": 2, "penalty": "3 sips"},
        {"q": "Which Indian-origin person is CEO of Microsoft?", "a": "Satya Nadella", "reward": 2, "penalty": "3 sips"},
        {"q": "Which rapper won the beef with Drake in 2024?", "a": "Kendrick Lamar", "reward": 2, "penalty": "3 sips"},
    ],

    # ── ASSOCIATION ───────────────────────────────────────────────────────────
    "association": [
        # Easy (reward 1)
        {"q": "Shah Rukh Khan & Kajol", "a": "DDLJ", "reward": 1, "penalty": "1 sip"},
        {"q": "Holi & Diwali", "a": "Indian festivals", "reward": 1, "penalty": "1 sip"},
        {"q": "Naan & Roti", "a": "Indian bread", "reward": 1, "penalty": "1 sip"},
        {"q": "Rasgulla & Gulab Jamun", "a": "Indian sweets", "reward": 1, "penalty": "1 sip"},
        {"q": "Samosa & Pakora", "a": "Fried Indian snacks", "reward": 1, "penalty": "1 sip"},
        {"q": "Gandhi & Nehru", "a": "Indian independence leaders", "reward": 1, "penalty": "1 sip"},
        {"q": "Bhangra & Garba", "a": "Indian dances", "reward": 1, "penalty": "1 sip"},
        {"q": "Virat Kohli & MS Dhoni", "a": "Indian cricket captains", "reward": 1, "penalty": "1 sip"},
        {"q": "Ranbir Kapoor & Alia Bhatt", "a": "Married Bollywood couple", "reward": 1, "penalty": "1 sip"},
        {"q": "Masala chai & Filter coffee", "a": "Indian hot drinks", "reward": 1, "penalty": "1 sip"},
        {"q": "KBC & Bigg Boss", "a": "Indian TV shows", "reward": 1, "penalty": "1 sip"},
        {"q": "Taj Mahal & Qutub Minar", "a": "Indian monuments", "reward": 1, "penalty": "1 sip"},
        {"q": "Paneer & Tofu", "a": "Vegetarian protein", "reward": 1, "penalty": "1 sip"},
        {"q": "Arijit Singh & Atif Aslam", "a": "Playback singers", "reward": 1, "penalty": "1 sip"},
        {"q": "Salman Khan & Katrina Kaif", "a": "Tiger franchise / former couple", "reward": 1, "penalty": "1 sip"},
        {"q": "Amitabh Bachchan & Dharmendra", "a": "Sholay co-stars", "reward": 1, "penalty": "1 sip"},
        {"q": "Netflix & Hotstar", "a": "Streaming platforms", "reward": 1, "penalty": "1 sip"},
        {"q": "Venmo & Zelle", "a": "US payment apps", "reward": 1, "penalty": "1 sip"},
        {"q": "ChatGPT & Gemini", "a": "AI chatbots", "reward": 1, "penalty": "1 sip"},
        {"q": "Uber Eats & DoorDash", "a": "Food delivery apps", "reward": 1, "penalty": "1 sip"},
        {"q": "LinkedIn & Handshake", "a": "Job hunting platforms", "reward": 1, "penalty": "1 sip"},
        {"q": "GRE & GMAT", "a": "Graduate school entrance exams", "reward": 1, "penalty": "1 sip"},
        {"q": "Chipotle & Qdoba", "a": "Mexican-American fast casual chains", "reward": 1, "penalty": "1 sip"},
        {"q": "Rang De Basanti & Swades", "a": "Patriotic Bollywood films", "reward": 1, "penalty": "1 sip"},
        {"q": "Doordarshan & Star Plus", "a": "Indian TV channels", "reward": 1, "penalty": "1 sip"},
        {"q": "Zomato & Swiggy", "a": "Indian food delivery apps", "reward": 1, "penalty": "1 sip"},
        {"q": "Taylor Swift & Beyoncé", "a": "Biggest concert tours of 2023", "reward": 1, "penalty": "1 sip"},
        {"q": "Spotify & Apple Music", "a": "Music streaming rivals", "reward": 1, "penalty": "1 sip"},
        {"q": "Reddit & Twitter/X", "a": "Social media / internet forums", "reward": 1, "penalty": "1 sip"},
        {"q": "OPT & CPT", "a": "US work authorisations for international students", "reward": 1, "penalty": "1 sip"},

        # Medium (reward 2)
        {"q": "Lata Mangeshkar & Asha Bhosle", "a": "Legendary singer sisters", "reward": 2, "penalty": "3 sips"},
        {"q": "AR Rahman & Anu Malik", "a": "Bollywood music composers", "reward": 2, "penalty": "3 sips"},
        {"q": "Akbar & Ashoka", "a": "Indian emperors", "reward": 2, "penalty": "3 sips"},
        {"q": "Karan Johar & Farah Khan", "a": "Bollywood directors", "reward": 2, "penalty": "3 sips"},
        {"q": "Priyanka Chopra & Deepika Padukone", "a": "Bollywood actresses who went global", "reward": 2, "penalty": "3 sips"},
        {"q": "Elon Musk & Sam Altman", "a": "Tech billionaires / AI rivals", "reward": 2, "penalty": "3 sips"},
        {"q": "OpenAI & Anthropic", "a": "AI companies", "reward": 2, "penalty": "3 sips"},
        {"q": "Sundar Pichai & Satya Nadella", "a": "Indian-origin tech CEOs", "reward": 2, "penalty": "3 sips"},
        {"q": "Kendrick Lamar & Drake", "a": "2024 rap beef", "reward": 2, "penalty": "3 sips"},
        {"q": "F1 visa & J1 visa", "a": "US student / exchange visas", "reward": 2, "penalty": "3 sips"},
        {"q": "Biryani & Nihari", "a": "Mughlai slow-cooked dishes", "reward": 2, "penalty": "3 sips"},
        {"q": "Rohit Sharma & Shikhar Dhawan", "a": "India's opening batsmen", "reward": 2, "penalty": "3 sips"},
        {"q": "Paan & Supari", "a": "Post-meal mouth fresheners", "reward": 2, "penalty": "3 sips"},
    ],

    # ── ACTION ────────────────────────────────────────────────────────────────
    "action": [
        # Standard (reward 2)
        {"q": "Do the hook step from 'Chaiyya Chaiyya' for 10 seconds.", "a": "Group votes pass or fail.", "reward": 2, "penalty": "3 sips"},
        {"q": "Sing the chorus of any Bollywood song right now. No stopping.", "a": "Group votes.", "reward": 2, "penalty": "3 sips"},
        {"q": "Hold the SRK arms-spread pose for 5 seconds. No smiling.", "a": "Group rates out of 10. Below 6 = fail.", "reward": 2, "penalty": "1 sip"},
        {"q": "Mimic a Bollywood slow-motion crying scene. Go all out.", "a": "Group votes pass or fail.", "reward": 2, "penalty": "3 sips"},
        {"q": "Live cricket commentary for 20 seconds on what is happening in this room right now.", "a": "Cannot stop speaking.", "reward": 2, "penalty": "3 sips"},
        {"q": "Do the Daler Mehndi Tunak Tunak arm wiggle for 15 seconds.", "a": "Full commitment. No exceptions.", "reward": 2, "penalty": "1 sip"},
        {"q": "Do an impression of an Indian mom finding out you got a B+.", "a": "Group votes pass or fail.", "reward": 2, "penalty": "1 sip"},
        {"q": "Do the nagin dance for 10 seconds.", "a": "Group votes pass or fail.", "reward": 2, "penalty": "1 sip"},
        {"q": "Do your best Govinda-style dance move for 10 seconds.", "a": "Group votes.", "reward": 2, "penalty": "1 sip"},
        {"q": "Do 10 squats while singing any Bollywood song.", "a": "Stop mid-way = fail.", "reward": 2, "penalty": "3 sips"},
        {"q": "Hum a Bollywood song. Everyone must guess the film within 15 seconds.", "a": "No words allowed.", "reward": 2, "penalty": "1 sip"},
        {"q": "Teach the group one Bhangra or Garba step. Everyone tries it.", "a": "Worst student sips. You get the reward.", "reward": 2, "penalty": "3 sips"},
        {"q": "Say the Hindi tongue twister 'Kaccha papad pakka papad' 3 times fast.", "a": "Without messing up.", "reward": 2, "penalty": "1 sip"},
        {"q": "Impersonate any Bollywood villain for 10 seconds.", "a": "Group votes.", "reward": 2, "penalty": "3 sips"},
        {"q": "Pose for a saas-bahu drama screenshot for 5 seconds. Maximum expression.", "a": "Group votes most dramatic.", "reward": 2, "penalty": "1 sip"},
        {"q": "Do your best impression of a confused aunty using a smartphone.", "a": "Group votes.", "reward": 2, "penalty": "1 sip"},
        {"q": "Say 'I love you' in 5 different languages in 15 seconds.", "a": "Timed. Miss one = fail.", "reward": 2, "penalty": "3 sips"},
        {"q": "Describe your last situationship in one sentence. Everyone guesses how long it lasted.", "a": "Closest guess = 1 bonus space.", "reward": 2, "penalty": "1 sip"},
        {"q": "Act out an auto-rickshaw price negotiation — play both driver and passenger.", "a": "Group votes.", "reward": 2, "penalty": "3 sips"},
        {"q": "Recreate the 'Kitne aadmi the?' Sholay exchange with the person next to you.", "a": "Both must commit. Group votes.", "reward": 2, "penalty": "3 sips"},
        {"q": "Do a 15-second item number. Choose your song. Commit fully.", "a": "Group votes.", "reward": 2, "penalty": "3 sips"},
        {"q": "React to finding out your university added a mandatory 7am class. Full Bollywood drama.", "a": "Must include at least one anguished look at the sky.", "reward": 2, "penalty": "1 sip"},
        {"q": "Do a 15-second breakdown reacting to Chipotle raising prices again.", "a": "Full dramatic breakdown required.", "reward": 2, "penalty": "1 sip"},
        {"q": "In 15 seconds: pretend you're on a video call with your parents asking when you're getting married.", "a": "Group votes on authenticity.", "reward": 2, "penalty": "1 sip"},
        {"q": "Do an impression of someone rage-quitting a group project at midnight the day it is due.", "a": "Must include at least one passive-aggressive message being typed.", "reward": 2, "penalty": "1 sip"},
        {"q": "Name the most LinkedIn-brained thing you have ever done. Be honest.", "a": "Group votes most cringe.", "reward": 2, "penalty": "1 sip"},
        {"q": "Do your best impression of someone explaining their startup idea at 2am to people who did not ask.", "a": "Must mention disruption, scale, or AI.", "reward": 2, "penalty": "1 sip"},
        {"q": "Do a flawless desi aunty impression judging someone's life choices for 15 seconds.", "a": "Must mention marks, marriage, or a cousin comparison.", "reward": 2, "penalty": "3 sips"},
        {"q": "In 15 seconds: cold open a podcast about Indian student life in the US. Give it a name.", "a": "Must have a name, topic, and hook.", "reward": 2, "penalty": "1 sip"},
        {"q": "Recreate the DDLJ train scene with another player. You choose who.", "a": "Both must fully commit. No half measures.", "reward": 2, "penalty": "3 sips"},

        # Hard (reward 3)
        {"q": "Freestyle rap for 15 seconds about someone in the room. Hindi or English.", "a": "Group votes. Must be at least semi-coherent.", "reward": 3, "penalty": "finish your drink"},
        {"q": "Pitch your life to Shark Tank in 20 seconds. State your valuation.", "a": "Group votes on whether they would invest.", "reward": 3, "penalty": "finish your drink"},
        {"q": "Explain what the H-1B lottery is to a 5 year old. 15 seconds. No jargon.", "a": "Group votes on clarity.", "reward": 3, "penalty": "finish your drink"},
        {"q": "Say the alphabet backwards in 20 seconds.", "a": "Timed. Miss a letter = fail.", "reward": 3, "penalty": "finish your drink"},
        {"q": "Give a full 30-second TED Talk on why your team will win. Your most professional voice.", "a": "Group votes on conviction.", "reward": 3, "penalty": "finish your drink"},
        {"q": "Describe your situationship history as a Bollywood film synopsis in 20 seconds.", "a": "Must have a title, a hero, and a villain.", "reward": 3, "penalty": "finish your drink"},
        {"q": "Roast the person to your left for 15 seconds. Desi aunty style.", "a": "No personal trauma. Just vibes. Group votes.", "reward": 3, "penalty": "finish your drink"},
        {"q": "Name 5 Bollywood films from the 90s in 10 seconds.", "a": "Timed. Must get all 5.", "reward": 3, "penalty": "finish your drink"},
        {"q": "Speak only in questions for the next 90 seconds. Any statement = fail.", "a": "Rest of the room enforces it.", "reward": 3, "penalty": "finish your drink"},
        {"q": "Actually text your mom right now that you are 'not sure about grad school anymore'. Show the room.", "a": "Must actually send it. Timer starts now.", "reward": 3, "penalty": "finish your drink"},
    ],

    # ── WILDCARD ──────────────────────────────────────────────────────────────
    "wildcard": [
        {"q": "HINDI ONLY: For the next 2 minutes, no English from anyone. Each English word = 1 sip. Appoint a language police now.", "a": "Strict enforcement. No exceptions.", "reward": 2, "penalty": "3 sips"},
        {"q": "DOUBLE OR NOTHING: Commit before the next card is read. Pass = move 4 spaces. Fail = finish your drink.", "a": "No backing out once you say yes.", "reward": 4, "penalty": "finish your drink"},
        {"q": "TEAM CHALLENGE: Your whole team does 5 jumping jacks simultaneously. First team done = bonus cup attempt. Your team loses = 1 sip each.", "a": "All members must complete.", "reward": 2, "penalty": "1 sip"},
        {"q": "SILENT ROUND: No speaking for 60 seconds. Any sound = 1 sip per offender.", "a": "Clock starts now.", "reward": 2, "penalty": "3 sips"},
        {"q": "AZADI CALL: Shout Azadi — everyone must reply Inquilab Zindabad. Anyone who does not = 3 sips. You move 2 spaces.", "a": "Instant. No warning allowed.", "reward": 2, "penalty": "3 sips"},
        {"q": "STEAL A CUP: Challenge the leading team to a thumb war. Win = steal their cup. Lose = 3 sips.", "a": "Thumb war is law.", "reward": 3, "penalty": "3 sips"},
        {"q": "REVERSE CARD: The next player to draw must do their challenge twice. You move 2 spaces now.", "a": "Announce it loudly. It is binding.", "reward": 2, "penalty": "1 sip"},
        {"q": "MOST DESI: Everyone shares the most desi thing their parents have ever said. Group votes funniest. Winner moves 2 extra spaces.", "a": "Group vote decides.", "reward": 2, "penalty": "1 sip"},
        {"q": "PHONE TAX: Everyone who has Instagram open on their phone right now takes 1 sip. You move 2 spaces free.", "a": "Honour system. We will judge you.", "reward": 2, "penalty": "1 sip"},
        {"q": "SPEED ROUND: Everyone simultaneously shouts a Bollywood actor name. Duplicates sip. Last unique name standing moves 2 spaces.", "a": "No pre-planning.", "reward": 2, "penalty": "1 sip"},
        {"q": "HONEST HOUR: Name one Bollywood film you have pretended to have seen but have not. Anyone who calls your bluff = you finish your drink.", "a": "Honour system.", "reward": 2, "penalty": "3 sips"},
        {"q": "LAVA TRAP: Point at any player. If they visibly move in the next 30 seconds their team loses a cup. You watch.", "a": "No warning given to target.", "reward": 2, "penalty": "1 sip"},
        {"q": "GPA CHECK: Anyone with above a 3.7 GPA takes a sip. Anyone below 3.0 moves 2 spaces — you are built different.", "a": "Honour system.", "reward": 2, "penalty": "1 sip"},
        {"q": "LINKEDIN PURGE: The last person to post on LinkedIn must finish their drink. Profiles will be checked.", "a": "If nobody has posted, whoever most recently liked a post drinks.", "reward": 2, "penalty": "3 sips"},
        {"q": "SITUATIONSHIP TAX: Anyone currently in a situationship takes 1 sip. Anyone who claims they are not but everyone knows they are = 3 sips.", "a": "Group enforces this democratically.", "reward": 2, "penalty": "1 sip"},
        {"q": "MEMORY TEST: Draw another card. Read only the question. Answer without any help. Pass = 4 spaces. Fail = finish your drink.", "a": "No hints. No conferring. No mercy.", "reward": 4, "penalty": "finish your drink"},
        {"q": "COMPLIMENT CIRCLE: Everyone gives the person to their left a genuine compliment in 10 seconds. Laugh or visibly cringe = sip.", "a": "Keep a straight face.", "reward": 2, "penalty": "1 sip"},
        {"q": "FINSTA CONFESSION: Anyone who has or has ever had a finsta takes 1 sip. Anyone who has NEVER had one takes 2 sips — suspicious.", "a": "Honour system.", "reward": 2, "penalty": "1 sip"},
        {"q": "GROUP CHAT CHECK: Whoever has the most unread WhatsApp messages right now finishes their drink. Show your screens.", "a": "Most unread loses.", "reward": 2, "penalty": "3 sips"},
        {"q": "CALLBACK: The last person who drew a card must redo their challenge — but this time in a different language or accent.", "a": "Group votes pass or fail.", "reward": 2, "penalty": "3 sips"},
    ],
}

def get_full_deck():
    deck = []
    for cat, cards in CARDS.items():
        for card in cards:
            deck.append({**card, "type": cat})
    random.shuffle(deck)
    return deck

if "deck" not in st.session_state:
    st.session_state["deck"] = get_full_deck()
    st.session_state["deck_index"] = 0

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
TEAM_COLORS = {"team1": "#E85D04", "team2": "#2D6A4F", "team3": "#7B2D8B", "team4": "#1565C0"}
TEAM_LABELS = {"team1": "Team 1",  "team2": "Team 2",  "team3": "Team 3",  "team4": "Team 4"}
TYPE_LABELS = {"trivia": "Trivia", "association": "Association", "action": "Action", "wildcard": "Wildcard"}
TYPE_COLORS = {"trivia": "#1565C0","association": "#2D6A4F","action": "#E85D04","wildcard": "#7B2D8B"}
ALL_TEAMS   = ["team1", "team2", "team3", "team4"]

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def draw_card():
    deck = st.session_state["deck"]
    idx  = st.session_state["deck_index"]
    if idx >= len(deck):
        st.session_state["deck"]       = get_full_deck()
        st.session_state["deck_index"] = 0
        idx = 0
    st.session_state["current_card"]  = deck[idx]
    st.session_state["deck_index"]    = idx + 1
    st.session_state["card_revealed"] = False
    st.session_state["card_result"]   = None

def team_name(tid):
    return st.session_state["teams"].get(tid, {}).get("name", TEAM_LABELS.get(tid, tid))

def team_cups(tid):
    return st.session_state["teams"].get(tid, {}).get("cups", 0)

def ensure_team(tid):
    if tid not in st.session_state["teams"]:
        st.session_state["teams"][tid] = {"name": TEAM_LABELS[tid], "cups": 0}

def add_log(player, tname, etype, result, detail):
    st.session_state["card_log"].append({
        "player": player, "team": tname, "type": etype,
        "result": result, "detail": detail,
        "time": datetime.now().strftime("%H:%M:%S"),
    })

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  .main { background:#0a0a0a; }
  .block-container { padding-top:1.2rem; padding-bottom:2rem; }
  .game-title { font-size:2rem; font-weight:700; text-align:center; color:#FF8C00;
                letter-spacing:1px; margin-bottom:.15rem; }
  .game-sub   { text-align:center; color:#888; font-size:.9rem; margin-bottom:1.2rem; }

  .card-box   { border-radius:18px; padding:2rem 1.5rem; text-align:center;
                margin:1rem 0; border:2px solid; }
  .card-badge { display:inline-block; border-radius:20px; padding:4px 16px;
                font-size:.75rem; font-weight:700; letter-spacing:1px;
                margin-bottom:1rem; text-transform:uppercase; }
  .card-q     { font-size:1.4rem; font-weight:600; color:#fff; line-height:1.5; }
  .card-a     { background:#151520; border-radius:10px; padding:.75rem 1rem;
                margin-top:.75rem; color:#ccc; font-size:.95rem; text-align:left; }

  .reward-box  { background:#0d2b0d; border:1px solid #2D6A4F; border-radius:10px;
                 padding:.75rem 1rem; margin-top:.75rem; color:#6fcf97;
                 font-size:1rem; font-weight:600; }
  .penalty-box { background:#2b0d0d; border:1px solid #c0392b; border-radius:10px;
                 padding:.75rem 1rem; margin-top:.75rem; color:#e74c3c;
                 font-size:1rem; font-weight:600; }

  .score-card  { border-radius:14px; padding:1rem; text-align:center; margin-bottom:.4rem; }
  .cup-row     { font-size:1.4rem; letter-spacing:3px; margin:5px 0; }

  .win-banner  { background:linear-gradient(135deg,#0d2b0d,#082008);
                 border:2px solid #27ae60; border-radius:16px;
                 padding:1.5rem; text-align:center; margin-bottom:1rem; }
  .log-row     { font-size:.8rem; color:#999; padding:4px 0;
                 border-bottom:1px solid #1a1a1a; }
  .section-lbl { font-size:.7rem; text-transform:uppercase; letter-spacing:1px;
                 color:#666; margin-bottom:.3rem; }

  div[data-testid="stButton"] button { border-radius:10px; font-weight:600; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# LOGIN SCREEN
# ─────────────────────────────────────────────────────────────────────────────
def login_screen():
    st.markdown('<div class="game-title">True American 🇮🇳</div>', unsafe_allow_html=True)
    st.markdown('<div class="game-sub">Desi Edition — UIUC</div>', unsafe_allow_html=True)

    with st.form("login_form"):
        email = st.text_input("Illinois email", placeholder="netid@illinois.edu")
        name  = st.text_input("Your name",      placeholder="What do people call you?")
        team_choice = st.selectbox(
            "Choose your team",
            options=ALL_TEAMS,
            format_func=lambda x: team_name(x),
        )
        submitted = st.form_submit_button("Join the game", use_container_width=True)

    if submitted:
        if not email.endswith("@illinois.edu"):
            st.error("Must be an @illinois.edu email."); return
        if not name.strip():
            st.error("Enter your name."); return
        if email in st.session_state["players"]:
            p = st.session_state["players"][email]
            st.session_state.update(
                logged_in_email=email, logged_in_name=p["name"], logged_in_team=p["team"])
            st.rerun()
        else:
            count = sum(1 for p in st.session_state["players"].values() if p["team"] == team_choice)
            if count >= 4:
                st.error("That team is full (max 4). Pick another."); return
            ensure_team(team_choice)
            st.session_state["players"][email] = {
                "name": name.strip(), "team": team_choice,
                "joined_at": datetime.now().strftime("%H:%M:%S"),
            }
            st.session_state.update(
                logged_in_email=email, logged_in_name=name.strip(), logged_in_team=team_choice)
            st.rerun()

    st.markdown("---")
    st.markdown("#### Set team names")
    cols = st.columns(4)
    for i, (tid, col) in enumerate(zip(ALL_TEAMS, cols)):
        with col:
            ensure_team(tid)
            cur = team_name(tid)
            new = st.text_input(f"Team {i+1}", value=cur, key=f"tname_{tid}")
            if new != cur:
                st.session_state["teams"][tid]["name"] = new

    if st.session_state["players"]:
        st.markdown("---")
        st.markdown("#### Who's joined")
        for tid in ALL_TEAMS:
            members = [p["name"] for p in st.session_state["players"].values() if p["team"] == tid]
            if members:
                c = TEAM_COLORS[tid]
                st.markdown(
                    f'<span style="color:{c};font-weight:700;">{team_name(tid)}</span>: '
                    + " · ".join(members), unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# GAME SCREEN
# ─────────────────────────────────────────────────────────────────────────────
def game_screen():
    my_name  = st.session_state["logged_in_name"]
    my_team  = st.session_state["logged_in_team"]
    my_tname = team_name(my_team)
    my_color = TEAM_COLORS[my_team]

    st.markdown('<div class="game-title">True American 🇮🇳</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="game-sub">Playing as <strong>{my_name}</strong> — '
        f'<span style="color:{my_color}">{my_tname}</span></div>',
        unsafe_allow_html=True)

    # SCOREBOARD
    st.markdown("### Scoreboard")
    winner = None
    scols = st.columns(4)
    for tid, col in zip(ALL_TEAMS, scols):
        ensure_team(tid)
        cups    = team_cups(tid)
        tname   = team_name(tid)
        color   = TEAM_COLORS[tid]
        members = [p["name"] for p in st.session_state["players"].values() if p["team"] == tid]
        cup_row = "🔴" * cups + "⚪" * max(0, 6 - cups)
        with col:
            st.markdown(
                f'<div class="score-card" style="background:#111;border:2px solid {color};">'
                f'<div style="color:{color};font-weight:700;font-size:1rem;">{tname}</div>'
                f'<div class="cup-row">{cup_row}</div>'
                f'<div style="color:#aaa;font-size:.8rem;">{cups} / 6 cups</div>'
                f'<div style="color:#555;font-size:.7rem;margin-top:4px;">'
                f'{", ".join(members) or "—"}</div></div>',
                unsafe_allow_html=True)
        if cups >= 6:
            winner = tname

    if winner:
        st.markdown(
            f'<div class="win-banner"><div style="font-size:2.5rem;">🏆</div>'
            f'<div style="color:#27ae60;font-size:1.6rem;font-weight:700;">{winner} wins!</div>'
            f'<div style="color:#aaa;margin-top:.4rem;">Game over.</div></div>',
            unsafe_allow_html=True)

    st.markdown("---")
    left, right = st.columns([3, 2], gap="large")

    # CARD SECTION
    with left:
        st.markdown("### Draw a card")
        st.caption(
            "**Trivia / Association** — open to everyone, shout your answer first. "
            "**Action** — player chooses a teammate if they want. "
            "✅ Pass = move forward the number shown. ❌ Fail = drink only, no movement."
        )

        total      = len(st.session_state["deck"])
        remaining  = total - st.session_state["deck_index"]
        st.caption(f"Deck: {remaining} / {total} cards remaining")

        if st.button("🃏  Draw card", use_container_width=True, type="primary"):
            draw_card()

        card = st.session_state.get("current_card")
        if card:
            ctype = card["type"]
            color = TYPE_COLORS.get(ctype, "#888")
            label = TYPE_LABELS.get(ctype, ctype)

            st.markdown(
                f'<div class="card-box" style="background:#0f0f0f;border-color:{color};">'
                f'<div class="card-badge" style="background:{color}22;color:{color};">{label}</div>'
                f'<div class="card-q">{card["q"]}</div>'
                f'</div>', unsafe_allow_html=True)

            if not st.session_state.get("card_revealed"):
                if st.button("Reveal answer / judging notes", use_container_width=True):
                    st.session_state["card_revealed"] = True
                    st.rerun()
            else:
                st.markdown(
                    f'<div class="card-a"><strong>Answer / notes:</strong> {card["a"]}</div>',
                    unsafe_allow_html=True)

                result = st.session_state.get("card_result")
                if result is None:
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("✅  Nailed it", use_container_width=True):
                            st.session_state["card_result"] = "pass"
                            add_log(my_name, my_tname, label, "pass",
                                    f"Move forward {card['reward']} space(s)")
                            st.rerun()
                    with c2:
                        if st.button("❌  Failed", use_container_width=True):
                            st.session_state["card_result"] = "fail"
                            add_log(my_name, my_tname, label, "fail",
                                    f"Penalty: {card['penalty']}")
                            st.rerun()

                elif result == "pass":
                    st.markdown(
                        f'<div class="reward-box">'
                        f'🎉 Move forward <strong>{card["reward"]}</strong> space(s)!</div>',
                        unsafe_allow_html=True)

                elif result == "fail":
                    p = card["penalty"]
                    emoji = "💀" if "finish" in p else "🍺"
                    st.markdown(
                        f'<div class="penalty-box">'
                        f'{emoji} Penalty: <strong>{p}</strong> — stay where you are.</div>',
                        unsafe_allow_html=True)

    # CUP ACTIONS
    with right:
        st.markdown("### Cup actions")

        st.markdown('<div class="section-lbl">Chug &amp; win a cup 🔴</div>', unsafe_allow_html=True)
        st.caption("Player reached the cup spot and chugged. Add the cup here.")
        cup_team = st.selectbox("Team that got the cup", ALL_TEAMS, format_func=team_name, key="cup_sel")
        if st.button("Add cup", use_container_width=True):
            ensure_team(cup_team)
            if team_cups(cup_team) < 6:
                st.session_state["teams"][cup_team]["cups"] += 1
                add_log(my_name, my_tname, "Cup", "cup added",
                        f"+1 cup → {team_name(cup_team)}")
                st.rerun()
            else:
                st.warning("That team already has 6 cups!")

        st.markdown("---")
        st.markdown('<div class="section-lbl">Floor is lava 🌋</div>', unsafe_allow_html=True)
        st.caption("Someone touched the floor. Remove their team's cup.")
        lava_team = st.selectbox("Team that touched the floor", ALL_TEAMS, format_func=team_name, key="lava_sel")
        if st.button("Remove cup (lava penalty)", use_container_width=True):
            ensure_team(lava_team)
            if team_cups(lava_team) > 0:
                st.session_state["teams"][lava_team]["cups"] -= 1
                add_log(my_name, my_tname, "Lava", "cup removed",
                        f"–1 cup → {team_name(lava_team)}")
                st.rerun()
            else:
                st.warning("That team has no cups to lose!")

        st.markdown("---")
        st.markdown('<div class="section-lbl">Admin</div>', unsafe_allow_html=True)
        if st.button("Logout", use_container_width=True):
            st.session_state.update(
                logged_in_email=None, logged_in_name=None, logged_in_team=None)
            st.rerun()

        if st.button("🔄  Reset entire game", use_container_width=True):
            for tid in ALL_TEAMS:
                ensure_team(tid)
                st.session_state["teams"][tid]["cups"] = 0
            st.session_state.update(
                players={}, card_log=[], current_card=None,
                card_result=None, card_revealed=False,
                logged_in_email=None, logged_in_name=None, logged_in_team=None,
                deck=get_full_deck(), deck_index=0,
            )
            st.rerun()

    # ACTIVITY LOG
    if st.session_state["card_log"]:
        st.markdown("---")
        st.markdown("### Activity log")
        icons = {"pass": "✅", "fail": "❌", "cup added": "🔴", "cup removed": "🌋"}
        for entry in reversed(st.session_state["card_log"][-25:]):
            icon = icons.get(entry["result"], "•")
            st.markdown(
                f'<div class="log-row">{icon} <strong>{entry["player"]}</strong> ({entry["team"]}) '
                f'[{entry["type"]}] — {entry["detail"]} '
                f'<span style="color:#444;">{entry["time"]}</span></div>',
                unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# ROUTER
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state["logged_in_email"]:
    game_screen()
else:
    login_screen()
