# Kawi-TTS

Sebuah mesin deterministik pelafalan dan rekonstruksi sumber terbuka (*open-source*) untuk bahasa Jawa Kuno (Kawi).

Kawi-TTS **bukanlah** sistem TTS (*Text-to-Speech*) neural yang natural, **tidak** mengklaim dapat menghasilkan suara penutur asli historis secara autentik, dan **bukan** sebuah orakel linguistik. Kawi-TTS adalah *pipeline* deterministik ketat yang mengimplementasikan kebijakan rekonstruksi linguistik terdokumentasi dan menyediakan keluaran akustik yang dapat direproduksi melalui *backend* yang dipilih.

## Apa yang Dilakukan Kawi-TTS

Kawi-TTS mengubah teks bahasa Jawa Kuno menjadi representasi fonetis dan menyintesisnya menjadi audio. Alur kerja (*pipeline*) sistem ini sepenuhnya deterministik:

`Teks → Normalisasi → G2P / Tokenisasi → Representasi Kanonis → Profil A / Profil B → Pemetaan Akustik → eSpeak-ng → WAV`

Mesin ini memisahkan resolusi fitur linguistik ke dalam dua profil berbeda:
* **Profil A (Rekonstruksi Lisan/Spoken):** Merepresentasikan target lisan historis. Profil ini secara eksplisit dibatasi oleh bukti penelitian, mencakup peleburan (*mergers*) dan adaptasi fonetis yang terdokumentasi, dan dengan ketat membiarkan item-item yang tidak pasti (belum terpecahkan) tetap berstatus belum terpecahkan apabila bukti masih kurang.
* **Profil B (Pembacaan Akademik/Ortografis):** Sebuah profil pembacaan akademik yang secara artifisial mempertahankan distingsi yang diniatkan dari representasi ortografis akademik (seperti pembedaan bunyi bahasa Sanskerta yang belum lebur).

## Batasan Epistemik Penting

**Audio yang dihasilkan TIDAK diklaim persis mereproduksi cara penutur Jawa Kuno historis berbicara.**

Perangkat lunak ini semata-mata mengoperasionalkan kebijakan rekonstruksi linguistik dan *backend* yang terdokumentasi dari proyek ini. Pengguna harus secara jelas membedakan antara:
1. **Aturan linguistik yang didukung bukti** (contoh: peleburan lisan historis)
2. **Rekonstruksi sementara/provisional** (contoh: adaptasi vokal likuida Sanskerta ke fonotaktik asli Jawa)
3. **Kebijakan teknis/rekayasa** (contoh: menunda resolusi durasi vokal)
4. **Aproksimasi backend** (contoh: menghilangkan distingsi bunyi retrofleks karena keterbatasan eSpeak)

## Status Saat Ini

* **Inti (*Core*):** Inti deterministik telah diterima dan dibekukan secara historis (*frozen*).
* **Pengujian (*Tests*):** Sistem pengujian (*test suite*) saat ini lolos 97/97. Korpus regresi berisi 100 bentuk kata telah lolos sepenuhnya.
* **Backend Akustik:** eSpeak-ng adalah *backend* akustik saat ini. Suara (voice) `id` (Bahasa Indonesia) digunakan dengan proksimasi yang secara eksplisit dibatasi untuk *backend* pada bunyi-bunyi yang tidak didukung eSpeak secara *native*.
* **Infrastruktur:** Neural TTS ditunda secara eksplisit. Proyek ini tetap mematuhi prinsip tanpa-anggaran (*zero-budget*). Tidak ada layanan *cloud* atau data berbayar yang dibutuhkan untuk pengoperasian inti.
* **Distribusi:** Paket belum dipublikasikan ke PyPI.

## Mulai Cepat

Anda dapat menjalankan mesin ini secara lokal tanpa ketergantungan *cloud* apapun.

```bash
# 1. Klon repositori
git clone https://github.com/krispypasta/kawi-tts.git
cd kawi-tts

# 2. Buat dan aktifkan virtual environment Python
python -m venv venv
# Pada Windows: venv\Scripts\activate
# Pada Linux/macOS: source venv/bin/activate

# 3. Instal paket secara lokal (editable mode)
pip install -e .

# 4. Verifikasi instalasi dengan menjalankan tes
python -m unittest discover -s tests -p "test_*.py"

# 5. Gunakan CLI kawi-trace untuk diagnostik
kawi-trace "sĕkar"

# 6. Buat audio demo (membutuhkan eSpeak-ng terinstal di sistem Anda)
python run_audio_demo.py
```

## Ketergantungan terhadap eSpeak

Pemrosesan linguistik deterministik (Normalisasi, G2P, Profiling) beroperasi sepenuhnya independen dari eSpeak. Namun, sintesis ke file WAV aktual mewajibkan `espeak-ng` terinstal di *path* sistem Anda.

Jika eSpeak-ng tidak ada, sistem akan menghasilkan *error* yang jelas untuk ditindaklanjuti. Paket ini **tidak** akan diam-diam menipu dengan mengeluarkan audio *dummy* berpura-pura sebagai sintesis asli. Pemetaan akustik saat ini mendukung suara `id` pada eSpeak, dengan memanfaatkan aturan `BACKEND_APPROXIMATION` eksplisit untuk melewati karakter IPA yang tidak didukung secara aman.

## Contoh

* `sĕkar` — Kosakata Jawa standar. Kedua profil memetakan kata ini secara identik ke pepet (schwa) Jawa dan konsonan asli.
* `BHAṬĀRA` — Kata serapan Sanskerta.
  * *Profil B* mempertahankan konsonan aspirasi `bʱ`, retrofleks `ṭ`, dan durasi vokal `aː`.
  * *Profil A* melebur aspirasi menjadi `b`, memetakan retrofleks menjadi `ṭ`, dan membiarkan durasi tetap tidak terpecahkan (unresolved).
  * *Acoustic Mapper* kemudian mengaproksimasi retrofleks `ṭ` menjadi dental `t` untuk kompatibilitas eSpeak.
* `śānti` — Kata serapan Sanskerta.
  * *Profil B* mempertahankan sibilan palatal `ś`.
  * *Profil A* meleburnya menjadi sibilan asli `s`.
* `kṝta` — Kata serapan Sanskerta dengan vokal likuida panjang.
  * *Profil B* mempertahankan bentuk kanonis panjang `r̩ː`.
  * *Profil A* mengadaptasinya ke fonotaktik asli sebagai bentuk dasar pepet Jawa (`rə`), secara sengaja membuang durasi non-pribumi sesuai kebijakan rekonstruksi.

## Trace / Diagnostik

Utilitas CLI `kawi-trace` memperlihatkan persis bagaimana transformasi setiap string bekerja. Utilitas ini menelusuri:
`Input → Normalized → Canonical → Profile Target → Backend Target`

Aproksimasi *backend* (contoh: ketidakmampuan eSpeak mengucapkan konsonan retrofleks) dibedakan secara jelas di output terminal dari target linguistik yang diniatkan.

## Struktur Proyek

```text
kawi_tts/        # Mesin inti (normalisasi, g2p, acoustic mappers)
docs/            # Dokumentasi proyek, kebijakan, dan log penelitian
tests/           # Rangkaian pengujian (test suite) dan korpus regresi
artifacts/       # Output manifest dan file WAV yang dihasilkan
pyproject.toml   # Konfigurasi build proyek
```

## Sumber Terbuka (*Open-Source*) & Kontribusi

Kawi-TTS adalah alat penelitian sumber terbuka.
* **Bukti Sebelum Kode:** Penelitian dan pembuktian literatur harus mendahului perubahan aturan linguistik apapun. Kontributor tidak boleh mengarang atau mereka-reka aturan pelafalan.
* **Perubahan:** Memodifikasi kebijakan linguistik memerlukan bukti yang dikutip (citable) dan cakupan regresi yang sesuai.
* **Batasan Layer:** Aproksimasi *backend* harus tetap dibatasi khusus pada *backend* (di dalam `AcousticMapper`). Representasi Kanonis harus tetap terlindungi.

Silakan lihat folder `docs/` untuk memahami keputusan arsitektur dan tata kelola (governance) proyek.

## Hubungan dengan Kawi Learn

**Kawi Learn** dianggap sebagai aplikasi edukasi eksternal di masa depan yang mungkin akan memanfaatkan Kawi-TTS.
* **Kawi-TTS:** Mesin deterministik untuk pelafalan dan rekonstruksi lisan.
* **Kawi Learn:** Aplikasi *end-user* di masa depan.

Kawi-TTS harus tetap terpisah dan sepenuhnya independen dari Kawi Learn. Saat ini Kawi Learn belum terwujud sebagai produk akhir.

## Pekerjaan Tertunda (*Deferred Work*)

Item-item berikut ditunda secara eksplisit untuk melindungi kendala tanpa-anggaran (*zero-budget constraint*):
* Model Neural TTS
* Pembuatan korpus suara rekaman khusus
* *Backend* akustik baru yang membutuhkan sumber daya komputasi di luar jangkauan (tidak tersedia)

Fitur-fitur tersebut hanya akan dibuka kembali jika persyaratan *packaging* dan ketersediaan *resource* telah terpenuhi secara memadai.

## Penelitian & Sitasi

Keputusan linguistik, pertanyaan terbuka, dan referensi rujukan utama dikelola di dalam `docs/RESEARCH_LOG.md` dan berbagai dokumen kebijakan terkait lainnya (contoh: `docs/P5_002_ACOUSTIC_PROFILE_POLICY.md`). Semua klaim linguistik dalam kode sumber ini bertaut dengan aturan-aturan kebijakan yang telah terliterasi tersebut.

## Lisensi

Kawi-TTS dilisensikan di bawah Lisensi MIT (MIT License). Lihat file `LICENSE` untuk keterangan lebih rinci.