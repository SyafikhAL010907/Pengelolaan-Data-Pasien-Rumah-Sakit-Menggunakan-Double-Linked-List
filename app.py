"""
Sistem Pengelolaan Data Pasien Rumah Sakit
==========================================
Backend Flask dengan struktur data Double Linked List (DLL) in-memory.

Algoritma DLL diterjemahkan secara ketat dari jurnal:
"JRIIN: Jurnal Riset Informatika dan Inovasi Vol.1 No.12 Mei 2024
 oleh Agung Wijoyo dkk."
"""

from flask import Flask, render_template, request, jsonify
import json  # Logic Tambahan (Penguat: Musulmonov, 2024) - Backup & Restore
import os    # Logic Tambahan (Penguat: Musulmonov, 2024) - Backup & Restore


app = Flask(__name__)


# =============================================================================
# DATA STRUCTURE: Node
# =============================================================================
class Node:
    """
    Representasi satu pasien dalam Double Linked List.
    Setiap node menyimpan data pasien serta pointer prev dan next.
    """

    def __init__(self, id_pasien: str, nama: str, usia: int, diagnosa: str):
        self.id_pasien = id_pasien  # String — kunci unik pasien
        self.nama = nama            # String — nama lengkap pasien
        self.usia = usia            # Integer — usia pasien
        self.diagnosa = diagnosa    # String — diagnosa medis
        self.prev = None            # Pointer ke node sebelumnya (NULL/None)
        self.next = None            # Pointer ke node berikutnya (NULL/None)

    def to_dict(self) -> dict:
        """Konversi data node ke dictionary untuk serialisasi JSON."""
        return {
            "id_pasien": self.id_pasien,
            "nama": self.nama,
            "usia": self.usia,
            "diagnosa": self.diagnosa,
        }


# =============================================================================
# DATA STRUCTURE: Double Linked List
# =============================================================================
class DoubleLinkedList:
    """
    Implementasi Double Linked List (DLL) sesuai metodologi jurnal JRIIN.
    Menyimpan pointer head (node pertama) dan tail (node terakhir).
    """

    def __init__(self):
        self.head = None  # Pointer ke node pertama
        self.tail = None  # Pointer ke node terakhir

    # -------------------------------------------------------------------------
    # HELPER: Cari node berdasarkan id_pasien
    # -------------------------------------------------------------------------
    def _find_node(self, id_pasien: str):
        """
        Menemukan Node: Lintasi DLL dari awal (head) hingga node
        dengan id_pasien yang cocok ditemukan.
        Mengembalikan node jika ditemukan, None jika tidak ada.

        Time Complexity: O(n) — traversal linier dari head ke tail.
        """
        current = self.head
        while current is not None:
            if current.id_pasien == id_pasien:
                return current
            current = current.next
        return None

    # -------------------------------------------------------------------------
    # HELPER: Cek apakah id_pasien sudah ada (mencegah duplikat)
    # -------------------------------------------------------------------------
    def _id_exists(self, id_pasien: str) -> bool:
        """
        Traversal dari head untuk mengecek keberadaan id_pasien.

        Time Complexity: O(n) — mendelegasikan ke _find_node yang O(n).
        """
        return self._find_node(id_pasien) is not None

    # =========================================================================
    # A. INSERTION (Penyisipan)
    # =========================================================================

    def insert_depan(self, id_pasien: str, nama: str, usia: int, diagnosa: str) -> dict:
        """
        Insert Di Depan (Sesuai Jurnal):
        - Alokasi & Inisialisasi: Program mengalokasikan node baru dan menginisialisasi nilai data pasien di dalamnya.
        - Pointer head menunjuk ke node baru.
        - Pointer prev dari node baru diatur menjadi NULL.
        - Pointer next dari node baru diatur ke node yang sebelumnya merupakan head.
        - Pointer prev dari head lama diperbarui untuk menunjuk kembali ke node baru.

        Time Complexity: O(1) — manipulasi langsung pointer head, tanpa traversal.
        """
        # Validasi duplikat
        if self._id_exists(id_pasien):
            return {"success": False, "message": f"ID Pasien '{id_pasien}' sudah ada."}

        # Alokasi & Inisialisasi: Program mengalokasikan node baru dan menginisialisasi nilai data pasien di dalamnya.
        new_node = Node(id_pasien, nama, usia, diagnosa)

        # Pointer prev dari node baru diatur menjadi NULL.
        new_node.prev = None

        if self.head is None:
            new_node.next = None
            # Pointer head menunjuk ke node baru.
            self.head = new_node
            self.tail = new_node
        else:
            # Pointer next dari node baru diatur ke node yang sebelumnya merupakan head.
            new_node.next = self.head

            # Pointer prev dari head lama diperbarui untuk menunjuk kembali ke node baru.
            self.head.prev = new_node

            # Pointer head menunjuk ke node baru.
            self.head = new_node

        return {"success": True, "message": f"Pasien '{nama}' berhasil ditambahkan di depan."}

    def insert_belakang(self, id_pasien: str, nama: str, usia: int, diagnosa: str) -> dict:
        """
        Insert Di Belakang (Sesuai Jurnal):
        - Alokasi & Inisialisasi: Program mengalokasikan node baru dan menginisialisasi nilai data pasien di dalamnya.
        - Program melacak node terakhir (tail).
        - Pointer next dari node terakhir menunjuk ke node baru, pointer prev node baru menunjuk ke node terakhir, dan pointer next node baru diatur menjadi NULL.

        Time Complexity: O(1) — manipulasi langsung pointer tail, tanpa traversal.
        """
        # Validasi duplikat
        if self._id_exists(id_pasien):
            return {"success": False, "message": f"ID Pasien '{id_pasien}' sudah ada."}

        # Alokasi & Inisialisasi: Program mengalokasikan node baru dan menginisialisasi nilai data pasien di dalamnya.
        new_node = Node(id_pasien, nama, usia, diagnosa)

        if self.head is None:
            new_node.prev = None
            new_node.next = None
            self.head = new_node
            self.tail = new_node
        else:
            # Program melacak node terakhir (tail).
            last_node = self.tail
            
            # Membantu type checker memastikan last_node tidak None
            if last_node is not None:
                # Pointer next dari node terakhir menunjuk ke node baru, pointer prev node baru menunjuk ke node terakhir, dan pointer next node baru diatur menjadi NULL.
                last_node.next = new_node
                new_node.prev = last_node
                new_node.next = None
    
                # Update tail
                self.tail = new_node
        return {"success": True, "message": f"Pasien '{nama}' berhasil ditambahkan di belakang."}

    def insert_tengah(self, id_pasien: str, nama: str, usia: int, diagnosa: str,
                      target_id: str) -> dict:
        """
        Insert Di Tengah (Sesuai Jurnal):
        - Alokasi & Inisialisasi: Program mengalokasikan node baru dan menginisialisasi nilai data pasien di dalamnya.
        - Program mampu menemukan node sebelum target penyisipan.
        - Pointer next dari node sebelum diubah ke node baru, pointer prev node baru diubah ke node sebelum.
        - Pointer next node baru diubah ke node target, dan pointer prev node target diubah ke node baru.

        Time Complexity: O(n) — traversal untuk menemukan node target.
        """
        # Validasi DLL kosong
        if self.head is None:
            return {"success": False, "message": "Linked list kosong. Tidak bisa insert di tengah."}

        # Validasi duplikat
        if self._id_exists(id_pasien):
            return {"success": False, "message": f"ID Pasien '{id_pasien}' sudah ada."}

        # Program mampu menemukan node sebelum target penyisipan.
        target_node = self._find_node(target_id)
        if target_node is None:
            return {"success": False, "message": f"Node target dengan ID '{target_id}' tidak ditemukan."}

        # Alokasi & Inisialisasi: Program mengalokasikan node baru dan menginisialisasi nilai data pasien di dalamnya.
        new_node = Node(id_pasien, nama, usia, diagnosa)

        # Referensi node setelah target
        node_after_target = target_node.next

        # Pointer next dari node sebelum diubah ke node baru, pointer prev node baru diubah ke node sebelum.
        target_node.next = new_node
        new_node.prev = target_node

        # Pointer next node baru diubah ke node target, dan pointer prev node target diubah ke node baru.
        new_node.next = node_after_target
        if node_after_target is not None:
            node_after_target.prev = new_node
        else:
            self.tail = new_node

        return {"success": True, "message": f"Pasien '{nama}' berhasil ditambahkan setelah ID '{target_id}'."}

    # =========================================================================
    # B. DELETION (Penghapusan)
    # =========================================================================

    def hapus_depan(self) -> dict:
        """
        Hapus Node Pertama / Head (Kasus 1 Sesuai Jurnal):
        - Pointer head digeser ke node berikutnya; 
        - jika list hanya berisi satu node, maka head dan tail diubah menjadi NULL.

        Time Complexity: O(1) — manipulasi langsung pointer head, tanpa traversal.
        """
        if self.head is None:
            return {"success": False, "message": "Linked list kosong. Tidak ada data untuk dihapus."}

        deleted_name = self.head.nama

        if self.head == self.tail:
            # jika list hanya berisi satu node, maka head dan tail diubah menjadi NULL.
            self.head = None
            self.tail = None
        else:
            # Pointer head digeser ke node berikutnya
            self.head = self.head.next
            self.head.prev = None

        return {"success": True, "message": f"Pasien '{deleted_name}' (node pertama) berhasil dihapus."}

    def hapus_belakang(self) -> dict:
        """
        Hapus Node Terakhir / Tail (Kasus 2 Sesuai Jurnal):
        - Pointer next dari node sebelum tail diubah menjadi NULL, dan ubah 'tail' untuk menunjuk ke node sebelum tail.

        Time Complexity: O(1) — manipulasi langsung pointer tail, tanpa traversal.
        """
        if self.tail is None:
            return {"success": False, "message": "Linked list kosong. Tidak ada data untuk dihapus."}

        deleted_name = self.tail.nama

        if self.head == self.tail:
            # jika list hanya berisi satu node, maka head dan tail diubah menjadi NULL.
            self.head = None
            self.tail = None
        else:
            # Pointer next dari node sebelum tail diubah menjadi NULL, dan ubah 'tail' untuk menunjuk ke node sebelum tail.
            self.tail.prev.next = None
            self.tail = self.tail.prev

        return {"success": True, "message": f"Pasien '{deleted_name}' (node terakhir) berhasil dihapus."}

    def hapus_by_id(self, id_pasien: str) -> dict:
        """
        Hapus Node (Pencarian Node Target & Kasus 3 Sesuai Jurnal):
        - Pencarian Node Target: Menggunakan kunci pencarian data untuk melintasi DLL dari awal hingga node yang sesuai ditemukan.
        - Kasus 3 (Node di Tengah): Ubah pointer 'next' dari node sebelum ke node setelah node yang dihapus, dan ubah pointer 'prev' dari node setelah ke node sebelum node yang dihapus.

        Time Complexity: O(n) — traversal untuk menemukan node target.
        """
        if self.head is None:
            return {"success": False, "message": "Linked list kosong. Tidak ada data untuk dihapus."}

        # Pencarian Node Target: Menggunakan kunci pencarian data untuk melintasi DLL dari awal hingga node yang sesuai ditemukan.
        target = self._find_node(id_pasien)
        if target is None:
            return {"success": False, "message": f"Pasien dengan ID '{id_pasien}' tidak ditemukan."}

        deleted_name = target.nama

        if target == self.head:
            return self.hapus_depan()

        if target == self.tail:
            return self.hapus_belakang()

        # Kasus 3 (Node di Tengah): Ubah pointer 'next' dari node sebelum ke node setelah node yang dihapus, dan ubah pointer 'prev' dari node setelah ke node sebelum node yang dihapus.
        target.prev.next = target.next
        target.next.prev = target.prev

        return {"success": True, "message": f"Pasien '{deleted_name}' (ID: {id_pasien}) berhasil dihapus."}

    # =========================================================================
    # C. TRAVERSAL (Tampil Data & Navigasi)
    # =========================================================================

    def display_all(self) -> list:
        """
        Traversal dari depan ke belakang.
        Melintasi DLL dari head → tail, mengumpulkan data setiap node
        ke dalam list of dictionary.

        Time Complexity: O(n) — traversal penuh dari head ke tail.
        """
        result = []
        current = self.head
        while current is not None:
            result.append(current.to_dict())
            current = current.next
        return result

    def count(self) -> int:
        """
        Hitung jumlah total node dalam DLL.

        Time Complexity: O(n) — traversal penuh dari head ke tail.
        """
        total = 0
        current = self.head
        while current is not None:
            total += 1
            current = current.next
        return total

    def cari_pasien(self, id_pasien: str):
        """
        Mencari pasien berdasarkan ID dengan melintasi (traversal) node dari head ke tail.
        Mengembalikan dict data pasien jika ditemukan, atau None jika tidak ditemukan.

        Time Complexity: O(n) — traversal linier untuk mencari node.
        """
        node = self._find_node(id_pasien)
        if node is not None:
            return node.to_dict()
        return None

    # =========================================================================
    # D. UPDATING (Logic Tambahan: Musulmonov, 2024)
    # =========================================================================

    # Logic Tambahan (Penguat: Musulmonov, 2024) - Updating
    def update_pasien(self, id_pasien: str, nama: str | None = None, usia: int | None = None, diagnosa: str | None = None) -> dict:
        """
        Memperbarui data pasien berdasarkan id_pasien.
        Traversal untuk menemukan node, lalu update field yang diberikan.

        Time Complexity: O(n) — traversal linier untuk menemukan node target.
        """
        # Logic Tambahan (Penguat: Musulmonov, 2024) - Updating (cari node target)
        node = self._find_node(id_pasien)
        if node is None:
            return {"success": False, "message": f"Pasien dengan ID '{id_pasien}' tidak ditemukan."}

        # Logic Tambahan (Penguat: Musulmonov, 2024) - Updating (perbarui field)
        if nama is not None:
            node.nama = nama
        if usia is not None:
            node.usia = usia
        if diagnosa is not None:
            node.diagnosa = diagnosa

        return {"success": True, "message": f"Data pasien '{node.nama}' (ID: {id_pasien}) berhasil diperbarui."}

    # =========================================================================
    # E. MULTI-CRITERIA SEARCH (Logic Tambahan: Musulmonov, 2024)
    # =========================================================================

    # Logic Tambahan (Penguat: Musulmonov, 2024) - Multi-Criteria Search
    def cari_by_nama(self, keyword: str) -> list:
        """
        Mencari pasien berdasarkan nama (substring matching, case-insensitive).
        Traversal dari head ke tail, mengumpulkan semua node yang cocok.

        Time Complexity: O(n) — traversal penuh dari head ke tail.
        """
        # Logic Tambahan (Penguat: Musulmonov, 2024) - Multi-Criteria Search (inisialisasi)
        results = []
        current = self.head
        keyword_lower = keyword.lower()  # Logic Tambahan (Penguat: Musulmonov, 2024) - Multi-Criteria Search
        while current is not None:
            # Logic Tambahan (Penguat: Musulmonov, 2024) - Multi-Criteria Search (substring match)
            if keyword_lower in current.nama.lower():
                results.append(current.to_dict())
            current = current.next
        return results

    # =========================================================================
    # F. SORTING (Logic Tambahan: Musulmonov, 2024)
    # =========================================================================

    # Logic Tambahan (Penguat: Musulmonov, 2024) - Sorting
    def sort_by_nama(self) -> dict:
        """
        Mengurutkan DLL berdasarkan nama pasien secara ascending (A-Z).
        Menggunakan Bubble Sort dengan pertukaran data antar node
        (bukan pointer) agar pointer prev/next tetap konsisten.

        Time Complexity: O(n²) — Bubble Sort nested loop.
        """
        # Logic Tambahan (Penguat: Musulmonov, 2024) - Sorting (edge case)
        if self.head is None or self.head == self.tail:
            return {"success": True, "message": "Linked list kosong atau hanya 1 node, tidak perlu sorting."}

        # Logic Tambahan (Penguat: Musulmonov, 2024) - Sorting (Bubble Sort loop)
        swapped = True
        while swapped:
            swapped = False
            current = self.head
            while current is not None and current.next is not None:
                # Logic Tambahan (Penguat: Musulmonov, 2024) - Sorting (perbandingan alphabetical)
                if current.nama.lower() > current.next.nama.lower():
                    # Logic Tambahan (Penguat: Musulmonov, 2024) - Sorting (swap data, bukan pointer)
                    current.id_pasien, current.next.id_pasien = current.next.id_pasien, current.id_pasien
                    current.nama, current.next.nama = current.next.nama, current.nama
                    current.usia, current.next.usia = current.next.usia, current.usia
                    current.diagnosa, current.next.diagnosa = current.next.diagnosa, current.diagnosa
                    swapped = True
                current = current.next

        return {"success": True, "message": "Data pasien berhasil diurutkan berdasarkan nama (A-Z)."}

    # =========================================================================
    # G. MULTI-CRITERIA DELETION (Logic Tambahan: Musulmonov, 2024)
    # =========================================================================

    # Logic Tambahan (Penguat: Musulmonov, 2024) - Multi-Criteria Deletion
    def hapus_by_nama(self, nama: str) -> dict:
        """
        Menghapus node pasien pertama yang cocok berdasarkan nama
        (exact match, case-insensitive). Traversal dari head untuk
        menemukan node target, lalu re-link pointer sekitar node tersebut.

        Time Complexity: O(n) — traversal linier untuk menemukan node target.
        """
        # Logic Tambahan (Penguat: Musulmonov, 2024) - Multi-Criteria Deletion (validasi kosong)
        if self.head is None:
            return {"success": False, "message": "Linked list kosong. Tidak ada data untuk dihapus."}

        # Logic Tambahan (Penguat: Musulmonov, 2024) - Multi-Criteria Deletion (traversal by nama)
        current = self.head
        nama_lower = nama.lower()
        while current is not None:
            if current.nama.lower() == nama_lower:
                deleted_name = current.nama

                # Logic Tambahan (Penguat: Musulmonov, 2024) - Multi-Criteria Deletion (re-link pointer)
                if current == self.head:
                    return self.hapus_depan()
                if current == self.tail:
                    return self.hapus_belakang()

                # Logic Tambahan (Penguat: Musulmonov, 2024) - Multi-Criteria Deletion (node tengah)
                current.prev.next = current.next
                current.next.prev = current.prev
                return {"success": True, "message": f"Pasien '{deleted_name}' berhasil dihapus berdasarkan nama."}

            current = current.next

        return {"success": False, "message": f"Pasien dengan nama '{nama}' tidak ditemukan."}

    # =========================================================================
    # H. BACKUP & RESTORE HELPERS (Logic Tambahan: Musulmonov, 2024)
    # =========================================================================

    # Logic Tambahan (Penguat: Musulmonov, 2024) - Backup & Restore
    def to_json_list(self) -> list:
        """
        Mengkonversi seluruh DLL ke list of dict untuk serialisasi JSON.

        Time Complexity: O(n) — traversal penuh dari head ke tail.
        """
        # Logic Tambahan (Penguat: Musulmonov, 2024) - Backup & Restore
        return self.display_all()

    # Logic Tambahan (Penguat: Musulmonov, 2024) - Backup & Restore
    def load_from_list(self, data_list: list) -> None:
        """
        Memuat data dari list of dict ke DLL menggunakan insert_belakang.
        Menghapus seluruh isi DLL sebelum memuat data baru.

        Time Complexity: O(n) — iterasi dan insert untuk setiap elemen.
        """
        # Logic Tambahan (Penguat: Musulmonov, 2024) - Backup & Restore (reset DLL)
        self.head = None
        self.tail = None

        # Logic Tambahan (Penguat: Musulmonov, 2024) - Backup & Restore (rebuild DLL)
        for item in data_list:
            self.insert_belakang(
                id_pasien=item["id_pasien"],
                nama=item["nama"],
                usia=item["usia"],
                diagnosa=item["diagnosa"],
            )



# =============================================================================
# GLOBAL STATE
# =============================================================================
# Instance DLL disimpan dalam variabel global agar state tersimpan in-memory
# selama server Flask berjalan.
dll = DoubleLinkedList()

# Current pointer untuk navigasi 2 arah (Prev/Next)
current_pointer = None


# =============================================================================
# BACKUP & RESTORE — FILE PERSISTENCE (Logic Tambahan: Musulmonov, 2024)
# =============================================================================
# Logic Tambahan (Penguat: Musulmonov, 2024) - Backup & Restore
BACKUP_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backup_pasien.json")

# Logic Tambahan (Penguat: Musulmonov, 2024) - Toggle Sorting
# File terpisah khusus untuk menyimpan snapshot SEBELUM sort, agar tidak
# bisa ditimpa oleh auto_backup_after_mutation (yang berjalan setelah sort).
PRESORT_BACKUP_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "presort_snapshot.json")


# Logic Tambahan (Penguat: Musulmonov, 2024) - Backup & Restore
def backup_to_file():
    """Menyimpan seluruh data DLL ke file JSON lokal."""
    # Logic Tambahan (Penguat: Musulmonov, 2024) - Backup & Restore (serialisasi ke JSON)
    try:
        with open(BACKUP_FILE, "w", encoding="utf-8") as f:
            json.dump(dll.to_json_list(), f, ensure_ascii=False, indent=2)
    except IOError as e:
        print(f"[Backup Error] Gagal menyimpan backup: {e}")


# Logic Tambahan (Penguat: Musulmonov, 2024) - Backup & Restore
def restore_from_file():
    """Memuat data dari file JSON ke DLL saat server startup."""
    # Logic Tambahan (Penguat: Musulmonov, 2024) - Backup & Restore (baca file JSON)
    if os.path.exists(BACKUP_FILE):
        try:
            with open(BACKUP_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list) and len(data) > 0:
                dll.load_from_list(data)
                print(f"[Restore] Berhasil memuat {len(data)} data pasien dari backup.")
        except (IOError, json.JSONDecodeError) as e:
            print(f"[Restore Error] Gagal memuat backup: {e}")


# Logic Tambahan (Penguat: Musulmonov, 2024) - Toggle Sorting
def presort_backup_to_file():
    """Simpan snapshot DLL ke file TERPISAH sebelum sorting dilakukan.
    File ini tidak akan pernah ditimpa oleh auto_backup_after_mutation."""
    try:
        with open(PRESORT_BACKUP_FILE, "w", encoding="utf-8") as f:
            json.dump(dll.to_json_list(), f, ensure_ascii=False, indent=2)
        print(f"[PreSort Snapshot] Urutan asli disimpan ke {PRESORT_BACKUP_FILE}")
    except IOError as e:
        print(f"[PreSort Snapshot Error] Gagal menyimpan: {e}")


# Logic Tambahan (Penguat: Musulmonov, 2024) - Toggle Sorting
def presort_restore_from_file():
    """Muat kembali snapshot urutan asli dari file presort ke DLL."""
    if os.path.exists(PRESORT_BACKUP_FILE):
        try:
            with open(PRESORT_BACKUP_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list) and len(data) > 0:
                dll.load_from_list(data)
                # Sync juga ke backup utama agar konsisten
                backup_to_file()
                print(f"[PreSort Restore] {len(data)} data pasien urutan asli berhasil dipulihkan.")
                return True
        except (IOError, json.JSONDecodeError) as e:
            print(f"[PreSort Restore Error] Gagal memuat: {e}")
    return False


# Logic Tambahan (Penguat: Musulmonov, 2024) - Backup & Restore (auto-restore saat startup)
restore_from_file()


# =============================================================================
# FLASK ROUTES
# =============================================================================

@app.route("/")
def index():
    """Render halaman utama."""
    return render_template("index.html")


# ---------- API: Insert ----------

@app.route("/api/insert/depan", methods=["POST"])
def api_insert_depan():
    """Insert node baru di depan (head) DLL."""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Request body kosong."}), 400

    # Validasi field wajib
    required = ["id_pasien", "nama", "usia", "diagnosa"]
    for field in required:
        if field not in data or str(data[field]).strip() == "":
            return jsonify({"success": False, "message": f"Field '{field}' wajib diisi."}), 400

    try:
        usia = int(data["usia"])
    except (ValueError, TypeError):
        return jsonify({"success": False, "message": "Usia harus berupa angka."}), 400

    result = dll.insert_depan(
        id_pasien=str(data["id_pasien"]).strip(),
        nama=str(data["nama"]).strip(),
        usia=usia,
        diagnosa=str(data["diagnosa"]).strip(),
    )
    status = 201 if result["success"] else 409
    return jsonify(result), status


@app.route("/api/insert/belakang", methods=["POST"])
def api_insert_belakang():
    """Insert node baru di belakang (tail) DLL."""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Request body kosong."}), 400

    required = ["id_pasien", "nama", "usia", "diagnosa"]
    for field in required:
        if field not in data or str(data[field]).strip() == "":
            return jsonify({"success": False, "message": f"Field '{field}' wajib diisi."}), 400

    try:
        usia = int(data["usia"])
    except (ValueError, TypeError):
        return jsonify({"success": False, "message": "Usia harus berupa angka."}), 400

    result = dll.insert_belakang(
        id_pasien=str(data["id_pasien"]).strip(),
        nama=str(data["nama"]).strip(),
        usia=usia,
        diagnosa=str(data["diagnosa"]).strip(),
    )
    status = 201 if result["success"] else 409
    return jsonify(result), status


@app.route("/api/move/tengah", methods=["POST"])
def api_move_tengah():
    """Pindahkan node yang SUDAH ADA ke posisi setelah node target (atomik: hapus + insert).
    Digunakan pada alur Edit + Insert Tengah ketika id_pasien sudah terdaftar di DLL."""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Request body kosong."}), 400

    required = ["id_pasien", "nama", "usia", "diagnosa", "target_id"]
    for field in required:
        if field not in data or str(data[field]).strip() == "":
            return jsonify({"success": False, "message": f"Field '{field}' wajib diisi."}), 400

    try:
        usia = int(data["usia"])
    except (ValueError, TypeError):
        return jsonify({"success": False, "message": "Usia harus berupa angka."}), 400

    id_pasien  = str(data["id_pasien"]).strip()
    nama       = str(data["nama"]).strip()
    diagnosa   = str(data["diagnosa"]).strip()
    target_id  = str(data["target_id"]).strip()

    # Pastikan target berbeda dengan node itu sendiri
    if id_pasien == target_id:
        return jsonify({"success": False, "message": "ID Target tidak boleh sama dengan ID pasien yang dipindahkan."}), 400

    # Cek node yang akan dipindahkan memang ada
    if not dll._id_exists(id_pasien):
        return jsonify({"success": False, "message": f"Pasien dengan ID '{id_pasien}' tidak ditemukan."}), 404

    # Cek node target ada
    if not dll._id_exists(target_id):
        return jsonify({"success": False, "message": f"Node target dengan ID '{target_id}' tidak ditemukan."}), 404

    # Langkah 1: Hapus node lama dari DLL
    del_result = dll.hapus_by_id(id_pasien)
    if not del_result["success"]:
        return jsonify({"success": False, "message": f"Gagal menghapus node lama: {del_result['message']}"}), 500

    # Langkah 2: Insert node baru setelah target
    ins_result = dll.insert_tengah(
        id_pasien=id_pasien,
        nama=nama,
        usia=usia,
        diagnosa=diagnosa,
        target_id=target_id,
    )
    if not ins_result["success"]:
        # Rollback: kembalikan node ke belakang agar data tidak hilang
        dll.insert_belakang(id_pasien=id_pasien, nama=nama, usia=usia, diagnosa=diagnosa)
        return jsonify({"success": False, "message": f"Gagal menyisipkan node: {ins_result['message']} (node dikembalikan ke posisi belakang)"}), 409

    return jsonify({"success": True, "message": f"Pasien '{nama}' (ID: {id_pasien}) berhasil dipindahkan setelah ID '{target_id}'."}), 200


@app.route("/api/insert/tengah", methods=["POST"])
def api_insert_tengah():
    """Insert node baru di tengah DLL (setelah node target)."""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Request body kosong."}), 400

    required = ["id_pasien", "nama", "usia", "diagnosa", "target_id"]
    for field in required:
        if field not in data or str(data[field]).strip() == "":
            return jsonify({"success": False, "message": f"Field '{field}' wajib diisi."}), 400

    try:
        usia = int(data["usia"])
    except (ValueError, TypeError):
        return jsonify({"success": False, "message": "Usia harus berupa angka."}), 400

    result = dll.insert_tengah(
        id_pasien=str(data["id_pasien"]).strip(),
        nama=str(data["nama"]).strip(),
        usia=usia,
        diagnosa=str(data["diagnosa"]).strip(),
        target_id=str(data["target_id"]).strip(),
    )
    status = 201 if result["success"] else 409
    return jsonify(result), status


# ---------- API: Delete ----------

@app.route("/api/hapus/depan", methods=["DELETE"])
def api_hapus_depan():
    """Hapus node pertama (head) dari DLL."""
    result = dll.hapus_depan()
    status = 200 if result["success"] else 404
    return jsonify(result), status


@app.route("/api/hapus/belakang", methods=["DELETE"])
def api_hapus_belakang():
    """Hapus node terakhir (tail) dari DLL."""
    result = dll.hapus_belakang()
    status = 200 if result["success"] else 404
    return jsonify(result), status


@app.route("/api/hapus/id", methods=["DELETE"])
def api_hapus_by_id():
    """Hapus node berdasarkan id_pasien."""
    data = request.get_json()
    if not data or "id_pasien" not in data or str(data["id_pasien"]).strip() == "":
        return jsonify({"success": False, "message": "Field 'id_pasien' wajib diisi."}), 400

    result = dll.hapus_by_id(str(data["id_pasien"]).strip())
    status = 200 if result["success"] else 404
    return jsonify(result), status


# ---------- API: Display All (Traversal) ----------

@app.route("/api/pasien", methods=["GET"])
def api_display_all():
    """Traversal: tampilkan semua data pasien dari head ke tail."""
    return jsonify({
        "success": True,
        "data": dll.display_all(),
        "count": dll.count(),
    })


# ---------- API: Cari Pasien by ID ----------

@app.route("/cari", methods=["POST"])
@app.route("/api/cari", methods=["POST"])
def api_cari_pasien():
    """Mencari pasien berdasarkan id_pasien (traversal head -> tail)."""
    data = request.get_json()
    if not data or "id_pasien" not in data or str(data["id_pasien"]).strip() == "":
        return jsonify({"success": False, "message": "Field 'id_pasien' wajib diisi."}), 400

    id_pasien = str(data["id_pasien"]).strip()
    pasien = dll.cari_pasien(id_pasien)
    if pasien:
        return jsonify({
            "success": True,
            "data": pasien,
            "message": f"Pasien dengan ID '{id_pasien}' berhasil ditemukan."
        }), 200
    else:
        return jsonify({
            "success": False,
            "data": None,
            "message": f"Pasien dengan ID '{id_pasien}' tidak ditemukan."
        }), 404



# ---------- API: Navigasi 2 Arah ----------

@app.route("/api/navigate/current", methods=["GET"])
def api_nav_current():
    """Dapatkan data pasien pada posisi pointer saat ini."""
    global current_pointer

    if dll.head is None:
        current_pointer = None
        return jsonify({"success": False, "data": None, "message": "Linked list kosong."})

    # Inisialisasi pointer jika belum ada atau sudah stale
    if current_pointer is None or dll._find_node(current_pointer.id_pasien) is None:
        current_pointer = dll.head

    return jsonify({
        "success": True,
        "data": current_pointer.to_dict(),
        "has_prev": current_pointer.prev is not None,
        "has_next": current_pointer.next is not None,
    })


@app.route("/api/navigate/prev", methods=["POST"])
def api_nav_prev():
    """Gerakkan pointer ke node sebelumnya (traversal mundur)."""
    global current_pointer

    if current_pointer is None or dll.head is None:
        return jsonify({"success": False, "message": "Tidak ada data untuk dinavigasi."})

    # Re-validasi pointer masih ada di DLL
    if dll._find_node(current_pointer.id_pasien) is None:
        current_pointer = dll.head

    if current_pointer.prev is not None:
        current_pointer = current_pointer.prev

    return jsonify({
        "success": True,
        "data": current_pointer.to_dict(),
        "has_prev": current_pointer.prev is not None,
        "has_next": current_pointer.next is not None,
    })


@app.route("/api/navigate/next", methods=["POST"])
def api_nav_next():
    """Gerakkan pointer ke node berikutnya (traversal maju)."""
    global current_pointer

    if current_pointer is None or dll.head is None:
        return jsonify({"success": False, "message": "Tidak ada data untuk dinavigasi."})

    # Re-validasi pointer masih ada di DLL
    if dll._find_node(current_pointer.id_pasien) is None:
        current_pointer = dll.head

    if current_pointer.next is not None:
        current_pointer = current_pointer.next

    return jsonify({
        "success": True,
        "data": current_pointer.to_dict(),
        "has_prev": current_pointer.prev is not None,
        "has_next": current_pointer.next is not None,
    })


# =============================================================================
# API ROUTES TAMBAHAN (Logic Tambahan: Musulmonov, 2024)
# =============================================================================

# ---------- API: Update Pasien (Logic Tambahan: Musulmonov, 2024) ----------

# Logic Tambahan (Penguat: Musulmonov, 2024) - Updating
@app.route("/api/update", methods=["PUT"])
def api_update_pasien():
    """Memperbarui data pasien berdasarkan id_pasien."""
    data = request.get_json()
    if not data or "id_pasien" not in data or str(data["id_pasien"]).strip() == "":
        return jsonify({"success": False, "message": "Field 'id_pasien' wajib diisi."}), 400

    # Logic Tambahan (Penguat: Musulmonov, 2024) - Updating (parsing field)
    id_pasien = str(data["id_pasien"]).strip()
    nama = str(data["nama"]).strip() if "nama" in data and data["nama"] else None
    diagnosa = str(data["diagnosa"]).strip() if "diagnosa" in data and data["diagnosa"] else None
    usia = None
    if "usia" in data and data["usia"] is not None and str(data["usia"]).strip() != "":
        try:
            usia = int(data["usia"])
        except (ValueError, TypeError):
            return jsonify({"success": False, "message": "Usia harus berupa angka."}), 400

    # Logic Tambahan (Penguat: Musulmonov, 2024) - Updating (panggil method DLL)
    result = dll.update_pasien(id_pasien, nama=nama, usia=usia, diagnosa=diagnosa)
    status = 200 if result["success"] else 404
    return jsonify(result), status


# ---------- API: Cari Pasien by Nama (Logic Tambahan: Musulmonov, 2024) ----------

# Logic Tambahan (Penguat: Musulmonov, 2024) - Multi-Criteria Search
@app.route("/api/cari/nama", methods=["POST"])
def api_cari_by_nama():
    """Mencari pasien berdasarkan nama (substring matching)."""
    data = request.get_json()
    if not data or "nama" not in data or str(data["nama"]).strip() == "":
        return jsonify({"success": False, "message": "Field 'nama' wajib diisi."}), 400

    # Logic Tambahan (Penguat: Musulmonov, 2024) - Multi-Criteria Search (panggil method DLL)
    keyword = str(data["nama"]).strip()
    results = dll.cari_by_nama(keyword)

    if results:
        return jsonify({
            "success": True,
            "data": results,
            "count": len(results),
            "message": f"Ditemukan {len(results)} pasien dengan nama mengandung '{keyword}'."
        }), 200
    else:
        return jsonify({
            "success": False,
            "data": [],
            "count": 0,
            "message": f"Tidak ditemukan pasien dengan nama mengandung '{keyword}'."
        }), 404


# ---------- API: Sort by Nama (Logic Tambahan: Musulmonov, 2024) ----------

# Logic Tambahan (Penguat: Musulmonov, 2024) - Toggle Sorting
@app.route("/api/sort/nama", methods=["POST"])
def api_sort_by_nama():
    """Mengurutkan DLL berdasarkan nama pasien (A-Z).
    Sebelum sort, simpan snapshot urutan asli ke file presort terpisah
    agar tidak tertimpa oleh auto-backup yang berjalan setelah sort.
    """
    # Logic Tambahan (Penguat: Musulmonov, 2024) - Toggle Sorting (simpan snapshot urutan asli)
    presort_backup_to_file()
    # Logic Tambahan (Penguat: Musulmonov, 2024) - Sorting (panggil method DLL)
    result = dll.sort_by_nama()
    return jsonify(result), 200


# Logic Tambahan (Penguat: Musulmonov, 2024) - Toggle Sorting
@app.route("/api/restore/presort", methods=["POST"])
def api_restore_presort():
    """Memulihkan DLL ke urutan asli sebelum sort (dari presort snapshot)."""
    # Logic Tambahan (Penguat: Musulmonov, 2024) - Toggle Sorting (restore dari presort snapshot)
    ok = presort_restore_from_file()
    if ok:
        return jsonify({
            "success": True,
            "message": f"Urutan asli berhasil dipulihkan. {dll.count()} pasien dimuat.",
            "count": dll.count(),
        }), 200
    return jsonify({
        "success": False,
        "message": "Snapshot urutan asli tidak ditemukan. Lakukan Sort A-Z terlebih dahulu.",
    }), 404


# ---------- API: Hapus by Nama (Logic Tambahan: Musulmonov, 2024) ----------

# Logic Tambahan (Penguat: Musulmonov, 2024) - Multi-Criteria Deletion
@app.route("/api/hapus/nama", methods=["DELETE"])
def api_hapus_by_nama():
    """Menghapus pasien berdasarkan nama (exact match, case-insensitive)."""
    data = request.get_json()
    if not data or "nama" not in data or str(data["nama"]).strip() == "":
        return jsonify({"success": False, "message": "Field 'nama' wajib diisi."}), 400

    # Logic Tambahan (Penguat: Musulmonov, 2024) - Multi-Criteria Deletion (panggil method DLL)
    result = dll.hapus_by_nama(str(data["nama"]).strip())
    status = 200 if result["success"] else 404
    return jsonify(result), status


# ---------- API: Backup & Restore Manual (Logic Tambahan: Musulmonov, 2024) ----------

# Logic Tambahan (Penguat: Musulmonov, 2024) - Backup & Restore
@app.route("/api/backup", methods=["POST"])
def api_backup():
    """Menyimpan data DLL ke file JSON (manual trigger)."""
    # Logic Tambahan (Penguat: Musulmonov, 2024) - Backup & Restore (manual backup)
    backup_to_file()
    return jsonify({"success": True, "message": "Backup berhasil disimpan ke file JSON."}), 200


# Logic Tambahan (Penguat: Musulmonov, 2024) - Backup & Restore
@app.route("/api/restore", methods=["POST"])
def api_restore():
    """Memuat data DLL dari file JSON (manual trigger)."""
    # Logic Tambahan (Penguat: Musulmonov, 2024) - Backup & Restore (manual restore)
    restore_from_file()
    return jsonify({
        "success": True,
        "message": f"Restore berhasil. {dll.count()} data pasien dimuat dari backup.",
        "count": dll.count(),
    }), 200


# ---------- Auto-Backup Middleware (Logic Tambahan: Musulmonov, 2024) ----------

# Logic Tambahan (Penguat: Musulmonov, 2024) - Backup & Restore (auto-backup middleware)
@app.after_request
def auto_backup_after_mutation(response):
    """Auto-backup setelah setiap operasi mutasi (insert/delete/update/sort) berhasil."""
    # Logic Tambahan (Penguat: Musulmonov, 2024) - Backup & Restore (auto-backup logic)
    if request.method in ("POST", "PUT", "DELETE") and response.status_code in (200, 201):
        # Hanya backup untuk operasi mutasi, bukan navigasi/pencarian/backup-restore itu sendiri.
        # /api/sort/nama dikecualikan karena sudah mengelola presort_backup sendiri sebelum sort;
        # auto-backup di sini justru akan menimpa snapshot urutan asli dengan data ter-sort.
        skip_paths = ["/api/navigate/", "/api/cari", "/api/backup", "/api/restore", "/api/sort/"]
        if not any(request.path.startswith(p) for p in skip_paths):
            backup_to_file()
    return response


# =============================================================================
# ENTRYPOINT
# =============================================================================
if __name__ == "__main__":
    app.run(debug=True, port=5000)
