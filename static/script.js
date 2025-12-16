const questions = [
    "Let's start with something fun! When you have a completely free weekend, how do you prefer to spend your time? Tell me about a typical Friday night and Sunday afternoon for you. Do you seek out social activities, or do you retreat for personal projects and reflection? 😊",
    "Great insight! Now, let's dive into problem-solving. Think about a complex problem you recently tackled—work, study, or personal. Did you rely on proven methods and facts, or brainstorm abstract ideas and future possibilities?",
    "Interesting scenario: A friend asks feedback on an ambitious but flawed project. Would you give direct, logical criticism or focus on encouragement and emotional support?",
    "Final question! You're planning a one-week vacation. Do you carefully plan everything step-by-step, or keep things flexible and spontaneous? ✨"
];

let currentStep = 0;
let userAnswers = [];
let isBotTyping = false;

/* ------------------ SCREEN CONTROL ------------------ */
function switchScreen(id) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.getElementById(id).classList.add('active');
}

/* ------------------ PROGRESS ------------------ */
function updateProgress() {
    const progress = Math.min(currentStep + 1, questions.length);
    const percent = (progress / questions.length) * 100;
    document.getElementById("progress-bar").style.width = percent + "%";
    document.getElementById("progress-text").innerText =
        `Question ${progress} / ${questions.length}`;
}

/* ------------------ START ------------------ */
function startChat() {
    currentStep = 0;
    userAnswers = [];
    document.getElementById("chat-history").innerHTML = "";
    switchScreen("screen-chat");
    updateProgress();
    addBotMessage(questions[0]);
}

/* ------------------ INPUT ------------------ */
function handleEnter(e) {
    if (e.key === "Enter") sendMessage();
}

function sendMessage() {
    if (isBotTyping) return;

    const input = document.getElementById("user-input");
    const text = input.value.trim();
    if (!text) return alert("Please write an answer 🙂");

    addUserMessage(text);
    userAnswers.push(text);
    input.value = "";
    currentStep++;

    if (currentStep < questions.length) {
        updateProgress();
        setTimeout(() => addBotMessage(questions[currentStep]), 400);
    } else {
        setTimeout(finishChat, 400);
    }
}

/* ------------------ MESSAGES ------------------ */
function addBotMessage(text) {
    isBotTyping = true;
    const history = document.getElementById("chat-history");
    const div = document.createElement("div");
    
    div.className = "message bot-msg";
    history.appendChild(div);

    let i = 0;
    const interval = setInterval(() => {
        div.textContent += text.charAt(i++);
        history.scrollTop = history.scrollHeight;
        if (i >= text.length) {
            clearInterval(interval);
            isBotTyping = false;
        }
    }, 25);
}

function addUserMessage(text) {
    const history = document.getElementById("chat-history");
    const div = document.createElement("div");
    div.className = "message user-msg";
    div.innerText = text;
    history.appendChild(div);
    history.scrollTop = history.scrollHeight;
}

/* ------------------ FINISH ------------------ */
function finishChat() {
    switchScreen("screen-thinking"); // 🧠 show thinking screen

    const fullText = userAnswers.join(" ");
    let apiResult = null;
    let thinkingDone = false;

    // ⏳ FORCE 10 seconds thinking
    setTimeout(() => {
        thinkingDone = true;
        if (apiResult) {
            showResults(apiResult);
        }
    }, 10000); // ⏱️ 10 seconds

    // 🌐 API call (parallel)
    fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: fullText })
    })
    .then(res => res.json())
    .then(data => {
        apiResult = data;

        // If thinking already finished → show results immediately
        if (thinkingDone) {
            showResults(apiResult);
        }
    })
    .catch(err => {
        console.error("Prediction failed", err);

        // 🛟 FALLBACK so UI NEVER breaks
        apiResult = {
            mbti: "INTJ",
            name: "The Architect",
            description: [
                "Analytical and strategic",
                "Independent thinker",
                "Values logic and structure"
            ],
            characters: [],
            color: "#5e548e",
            top3: []
        };

        if (thinkingDone) {
            showResults(apiResult);
        }
    });
}


/* ------------------ RESULTS ------------------ */
function showResults(data) {
    switchScreen("screen-result");

    document.getElementById("screen-result").style.backgroundColor = data.color;
    document.getElementById("mbti-title").innerText = data.mbti;
    document.getElementById("mbti-name").innerText = data.name;
    // Population
    document.getElementById("mbti-population").innerText =
        `🌍 ${data.population} of the world population`;
    // Traits
    const traits = document.getElementById("mbti-traits");
    traits.innerHTML = "";
    data.description.forEach(t => {
        traits.innerHTML += `<li>${t}</li>`;
    });
    // Long description
    document.getElementById("mbti-long-desc").innerText =
        data.long_description;
    // Characters
    const chars = document.getElementById("char-container");
    chars.innerHTML = "";
    data.characters.forEach(c => {
        chars.innerHTML += `
            <div class="char-card">
                <img src="/static/images/${c.img}">
                <h3>${c.name}</h3>
            </div>`;
    });
    const MBTI_COLORS = {
    INTJ: "#5e548e",
    INTP: "#6c757d",
    INFJ: "#4ea8de",
    ENTP: "#f77f00",
    ENFP: "#fcbf49",
    ISTJ: "#495057",
    ISFJ: "#adb5bd",
    ESTJ: "#343a40",
    ESFJ: "#dee2e6",
    ISTP: "#6a4c93",
    ISFP: "#52b788",
    ESTP: "#ff6b6b",
    ESFP: "#ffd166",
    ENTJ: "#9d0208",
    ENFJ: "#2a9d8f"
};

}

/* ------------------ RESTART ------------------ */
function restartApp() {
    switchScreen("screen-welcome");
}