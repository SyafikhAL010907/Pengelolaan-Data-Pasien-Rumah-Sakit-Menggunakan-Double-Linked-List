# PROMPT UNTUK AI AGENT (ADVANCED PROMPT ENGINEERING)

<Role>
Anda adalah seorang Senior Fullstack Python Developer (Flask), Ahli Struktur Data (Data Structures), dan UI/UX Web Designer. Anda memiliki keahlian menulis kode tingkat produksi (Production-Ready) dan arsitektur aplikasi serverless untuk Vercel.
</Role>

<Context>
Saya sedang membangun Web Application bertema HealthTech untuk "Sistem Pengelolaan Data Pasien Rumah Sakit" menggunakan Flask (Python) dan HTML/Tailwind CSS. Aplikasi ini harus dirancang agar "Vercel-Ready". Inti dari aplikasi ini adalah memanipulasi data menggunakan struktur data **Double Linked List (DLL)** secara in-memory.
</Context>

<Task>
Buatlah Full Source Code aplikasi web tersebut. Anda WAJIB SECARA KETAT menerjemahkan metodologi algoritma Double Linked List dari jurnal "JRIIN: Jurnal Riset Informatika dan Inovasi Volume 1, No. 12 Mei 2024 oleh Agung Wijoyo dkk" ke dalam class Python.
</Task>

<Data_Structure_Specs>
1. Class `Node` mewakili pasien, berisi: `id_pasien` (String), `nama` (String), `usia` (Integer), `diagnosa` (String), `prev` (Pointer), `next` (Pointer).
2. Class `DoubleLinkedList` berisi pointer `head` dan `tail`.
</Data_Structure_Specs>

<Strict_Algorithm_Rules>
Anda WAJIB menerjemahkan langkah-langkah algoritma berikut secara persis menjadi metode di dalam class `DoubleLinkedList`:

# A. INSERTION (Penyisipan)
1. Insert Di Depan:
   - Alokasikan memori untuk node baru dan inisialisasi nilai data.
   - Ubah pointer 'head' untuk menunjuk ke node baru.
   - Atur pointer 'prev' dari node baru ke NULL.
   - Atur pointer 'next' dari node baru ke node yang sebelumnya merupakan 'head'.
   - Perbarui pointer 'prev' dari node yang sebelumnya merupakan 'head' untuk menunjuk ke node baru.
2. Insert Di Tengah (Setelah Node Target):
   - Temukan node target di mana penyisipan akan dilakukan.
   - Ubah pointer 'next' dari node target ke node baru.
   - Ubah pointer 'prev' dari node baru ke node target.
   - Ubah pointer 'next' dari node baru ke node setelah target.
   - Ubah pointer 'prev' dari node setelah target ke node baru.
3. Insert Di Belakang:
   - Temukan node terakhir (tail).
   - Ubah pointer 'next' dari node terakhir ke node baru.
   - Atur pointer 'prev' dari node baru ke node terakhir.
   - Atur pointer 'next' dari node baru ke NULL.

# B. DELETION (Penghapusan)
1. Menemukan Node: Gunakan `id_pasien` sebagai kunci pencarian dan lintasi DLL dari awal hingga node ditemukan.
2. Hapus Node Pertama (Head):
   - Ubah pointer 'head' untuk menunjuk ke node berikutnya.
   - Jika DLL hanya memiliki satu node, ubah 'head' dan 'tail' menjadi NULL.
3. Hapus Node Terakhir (Tail):
   - Ubah pointer 'next' dari node sebelum tail ke NULL.
   - Ubah 'tail' untuk menunjuk ke node sebelum tail.
4. Hapus Node di Tengah:
   - Ubah pointer 'next' dari node sebelum ke node setelah node yang dihapus.
   - Ubah pointer 'prev' dari node setelah ke node sebelum node yang dihapus.

# C. TRAVERSAL (Tampil Data & Navigasi)
- Implementasikan metode `display_all()` yang melintasi (traversal) DLL dari depan ke belakang untuk mengembalikan semua data pasien dalam bentuk list of dictionary.
- Implementasikan mekanisme traversal dua arah menggunakan current state pointer untuk fitur "Prev" dan "Next".
</Strict_Algorithm_Rules>

<UI_UX_Specs>
Gunakan HTML dan Tailwind CSS (via CDN) dengan tema Medical Blue (`#0277BD`) dan background `#F8FAFC`. Desain WAJIB menggunakan sudut melengkung (`rounded-2xl`) dan bayangan (`shadow-lg`).
Buat layout Grid/Flexbox terbagi menjadi 3 bagian fungsional:
1. Card Form Aksi: Input Form (ID, Nama, Usia, Diagnosa) dan susunan tombol (Insert Depan, Insert Tengah, Insert Belakang, Hapus Depan, Hapus Belakang, Hapus by ID).
2. Card Data Seluruh Pasien: Sebuah tabel modern yang menampilkan seluruh data pasien secara berurutan (hasil dari `display_all()`).
3. Card Navigasi 2 Arah: Menampilkan data SATU pasien spesifik berdasarkan pointer saat ini, dilengkapi dengan tombol `[⬅ Prev]` dan `[Next ➡️]` untuk menelusuri DLL ke belakang dan ke depan.
</UI_UX_Specs>

<Output_Requirements>
Berikan blok kode yang terpisah dan siap pakai untuk 4 file berikut:
1. `app.py`: Backend Flask (Simpan instance DLL dalam variabel global agar state tersimpan).
2. `templates/index.html`: Frontend UI/UX.
3. `requirements.txt`: Dependensi (Flask, dll).
4. `vercel.json`: Konfigurasi Vercel (arahkan routes ke `app.py`).
Berikan kode penuh tanpa placeholder. Pastikan kodenya Clean Code!
</Output_Requirements>

# PROMPT UNTUK AI AGENT: UI/UX REFACTORING (TAILWIND CSS)

<Role>
Anda adalah seorang Senior UI/UX Web Developer dan Ahli Tailwind CSS.
</Role>

<Context>
Saya memiliki file `index.html` untuk aplikasi "Sistem Pengelolaan Data Pasien" yang sudah berfungsi dengan baik bersama backend Flask. Namun, desain UI saat ini terlalu pucat, kontras teksnya sangat rendah (sulit dibaca), dan tata letaknya terasa kurang profesional.
</Context>

<Task>
Tugas Anda adalah **HANYA memperbarui dan mempercantik kode Tailwind CSS di dalam file `index.html`**. 
Tingkatkan kontras, hierarki visual, tipografi, dan berikan sentuhan desain aplikasi HealthTech / Rumah Sakit yang modern, elegan, dan premium.
</Task>

<Strict_Rules>
1. **DILARANG KERAS** mengubah logika Jinja2 (`{% if %}`, `{% for %}`, `{{ variable }}`).
2. **DILARANG KERAS** mengubah atribut `name` pada `<input>`, `value` pada tombol, atau `action` pada `<form>`. Jika Anda mengubah ini, backend saya akan rusak!
3. HANYA ubah atribut `class` (Tailwind) dan struktur tag pembungkus (HTML tags seperti `div`, `span`, `header`) untuk keperluan *styling*.
</Strict_Rules>

<UI_UX_Improvement_Specs>
Terapkan panduan desain berikut menggunakan utilitas Tailwind CSS:

1. **Warna Tema & Latar Belakang:**
   - Ubah background `<body>` menjadi abu-abu kebiruan yang sangat muda (misal: `bg-slate-50`).
   - Buat sebuah `<header>` atau Navbar yang tegas di bagian atas menggunakan warna Medical Blue (misal: `bg-blue-700` atau `bg-sky-700`) dengan teks putih tebal agar judul aplikasi lebih menonjol.

2. **Tipografi & Kontras Teks (Sangat Penting):**
   - Hapus semua teks yang berwarna terlalu muda/pucat pada label form dan header tabel.
   - Gunakan `text-slate-800` atau `text-gray-900` untuk teks utama.
   - Gunakan `text-slate-500` atau `text-slate-600` dengan font `font-semibold` untuk label form.

3. **Gaya Kontainer (Cards):**
   - Pastikan semua panel (Form, Tabel, Navigasi) menggunakan card putih murni (`bg-white`), sudut melengkung modern (`rounded-2xl`), dan bayangan elegan (`shadow-xl` atau `shadow-lg`). Berikan jarak antar card (`gap` atau `margin`) yang proporsional.

4. **Desain Form & Input:**
   - Berikan border yang jelas pada `<input>` (`border-gray-300`).
   - Tambahkan efek fokus yang modern (misal: `focus:ring-2 focus:ring-blue-500 focus:border-blue-500`).

5. **Desain Tombol (Buttons):**
   - **Tombol Insert:** Gunakan gradasi atau warna solid yang segar (misal: `bg-teal-600 hover:bg-teal-700`).
   - **Tombol Delete:** Gunakan warna merah yang elegan (misal: `bg-rose-600 hover:bg-rose-700`).
   - Tambahkan transisi animasi pada semua tombol: `transition-all duration-200 transform hover:-translate-y-1 hover:shadow-md`.

6. **Desain Tabel Data Pasien:**
   - Bedakan warna bagian header tabel `<thead>` (misal dengan `bg-blue-50 text-blue-800`).
   - Berikan garis pemisah antar baris (`border-b border-gray-200`) dan efek `hover:bg-slate-50` pada `<tr>` agar interaktif.

7. **Desain Card Navigasi (Pointer):**
   - Rombak card "Current Pointer" agar terlihat seperti Kartu Pasien (ID Card). Posisikan teks ke tengah (`text-center`).
   - Buat tombol `[⬅ Prev]` dan `[Next ➡️]` lebih besar dan sejajar secara vertikal dengan informasi pasien.
</UI_UX_Improvement_Specs>

<Output_Requirements>
Berikan KODE LENGKAP HANYA UNTUK FILE `index.html`. Jangan berikan kode backend. Pastikan kode yang Anda berikan siap untuk di-copy-paste menggantikan `index.html` saya yang lama.
</Output_Requirements>