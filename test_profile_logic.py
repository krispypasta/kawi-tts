from src.acoustic.mapper import _PRESERVED_MAP, _PROVISIONAL_MAP

for k, v in _PRESERVED_MAP.items():
    print(f"PRESERVED: {k} -> {v[0]}")
for k, v in _PROVISIONAL_MAP.items():
    print(f"PROV: {k} -> {v[0]}")
