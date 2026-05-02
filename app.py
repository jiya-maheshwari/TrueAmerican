import streamlit as st
import random
import json
from datetime import datetime

st.set_page_config(page_title="True American – Desi Edition", page_icon="🇮🇳", layout="wide")

# ── Persistent state via st.session_state (shared via rerun) ──────────────────
def init_state():
    defaults = {
        "players": {},       # email -> {name, team, joined_at}
        "teams": {},         # team_id -> {name, cups, color}
        "card_log": [],      # list of drawn card events
        "current_card": None,
        "game_started": False,
        "logged_in_email": None,
        "logged_in_name": None,
        "logged_in_team": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ── Card Deck ─────────────────────────────────────────────────────────────────
CARDS = {
    "trivia": [
        {"q": "Which film featured 'Ek Do Teen' originally?", "a": "Tezaab (1988)", "reward": 2, "penalty": "1 sip"},
        {"q": "Name the 3 leads of Dil Chahta Hai.", "a": "Aamir Khan, Akshaye Khanna, Saif Ali Khan", "reward": 2, "penalty": "1 sip"},
        {"q": "Which year did DDLJ release?", "a": "1995", "reward": 2, "penalty": "1 sip"},
        {"q": "Who directed 3 Idiots?", "a": "Rajkumar Hirani", "reward": 2, "penalty": "1 sip"},
        {"q": "Which film featured 'Mogambo Khush Hua'?", "a": "Mr. India (1987)", "reward": 2, "penalty": "1 sip"},
        {"q": "Who played Poo in Kabhi Khushi Kabhie Gham?", "a": "Kareena Kapoor Khan", "reward": 2, "penalty": "1 sip"},
        {"q": "What sport is played against the British in Lagaan?", "a": "Cricket", "reward": 2, "penalty": "1 sip"},
        {"q": "Which Indian state is called 'God's Own Country'?", "a": "Kerala", "reward": 2, "penalty": "1 sip"},
        {"q": "Who wrote India's national anthem?", "a": "Rabindranath Tagore", "reward": 2, "penalty": "1 sip"},
        {"q": "What is India's national animal?", "a": "Bengal Tiger", "reward": 2, "penalty": "1 sip"},
        {"q": "In which city is the Gateway of India?", "a": "Mumbai", "reward": 2, "penalty": "1 sip"},
        {"q": "How many states does India have?", "a": "28 states", "reward": 2, "penalty": "1 sip"},
        {"q": "Which city is called the 'City of Joy'?", "a": "Kolkata", "reward": 2, "penalty": "1 sip"},
        {"q": "Which Bollywood actor is known as 'Bhai'?", "a": "Salman Khan", "reward": 2, "penalty": "1 sip"},
        {"q": "Name the villain in Sholay.", "a": "Gabbar Singh (Amjad Khan)", "reward": 2, "penalty": "1 sip"},
        {"q": "Which film had the song 'Chaiyya Chaiyya'?", "a": "Dil Se (1998)", "reward": 2, "penalty": "1 sip"},
        {"q": "Who composed the music for Mughal-E-Azam?", "a": "Naushad", "reward": 3, "penalty": "3 sips"},
        {"q": "Which Indian city is called 'Silicon Valley of India'?", "a": "Bengaluru", "reward": 2, "penalty": "1 sip"},
        {"q": "Name the first Indian to win an individual Olympic gold.", "a": "Abhinav Bindra (2008)", "reward": 3, "penalty": "3 sips"},
        {"q": "Which cricketer is known as 'The Wall'?", "a": "Rahul Dravid", "reward": 2, "penalty": "1 sip"},
        {"q": "What does IPL stand for?", "a": "Indian Premier League", "reward": 2, "penalty": "1 sip"},
        {"q": "Which film won the first Indian Oscar nomination in 1958?", "a": "Mother India", "reward": 3, "penalty": "3 sips"},
        {"q": "Name the director of Gully Boy.", "a": "Zoya Akhtar", "reward": 2, "penalty": "1 sip"},
        {"q": "Which singer is known as 'The Nightingale of India'?", "a": "Lata Mangeshkar", "reward": 2, "penalty": "1 sip"},
        {"q": "Which Bollywood film is set in a fictional kingdom called Rajputana?", "a": "Padmaavat", "reward": 3, "penalty": "3 sips"},
        {"q": "Name two songs from Zindagi Na Milegi Dobara.", "a": "Senorita, Ik Junoon, Khaabon Ke Parinday", "reward": 2, "penalty": "1 sip"},
        {"q": "What is the full form of DDLJ?", "a": "Dilwale Dulhania Le Jayenge", "reward": 2, "penalty": "1 sip"},
        {"q": "Who played Aman in Kal Ho Na Ho?", "a": "Shah Rukh Khan", "reward": 2, "penalty": "1 sip"},
        {"q": "Which Indian festival is known as the festival of colours?", "a": "Holi", "reward": 2, "penalty": "1 sip"},
        {"q": "Name the highest civilian award in India.", "a": "Bharat Ratna", "reward": 3, "penalty": "3 sips"},
        {"q": "Which Bollywood film features the 'DDLJ' train scene?", "a": "Dilwale Dulhania Le Jayenge", "reward": 2, "penalty": "1 sip"},
        {"q": "Who sang 'Tum Hi Ho' in Aashiqui 2?", "a": "Arijit Singh", "reward": 2, "penalty": "1 sip"},
        {"q": "Which Indian dish is made with fermented rice and lentils?", "a": "Idli / Dosa", "reward": 2, "penalty": "1 sip"},
        {"q": "Name the Indian cricketer with the most ODI centuries.", "a": "Sachin Tendulkar (49)", "reward": 2, "penalty": "1 sip"},
        {"q": "Which film had Amitabh Bachchan's iconic 'angry young man' debut?", "a": "Zanjeer (1973)", "reward": 3, "penalty": "3 sips"},
        {"q": "What is 'chai pe charcha' literally?", "a": "Discussion over tea", "reward": 2, "penalty": "1 sip"},
        {"q": "Which Bollywood film popularised the song 'Kuch Kuch Hota Hai'?", "a": "Kuch Kuch Hota Hai (1998)", "reward": 2, "penalty": "1 sip"},
        {"q": "Name the director of Dangal.", "a": "Nitesh Tiwari", "reward": 2, "penalty": "1 sip"},
        {"q": "Which city hosts the Kumbh Mela most famously?", "a": "Prayagraj (Allahabad)", "reward": 3, "penalty": "3 sips"},
        {"q": "Which Bollywood actress is known as 'Desi Girl'?", "a": "Priyanka Chopra", "reward": 2, "penalty": "1 sip"},
        {"q": "Name India's first prime minister.", "a": "Jawaharlal Nehru", "reward": 2, "penalty": "1 sip"},
        {"q": "Which film featured Hrithik Roshan's debut?", "a": "Kaho Naa... Pyaar Hai (2000)", "reward": 2, "penalty": "1 sip"},
        {"q": "What is the currency of India?", "a": "Indian Rupee (INR)", "reward": 2, "penalty": "1 sip"},
        {"q": "Name the longest river in India.", "a": "Ganga (Ganges)", "reward": 2, "penalty": "1 sip"},
        {"q": "Which film won Aamir Khan his first Filmfare Best Actor?", "a": "Raja Hindustani (1996)", "reward": 3, "penalty": "3 sips"},
        {"q": "Who is known as 'The Maestro' of Indian classical music?", "a": "Ravi Shankar", "reward": 3, "penalty": "3 sips"},
        {"q": "Which Bollywood film is based on the 1983 Cricket World Cup?", "a": "83 (2021)", "reward": 2, "penalty": "1 sip"},
        {"q": "Name the Indian who invented the game of Snakes and Ladders.", "a": "Gyandev (13th century)", "reward": 4, "penalty": "move back 1"},
        {"q": "What does 'jugaad' mean in Indian culture?", "a": "A clever hack / improvised solution", "reward": 2, "penalty": "1 sip"},
        {"q": "Which Indian state produces the most tea?", "a": "Assam", "reward": 3, "penalty": "3 sips"},
    ],
    "association": [
        {"q": "Amitabh Bachchan & Dharmendra", "a": "Sholay", "reward": 3, "penalty": "3 sips"},
        {"q": "Shah Rukh Khan & Kajol", "a": "DDLJ / Kuch Kuch Hota Hai", "reward": 2, "penalty": "1 sip"},
        {"q": "Biryani & Nihari", "a": "Mughlai / Hyderabadi food", "reward": 3, "penalty": "3 sips"},
        {"q": "Sachin & Dravid", "a": "Cricket / India legends", "reward": 2, "penalty": "1 sip"},
        {"q": "Holi & Diwali", "a": "Hindu festivals", "reward": 2, "penalty": "1 sip"},
        {"q": "Ranbir Kapoor & Alia Bhatt", "a": "Brahmastra / married couple", "reward": 2, "penalty": "1 sip"},
        {"q": "Arijit Singh & Atif Aslam", "a": "Playback singers", "reward": 3, "penalty": "3 sips"},
        {"q": "Chennai & Kolkata", "a": "IPL teams / metro cities", "reward": 2, "penalty": "1 sip"},
        {"q": "Paneer & Tofu", "a": "Cheese / protein / vegetarian", "reward": 2, "penalty": "1 sip"},
        {"q": "Karan Johar & Farah Khan", "a": "Bollywood directors", "reward": 3, "penalty": "3 sips"},
        {"q": "Taj Mahal & Qutub Minar", "a": "UNESCO World Heritage Sites / Mughal", "reward": 3, "penalty": "3 sips"},
        {"q": "Rasgulla & Gulab Jamun", "a": "Indian sweets / mithai", "reward": 2, "penalty": "1 sip"},
        {"q": "Virat Kohli & MS Dhoni", "a": "Indian cricket captains", "reward": 2, "penalty": "1 sip"},
        {"q": "Mumbai & Delhi", "a": "Indian metro cities / IPL", "reward": 2, "penalty": "1 sip"},
        {"q": "Priyanka Chopra & Deepika Padukone", "a": "Bollywood actresses gone global", "reward": 3, "penalty": "3 sips"},
        {"q": "Naan & Roti", "a": "Indian bread", "reward": 2, "penalty": "1 sip"},
        {"q": "AR Rahman & Anu Malik", "a": "Bollywood composers", "reward": 3, "penalty": "3 sips"},
        {"q": "Akbar & Ashoka", "a": "Indian emperors", "reward": 3, "penalty": "3 sips"},
        {"q": "Paan & Supari", "a": "Mouth freshener / post-meal ritual", "reward": 3, "penalty": "3 sips"},
        {"q": "Rohit Sharma & Shikhar Dhawan", "a": "India's opening batsmen", "reward": 2, "penalty": "1 sip"},
        {"q": "Rajasthan & Gujarat", "a": "Indian states / desert / western India", "reward": 2, "penalty": "1 sip"},
        {"q": "Lata Mangeshkar & Asha Bhosle", "a": "Legendary sisters / playback singers", "reward": 3, "penalty": "3 sips"},
        {"q": "Masala chai & Filter coffee", "a": "Indian hot drinks", "reward": 2, "penalty": "1 sip"},
        {"q": "Rang De Basanti & Swades", "a": "Patriotic Bollywood films", "reward": 3, "penalty": "3 sips"},
        {"q": "Salman Khan & Katrina Kaif", "a": "Tiger / former couple / co-stars", "reward": 2, "penalty": "1 sip"},
        {"q": "Bhangra & Garba", "a": "Regional Indian dances", "reward": 2, "penalty": "1 sip"},
        {"q": "Gandhi & Nehru", "a": "Indian independence leaders", "reward": 2, "penalty": "1 sip"},
        {"q": "Samosa & Pakora", "a": "Indian fried snacks", "reward": 2, "penalty": "1 sip"},
        {"q": "KBC & Bigg Boss", "a": "Indian reality / game shows", "reward": 2, "penalty": "1 sip"},
        {"q": "Doordarshan & Star Plus", "a": "Indian TV channels", "reward": 3, "penalty": "3 sips"},
    ],
    "action": [
        {"q": "Do the hook step from 'Chaiyya Chaiyya' for 10 seconds.", "a": "Group votes pass/fail.", "reward": 4, "penalty": "3 sips"},
        {"q": "Sing the first verse of any Bollywood song. No stopping.", "a": "Group votes.", "reward": 3, "penalty": "3 sips"},
        {"q": "Do your best SRK arms-spread pose and hold for 5 seconds.", "a": "Group rates 1–10. Below 6 = fail.", "reward": 3, "penalty": "1 sip"},
        {"q": "Mimic a Bollywood dramatic slow-motion crying scene.", "a": "Group votes pass/fail.", "reward": 4, "penalty": "3 sips"},
        {"q": "Be a cricket commentator for 20 seconds on whatever is happening in the room.", "a": "Must not stop.", "reward": 3, "penalty": "3 sips"},
        {"q": "Teach the group one step of Bhangra or Garba. Everyone tries it.", "a": "Worst student sips, teacher scores.", "reward": 4, "penalty": "3 sips"},
        {"q": "Act out a full auto-rickshaw price negotiation — play both driver and passenger.", "a": "Group votes.", "reward": 4, "penalty": "3 sips"},
        {"q": "Do 10 squats while singing any IPL theme or jingle.", "a": "Stop mid-way = fail.", "reward": 3, "penalty": "3 sips"},
        {"q": "Say a tongue twister in Hindi 3 times fast.", "a": "Kaccha papad, pakka papad.", "reward": 3, "penalty": "1 sip"},
        {"q": "Impersonate any Bollywood villain for 10 seconds.", "a": "Group votes.", "reward": 4, "penalty": "3 sips"},
        {"q": "Do the Daler Mehndi 'Tunak Tunak' arm move for 15 seconds.", "a": "Full commitment required.", "reward": 3, "penalty": "1 sip"},
        {"q": "Recreate the Sholay 'Kitne aadmi the?' dialogue exchange with another player.", "a": "Both must know their lines.", "reward": 4, "penalty": "3 sips"},
        {"q": "Hum any Bollywood song. Others must guess the film within 15 seconds.", "a": "No words, only humming.", "reward": 3, "penalty": "1 sip"},
        {"q": "Do an impression of an Indian mom scolding someone.", "a": "Group votes pass/fail.", "reward": 3, "penalty": "1 sip"},
        {"q": "Say the alphabet backwards in 20 seconds.", "a": "Timed. Fail = miss a letter.", "reward": 4, "penalty": "move back 1"},
        {"q": "Pose for a 'saas-bahu' drama screenshot for 5 seconds. Maximum expression.", "a": "Group votes most dramatic.", "reward": 3, "penalty": "1 sip"},
        {"q": "Speak only in questions for the next 60 seconds.", "a": "Any statement = fail.", "reward": 3, "penalty": "3 sips"},
        {"q": "Do your best Govinda dance move for 10 seconds.", "a": "Group votes.", "reward": 3, "penalty": "1 sip"},
        {"q": "Name 5 Bollywood films from the 90s in 10 seconds.", "a": "Timed.", "reward": 3, "penalty": "3 sips"},
        {"q": "Recreate the DDLJ train scene — you need one other player.", "a": "Both must commit.", "reward": 5, "penalty": "move back 1"},
        {"q": "Do a 15-second Bollywood item number. Choose your song.", "a": "Group votes.", "reward": 4, "penalty": "3 sips"},
        {"q": "Describe your morning routine entirely in a Bollywood dramatic monologue style.", "a": "Must last 20 seconds.", "reward": 4, "penalty": "3 sips"},
        {"q": "Freestyle rap for 15 seconds about someone in the room. In Hindi or English.", "a": "Group votes.", "reward": 5, "penalty": "move back 1"},
        {"q": "Do the 'nagin dance' for 10 seconds.", "a": "Group votes pass/fail.", "reward": 3, "penalty": "1 sip"},
        {"q": "Pretend to negotiate at a street market. Buy something from someone in the room.", "a": "Must get the price down.", "reward": 4, "penalty": "3 sips"},
    ],
    "wildcard": [
        {"q": "HINDI ONLY: For the next 2 minutes, no English from anyone. Each English word = 1 sip. Appoint a language police.", "a": "Strict enforcement.", "reward": 3, "penalty": "move back 1"},
        {"q": "DOUBLE OR NOTHING: Answer next trivia right = move 4 spaces. Wrong = finish your drink. Commit before the question is read.", "a": "No backing out.", "reward": 4, "penalty": "move back 1"},
        {"q": "TEAM CHALLENGE: Your whole team must do 5 jumping jacks simultaneously. First team to finish wins a cup attempt. Lose = 1 sip each.", "a": "All members must complete.", "reward": 4, "penalty": "1 sip"},
        {"q": "SILENT ROUND: No speaking for 60 seconds. Any sound from anyone = 1 sip per person who made noise.", "a": "Clock starts now.", "reward": 3, "penalty": "3 sips"},
        {"q": "COMPLIMENT CIRCLE: Everyone gives the person to their left a genuine compliment in 10 seconds each. Laugh mid-compliment = sip.", "a": "Keep a straight face.", "reward": 3, "penalty": "1 sip"},
        {"q": "AZADI CALL: Shout 'Azadi!' — everyone must reply 'Inquilab Zindabad!' Anyone who doesn't = 3 sips. You move 3 spaces.", "a": "Instant.", "reward": 3, "penalty": "3 sips"},
        {"q": "SWAP SPACES: You and any player of your choice swap board positions right now.", "a": "No refusals.", "reward": 3, "penalty": "1 sip"},
        {"q": "STEAL A CUP: If your team has fewer cups than the leading team, steal one cup from them right now. They can challenge with a thumb war.", "a": "Thumb war decides.", "reward": 5, "penalty": "move back 1"},
        {"q": "REVERSE CARD: The next person to draw a card must do the challenge twice. You move 2 spaces now.", "a": "Announce it loudly.", "reward": 2, "penalty": "1 sip"},
        {"q": "MOST DESI: Go around the room — everyone shares the most desi thing their parents have said to them. Group votes funniest. Winner moves 2 extra spaces.", "a": "Group vote.", "reward": 2, "penalty": "1 sip"},
        {"q": "HONEST HOUR: Name one Bollywood film you've pretended to have seen but haven't. Anyone who catches you lying = you sip.", "a": "Honour system.", "reward": 2, "penalty": "1 sip"},
        {"q": "LAVA TRAP: Point at any player. If they move in the next 30 seconds (even slightly), their team loses a cup. You get to watch.", "a": "Judge decides movement.", "reward": 4, "penalty": "move back 1"},
        {"q": "SPEED ROUND: Everyone simultaneously shouts a Bollywood actor name. Any duplicates must sip. Last unique name standing moves 3 spaces.", "a": "Simultaneous.", "reward": 3, "penalty": "1 sip"},
        {"q": "PHONE TAX: Everyone who has Instagram on their phone right now takes 1 sip. You move 2 spaces free.", "a": "Honour system.", "reward": 2, "penalty": "1 sip"},
        {"q": "MEMORY TEST: The player draws another card and reads only the question. Must answer without any hints. Succeed = 5 spaces. Fail = move back 1.", "a": "No hints from anyone.", "reward": 5, "penalty": "move back 1"},
    ]
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

# ── Helpers ───────────────────────────────────────────────────────────────────
TEAM_COLORS = {
    "team1": "#E85D04",
    "team2": "#2D6A4F",
    "team3": "#7B2D8B",
    "team4": "#1565C0",
}
TEAM_LABELS = {"team1": "Team 1", "team2": "Team 2", "team3": "Team 3", "team4": "Team 4"}

TYPE_LABELS = {
    "trivia": "Trivia",
    "association": "Association",
    "action": "Action",
    "wildcard": "Wildcard",
}
TYPE_COLORS = {
    "trivia": "#1565C0",
    "association": "#2D6A4F",
    "action": "#E85D04",
    "wildcard": "#7B2D8B",
}

def draw_card():
    deck = st.session_state["deck"]
    idx = st.session_state["deck_index"]
    if idx >= len(deck):
        st.session_state["deck"] = get_full_deck()
        st.session_state["deck_index"] = 0
        idx = 0
    card = deck[idx]
    st.session_state["deck_index"] = idx + 1
    st.session_state["current_card"] = card
    st.session_state["card_revealed"] = False
    st.session_state["card_result"] = None

def get_penalty_text(penalty):
    if penalty == "1 sip":
        return "Take 1 sip"
    elif penalty == "3 sips":
        return "Take 3 sips"
    elif penalty == "move back 1":
        return "Move back 1 space"
    return penalty

def get_reward_text(reward):
    return f"Move forward {reward} spaces"

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0f0f0f; }
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
    h1, h2, h3 { font-family: sans-serif; }

    .game-title {
        font-size: 2rem; font-weight: 700; text-align: center;
        color: #FF8C00; letter-spacing: 1px; margin-bottom: 0.2rem;
    }
    .game-sub {
        text-align: center; color: #aaa; font-size: 0.95rem; margin-bottom: 1.5rem;
    }
    .card-box {
        border-radius: 16px; padding: 2rem 1.5rem; text-align: center;
        margin: 1rem 0; border: 2px solid;
    }
    .card-type-badge {
        display: inline-block; border-radius: 20px; padding: 4px 16px;
        font-size: 0.8rem; font-weight: 700; letter-spacing: 1px;
        margin-bottom: 1rem; text-transform: uppercase;
    }
    .card-question {
        font-size: 1.3rem; font-weight: 600; color: #fff;
        line-height: 1.5; margin-bottom: 0.5rem;
    }
    .card-answer {
        font-size: 1rem; color: #ccc; margin-top: 0.75rem;
    }
    .reward-box {
        background: #1a3a1a; border: 1px solid #2D6A4F;
        border-radius: 10px; padding: 0.75rem 1rem; margin-top: 0.75rem;
        color: #6fcf97; font-size: 1rem; font-weight: 600;
    }
    .penalty-box {
        background: #3a1a1a; border: 1px solid #c0392b;
        border-radius: 10px; padding: 0.75rem 1rem; margin-top: 0.75rem;
        color: #e74c3c; font-size: 1rem; font-weight: 600;
    }
    .team-cup-card {
        border-radius: 12px; padding: 1rem; text-align: center; margin-bottom: 0.5rem;
    }
    .cup-dots {
        font-size: 1.5rem; letter-spacing: 4px;
    }
    .player-chip {
        display: inline-block; background: #1e1e1e; border: 1px solid #333;
        border-radius: 20px; padding: 4px 12px; font-size: 0.8rem;
        color: #ddd; margin: 2px;
    }
    .section-label {
        font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px;
        color: #888; margin-bottom: 0.4rem;
    }
    .win-banner {
        background: linear-gradient(135deg, #1a3a1a, #0d2b0d);
        border: 2px solid #27ae60; border-radius: 16px;
        padding: 1.5rem; text-align: center; margin-bottom: 1rem;
    }
    .log-entry {
        font-size: 0.82rem; color: #aaa; padding: 4px 0;
        border-bottom: 1px solid #222;
    }
    div[data-testid="stButton"] button {
        border-radius: 10px; font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ── Login Screen ──────────────────────────────────────────────────────────────
def login_screen():
    st.markdown('<div class="game-title">True American 🇮🇳</div>', unsafe_allow_html=True)
    st.markdown('<div class="game-sub">Desi Edition &mdash; UIUC</div>', unsafe_allow_html=True)

    with st.form("login_form"):
        email = st.text_input("Illinois email", placeholder="netid@illinois.edu")
        name = st.text_input("Your name", placeholder="What do people call you?")
        
        team_options = {tid: st.session_state["teams"].get(tid, {}).get("name", TEAM_LABELS[tid])
                        for tid in ["team1","team2","team3","team4"]}
        team_choice = st.selectbox(
            "Choose your team",
            options=list(team_options.keys()),
            format_func=lambda x: team_options[x]
        )
        submitted = st.form_submit_button("Join the game", use_container_width=True)

    if submitted:
        if not email.endswith("@illinois.edu"):
            st.error("You must use an @illinois.edu email address.")
            return
        if not name.strip():
            st.error("Please enter your name.")
            return
        if email in st.session_state["players"]:
            # Re-login
            p = st.session_state["players"][email]
            st.session_state["logged_in_email"] = email
            st.session_state["logged_in_name"] = p["name"]
            st.session_state["logged_in_team"] = p["team"]
            st.rerun()
        else:
            team_count = sum(1 for p in st.session_state["players"].values() if p["team"] == team_choice)
            if team_count >= 4:
                st.error("That team is full (max 4 players). Pick another team.")
                return
            st.session_state["players"][email] = {
                "name": name.strip(),
                "team": team_choice,
                "joined_at": datetime.now().strftime("%H:%M:%S")
            }
            st.session_state["logged_in_email"] = email
            st.session_state["logged_in_name"] = name.strip()
            st.session_state["logged_in_team"] = team_choice
            st.rerun()

    # Team name setup
    st.markdown("---")
    st.markdown("#### Set team names")
    cols = st.columns(4)
    for i, (tid, col) in enumerate(zip(["team1","team2","team3","team4"], cols)):
        with col:
            current = st.session_state["teams"].get(tid, {}).get("name", f"Team {i+1}")
            new_name = st.text_input(f"Team {i+1} name", value=current, key=f"tname_{tid}")
            if new_name != current:
                if tid not in st.session_state["teams"]:
                    st.session_state["teams"][tid] = {}
                st.session_state["teams"][tid]["name"] = new_name
                if "cups" not in st.session_state["teams"][tid]:
                    st.session_state["teams"][tid]["cups"] = 0

    # Show who's already joined
    if st.session_state["players"]:
        st.markdown("---")
        st.markdown("#### Players who've joined")
        for tid in ["team1","team2","team3","team4"]:
            tname = st.session_state["teams"].get(tid, {}).get("name", TEAM_LABELS[tid])
            members = [p["name"] for p in st.session_state["players"].values() if p["team"] == tid]
            if members:
                color = TEAM_COLORS[tid]
                st.markdown(f'<span style="color:{color}; font-weight:700;">{tname}</span>: ' +
                            " · ".join(members), unsafe_allow_html=True)

# ── Main Game Screen ──────────────────────────────────────────────────────────
def game_screen():
    email = st.session_state["logged_in_email"]
    my_name = st.session_state["logged_in_name"]
    my_team = st.session_state["logged_in_team"]
    my_team_name = st.session_state["teams"].get(my_team, {}).get("name", TEAM_LABELS[my_team])
    my_color = TEAM_COLORS[my_team]

    st.markdown('<div class="game-title">True American 🇮🇳</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="game-sub">Playing as <strong>{my_name}</strong> &mdash; '
                f'<span style="color:{my_color}">{my_team_name}</span></div>', unsafe_allow_html=True)

    # ── Scoreboard ────────────────────────────────────────────────────────────
    st.markdown("### Scoreboard")
    score_cols = st.columns(4)
    winner = None
    for i, (tid, col) in enumerate(zip(["team1","team2","team3","team4"], score_cols)):
        cups = st.session_state["teams"].get(tid, {}).get("cups", 0)
        tname = st.session_state["teams"].get(tid, {}).get("name", TEAM_LABELS[tid])
        color = TEAM_COLORS[tid]
        members = [p["name"] for p in st.session_state["players"].values() if p["team"] == tid]
        filled = "🔴" * cups + "⚪" * max(0, 6 - cups)
        with col:
            st.markdown(
                f'<div class="team-cup-card" style="background:#1a1a1a; border: 2px solid {color};">'
                f'<div style="color:{color}; font-weight:700; font-size:1rem;">{tname}</div>'
                f'<div class="cup-dots" style="margin:6px 0;">{filled}</div>'
                f'<div style="color:#ccc; font-size:0.8rem;">{cups} / 6 cups</div>'
                f'<div style="color:#888; font-size:0.72rem; margin-top:4px;">'
                + (", ".join(members) if members else "No players yet") +
                f'</div></div>',
                unsafe_allow_html=True
            )
        if cups >= 6:
            winner = tname

    if winner:
        st.markdown(
            f'<div class="win-banner"><div style="font-size:2rem;">🏆</div>'
            f'<div style="color:#27ae60; font-size:1.5rem; font-weight:700;">{winner} wins!</div>'
            f'<div style="color:#aaa;">The Scepter of Azadi is forged. Game over!</div></div>',
            unsafe_allow_html=True
        )

    st.markdown("---")

    # ── Two columns: Card + Actions ────────────────────────────────────────────
    left, right = st.columns([3, 2], gap="large")

    with left:
        st.markdown("### Draw a card")
        st.caption("Draw a card for the player in front of you. Trivia = open to everyone. Action = they choose a teammate.")

        if st.button("Draw card", use_container_width=True, type="primary"):
            draw_card()

        card = st.session_state.get("current_card")
        if card:
            ctype = card["type"]
            color = TYPE_COLORS.get(ctype, "#888")
            label = TYPE_LABELS.get(ctype, ctype)

            st.markdown(
                f'<div class="card-box" style="background:#111; border-color:{color};">'
                f'<div class="card-type-badge" style="background:{color}22; color:{color};">{label}</div>'
                f'<div class="card-question">{card["q"]}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

            if not st.session_state.get("card_revealed"):
                if st.button("Reveal answer", use_container_width=True):
                    st.session_state["card_revealed"] = True
                    st.rerun()
            else:
                st.markdown(
                    f'<div style="background:#1a1a2e; border-radius:10px; padding:0.75rem 1rem; '
                    f'color:#ddd; font-size:0.95rem; margin-bottom:0.75rem;">'
                    f'<strong>Answer:</strong> {card["a"]}</div>',
                    unsafe_allow_html=True
                )

                result = st.session_state.get("card_result")
                if result is None:
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("✅  Nailed it", use_container_width=True):
                            st.session_state["card_result"] = "pass"
                            st.session_state["card_log"].append({
                                "player": my_name,
                                "team": my_team_name,
                                "type": label,
                                "result": "pass",
                                "detail": get_reward_text(card["reward"]),
                                "time": datetime.now().strftime("%H:%M:%S"),
                            })
                            st.rerun()
                    with c2:
                        if st.button("❌  Failed", use_container_width=True):
                            st.session_state["card_result"] = "fail"
                            st.session_state["card_log"].append({
                                "player": my_name,
                                "team": my_team_name,
                                "type": label,
                                "result": "fail",
                                "detail": get_penalty_text(card["penalty"]),
                                "time": datetime.now().strftime("%H:%M:%S"),
                            })
                            st.rerun()
                elif result == "pass":
                    st.markdown(
                        f'<div class="reward-box">🎉 Reward: {get_reward_text(card["reward"])}</div>',
                        unsafe_allow_html=True
                    )
                elif result == "fail":
                    st.markdown(
                        f'<div class="penalty-box">💀 Penalty: {get_penalty_text(card["penalty"])}</div>',
                        unsafe_allow_html=True
                    )

    with right:
        st.markdown("### Cup actions")

        st.markdown('<div class="section-label">Chug &amp; win a cup</div>', unsafe_allow_html=True)
        st.caption("When your team's player chugs at the cup spot, add a cup here.")
        cup_team = st.selectbox(
            "Which team got a cup?",
            options=["team1","team2","team3","team4"],
            format_func=lambda x: st.session_state["teams"].get(x, {}).get("name", TEAM_LABELS[x]),
            key="cup_team_select"
        )
        if st.button("Add cup to team", use_container_width=True):
            if cup_team not in st.session_state["teams"]:
                st.session_state["teams"][cup_team] = {"cups": 0}
            if st.session_state["teams"][cup_team].get("cups", 0) < 6:
                st.session_state["teams"][cup_team]["cups"] = st.session_state["teams"][cup_team].get("cups", 0) + 1
                st.session_state["card_log"].append({
                    "player": my_name,
                    "team": my_team_name,
                    "type": "Cup",
                    "result": "cup added",
                    "detail": f"Cup added to {st.session_state['teams'][cup_team]['name']}",
                    "time": datetime.now().strftime("%H:%M:%S"),
                })
                st.rerun()
            else:
                st.warning("That team already has 6 cups!")

        st.markdown("---")
        st.markdown('<div class="section-label">Floor is lava 🌋</div>', unsafe_allow_html=True)
        st.caption("Someone touched the floor? Remove a cup from their team.")
        lava_team = st.selectbox(
            "Which team touched the floor?",
            options=["team1","team2","team3","team4"],
            format_func=lambda x: st.session_state["teams"].get(x, {}).get("name", TEAM_LABELS[x]),
            key="lava_team_select"
        )
        if st.button("Remove cup (lava penalty)", use_container_width=True):
            if lava_team not in st.session_state["teams"]:
                st.session_state["teams"][lava_team] = {"cups": 0}
            current = st.session_state["teams"][lava_team].get("cups", 0)
            if current > 0:
                st.session_state["teams"][lava_team]["cups"] = current - 1
                st.session_state["card_log"].append({
                    "player": my_name,
                    "team": my_team_name,
                    "type": "Lava",
                    "result": "cup removed",
                    "detail": f"Lava penalty on {st.session_state['teams'][lava_team]['name']}",
                    "time": datetime.now().strftime("%H:%M:%S"),
                })
                st.rerun()
            else:
                st.warning("That team has no cups to lose!")

        st.markdown("---")
        st.markdown('<div class="section-label">Actions</div>', unsafe_allow_html=True)
        if st.button("Logout", use_container_width=True):
            st.session_state["logged_in_email"] = None
            st.session_state["logged_in_name"] = None
            st.session_state["logged_in_team"] = None
            st.rerun()
        if st.button("Reset entire game", use_container_width=True):
            for tid in ["team1","team2","team3","team4"]:
                if tid in st.session_state["teams"]:
                    st.session_state["teams"][tid]["cups"] = 0
            st.session_state["players"] = {}
            st.session_state["card_log"] = []
            st.session_state["current_card"] = None
            st.session_state["card_result"] = None
            st.session_state["card_revealed"] = False
            st.session_state["logged_in_email"] = None
            st.session_state["logged_in_name"] = None
            st.session_state["logged_in_team"] = None
            st.session_state["deck"] = get_full_deck()
            st.session_state["deck_index"] = 0
            st.rerun()

    # ── Activity log ──────────────────────────────────────────────────────────
    if st.session_state["card_log"]:
        st.markdown("---")
        st.markdown("### Activity log")
        for entry in reversed(st.session_state["card_log"][-20:]):
            icon = "✅" if entry["result"] == "pass" else ("🔴" if entry["result"] == "cup added" else ("🌋" if entry["result"] == "cup removed" else "❌"))
            st.markdown(
                f'<div class="log-entry">{icon} <strong>{entry["player"]}</strong> ({entry["team"]}) &mdash; '
                f'[{entry["type"]}] {entry["detail"]} <span style="color:#555;">{entry["time"]}</span></div>',
                unsafe_allow_html=True
            )

# ── Router ────────────────────────────────────────────────────────────────────
if st.session_state["logged_in_email"]:
    game_screen()
else:
    login_screen()
