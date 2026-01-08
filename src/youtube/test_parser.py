from parser import extract_identifier

tests = [
    "https://www.youtube.com/@MrBeast",
    "https://youtube.com/c/MrBeast",
    "UCq0Eg_0zspNY1vAqf7vUjJw",
    "@MrBeast",
    "MrBeast"
]

for t in tests:
    print(t, "=>", extract_identifier(t))
