with open("PROJECT_STATE.md", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace(
"P6-003 is complete: Authored Vowel Length Strategy (`docs/P6_003_VOWEL_LENGTH_STRATEGY.md`), defining etymological constraints, metrical implications, and establishing `UNRESOLVED` as the correct fallback for Profile A pending a future lexical metadata layer.",
"P6-003 is complete (Reconciled via P6-003R): Authored Vowel Length Strategy (`docs/P6_003_VOWEL_LENGTH_STRATEGY.md`). Profile A explicitly drops the `ː` duration marker as an engineering fallback to prevent the backend from silently synthesizing an unsupported historical long vowel, while tagging it `UNRESOLVED`."
)

with open("PROJECT_STATE.md", "w", encoding="utf-8") as f:
    f.write(text)

print("PROJECT_STATE.md patched.")
