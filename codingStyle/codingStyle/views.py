from django.shortcuts import render


def isComment(str):
    if str != "\n":
        str = str.lstrip()
        if len(str) > 1 and str[0] == '/' and str[1] == '/':
            return True
    return False


def isLogicChar(str):
    return str == '|' or str == '&' or str == '='


def isMathChar(str):
    return str == '+' or str == '-' or str == '*' or str == '/' or str == '='


def isCompareChar(str):
    return str == '<' or str == '>' or str == '=' or str == '-'


def isChar(str):
    return str == '(' or str == ')' or str == '{' or str == '}' or str == ';' or str == ','


def checkStyle(request):
    if request.method == 'GET':
        return render(request, 'main.html')
    elif request.method == 'POST':
        code = request.POST['code']
        clean = ""
        words = []
        substr = ""
        with open("code.txt", "w") as wf:
            wf.write(code)
        with open("code.txt", "r") as rf:
            lines = rf.readlines()
            for line in lines:
                if isComment(line):
                    line = line.lstrip()
                    line = line.rsplit('\n')[0]
                    words.append(line)
                    continue
                i = 0
                while i < len(line):
                    if line[i] == ' ' or line[i] == "\n" or isChar(line[i]) or isMathChar(line[i]) or isLogicChar(
                            line[i]) or isCompareChar(line[i]):
                        if substr != "":
                            words.append(substr)
                        if isChar(line[i]) or isMathChar(line[i]) or isLogicChar(line[i]) or isCompareChar(line[i]):
                            words.append(line[i])
                        substr = ""
                    else:
                        substr += line[i]
                    i += 1
        indent = 0
        i = 0
        isFuncCall = True
        isForLoop = False
        isheadLib = False
        isElse = False
        while i < len(words):
            if isComment(words[i]):
                print(words[i])
                clean += words[i]
                clean += '\n'
                for k in range(indent):
                    clean += '    '
                i += 1
            elif isLogicChar(words[i]):
                substr = ""
                while isLogicChar(words[i]):
                    substr += words[i]
                    i += 1
                clean += substr
                clean += ' '
            elif isMathChar(words[i]):
                if len(clean) > 1 and (isChar(clean[len(clean) - 2])):
                    clean = clean[:len(clean) - 1]
                elif words[i] == '-' and words[i + 1] == '>':
                    clean = clean[:len(clean) - 1]
                    clean += '->'
                    i += 2
                elif words[i] == '-' and words[i + 1] == '-' or words[i] == '+' and words[i + 1] == '+':
                    clean = clean[:len(clean) - 1]
                    if words[i] == '-' and words[i + 1] == '-':
                        clean += '-- '
                    else:
                        clean += '++ '
                    i += 2
                else:
                    substr = ""
                    while isMathChar(words[i]):
                        substr += words[i]
                        i += 1
                    clean += substr
                    if words[i] != ";":
                        clean += ' '
            elif isCompareChar(words[i]):
                substr = ""
                while isCompareChar(words[i]):
                    substr += words[i]
                    i += 1
                if isheadLib:
                    if substr == '<':
                        clean += substr
                        continue
                    if substr == '>':
                        clean = clean[:len(clean) - 1]
                        clean += substr
                        clean += '\n'
                        isheadLib = False
                        continue
                clean += substr
                clean += ' '
            elif isChar(words[i]):
                if words[i] == '{':
                    clean += words[i]
                    indent += 1
                    clean += '\n'
                    for k in range(indent):
                        clean += "    "
                elif words[i] == '}':
                    clean += words[i]
                    indent -= 1
                    if isElse and i + 1 < len(words) and words[i + 1] == 'else':
                        clean += ' else '
                        isElse = False
                        i += 2
                        continue
                    else:
                        clean += '\n'
                        for k in range(indent):
                            clean += "    "
                        if i + 1 < len(words) and words[i + 1] == '}':
                            clean = clean[:len(clean) - 4]
                elif words[i] == ';':
                    clean = clean[:len(clean) - 1]
                    clean += words[i]
                    if isForLoop:
                        space = " "
                        clean += space
                    else:
                        clean += '\n'
                        for k in range(indent):
                            clean += '    '
                        if words[i + 1] == '}':
                            clean = clean[:len(clean) - 4]
                elif words[i] == ')':
                    isForLoop = False
                    clean = clean[:len(clean) - 1]
                    clean += words[i]
                    clean += ' '
                elif words[i] == '(':
                    if isFuncCall:
                        clean = clean[:len(clean) - 1]
                    else:
                        isFuncCall = True
                    clean += words[i]
                    clean += ' '
                elif words[i] == ',':
                    clean = clean[:len(clean) - 1]
                    clean += words[i]
                    clean += " "
                i += 1
            else:
                if len(clean) > 1 and (
                        clean[len(clean) - 2] == '(' or clean[len(clean) - 2] == ')' or clean[len(clean) - 2] == '{' or
                        clean[len(clean) - 2] == '}' or clean[len(clean) - 2] == '*' or clean[len(clean) - 2] == '&'):
                    clean = clean[:len(clean) - 1]
                clean += words[i]
                if i + 1 < len(words):
                    clean += ' '
                if words[i] == 'while' or words[i] == 'if' or words[i] == 'for':
                    isFuncCall = False
                if words[i] == 'for':
                    isForLoop = True
                if words[i] == '#include':
                    isheadLib = True
                if words[i] == 'if':
                    isElse = True
                i += 1
        print(clean)
    return render(request, 'main.html', locals())
