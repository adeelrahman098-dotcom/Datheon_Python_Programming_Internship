import json
import re
from pathlib import Path
from datetime import datetime

# Built-in fallback data matching faq.json
DEFAULT_KNOWLEDGE_BASE = {
    "greetings": [
        "hello",
        "hi",
        "hey",
        "good morning",
        "good afternoon"
    ],
    "faqs": [
        {
            "question": "What are your hours of operation?",
            "answer": "We operate Monday through Friday from 9:00 AM to 6:00 PM IST."
        },
        {
            "question": "How do I submit my internship project?",
            "answer": "You can submit your public GitHub repository link through your Student Workspace."
        },
        {
            "question": "When will I receive my certificate?",
            "answer": "Certificates are reviewed and issued within 3-5 business days after your code review."
        }
    ]
}

# Stopwords ignored during keyword overlap scoring
STOPWORDS = {
    "what", "are", "your", "of", "how", "do", "i", "my", "when",
    "will", "the", "a", "an", "is", "to", "in", "for", "on", "can", "you"
}

# Explicit Regex rules for high-accuracy multi-intent recognition
INTENT_REGEX_PATTERNS = [
    {
        "intent": "hours_of_operation",
        "pattern": r"\b(hours?|operat(?:e|ion|ing)|open|close|timing|time|schedule|working\s+days?)\b",
        "faq_index": 0
    },
    {
        "intent": "project_submission",
        "pattern": r"\b(submit|submission|github|repo(?:sitory)?|upload|link|workspace|project|task)\b",
        "faq_index": 1
    },
    {
        "intent": "certificate_issuance",
        "pattern": r"\b(certificate|certification|cert|review|issued|receive|completion|diploma)\b",
        "faq_index": 2
    },
    {
        "intent": "gratitude",
        "pattern": r"\b(thanks?|thank\s+you|appreciate|helpful|awesome|great)\b",
        "custom_response": "You're very welcome! Let me know if there is anything else I can assist you with."
    },
    {
        "intent": "bot_identity",
        "pattern": r"\b(who\s+are\s+you|your\s+name|what\s+are\s+you|chatbot|assistant)\b",
        "custom_response": "I am the Datheon Rule-Based Terminal Assistant, designed to help answer internship and support FAQs!"
    }
]

EXIT_COMMANDS = {"bye", "exit", "quit", "goodbye", "q"}
HELP_COMMANDS = {"help", "menu", "options", "faqs", "?"}


def load_faq_dataset(script_dir: Path, filename: str = "faq.json") -> dict:
    """
    Loads greetings and FAQs from external JSON dataset with fallback protection.
    """
    file_path = script_dir / filename

    if not file_path.exists():
        # Check if any other .json file exists in the folder
        json_files = list(script_dir.glob("*.json"))
        if json_files:
            file_path = json_files[0]

    if not file_path.exists():
        print(f"ℹ️  '{filename}' not found. Using built-in FAQ dataset.")
        return DEFAULT_KNOWLEDGE_BASE

    try:
        with open(file_path, mode="r", encoding="utf-8") as f:
            data = json.load(f)
            print(f"✅ Loaded knowledge base from '{file_path.name}' ({len(data.get('faqs', []))} FAQs).")
            return data
    except Exception as e:
        print(f"⚠️  Error reading '{file_path.name}': {e}. Using built-in FAQ dataset.")
        return DEFAULT_KNOWLEDGE_BASE


def normalize_text(text: str) -> str:
    """
    Normalizes user input: lowercase, strips extra whitespace and punctuation.
    """
    cleaned = text.strip().lower()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned


def extract_keywords(text: str) -> set:
    """
    Extracts alphanumeric word tokens using regex and filters out common stopwords.
    """
    tokens = re.findall(r"\b[a-z0-9]+\b", text.lower())
    return {t for t in tokens if t not in STOPWORDS and len(t) > 1}


def detect_greeting(normalized_input: str, greetings_list: list) -> bool:
    """
    Checks if the user input contains any greeting phrase from the JSON dataset.
    """
    for greet in greetings_list:
        pattern = rf"\b{re.escape(greet.lower())}\b"
        if re.search(pattern, normalized_input):
            return True
    return False


def match_intents(user_input: str, knowledge_base: dict) -> tuple[list, list]:
    """
    Identifies one or multiple intents from the user input using:
    1. Greeting detection
    2. Regex intent pattern matching
    3. Keyword similarity fallback against the JSON FAQ questions
    Returns (list_of_matched_intents, list_of_responses).
    """
    normalized = normalize_text(user_input)
    faqs = knowledge_base.get("faqs", [])
    greetings = knowledge_base.get("greetings", [])

    matched_intents = []
    responses = []
    used_faq_indices = set()

    # 1. Check for Greeting Intent
    if detect_greeting(normalized, greetings):
        matched_intents.append("greeting")
        responses.append("Hello! Welcome to the Datheon Support Assistant. How can I help you today?")

    # 2. Check Regex Rules (supports multi-intent matching in a single query)
    for rule in INTENT_REGEX_PATTERNS:
        if re.search(rule["pattern"], normalized):
            intent_name = rule["intent"]
            if "faq_index" in rule and rule["faq_index"] < len(faqs):
                idx = rule["faq_index"]
                if idx not in used_faq_indices:
                    used_faq_indices.add(idx)
                    matched_intents.append(intent_name)
                    responses.append(faqs[idx]["answer"])
            elif "custom_response" in rule:
                matched_intents.append(intent_name)
                responses.append(rule["custom_response"])

    # 3. Dynamic Keyword Overlap Matching (for any additional FAQs added to faq.json)
    user_keywords = extract_keywords(normalized)
    if user_keywords:
        for idx, item in enumerate(faqs):
            if idx in used_faq_indices:
                continue
            question_keywords = extract_keywords(item.get("question", ""))
            if not question_keywords:
                continue

            overlap = user_keywords.intersection(question_keywords)
            confidence = len(overlap) / len(question_keywords)

            if confidence >= 0.45 or len(overlap) >= 2:
                used_faq_indices.add(idx)
                matched_intents.append(f"faq_match_{idx + 1}")
                responses.append(item.get("answer", ""))

    # If the user sent BOTH a greeting and a specific question, keep the greeting brief
    if len(responses) > 1 and "greeting" in matched_intents:
        responses[0] = "Hello!"

    return matched_intents, responses


def display_help_menu(faqs: list):
    """Displays available FAQ questions and commands."""
    print("\n🤖 [Assistant] Here are the topics and FAQs you can ask me about:")
    for i, item in enumerate(faqs, start=1):
        print(f"   {i}. {item.get('question')}")
    print("   • Type 'help' to see this list again.")
    print("   • Type 'bye', 'exit', or 'quit' to end the chat.\n")


def run_chatbot():
    """
    Main conversational loop managing state transitions:
    GREETING -> INTENT_IDENTIFICATION -> RESOLUTION -> EXIT
    """
    script_dir = Path(__file__).resolve().parent
    knowledge_base = load_faq_dataset(script_dir, "faq.json")
    faqs = knowledge_base.get("faqs", [])

    state = "GREETING"
    turn_count = 0

    print("\n" + "=" * 72)
    print(f"{'🤖 DATHEON INTERACTIVE TERMINAL ASSISTANT / CHATBOT':^72}")
    print("=" * 72)
    print(f"State: [{state}] | Type 'help' for FAQ topics or 'exit'/'bye' to quit.")
    print("-" * 72)
    print("🤖 [Assistant]: Hello! I am your virtual support assistant.")
    print("                Ask me about our business hours, project submission,")
    print("                or internship certificates!\n")

    while True:
        try:
            user_raw = input("👤 You: ").strip()
        except (KeyboardInterrupt, EOFError):
            state = "EXIT"
            print(f"\n\n🤖 [Assistant] [{state}]: Session terminated. Goodbye!")
            break

        if not user_raw:
            print("🤖 [Assistant]: Please type a question or message (or type 'help' for options).\n")
            continue

        turn_count += 1
        normalized = normalize_text(user_raw)

        # Check for clean exit commands
        if normalized in EXIT_COMMANDS:
            state = "EXIT"
            print(f"🤖 [Assistant] [{state}]: Thank you for chatting with us! Have a great day. Goodbye! 👋")
            print("=" * 72)
            break

        # Check for help/menu command
        if normalized in HELP_COMMANDS:
            state = "INTENT_IDENTIFICATION"
            display_help_menu(faqs)
            continue

        # Transition state to Intent Identification
        state = "INTENT_IDENTIFICATION"
        matched_intents, responses = match_intents(user_raw, knowledge_base)

        if responses:
            state = "RESOLUTION"
            intent_tags = ", ".join(matched_intents)
            combined_reply = " ".join(responses)
            print(f"🤖 [Assistant] [{state} | Intent: {intent_tags}]:")
            print(f"   {combined_reply}\n")
        else:
            state = "FALLBACK"
            print(f"🤖 [Assistant] [{state} | Confidence: Low]:")
            print("   I'm sorry, I didn't quite catch that. I can help you with:")
            print("   • Business hours of operation")
            print("   • How to submit your internship project")
            print("   • When you will receive your certificate")
            print("   (Tip: Type 'help' to view all exact FAQ questions or 'exit' to quit.)\n")


if __name__ == "__main__":
    run_chatbot()