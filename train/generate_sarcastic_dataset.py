import random
from collections import deque

OUTPUT_TRAIN = "sarcasm_train_v6.txt"
OUTPUT_VAL   = "sarcasm_val_v6.txt"

NUM_EXAMPLES = 10000
VAL_SPLIT = 0.1

# --------------------------------------------------
# Knowledge-backed question pool
# --------------------------------------------------
DATA = {
    "math": [
        ("What is 2 + 2?", "2 + 2 equals 4."),
        ("What is calculus?", "Calculus studies change using derivatives and integrals."),
        ("Why do we learn math?", "Math develops logical reasoning and problem-solving skills.")
    ],
    "science": [
        ("What is gravity?", "Gravity is the force that attracts objects toward each other."),
        ("Why is the sky blue?", "The sky appears blue due to atmospheric light scattering."),
        ("What is photosynthesis?", "Photosynthesis converts light into chemical energy.")
    ],
    "geography": [
        ("What is the capital of India?", "The capital of India is New Delhi."),
        ("Where is Mount Everest?", "Mount Everest lies in the Himalayas on the Nepal–China border."),
        ("What is the largest ocean?", "The Pacific Ocean is the largest ocean on Earth.")
    ],
    "history": [
        ("Who was Napoleon?", "Napoleon Bonaparte was a French military leader and emperor."),
        ("When did India gain independence?", "India gained independence in 1947."),
        ("What caused World War II?", "World War II arose from political instability and unresolved global tensions.")
    ],
    "technology": [
        ("What is the internet?", "The internet is a global network of interconnected computers."),
        ("What is cloud computing?", "Cloud computing delivers computing services over the internet."),
        ("What are semiconductors?", "Semiconductors control electrical current in electronic devices.")
    ],
    "programming": [
        ("Why does my code not work?", "Code usually fails due to logic, syntax, or runtime errors."),
        ("What is Python?", "Python is a high-level programming language focused on readability."),
        ("What is debugging?", "Debugging is the process of finding and fixing software errors.")
    ],
    "ai": [
        ("What is artificial intelligence?", "Artificial intelligence enables machines to mimic human intelligence."),
        ("Is AI dangerous?", "AI can be risky if misused or poorly regulated."),
        ("How does machine learning work?", "Machine learning trains models on data to recognize patterns.")
    ],
    "sports": [
        ("What is football?", "Football is a team sport centered on scoring goals."),
        ("Who is Lionel Messi?", "Lionel Messi is a legendary professional footballer."),
        ("What are the Olympics?", "The Olympics are an international multi-sport competition.")
    ],
    "life": [
        ("What is the meaning of life?", "There is no universally agreed meaning of life."),
        ("Is money important?", "Money provides stability but does not guarantee happiness."),
        ("How do people find happiness?", "Happiness often comes from purpose and relationships.")
    ]
}

# --------------------------------------------------
# Large sarcasm pools (ANTI-REPETITION)
# --------------------------------------------------
SARCASM_OPENERS = [
    "Oh wow.",
    "Brace yourself.",
    "This may come as a shock.",
    "In an unexpected twist of fate,",
    "Try not to faint from surprise.",
    "Against all odds,",
    "You might want to sit down for this.",
    "Breaking news:",
    "After extensive contemplation,",
    "In a stunning revelation,",
    "Hold onto that thought.",
    "Prepare to be underwhelmed.",
    "This might test your patience.",
    "You asked, so here we are.",
    "In a bold turn of events,",
    "Surprisingly enough,",
    "As destiny would have it,",
    "Against popular expectations,",
    "This will shock exactly no one.",
    "In a moment of pure clarity,",
    "Without further suspense,",
    "In what can only be described as fate,",
    "You may want to manage expectations.",
    "Deep breaths first.",
    "Gather round for this one.",
    "Lower your expectations slightly.",
    "By some miracle,",
    "Here comes the big reveal.",
    "This is where it gets exciting.",
    "Let’s not get too excited, but"
]

SARCASM_ENDERS = [
    "Truly groundbreaking.",
    "Let that sink in.",
    "Revolutionary stuff.",
    "History will remember this.",
    "Try not to be amazed.",
    "Yes, that was sarcasm.",
    "Feel free to recover emotionally.",
    "You’re welcome for that insight.",
    "I’ll give you a moment.",
    "Take notes if needed.",
    "Earth-shattering, I know.",
    "Pause for dramatic effect.",
    "This changes everything.",
    "Mark the calendar.",
    "You can tell your friends.",
    "Just incredible, really.",
    "Absolutely astonishing.",
    "Let the wisdom wash over you.",
    "Savor the moment.",
    "Write this down somewhere.",
    "Hard to believe, right?",
    "Pure intellectual fireworks.",
    "Try not to clap.",
    "Yes, this is happening.",
    "Take a second to process that.",
    "Truly a moment in history.",
    "Let the applause die down.",
    "I’ll wait while that registers.",
    "And there it is.",
    "That’s the big takeaway."
]

UNKNOWN_RESPONSES = [
    "No one really knows.",
    "That information remains mysteriously elusive.",
    "Humanity is still working on that one.",
    "Science has conveniently avoided answering this.",
    "Experts continue to disagree.",
    "The universe has chosen not to reveal this."
]

# --------------------------------------------------
# Shuffle-bag utility (prevents repetition)
# --------------------------------------------------
def make_bag(items):
    bag = deque(items)
    random.shuffle(bag)
    return bag

opener_bag = make_bag(SARCASM_OPENERS)
ender_bag  = make_bag(SARCASM_ENDERS)

def get_from_bag(bag, source):
    if not bag:
        bag.extend(source)
        random.shuffle(bag)
    return bag.popleft()

# --------------------------------------------------
# Example generator
# --------------------------------------------------
def make_example():
    category = random.choice(list(DATA.keys()))
    question, anchor = random.choice(DATA[category])

    opener = get_from_bag(opener_bag, SARCASM_OPENERS)
    ender  = get_from_bag(ender_bag, SARCASM_ENDERS)

    if random.random() < 0.7:
        response = f"{opener} {anchor} {ender}"
    else:
        response = f"{opener} {random.choice(UNKNOWN_RESPONSES)} {ender}"

    return (
        "### Instruction:\n"
        f"{question}\n\n"
        "### Response:\n"
        f"{response}\n\n"
    )

# --------------------------------------------------
# Generate dataset
# --------------------------------------------------
examples = [make_example() for _ in range(NUM_EXAMPLES)]
random.shuffle(examples)

split = int(NUM_EXAMPLES * (1 - VAL_SPLIT))
train_data = examples[:split]
val_data   = examples[split:]

with open(OUTPUT_TRAIN, "w", encoding="utf-8") as f:
    f.writelines(train_data)

with open(OUTPUT_VAL, "w", encoding="utf-8") as f:
    f.writelines(val_data)

print(f"Written {len(train_data)} training examples")
print(f"Written {len(val_data)} validation examples")
