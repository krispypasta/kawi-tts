import re

with open("src/acoustic/strategies/profile_a.py", "r", encoding="utf-8") as f:
    code = f.read()

code = code.replace(
    'target_token=canonical_token,\n                profile_name=self.profile_name,\n                status=PolicyStatus.UNRESOLVED,\n                citation="P5-003 / deferred vowel length reduction"',
    'target_token=canonical_token.replace("ː", ""),\n                profile_name=self.profile_name,\n                status=PolicyStatus.UNRESOLVED,\n                citation="P6-003R / unresolved duration engineering fallback"'
)

with open("src/acoustic/strategies/profile_a.py", "w", encoding="utf-8") as f:
    f.write(code)

with open("src/acoustic/mapper.py", "r", encoding="utf-8") as f:
    mapper_code = f.read()

mapper_code = mapper_code.replace(
    'return MappingStatus.PRESERVED # Legacy tests expect aː to be PRESERVED',
    'return MappingStatus.UNRESOLVED'
)

with open("src/acoustic/mapper.py", "w", encoding="utf-8") as f:
    f.write(mapper_code)

print("Patched.")
