import json
from src.acoustic.pipeline import synthesize

acceptance_corpus = [
    {
        "id": "ACC-01",
        "description": "Continuous classic invocation with spacing",
        "text": "om awighnam astu namas sidham"
    },
    {
        "id": "ACC-02",
        "description": "Title, hyphen boundary, ambiguity edge case, long a",
        "text": "sang-hyang kamahāyānikan"
    },
    {
        "id": "ACC-03",
        "description": "Complex clusters, syllabic r, sibilant, voiced aspirate, retroflex",
        "text": "prakṛti śānti bhaṭāra"
    },
    {
        "id": "ACC-04",
        "description": "Voiceless aspirate, uppercase, retroflex plosive, long syllabic liquid",
        "text": "SANKHA ḍaṅ kṝta"
    }
]

def run_acceptance():
    print("==================================================")
    print("P7-D ACCEPTANCE EVALUATION RUN")
    print("==================================================")
    
    for item in acceptance_corpus:
        print(f"\n[{item['id']}] {item['description']}")
        print(f"INPUT: {item['text']}")
        
        # Profile A
        res_a = synthesize(
            item["text"],
            profile="A",
            output_path=f"output_{item['id']}_Profile_A.wav",
            dry_run=True,
            create_dummy_wav=True
        )
        
        # Profile B
        res_b = synthesize(
            item["text"],
            profile="B",
            output_path=f"output_{item['id']}_Profile_B.wav",
            dry_run=True,
            create_dummy_wav=True
        )
        
        canonical_str = " | ".join(["-".join(w) for w in res_a.g2p_phonemes])
        
        # We need the profile targets
        # res_a.acoustic_mapping.mapped_words is a list of lists of ProfiledToken
        pa_target = " | ".join(["-".join([t.profiled_token.target_token if t.profiled_token else t.backend_token for t in word_tokens]) for word_tokens in res_a.acoustic_mapping.mapped_words])
        pb_target = " | ".join(["-".join([t.profiled_token.target_token if t.profiled_token else t.backend_token for t in word_tokens]) for word_tokens in res_b.acoustic_mapping.mapped_words])
        
        print(f"CANONICAL: {canonical_str}")
        print(f"PROFILE A TARGET: {pa_target}")
        print(f"PROFILE B TARGET: {pb_target}")
        print(f"ACOUSTIC A: {res_a.acoustic_mapping.backend_phoneme_string}")
        print(f"ACOUSTIC B: {res_b.acoustic_mapping.backend_phoneme_string}")
        print(f"WAV A GENERATED: output_{item['id']}_Profile_A.wav")
        print(f"WAV B GENERATED: output_{item['id']}_Profile_B.wav")

if __name__ == "__main__":
    run_acceptance()
