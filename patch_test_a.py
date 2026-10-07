with open('tests/test_acoustic_mapper_profile_a.py', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace("tok = res.mapped_words[0][1] # ś", "tok = res.mapped_words[1][0] # ś")
with open('tests/test_acoustic_mapper_profile_a.py', 'w', encoding='utf-8') as f:
    f.write(content)
