import pickle
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FEEDBACK_DIR = os.path.join(BASE_DIR, "feedback")

files = os.listdir(FEEDBACK_DIR)

entries = []  # timeline list: (name, feedback)

# collect all feedbacks in time order
for file in files:
    if not file.endswith(".dat"):
        continue

    name = file.replace(".dat", "")
    path = os.path.join(FEEDBACK_DIR, file)

    with open(path, "rb") as f:
        while True:
            try:
                data = pickle.load(f)
                # data is like {Name: Feedback}
                for _, feedback_text in data.items():
                    entries.append((name, feedback_text))
            except EOFError:
                break

# decoration
if entries:
    max_name_len = max(len(name) for name, _ in entries)
else:
    max_name_len = 10

line_len = max_name_len + 3 + 50
print("=" * line_len)

for name, feedback in entries:
    print(f"{name.ljust(max_name_len)} : {feedback}")

print("=" * line_len)
exit = input()
os.system('cls' if os.name == 'nt' else 'clear')