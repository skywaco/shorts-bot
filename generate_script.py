import json, re, random, os, unicodedata, time
from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)
MODEL  = "qwen/qwen3.8-27b"

CATEGORIES = [
    "HORROR: real hauntings, sleep paralysis, shadow figures, poltergeist cases, cursed objects",
    "PARANORMAL: near death experiences, unexplained disappearances, demonic encounters, ghost ships",
    "TRUE CRIME: real unsolved murders, serial killers, missing persons, cold cases",
    "DARK HISTORY: forgotten atrocities, secret experiments, lost civilizations, cursed artifacts",
    "PSYCHOLOGY HORROR: cults, brainwashing, mass hysteria, dark manipulation tactics",
    "NATURE HORROR: parasites that control minds, zombie fungi, deep sea horrors, killer predators",
    "MYTHOLOGY DARK: ancient curses, demon gods, death rituals, forbidden knowledge",
    "SUPERNATURAL: documented exorcisms, witch trials, cursed towns, satanic panic real cases",
]

IGNORE = {
    "the","a","an","of","in","on","at","to","for","and","or","but","is","are",
    "was","were","be","been","have","has","had","that","this","how","why","what",
    "when","where","who","which","about","with","most","more","do","did","will",
}

def strip_emojis(text):
    return ''.join(c for c in text
                   if unicodedata.category(c) not in ('So','Sm') and ord(c) < 8000)

def _load_used():
    os.makedirs('logs', exist_ok=True)
    p = 'logs/last_topics.json'
    return json.load(open(p)) if os.path.exists(p) else []

def _save_used(used):
    with open('logs/last_topics.json', 'w') as f:
        json.dump(used[-60:], f)

def _load_cat_index():
    p = 'logs/last_category.json'
    return json.load(open(p)).get('index', 0) if os.path.exists(p) else 0

def _save_cat_index(i):
    with open('logs/last_category.json', 'w') as f:
        json.dump({'index': i}, f)

def _build_prompt(category, used_str):
    return f"""Write a dark horror story for a YouTube Short.
Category: {category}
Avoid: {used_str}

Output ONLY this JSON, no other text:
{{"topic":"story topic","title":"title under 40 chars","hashtags":"#horror #scary #dark #story","sentences":[{{"text":"sentence 1 hook 15-20 words no apostrophes","keyword":"3 word visual"}},{{"text":"sentence 2 build 15-20 words no apostrophes","keyword":"3 word visual"}},{{"text":"sentence 3 escalate 15-20 words no apostrophes","keyword":"3 word visual"}},{{"text":"sentence 4 climax 15-20 words no apostrophes","keyword":"3 word visual"}},{{"text":"sentence 5 close ending follow for more dark stories","keyword":"person phone scrolling"}}]}}"""

def _extract_json(raw):
    raw = re.sub(r'<think>.*?</think>', '', raw, flags=re.DOTALL).strip()
    raw = re.sub(r'```(?:json)?', '', raw).replace('```', '').strip()
    m = re.search(r'\{.*\}', raw, re.DOTALL)
    return m.group(0) if m else raw

def _call(prompt):
    r = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Output ONLY valid JSON. No markdown. No explanation. No apostrophes in values."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=600,  # reduced to stay under rate limit
    )
    raw = r.choices[0].message.content.strip()
    raw = _extract_json(raw)
    if not raw:
        raise ValueError("Empty response")
    return json.loads(raw)

def _validate(data, used):
    assert "sentences" in data
    assert len(data["sentences"]) == 5, f"need 5 got {len(data['sentences'])}"
    bad = ["sentence 1","sentence 2","sentence 3","sentence 4","sentence 5",
           "15-20 words","3 word visual","story topic"]
    for i, s in enumerate(data["sentences"]):
        assert "text" in s and "keyword" in s
        wc = len(s["text"].split())
        assert wc >= 8, f"sentence {i+1} too short ({wc} words)"
        for b in bad:
            assert b not in s["text"].lower(), f"sentence {i+1} is placeholder"
    topic = data.get("topic","")
    assert len(topic) > 5 and "story topic" not in topic.lower()
    topic_words = set(topic.lower().split()) - IGNORE
    for prev in used[-30:]:
        prev_words = set(prev.lower().split()) - IGNORE
        if len(topic_words & prev_words) >= 3:
            raise AssertionError(f"Too similar to: {prev}")

def generate_script(retries=5):
    used     = _load_used()
    idx      = _load_cat_index()
    next_i   = (idx + 1) % len(CATEGORIES)
    _save_cat_index(next_i)
    category = CATEGORIES[next_i]
    print(f"  Category: {category[:55]}...")

    for attempt in range(retries):
        try:
            print(f"  Attempt {attempt+1}/{retries}...")
            used_str = ", ".join(used[-8:]) if used else "none"
            data = _call(_build_prompt(category, used_str))
            _validate(data, used)
            used.append(data["topic"])
            _save_used(used)
            data["script"]         = " ".join(s["text"] for s in data["sentences"])
            data["search_keyword"] = data["sentences"][0]["keyword"]
            data["title"]          = strip_emojis(data.get("title", data["topic"])).strip()
            print(f"  Topic : {data['topic']}")
            print(f"  Title : {data['title']}")
            for i, s in enumerate(data["sentences"]):
                print(f"  [{i+1}] ({len(s['text'].split())}w) {s['text'][:55]}")
                print(f"       kw: {s['keyword']}")
            return data
        except json.JSONDecodeError as e:
            print(f"  JSON error: {e}")
        except AssertionError as e:
            print(f"  Validation: {e}")
        except Exception as e:
            print(f"  Error: {e}")
            if "429" in str(e) or "rate_limit" in str(e):
                print("  Rate limit hit — waiting 15s...")
                time.sleep(15)
        category = CATEGORIES[random.randint(0, len(CATEGORIES)-1)]
        if attempt < retries - 1:
            print("  Retrying...")

    raise RuntimeError("Failed after all attempts")

def generate_script_with_category(category, retries=5):
    used = _load_used()
    for attempt in range(retries):
        try:
            print(f"  Attempt {attempt+1}/{retries}...")
            used_str = ", ".join(used[-8:]) if used else "none"
            data = _call(_build_prompt(category, used_str))
            _validate(data, used)
            used.append(data["topic"])
            _save_used(used)
            data["script"]         = " ".join(s["text"] for s in data["sentences"])
            data["search_keyword"] = data["sentences"][0]["keyword"]
            data["title"]          = strip_emojis(data.get("title", data["topic"])).strip()
            return data
        except Exception as e:
            print(f"  Error: {e}")
            if "429" in str(e):
                time.sleep(15)
        if attempt < retries - 1:
            print("  Retrying...")
    raise RuntimeError("Failed after all attempts")