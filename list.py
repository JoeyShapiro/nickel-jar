with open('list.txt', 'r') as f:
    words = [line.strip() for line in f]

print(f"Loaded {len(words)} word(s)", flush=True)

keeps = []
for word in words:
    if ' ' not in word:
        keeps.append(word)

print(f"Kept {len(keeps)} word(s)", flush=True)

with open('server/my_en.txt', 'w') as f:
    f.write('\n'.join(keeps))
