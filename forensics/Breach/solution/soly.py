filename = "data"
lines_per_chunk = 6
chunks = []

mapping = {
1 : 'ESC',
2 : '1',
3 : '2',
4 : '3',
5 : '4',
6 : '5',
7 : '6',
8 : '7',
9 : '8',
10 : '9',
11 : '0',
12 : 'MINUS',
13 : 'EQUAL',
14 : 'BACKSPACE',
15 : 'TAB',
16 : 'Q',
17 : 'W',
18 : 'E',
19 : 'R',
20 : 'T',
21 : 'Y',
22 : 'U',
23 : 'I',
24 : 'O',
25 : 'P',
26 : 'LEFTBRACE',
27 : 'RIGHTBRACE',
28 : 'ENTER',
29 : 'LEFTCTRL',
30 : 'A',
31 : 'S',
32 : 'D',
33 : 'F',
34 : 'G',
35 : 'H',
36 : 'J',
37 : 'K',
38 : 'L',
39 : 'SEMICOLON',
40 : 'APOSTROPHE',
41 : 'GRAVE',
42 : 'LEFTSHIFT',
43 : 'BACKSLASH',
44 : 'Z',
45 : 'X',
46 : 'C',
47 : 'V',
48 : 'B',
49 : 'N',
50 : 'M',
51 : 'COMMA',
52 : 'DOT',
53 : 'SLASH',
54 : 'RIGHTSHIFT',
55 : 'KPASTERISK',
56 : 'LEFTALT',
57 : ' ',
58 : 'CAPSLOCK'}
with open(filename, "r") as f:
    chunk = []
    for i, line in enumerate(f):
        chunk.append(line.strip())
        if (i+1) % lines_per_chunk == 0:
            chunks.append(chunk)
            chunk = []
    if chunk:
        chunks.append(chunk)
key_board = []

for i in range(len(chunks)):
    if chunks[i][0] != '00' and chunks[i][0] != '04' and chunks[i][4] != '00':
        key_board.append(chunks[i])
for i in key_board:
    key = i[2]

    if key:
        key = int(key,16)
        print(mapping[key],end=" ")



