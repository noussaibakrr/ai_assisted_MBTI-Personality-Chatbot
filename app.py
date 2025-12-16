from flask import Flask, request, jsonify, render_template
from transformers import pipeline
import logging

app = Flask(__name__)

# ---------------- LOGGING ---------------- #
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------- MODEL LOADER ---------------- #
print("Loading FLAN-T5 Model...")
nlu_model = pipeline(
    "text2text-generation", 
    model="google/flan-t5-base", 
    framework="pt"
)
print("Model Loaded Successfully!")

# ---------------- MBTI DATA (Knowledge Base) ---------------- #
MMBTI_DATA = {
    "INTJ": {
        "name": "The Architect",
        "population": "2.1%",
        "description": [
            "Strategic and analytical thinker",
            "Highly independent and self-motivated",
            "Prefers long-term planning",
            "Values logic over emotions"
        ],
        "color": "#5e548e",
        "long_description": (
        "People with the INTJ personality type (Architects) are intellectually curious individuals with a deep-seated thirst for knowledge. INTJs tend to value creative ingenuity, straightforward rationality, and self-improvement. They consistently work toward enhancing intellectual abilities and are often driven by an intense desire to master any and every topic that piques their interest."
    ),
        "characters": [
            {"name": "Batman", "img": "batman.jpg"},
            {"name": "Gandalf", "img": "Gandalf.jpg"}
        ]
    },

    "INTP": {
        "name": "The Thinker",
        "population": "3.3%",
        "description": [
            "Logical and objective problem-solver",
            "Enjoys abstract theories and ideas",
            "Highly curious and analytical",
            "Values knowledge and understanding"
        ],
        "color": "#5e548e",
         "long_description": (
        "People with the INTP personality type (Logicians) pride themselves on their unique perspective and vigorous intellect. They can’t help but puzzle over the mysteries of the universe – which may explain why some of the most influential philosophers and scientists of all time have been INTPs. People with this personality type tend to prefer solitude, as they can easily become immersed in their thoughts when they are left to their own devices. They are also incredibly creative and inventive, and they are not afraid to express their novel ways of thinking or to stand out from the crowd."
    ),
        "characters": [
            {"name": "L (Death Note)", "img": "l.jpg"},
            {"name": "sherlock Holmes", "img": "sherlok.jpg"}
        ]
    },

    "ENTJ": {
        "name": "The Commander",
        "population": "1.8%",
        "description": [
            "Confident and decisive leader",
            "Strategic and goal-oriented",
            "Values efficiency and structure",
            "Strong organizational skills"
        ],
         "long_description": (
        "While ENTPs love to brainstorm and think big, these personalities tend to avoid getting caught doing the “grunt work” of implementing their ideas, and they sometimes have a hard time sticking to their goals. To some extent, this makes sense – they have far too many thoughts and suggestions to keep track of them all, let alone turn them into reality. But unless ENTPs develop the willingness to identify and actually follow through on their priorities, they may struggle to harness their full potential."
    ),
        "color": "#5e548e",
        "characters": [
            {"name": "Light Yagami", "img": "light.jpg"},
            {"name": "Patrick Bateman", "img": "bateman.jpg"}
        ]
    },

    "ENTP": {
        "name": "The Debater",
        "population": "3.2%",
        "description": [
            "Energetic and quick-witted",
            "Enjoys exploring new ideas",
            "Excellent communicator",
            "Thrives on intellectual challenges"
        ],
        "color": "#5e548e",
        "long_description": (
        "People with the ENTJ personality type (Commanders) are natural-born leaders. Embodying the gifts of charisma and confidence, ENTJs project authority in a way that draws crowds together behind a common goal. However, these personalities are also characterized by an often ruthless level of rationality, using their drive, determination, and sharp mind to achieve whatever objectives they’ve set for themselves. Their intensity might sometimes rub people the wrong way, but ultimately, ENTJs take pride in both their work ethic and their impressive level of self-discipline."),
        "characters": [
            {"name": "Iron Man", "img": "ironman.jpg"},
            {"name": "The Joker", "img": "joker.jpg"}
        ]
    },

    "INFJ": {
        "name": "The Advocate",
        "population": "1.5%",
        "description": [
            "Insightful and idealistic",
            "Driven by strong personal values",
            "Empathetic and compassionate",
            "Seeks meaning and purpose"
        ],
        "color": "#88d498",
        "long_description": (
        "Idealistic and principled, people with the INFJ personality type (Advocates) aren’t content to coast through life – they want to stand up and make a difference. For these compassionate personalities, success doesn’t come from money or status but from seeking fulfillment, helping others, and being a force for good in the world."
        ),
        "characters": [
            {"name": "Itachi Uchiha", "img": "itachi.jpg"},
            {"name": "Elsa", "img": "elsa.jpg"}
        ]
    },

    "INFP": {
        "name": "The Mediator",
        "population": "4.4%",
        "description": [
            "Deeply empathetic and idealistic",
            "Strong sense of personal values",
            "Creative and imaginative",
            "Seeks harmony and authenticity"
        ],
        "color": "#88d498",
         "long_description": (
        "Although they may seem quiet or unassuming, people with the INFP personality type (Mediators) have vibrant, passionate inner lives. Creative and imaginative, they happily lose themselves in daydreams, inventing all sorts of stories and conversations in their mind. INFPs are known for their sensitivity – these personalities can have profound emotional responses to music, art, nature, and the people around them. They are known to be extremely sentimental and nostalgic, often holding onto special keepsakes and memorabilia that brighten their days and fill their heart with joy."
        ),
        "characters": [
            {"name": "Frodo Baggins", "img": "frodo.jpg"},
            {"name": "Joker (2019)", "img": "joker_arthur.jpg"}
        ]
    },

    "ENFJ": {
        "name": "The Protagonist",
        "population": "2.5%",
        "description": [
            "Charismatic and inspiring",
            "Highly empathetic and supportive",
            "Natural leader",
            "Values cooperation and harmony"
        ],
        "color": "#88d498",
        "long_description": (
        "People with the ENFJ personality type (Protagonists) feel called to serve a greater purpose in life. Thoughtful and idealistic, ENFJs strive to have a positive impact on other people and the world around them. These personalities rarely shy away from an opportunity to do the right thing, even when doing so is far from easy."
        ),
        "characters": [
            {"name": "Tanjiro Kamado", "img": "tanjiro.jpg"},
            {"name": "Wonder Woman", "img": "wonderwoman.jpg"}
        ]
    },

    "ENFP": {
        "name": "The Campaigner",
        "population": "8.1%",
        "description": [
            "Enthusiastic and creative",
            "Values emotional connections",
            "Open-minded and adaptable",
            "Seeks meaning in experiences"
        ],
        "long_description": (
        "People with the ENFP personality type (Campaigners) are true free spirits – outgoing, openhearted, and open-minded. With their lively, upbeat approach to life, ENFPs stand out in any crowd. But even though they can be the life of the party, they don’t just care about having a good time. These personalities have profound depths that are fueled by their intense desire for meaningful, emotional connections with others."
        ),
        "color": "#88d498",
        "characters": [
            {"name": "Naruto Uzumaki", "img": "naruto.jpg"},
            {"name": "Spider-Man", "img": "spiderman.jpg"}
        ]
    },

    "ISTJ": {
        "name": "The Logistician",
        "population": "11.6%",
        "description": [
            "Responsible and dependable",
            "Values tradition and order",
            "Detail-oriented and practical",
            "Strong sense of duty"
        ],
        "long_description": (
        "People with the ISTJ personality type (Logisticians) mean what they say and say what they mean, and when they commit to doing something, they make sure to follow through. With their responsible and dependable nature, it might not be so surprising that ISTJ personalities also tend to have a deep respect for structure and tradition. They are often drawn to organizations, workplaces, and educational settings that offer clear hierarchies and expectations."
        ),
        "color": "#4ea8de",
        "characters": [
            {"name": "Hermione Granger", "img": "hermonie.jpg"},
            {"name": "Mikasa Ackerman", "img": "mikasa.jpg"}
        ]
    },

    "ISFJ": {
        "name": "The Defender",
        "population": "13.8%",
        "description": [
            "Caring and loyal",
            "Strong sense of responsibility",
            "Detail-oriented and patient",
            "Values harmony and stability"
        ],
        "long_description": (
        "In their unassuming, understated way, people with the ISFJ personality type (Defenders) help make the world go round. Hardworking and devoted, these personalities feel a deep sense of responsibility to those around them. ISFJs can be counted on to meet deadlines, remember birthdays and special occasions, uphold traditions, and shower their loved ones with gestures of care and support. But they rarely demand recognition for all that they do, preferring instead to operate behind the scenes."
        ),
        "color": "#4ea8de",
        "characters": [
            {"name": "Captain America", "img": "cap.jpg"},
            {"name": "Hinata Hyuga", "img": "hinata.jpg"}
        ]
    },

    "ESTJ": {
        "name": "The Executive",
        "population": "8.7%",
        "description": [
            "Organized and decisive",
            "Strong leadership skills",
            "Values rules and structure",
            "Results-oriented"
        ],
        "long_description": (
        "People with the ESTJ personality type (Executives) are representatives of tradition and order, utilizing their understanding of what is right, wrong, and socially acceptable to bring families and communities together. Embracing the values of honesty and dedication, ESTJs are valued for their mentorship mindset and their ability to create and follow through on plans in a diligent and efficient manner. They will happily lead the way on difficult paths, and they won’t give up when things become stressful."
        ),
        "color": "#4ea8de",
        "characters": [
            {"name": "Dwight Schrute", "img": "dwight.jpg"},
            {"name": "Vegeta", "img": "vegeta.jpg"}
        ]
    },

    "ESFJ": {
        "name": "The Consul",
        "population": "12.3%",
        "description": [
            "Warm and sociable",
            "Strong sense of duty",
            "Values cooperation",
            "Enjoys helping others"
        ],
        "long_description": (
        "For people with the ESFJ personality type (Consuls), life is sweetest when it’s shared with others. These social individuals form the bedrock of many communities, opening their homes – and their hearts – to friends, loved ones, and neighbors."
        ),
        "color": "#4ea8de",
        "characters": [
            {"name": "SpongeBob", "img": "spongebob.jpg"},
            {"name": "Sakura Haruno", "img": "sakura.jpg"}
        ]
    },

    "ISTP": {
        "name": "The Virtuoso",
        "population": "5.4%",
        "description": [
            "Practical and hands-on",
            "Calm under pressure",
            "Enjoys problem-solving",
            "Values independence"
        ],
        "long_description": (
        "People with the ISTP personality type (Virtuosos) love to explore with their hands and their eyes, touching and examining the world around them with an impressive diligence, a casual curiosity, and a healthy dose of skepticism. They are natural makers, moving from project to project, building the useful and the superfluous for the fun of it and learning from their environment as they go. They find no greater joy than in getting their hands dirty pulling things apart and putting them back together, leaving them just a little bit better than they were before."
        ),
        "color": "#ffd166",
        "characters": [
            {"name": "Levi Ackerman", "img": "levi.jpg"},
            {"name": "Shrek", "img": "shrek.jpg"}
        ]
    },

    "ISFP": {
        "name": "The Adventurer",
        "population": "8.8%",
        "description": [
            "Artistic and sensitive",
            "Lives in the present moment",
            "Strong personal values",
            "Avoids conflict"
        ],
        "long_description": (
        "People with the ISFP personality type (Adventurers) are true artists – although not necessarily in the conventional sense. For these types, life itself is a canvas for self-expression. From what they wear to how they spend their free time, they act in ways that vividly reflect who they are as unique individuals. With their exploratory spirit and their ability to find joy in everyday life, ISFPs can be among the most interesting people you’ll ever meet."
        ),
        "color": "#ffd166",
        "characters": [
            {"name": "Harry Potter", "img": "harry.jpg"},
            {"name": "Eren Yeager", "img": "eren.jpg"}
        ]
    },

    "ESTP": {
        "name": "The Entrepreneur",
        "population": "4.3%",
        "description": [
            "Energetic and action-oriented",
            "Thrives in fast-paced environments",
            "Practical decision-maker",
            "Enjoys taking risks"
        ],
        "long_description": (
        "People with the ESTP personality type (Entrepreneurs) are vibrant individuals brimming with an enthusiastic and spontaneous energy. They tend to be on the competitive side, often assuming that a competitive mindset is a necessity in order to achieve success in life. With their driven, action-oriented attitudes, they rarely waste time thinking about the past. In fact, they excel at keeping their attention rooted in their present – so much so that they rarely find themselves fixated on the time throughout the day."
        ),
        "color": "#ffd166",
        "characters": [
            {"name": "Thor", "img": "thor.jpg"},
            {"name": "Rocket Raccoon", "img": "rocket.jpg"}
        ]
    },

    "ESFP": {
        "name": "The Entertainer",
        "population": "8.5%",
        "description": [
            "Outgoing and spontaneous",
            "Loves new experiences",
            "Highly expressive",
            "Enjoys making others happy"
        ],
        "long_description": (
        "If anyone is to be found spontaneously breaking into song and dance, it is people with the ESFP personality type (Entertainers). They get caught up in the excitement of the moment and want everyone else to feel that way too. No other type is as generous with their time and energy when it comes to encouraging others, and no other type does it with such irresistible style."
          ),
        "color": "#ffd166",
        "characters": [
            {"name": "Goku", "img": "goku.jpg"},
            {"name": "Luffy", "img": "luffy.jpg"}
        ]
    }
}
# ---------------- KEYWORD DICTIONARY ---------------- #
KEYWORDS = {
    # Introversion (I)
    "I": [
        "alone", "quiet", "home", "book", "read", "solitude", "recharge", "tired", 
        "private", "peace", "calm", "reflect", "listen", "withdraw", "intimate", 
        "inner", "silence", "exhausted", "myself", "room", "cozy", "movie", "stay in"
    ],
    # Extraversion (E)
    "E": [
        "party", "friend", "social", "people", "talk", "meet", "energy", "fun", 
        "loud", "group", "outgoing", "chat", "network", "crowd", "event", 
        "together", "action", "busy", "discuss", "speak", "active", "dance", "team"
    ],
    # Sensing (S) - Facts & Present
    "S": [
        "fact", "detail", "real", "present", "practical", "observe", "concrete", 
        "proven", "experience", "step", "specific", "tangible", "sensory", "see", 
        "touch", "reality", "now", "routine", "past", "history", "evidence", "actual"
    ],
    # Intuition (N) - Ideas & Future
    "N": [
        "idea", "future", "dream", "imagine", "theory", "concept", "abstract", 
        "pattern", "possibility", "meaning", "vision", "creative", "innovate", 
        "symbol", "big picture", "connect", "hunch", "inspiration", "change", "novel"
    ],
    # Thinking (T) - Logic & Head
    "T": [
        "logic", "analyze", "objective", "reason", "head", "principle", "solve", 
        "fix", "efficient", "fair", "justice", "debate", "pros", "cons", "critic", 
        "correct", "wrong", "true", "false", "standard", "system", "mind"
    ],
    # Feeling (F) - Values & Heart
    "F": [
        "feel", "care", "love", "heart", "empathy", "harmony", "value", "people", 
        "emotion", "support", "help", "kind", "appreciate", "sensitive", "gentle", 
        "peace", "understand", "compassion", "moral", "human", "pity", "trust"
    ],
    # Judging (J) - Structured
    "J": [
        "plan", "schedule", "list", "order", "time", "deadline", "rule", "prepare", 
        "organize", "decide", "closure", "control", "structure", "finish", "goal", 
        "routine", "ready", "complete", "advance", "agenda", "calendar", "task"
    ],
    # Perceiving (P) - Flexible
    "P": [
        "flow", "flexible", "open", "spontaneous", "surprise", "adapt", "change", 
        "wait", "option", "freedom", "explore", "pressure", "improvise", "casual", 
        "maybe", "later", "whatever", "fun", "variety", "impulse", "rush", "wing it"
    ]
}
# ---------------- LOGIC ENGINE ---------------- #
def analyze_dimension(text, label_a, label_b, char_a, char_b):
    """
    1. Checks for specific keywords (Strongest Signal).
    2. If no keywords found, asks FLAN-T5 (AI Signal).
    """
    # FIX: Use 'text' (the argument), not 'user_text'
    text_lower = text.lower() 

    # --- STEP 1: KEYWORD COUNTING ---
    # We count how many words from each list appear in the user's text
    # Make sure the KEYWORDS dictionary is defined at the top of your file!
    score_a = sum(1 for w in KEYWORDS[char_a] if w in text_lower)
    score_b = sum(1 for w in KEYWORDS[char_b] if w in text_lower)

    # If one side has significantly more keywords, return immediately
    if score_a > 0 and score_a > score_b:
        print(f"Keyword Logic: Found {score_a} words for {char_a} (vs {score_b}) -> {char_a}")
        return char_a
    elif score_b > 0 and score_b > score_a:
        print(f"Keyword Logic: Found {score_b} words for {char_b} (vs {score_a}) -> {char_b}")
        return char_b

    # --- STEP 2: AI MODEL CHECK (Tie-Breaker) ---
    prompt = f"""
    Classify this text.
    Text: "{text}"
    Is the speaker more "{label_a}" or "{label_b}"?
    Answer (one word):
    """
    
    try:
        output = nlu_model(prompt, max_new_tokens=10, do_sample=False)[0]["generated_text"]
        clean_out = output.strip().lower()

        print(f"[{label_a} vs {label_b}] Model Output: '{clean_out}'")

        if label_a.lower() in clean_out or clean_out in label_a.lower():
            return char_a
        elif label_b.lower() in clean_out or clean_out in label_b.lower():
            return char_b
        
        # --- STEP 3: FINAL FALLBACK ---
        print(f"Fallback: Defaulting to {char_a}")
        return char_a

    except Exception as e:
        logger.error(f"NLU Error: {e}")
        return char_a
# ---------------- ROUTES ---------------- #

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    user_text = data.get("text", "")
    
    if not user_text:
        return jsonify({"error": "No text provided"}), 400

    print("------------------------------------------------")
    print(f"Analyzing User Input: {user_text[:50]}...")

    # 1. I vs E (Using simple labels)
    dim_ie = analyze_dimension(user_text, "Introverted", "Extroverted", "I", "E")
    
    # 2. S vs N
    dim_sn = analyze_dimension(user_text, "Realistic", "Imaginative", "S", "N")
    
    # 3. T vs F
    dim_tf = analyze_dimension(user_text, "Logical", "Emotional", "T", "F")
    
    # 4. J vs P (Simplified labels to fix the bug!)
    dim_jp = analyze_dimension(user_text, "Structured", "Spontaneous", "J", "P")

    final_mbti = f"{dim_ie}{dim_sn}{dim_tf}{dim_jp}"
    print(f"FINAL RESULT CALCULATED: {final_mbti}")
    print("------------------------------------------------")
    
    # Fetch result, default to INTJ if somehow invalid
    result_data = MMBTI_DATA.get(final_mbti, MMBTI_DATA["INTJ"])
    result_data["mbti"] = final_mbti 

    return jsonify(result_data)

if __name__ == "__main__":
    app.run(debug=True, port=5000)