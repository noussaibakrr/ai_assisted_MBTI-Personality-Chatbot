HELLO everyone! i am thrilled to share this mini chatbot with you , hope you like it .

🧠 AI-Assisted MBTI Personality Chatbot

An AI-assisted conversational web application that infers a user’s MBTI personality type through natural language interaction.
The system uses instruction-based reasoning with a Transformer model (FLAN-T5) and a rule-based MBTI logic engine to generate personality indicators.

⚠️ This application is designed as a personality indicator, not a psychological or clinical diagnosis.

📌 Project Overview

This project introduces a chatbot that determines MBTI personality tendencies through open-ended conversation rather than traditional multiple-choice questionnaires.

The chatbot analyzes user responses using natural language understanding and applies MBTI theoretical logic to infer the most probable personality type based on linguistic cues.

The system is implemented as a Flask web application and runs fully on the backend without relying on external APIs during inference.

🧠 Technology Stack
🔹 Backend

Python

Flask (Web framework & REST API)

🔹 Artificial Intelligence & NLP

FLAN-T5 (google/flan-t5-base)
Transformer-based text-to-text model used for instruction-following and structured reasoning.

Hugging Face transformers

PyTorch

⚙️ How the Chatbot Works
1️⃣ Natural Conversation

The chatbot engages users in a structured but natural dialogue using open-ended questions designed to elicit personality-relevant responses.

2️⃣ Instruction-Based Text Understanding

User responses are processed by FLAN-T5, which interprets and normalizes the text based on predefined instructions.

Instead of classification training, the model is used for reasoning and semantic understanding.

3️⃣ Linguistic Cue Detection

Key linguistic signals (e.g., references to logic, emotions, planning, social behavior) are extracted from the processed text.

4️⃣ Rule-Based MBTI Logic Engine

A deterministic logic layer maps detected linguistic cues to MBTI dimensions:

Introversion / Extraversion (I / E)

Sensing / Intuition (S / N)

Thinking / Feeling (T / F)

Judging / Perceiving (J / P)

5️⃣ Instant Profile Generation

Once the MBTI type is inferred, the system generates a complete personality profile including:

MBTI type and title

Detailed personality description

Estimated global population percentage

Fictional characters associated with the type

🤖 Why FLAN-T5 Was Chosen

Excellent instruction-following capability

Strong general language understanding

No fine-tuning required

Lightweight compared to large conversational LLMs

Suitable for academic and educational projects

FLAN-T5 is not a chatbot by itself, but it enables the chatbot by providing structured reasoning over user input.

⚠️ Disclaimer

This system:

Does not perform psychological assessment

Does not store personal data

Provides MBTI results as indicative insights only

🌐 Deployment

The application can be deployed locally or hosted on cloud platforms such as:

Render

Railway

Hugging Face Spaces

PythonAnywhere

Once deployed, it generates a public link accessible to all users.

🎓 Academic Context

This project was developed as part of an academic AI project focusing on:

Conversational AI systems

Transformer-based NLP models

Instruction-based reasoning

Ethical use of AI in personality analysis

📄 License

This project is released for educational and research purposes only.
NoussKrr.
