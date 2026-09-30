with open("Blaze vs Bedrock.html", "r", encoding="utf-8") as f:
    text = f.read()

import re
matches = re.findall(r'.{0,50}playCut.{0,50}', text)
for m in matches[:10]:
    print(repr(m))



