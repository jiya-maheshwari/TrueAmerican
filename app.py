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
        # ── Upgraded from easiest (were reward:2 / 1 sip) ──
        {"q": "Which film featured 'Ek Do Teen' originally, and name the actress who performed it?", "a": "Tezaab (1988); Madhuri Dixit", "reward": 2, "penalty": "1 sip"},
        {"q": "Name the 3 leads of Dil Chahta Hai AND the director.", "a": "Aamir Khan, Akshaye Khanna, Saif Ali Khan; directed by Farhan Akhtar", "reward": 2, "penalty": "1 sip"},
        {"q": "DDLJ released in 1995 — name the director AND the music composer.", "a": "Aditya Chopra; Jatin-Lalit", "reward": 2, "penalty": "1 sip"},
        {"q": "Who directed 3 Idiots and name one other film he directed.", "a": "Rajkumar Hirani; Munna Bhai MBBS / PK / Sanju", "reward": 2, "penalty": "1 sip"},
        {"q": "Which film featured 'Mogambo Khush Hua' and who played Mogambo?", "a": "Mr. India (1987); Amrish Puri", "reward": 2, "penalty": "1 sip"},
        {"q": "Who played Poo in K3G, and name one other character Kareena played in a 2000s Bollywood hit.", "a": "Poo; e.g. Geet in Jab We Met / Kareena in Tashan etc.", "reward": 2, "penalty": "1 sip"},
        {"q": "Lagaan is set during which British Indian period, and roughly what year?", "a": "British colonial era / 1893", "reward": 2, "penalty": "1 sip"},
        {"q": "Kerala is 'God's Own Country' — name its capital and one famous festival.", "a": "Thiruvananthapuram; Onam / Thrissur Pooram", "reward": 2, "penalty": "1 sip"},
        {"q": "Rabindranath Tagore wrote India's national anthem — name the other country whose anthem he also wrote.", "a": "Bangladesh (Amar Shonar Bangla)", "reward": 3, "penalty": "2 sips"},
        {"q": "India's national animal is the Bengal Tiger — what is the national bird?", "a": "Indian Peacock (Pavo cristatus)", "reward": 2, "penalty": "1 sip"},
        {"q": "Gateway of India is in Mumbai — in which year was it built and for which royal visit?", "a": "1924; King George V and Queen Mary", "reward": 3, "penalty": "2 sips"},
        {"q": "India currently has 28 states — how many Union Territories?", "a": "8 Union Territories", "reward": 2, "penalty": "1 sip"},
        {"q": "Kolkata is the 'City of Joy' — name the author who wrote a book with that title.", "a": "Dominique Lapierre", "reward": 3, "penalty": "2 sips"},
        {"q": "Salman Khan is 'Bhai' — name all three of his Tiger franchise films.", "a": "Ek Tha Tiger, Tiger Zinda Hai, Tiger 3", "reward": 3, "penalty": "2 sips"},
        {"q": "Gabbar Singh is the villain in Sholay — what is his most famous dialogue?", "a": "Kitne aadmi the? / Jo dar gaya, samjho mar gaya", "reward": 2, "penalty": "1 sip"},
        {"q": "Which film had 'Chaiyya Chaiyya' and who was the playback singer?", "a": "Dil Se (1998); Sukhwinder Singh", "reward": 2, "penalty": "1 sip"},
        {"q": "Bengaluru is the Silicon Valley of India — name India's second-largest IT hub city.", "a": "Hyderabad (or Pune)", "reward": 2, "penalty": "1 sip"},
        {"q": "Abhinav Bindra won India's first individual Olympic gold — in which event and which city?", "a": "10m Air Rifle; Beijing 2008", "reward": 3, "penalty": "2 sips"},
        {"q": "Rahul Dravid is 'The Wall' — how many Test centuries did he score?", "a": "36 Test centuries", "reward": 3, "penalty": "2 sips"},
        {"q": "What does IPL stand for, and in which year was the first season played?", "a": "Indian Premier League; 2008", "reward": 2, "penalty": "1 sip"},
        {"q": "Zindagi Na Milegi Dobara — name all three lead actors and one country it was filmed in.", "a": "Hrithik Roshan, Farhan Akhtar, Abhay Deol; Spain", "reward": 3, "penalty": "2 sips"},
        {"q": "What is the full form of DDLJ, and where was the iconic mustard field scene shot?", "a": "Dilwale Dulhania Le Jayenge; Punjab / UK (filmed in UK)", "reward": 2, "penalty": "1 sip"},
        {"q": "SRK played Aman in Kal Ho Na Ho — name the director of that film.", "a": "Nikkhil Advani", "reward": 3, "penalty": "2 sips"},
        {"q": "Holi is the festival of colours — in which Hindu month does it traditionally fall?", "a": "Phalguna (Feb–March)", "reward": 3, "penalty": "2 sips"},
        {"q": "Name the highest civilian award in India and two people who received it posthumously.", "a": "Bharat Ratna; e.g. Lata Mangeshkar (posthumous), Subhas Chandra Bose, BR Ambedkar etc.", "reward": 3, "penalty": "2 sips"},
        {"q": "Arijit Singh sang 'Tum Hi Ho' — name the film and the lead actors.", "a": "Aashiqui 2; Aditya Roy Kapur and Shraddha Kapoor", "reward": 2, "penalty": "1 sip"},
        {"q": "Sachin Tendulkar has the most ODI centuries — how many, and who is second?", "a": "49 centuries; Virat Kohli (50 in all formats but 46 in ODIs — accept reasonable answers)", "reward": 3, "penalty": "2 sips"},
        {"q": "Amitabh Bachchan's 'angry young man' era began with Zanjeer — name the writer duo behind it.", "a": "Salim-Javed (Salim Khan & Javed Akhtar)", "reward": 3, "penalty": "2 sips"},
        {"q": "Which Bollywood film is based on the 1983 Cricket World Cup and who plays Kapil Dev?", "a": "83 (2021); Ranveer Singh", "reward": 2, "penalty": "1 sip"},
        {"q": "Which Indian state produces the most tea, and name one famous variety from it?", "a": "Assam; Assam CTC / Assam Orthodox / Brahmaputra tea", "reward": 3, "penalty": "2 sips"},
        # ── Medium originals (kept as-is) ──
        {"q": "Who composed the music for Mughal-E-Azam?", "a": "Naushad", "reward": 3, "penalty": "3 sips"},
        {"q": "Which film won the first Indian Oscar nomination in 1958?", "a": "Mother India", "reward": 3, "penalty": "3 sips"},
        {"q": "Which Bollywood film is set in a fictional kingdom called Rajputana?", "a": "Padmaavat", "reward": 3, "penalty": "3 sips"},
        {"q": "Which city hosts the Kumbh Mela most famously?", "a": "Prayagraj (Allahabad)", "reward": 3, "penalty": "3 sips"},
        {"q": "Which film won Aamir Khan his first Filmfare Best Actor?", "a": "Raja Hindustani (1996)", "reward": 3, "penalty": "3 sips"},
        {"q": "Who is known as 'The Maestro' of Indian classical music?", "a": "Ravi Shankar", "reward": 3, "penalty": "3 sips"},
        {"q": "Name the Indian who invented the game of Snakes and Ladders.", "a": "Gyandev (13th century)", "reward": 4, "penalty": "move back 1"},
        # ── NEW harder trivia cards ──
        {"q": "Name the only Indian film to win the Palme d'Or at Cannes and its director.", "a": "No Indian film has won — accept 'none' or discussions of Salaam Bombay (1988, nominated)", "reward": 4, "penalty": "move back 1"},
        {"q": "Which Indian cricketer has the most Test wickets and how many?", "a": "Anil Kumble; 619 wickets", "reward": 3, "penalty": "3 sips"},
        {"q": "Name the three Khans of Bollywood AND each one's biggest 2010s blockbuster.", "a": "Shah Rukh (Chennai Express/Dilwale), Salman (Bajrangi Bhaijaan/Sultan), Aamir (Dangal/PK)", "reward": 4, "penalty": "move back 1"},
        {"q": "Which year did India win both the Cricket World Cup AND the Champions Trophy?", "a": "2013 (Champions Trophy); 1983 & 2011 (World Cup) — full answer: 2013 for CT", "reward": 4, "penalty": "3 sips"},
        {"q": "Name Gulzar's birth name and one National Award-winning film he wrote.", "a": "Sampooran Singh Kalra; Maachis / Ijaazat / Aandhi etc.", "reward": 4, "penalty": "move back 1"},
        {"q": "Which Hindi film holds the record for most weeks at #1 at the Indian box office?", "a": "Sholay (ran for over 5 years at some cinemas; 286 weeks at Minerva in Mumbai)", "reward": 4, "penalty": "3 sips"},
        {"q": "Name the singer, lyricist, and music director of 'Jai Ho' from Slumdog Millionaire.", "a": "Sukhwinder Singh (singer); Gulzar (lyrics); AR Rahman (music)", "reward": 4, "penalty": "move back 1"},
        {"q": "How many Filmfare awards has SRK won in total (approximately)?", "a": "14 Filmfare Awards (accept 12–16 range)", "reward": 3, "penalty": "2 sips"},
        {"q": "Which Indian state has the most UNESCO World Heritage Sites?", "a": "Maharashtra (Ajanta, Ellora, Elephanta, Mumbai Victorian Gothic & Art Deco)", "reward": 4, "penalty": "3 sips"},
        {"q": "Name the two Indian players in the ICC Cricket Hall of Fame as of 2023.", "a": "Sachin Tendulkar, Kapil Dev, Bishan Singh Bedi, Sunil Gavaskar (accept any two)", "reward": 3, "penalty": "2 sips"},
        {"q": "In Taare Zameen Par, what learning disability does Ishaan have, and who directed the film?", "a": "Dyslexia; Aamir Khan", "reward": 3, "penalty": "2 sips"},
        {"q": "Which classic Bollywood film was remade as 'The Magnificent Seven' of Indian cinema and features the song 'Yeh Dosti'?", "a": "Sholay", "reward": 3, "penalty": "2 sips"},
        {"q": "Name India's first satellite and the year it was launched.", "a": "Aryabhata; 1975", "reward": 4, "penalty": "3 sips"},
        {"q": "Which Indian author wrote 'The God of Small Things' and won the Booker Prize?", "a": "Arundhati Roy; 1997", "reward": 3, "penalty": "2 sips"},
        {"q": "In Kabir Singh / Arjun Reddy, who directed the original Telugu version?", "a": "Sandeep Reddy Vanga", "reward": 3, "penalty": "2 sips"},
        {"q": "Which Indian badminton player won back-to-back Olympics silver and bronze medals?", "a": "PV Sindhu (Silver 2016, Bronze 2020)", "reward": 3, "penalty": "2 sips"},
        {"q": "Name the actor who played Bhiku Mhatre in Satya (1998) — the film that launched his career.", "a": "Manoj Bajpayee", "reward": 3, "penalty": "2 sips"},
        {"q": "What is the real name of rapper Divine, the inspiration behind Gully Boy?", "a": "Vivian Fernandes", "reward": 4, "penalty": "3 sips"},
        {"q": "In which year did Doordarshan begin colour broadcasts in India?", "a": "1982 (during the Asian Games in Delhi)", "reward": 4, "penalty": "move back 1"},
        {"q": "Which Indian city is home to Tollywood (Telugu film industry)?", "a": "Hyderabad (Film City in Hyderabad)", "reward": 2, "penalty": "1 sip"},
        {"q": "Name the Indian wrestler who won a gold medal at the 2018 Commonwealth Games and inspired Dangal.", "a": "Geeta Phogat (the film is inspired by the Phogat family, including Geeta & Babita)", "reward": 3, "penalty": "2 sips"},
    ],
    "association": [
        # ── Upgraded from easiest (were reward:2 / 1 sip) ──
        {"q": "Shah Rukh Khan & Kajol", "a": "DDLJ / romantic Bollywood pair", "reward": 2, "penalty": "1 sip"},
        {"q": "Sachin & Dravid", "a": "India's greatest batting pair / cricket legends", "reward": 2, "penalty": "1 sip"},
        {"q": "Holi & Diwali", "a": "Major Hindu festivals", "reward": 2, "penalty": "1 sip"},
        {"q": "Ranbir Kapoor & Alia Bhatt", "a": "Married couple / Brahmastra co-stars", "reward": 2, "penalty": "1 sip"},
        {"q": "Chennai & Kolkata", "a": "IPL teams / India metro cities", "reward": 2, "penalty": "1 sip"},
        {"q": "Paneer & Tofu", "a": "Vegetarian protein / soft white cheese alternatives", "reward": 2, "penalty": "1 sip"},
        {"q": "Rasgulla & Gulab Jamun", "a": "Indian mithai / syrup-soaked sweets", "reward": 2, "penalty": "1 sip"},
        {"q": "Virat Kohli & MS Dhoni", "a": "Indian cricket captains", "reward": 2, "penalty": "1 sip"},
        {"q": "Mumbai & Delhi", "a": "India's two biggest metro cities", "reward": 2, "penalty": "1 sip"},
        {"q": "Naan & Roti", "a": "Indian flatbreads", "reward": 2, "penalty": "1 sip"},
        {"q": "Rohit Sharma & Shikhar Dhawan", "a": "India's ODI opening pair", "reward": 2, "penalty": "1 sip"},
        {"q": "Rajasthan & Gujarat", "a": "Neighbouring western Indian states", "reward": 2, "penalty": "1 sip"},
        {"q": "Masala chai & Filter coffee", "a": "Iconic Indian hot beverages", "reward": 2, "penalty": "1 sip"},
        {"q": "Salman Khan & Katrina Kaif", "a": "Tiger franchise / former rumoured couple", "reward": 2, "penalty": "1 sip"},
        {"q": "Bhangra & Garba", "a": "Regional Indian folk dances (Punjab & Gujarat)", "reward": 2, "penalty": "1 sip"},
        {"q": "Gandhi & Nehru", "a": "Indian independence movement leaders", "reward": 2, "penalty": "1 sip"},
        {"q": "Samosa & Pakora", "a": "Classic Indian fried street snacks", "reward": 2, "penalty": "1 sip"},
        {"q": "KBC & Bigg Boss", "a": "India's biggest TV game/reality shows", "reward": 2, "penalty": "1 sip"},
        # ── Medium originals (kept) ──
        {"q": "Amitabh Bachchan & Dharmendra", "a": "Sholay", "reward": 3, "penalty": "3 sips"},
        {"q": "Biryani & Nihari", "a": "Mughlai cuisine", "reward": 3, "penalty": "3 sips"},
        {"q": "Arijit Singh & Atif Aslam", "a": "Bollywood/Pakistani playback singers", "reward": 3, "penalty": "3 sips"},
        {"q": "Karan Johar & Farah Khan", "a": "Bollywood directors and best friends", "reward": 3, "penalty": "3 sips"},
        {"q": "Taj Mahal & Qutub Minar", "a": "UNESCO Mughal-era World Heritage Sites", "reward": 3, "penalty": "3 sips"},
        {"q": "Priyanka Chopra & Deepika Padukone", "a": "Bollywood actresses turned global icons", "reward": 3, "penalty": "3 sips"},
        {"q": "AR Rahman & Anu Malik", "a": "Bollywood music composers", "reward": 3, "penalty": "3 sips"},
        {"q": "Akbar & Ashoka", "a": "India's greatest emperors", "reward": 3, "penalty": "3 sips"},
        {"q": "Paan & Supari", "a": "Post-meal Indian mouth fresheners", "reward": 3, "penalty": "3 sips"},
        {"q": "Lata Mangeshkar & Asha Bhosle", "a": "Legendary playback singer sisters", "reward": 3, "penalty": "3 sips"},
        {"q": "Rang De Basanti & Swades", "a": "Patriotic Bollywood films of the 2000s", "reward": 3, "penalty": "3 sips"},
        {"q": "Doordarshan & Star Plus", "a": "Indian television channels (government vs. private)", "reward": 3, "penalty": "3 sips"},
        # ── NEW harder association cards ──
        {"q": "Naseeruddin Shah & Om Puri", "a": "Parallel cinema legends / FTII alumni", "reward": 3, "penalty": "3 sips"},
        {"q": "Rekha & Amitabh Bachchan", "a": "Bollywood's most legendary rumoured affair / Silsila", "reward": 3, "penalty": "2 sips"},
        {"q": "Vishal & Shekhar", "a": "Bollywood composer duo (Vishal Dadlani & Shekhar Ravjiani)", "reward": 4, "penalty": "3 sips"},
        {"q": "Shoojit Sircar & Juhi Chaturvedi", "a": "Director-writer duo (Piku, Vicky Donor, Gulabo Sitabo)", "reward": 4, "penalty": "move back 1"},
        {"q": "Baahubali & RRR", "a": "SS Rajamouli's epic Telugu blockbusters", "reward": 3, "penalty": "2 sips"},
        {"q": "Diljit Dosanjh & AP Dhillon", "a": "Punjabi artists who broke internationally", "reward": 3, "penalty": "2 sips"},
        {"q": "Irrfan Khan & Nawazuddin Siddiqui", "a": "Critically acclaimed character actors from parallel Bollywood", "reward": 3, "penalty": "2 sips"},
        {"q": "Shankar, Ehsaan & Loy", "a": "Bollywood composer trio (Dil Chahta Hai, Kal Ho Na Ho)", "reward": 4, "penalty": "3 sips"},
        {"q": "Pooja Bhatt & Mahesh Bhatt", "a": "Father-daughter Bollywood filmmaker duo", "reward": 3, "penalty": "2 sips"},
        {"q": "Sacred Games & Mirzapur", "a": "Indian crime drama web series (Netflix & Prime)", "reward": 3, "penalty": "2 sips"},
        {"q": "Panchayat & Kota Factory", "a": "TVF Indian web series", "reward": 3, "penalty": "2 sips"},
        {"q": "Yo Yo Honey Singh & Badshah", "a": "Desi hip-hop / Punjabi rap artists", "reward": 2, "penalty": "1 sip"},
        {"q": "Zoya Akhtar & Reema Kagti", "a": "Director-writer duo (Gully Boy, Talaash, Made in Heaven)", "reward": 4, "penalty": "move back 1"},
        {"q": "Rajkummar Rao & Pankaj Tripathi", "a": "Mirzapur / critically acclaimed actors from small-town India", "reward": 3, "penalty": "2 sips"},
        {"q": "Chhod Do Aanchal & Mera Joota Hai Japani", "a": "Classic Raj Kapoor songs / 1950s Bollywood", "reward": 4, "penalty": "move back 1"},
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
        {"q": "Say the tongue twister 'Kaccha papad, pakka papad' 5 times fast.", "a": "No mistakes allowed.", "reward": 3, "penalty": "1 sip"},
        {"q": "Impersonate any Bollywood villain for 10 seconds.", "a": "Group votes.", "reward": 4, "penalty": "3 sips"},
        {"q": "Do the Daler Mehndi 'Tunak Tunak' arm move for 15 seconds.", "a": "Full commitment required.", "reward": 3, "penalty": "1 sip"},
        {"q": "Recreate the Sholay 'Kitne aadmi the?' dialogue exchange with another player.", "a": "Both must know their lines.", "reward": 4, "penalty": "3 sips"},
        {"q": "Hum any Bollywood song. Others must guess the film within 15 seconds.", "a": "No words, only humming.", "reward": 3, "penalty": "1 sip"},
        {"q": "Do an impression of an Indian mom scolding someone for 15 seconds — must include a chappai threat.", "a": "Group votes pass/fail.", "reward": 3, "penalty": "2 sips"},
        {"q": "Say the English alphabet backwards in 20 seconds.", "a": "Timed. Fail = miss a letter.", "reward": 4, "penalty": "move back 1"},
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
        # ── NEW action cards ──
        {"q": "Do your best 'Lungi Dance' move for 10 seconds — full energy.", "a": "Group votes pass/fail. No half-measures.", "reward": 4, "penalty": "2 sips"},
        {"q": "In an Indian accent, pitch a saas-bahu show to the group in 20 seconds.", "a": "Must include a villain, a crying scene, and a dramatic pause.", "reward": 4, "penalty": "3 sips"},
        {"q": "Recreate the Kuch Kuch Hota Hai basketball game — you need one other person, no ball needed.", "a": "Group votes on commitment.", "reward": 4, "penalty": "2 sips"},
        {"q": "You are a news anchor on Arnab Goswami mode. Report on whatever snack is nearest to you. 20 seconds.", "a": "Volume and intensity judged by group.", "reward": 4, "penalty": "3 sips"},
        {"q": "Do an impression of a Bollywood hero proposing in the rain for 15 seconds.", "a": "Must reference flowers, slow-mo, and eye contact.", "reward": 4, "penalty": "2 sips"},
        {"q": "Without using the words 'film', 'movie', 'Bollywood', describe Dilwale Dulhania Le Jayenge in 30 seconds. Group must guess.", "a": "Timed. No banned words.", "reward": 4, "penalty": "3 sips"},
        {"q": "Mime a classic Bollywood death scene for 15 seconds. Group must name the film it reminds them of.", "a": "Most dramatic mime wins the group's approval.", "reward": 4, "penalty": "2 sips"},
        {"q": "Teach the group a 10-second hook-step from any song that is NOT from the 90s.", "a": "Song must be named. Group replicates it.", "reward": 4, "penalty": "2 sips"},
        {"q": "Do a 20-second impression of a strict Indian college professor catching someone cheating.", "a": "Group votes pass/fail.", "reward": 3, "penalty": "2 sips"},
        {"q": "You have 15 seconds to beatbox the tune of 'Bole Chudiyan'. Go.", "a": "Group votes pass/fail.", "reward": 3, "penalty": "1 sip"},
        {"q": "Act out ordering a large family meal at a dhaba — you are simultaneously 4 different family members all disagreeing.", "a": "All 4 voices required. Group votes.", "reward": 5, "penalty": "move back 1"},
        {"q": "Sing 10 seconds of a Himesh Reshammiya song in his exact nasal style — nose movement mandatory.", "a": "Group votes. Authenticity judged harshly.", "reward": 3, "penalty": "2 sips"},
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
        # ── NEW wildcard cards ──
        {"q": "TEAM ROAST: Your team has 90 seconds to roast any other team. The roasted team votes 1–10. Score below 6 = your whole team takes 2 sips each.", "a": "Keep it fun. Group rates.", "reward": 4, "penalty": "2 sips"},
        {"q": "ACCENT ROULETTE: Everyone speaks in a different Indian regional accent for the next 3 turns. Whoever breaks first takes 3 sips.", "a": "Accents assigned by group (Punjabi, Tamilian, Bengali, Hyderabadi, etc.)", "reward": 3, "penalty": "3 sips"},
        {"q": "WRONG LYRICS: Sing any Bollywood chorus with completely wrong (but plausible-sounding) lyrics. Group votes if it was convincing.", "a": "Must be sung, not spoken.", "reward": 3, "penalty": "2 sips"},
        {"q": "WEDDING DJ: You are the DJ at a desi wedding. Call out 3 songs back to back (just the titles and first line). Group must vote if they'd dance.", "a": "Need 3 different songs. Majority vote decides.", "reward": 3, "penalty": "1 sip"},
        {"q": "SHAADI NEGOTIATION: Two players. One is the bride's father, one is the groom's father negotiating the wedding venue. 45 seconds. Funniest outcome wins.", "a": "Group votes winner. Loser takes 2 sips.", "reward": 4, "penalty": "2 sips"},
        {"q": "WHATSAPP FORWARD: Deliver the most convincing fake 'good morning' WhatsApp uncle/aunty forward in 20 seconds. Must include a motivational quote and a God's blessing.", "a": "Group votes most authentic.", "reward": 3, "penalty": "1 sip"},
        {"q": "POWER MOVE: You may add 1 cup to your team's score right now — BUT you must first do 20 push-ups, accepted or not by the group.", "a": "Push-ups must be full. Group counts.", "reward": 5, "penalty": "move back 1"},
        {"q": "BOLLYWOOD BINGO: Name a Bollywood film for every letter in 'INDIA' in 30 seconds. All 5 must be different.", "a": "I-N-D-I-A. No repeats. Timed.", "reward": 4, "penalty": "3 sips"},
        {"q": "DESI CONFESSIONAL: Confess the most 'desi parent nightmare' thing you did in college without getting caught. Group votes if believable.", "a": "Honour system. Vote decides.", "reward": 3, "penalty": "1 sip"},
        {"q": "FREEZE FRAME: Call 'Freeze!' — everyone must hold their position for 15 seconds. Anyone who moves, their team loses 1 sip each. You move 3 spaces free.", "a": "You are exempt. Everyone else freezes.", "reward": 3, "penalty": "3 sips"},
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
    elif penalty == "2 sips":
        return "Take 2 sips"
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
