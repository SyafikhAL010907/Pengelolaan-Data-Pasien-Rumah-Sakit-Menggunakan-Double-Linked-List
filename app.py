"""
Sistem Pengelolaan Data Pasien Rumah Sakit
==========================================
Backend Flask dengan struktur data Double Linked List (DLL) in-memory.

Algoritma DLL diterjemahkan secara ketat dari jurnal:
"JRIIN: Jurnal Riset Informatika dan Inovasi Vol.1 No.12 Mei 2024
 oleh Agung Wijoyo dkk."
"""

from flask import Flask, render_template, request, jsonify

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
        """Traversal dari head untuk mengecek keberadaan id_pasien."""
        return self._find_node(id_pasien) is not None

    # =========================================================================
    # A. INSERTION (Penyisipan)
    # =========================================================================

    def insert_depan(self, id_pasien: str, nama: str, usia: int, diagnosa: str) -> dict:
        """
        Insert Di Depan (Algoritma Jurnal):
        1. Alokasikan memori untuk node baru dan inisialisasi nilai data.
        2. Atur pointer 'prev' dari node baru ke NULL.
        3. Atur pointer 'next' dari node baru ke node yang sebelumnya
           merupakan 'head'.
        4. Jika head lama ada, perbarui pointer 'prev'-nya ke node baru.
        5. Ubah pointer 'head' untuk menunjuk ke node baru.
        6. Jika DLL sebelumnya kosong, tail juga menunjuk ke node baru.
        """
        # Validasi duplikat
        if self._id_exists(id_pasien):
            return {"success": False, "message": f"ID Pasien '{id_pasien}' sudah ada."}

        # Langkah 1: Alokasi node baru + inisialisasi data
        new_node = Node(id_pasien, nama, usia, diagnosa)

        # Langkah 2: prev node baru = NULL (karena akan jadi head)
        new_node.prev = None

        if self.head is None:
            # DLL kosong: head dan tail sama-sama menunjuk node baru
            new_node.next = None
            self.head = new_node
            self.tail = new_node
        else:
            # Langkah 3: next node baru menunjuk ke head lama
            new_node.next = self.head

            # Langkah 4: prev head lama menunjuk ke node baru
            self.head.prev = new_node

            # Langkah 5: head menunjuk ke node baru
            self.head = new_node

        return {"success": True, "message": f"Pasien '{nama}' berhasil ditambahkan di depan."}

    def insert_belakang(self, id_pasien: str, nama: str, usia: int, diagnosa: str) -> dict:
        """
        Insert Di Belakang (Algoritma Jurnal):
        1. Alokasikan memori untuk node baru dan inisialisasi data.
        2. Temukan node terakhir (tail).
        3. Ubah pointer 'next' dari node terakhir ke node baru.
        4. Atur pointer 'prev' dari node baru ke node terakhir.
        5. Atur pointer 'next' dari node baru ke NULL.
        6. Update tail ke node baru.
        """
        # Validasi duplikat
        if self._id_exists(id_pasien):
            return {"success": False, "message": f"ID Pasien '{id_pasien}' sudah ada."}

        # Langkah 1: Alokasi node baru + inisialisasi data
        new_node = Node(id_pasien, nama, usia, diagnosa)

        if self.head is None:
            # DLL kosong: head dan tail sama-sama menunjuk node baru
            new_node.prev = None
            new_node.next = None
            self.head = new_node
            self.tail = new_node
        else:
            # Langkah 2: Temukan node terakhir (tail sudah ditrack)
            last_node = self.tail
            
            # Membantu type checker memastikan last_node tidak None
            if last_node is not None:
                # Langkah 3: next node terakhir menunjuk ke node baru
                last_node.next = new_node
    
                # Langkah 4: prev node baru menunjuk ke node terakhir
                new_node.prev = last_node
    
                # Langkah 5: next node baru = NULL
                new_node.next = None
    
                # Langkah 6: Update tail
                self.tail = new_node
        return {"success": True, "message": f"Pasien '{nama}' berhasil ditambahkan di belakang."}

    def insert_tengah(self, id_pasien: str, nama: str, usia: int, diagnosa: str,
                      target_id: str) -> dict:
        """
        Insert Di Tengah — Setelah Node Target (Algoritma Jurnal):
        1. Temukan node target di mana penyisipan akan dilakukan.
        2. Alokasi node baru dan inisialisasi data.
        3. Ubah pointer 'next' dari node target ke node baru.
        4. Ubah pointer 'prev' dari node baru ke node target.
        5. Ubah pointer 'next' dari node baru ke node setelah target.
        6. Jika node setelah target ada, ubah pointer 'prev'-nya ke node baru.
        7. Jika target adalah tail, update tail ke node baru.
        """
        # Validasi DLL kosong
        if self.head is None:
            return {"success": False, "message": "Linked list kosong. Tidak bisa insert di tengah."}

        # Validasi duplikat
        if self._id_exists(id_pasien):
            return {"success": False, "message": f"ID Pasien '{id_pasien}' sudah ada."}

        # Langkah 1: Temukan node target
        target_node = self._find_node(target_id)
        if target_node is None:
            return {"success": False, "message": f"Node target dengan ID '{target_id}' tidak ditemukan."}

        # Langkah 2: Alokasi node baru + inisialisasi data
        new_node = Node(id_pasien, nama, usia, diagnosa)

        # Simpan referensi node setelah target
        node_after_target = target_node.next

        # Langkah 3: next target menunjuk ke node baru
        target_node.next = new_node

        # Langkah 4: prev node baru menunjuk ke target
        new_node.prev = target_node

        # Langkah 5: next node baru menunjuk ke node setelah target
        new_node.next = node_after_target

        # Langkah 6: Jika ada node setelah target, prev-nya menunjuk ke node baru
        if node_after_target is not None:
            node_after_target.prev = new_node
        else:
            # Langkah 7: Target adalah tail, update tail
            self.tail = new_node

        return {"success": True, "message": f"Pasien '{nama}' berhasil ditambahkan setelah ID '{target_id}'."}

    # =========================================================================
    # B. DELETION (Penghapusan)
    # =========================================================================

    def hapus_depan(self) -> dict:
        """
        Hapus Node Pertama (Head) — Algoritma Jurnal:
        1. Jika DLL kosong, tidak ada yang dihapus.
        2. Jika DLL hanya memiliki satu node, ubah 'head' dan 'tail' menjadi NULL.
        3. Jika lebih dari satu node:
           - Ubah pointer 'head' untuk menunjuk ke node berikutnya.
           - Atur prev dari head baru ke NULL.
        """
        if self.head is None:
            return {"success": False, "message": "Linked list kosong. Tidak ada data untuk dihapus."}

        deleted_name = self.head.nama

        if self.head == self.tail:
            # Langkah 2: Hanya satu node — head dan tail jadi NULL
            self.head = None
            self.tail = None
        else:
            # Langkah 3: Ubah head ke node berikutnya
            self.head = self.head.next
            self.head.prev = None

        return {"success": True, "message": f"Pasien '{deleted_name}' (node pertama) berhasil dihapus."}

    def hapus_belakang(self) -> dict:
        """
        Hapus Node Terakhir (Tail) — Algoritma Jurnal:
        1. Jika DLL kosong, tidak ada yang dihapus.
        2. Jika DLL hanya memiliki satu node, ubah 'head' dan 'tail' menjadi NULL.
        3. Jika lebih dari satu node:
           - Ubah pointer 'next' dari node sebelum tail ke NULL.
           - Ubah 'tail' untuk menunjuk ke node sebelum tail.
        """
        if self.tail is None:
            return {"success": False, "message": "Linked list kosong. Tidak ada data untuk dihapus."}

        deleted_name = self.tail.nama

        if self.head == self.tail:
            # Langkah 2: Hanya satu node — head dan tail jadi NULL
            self.head = None
            self.tail = None
        else:
            # Langkah 3: next dari node sebelum tail jadi NULL
            self.tail.prev.next = None
            # Tail menunjuk ke node sebelumnya
            self.tail = self.tail.prev

        return {"success": True, "message": f"Pasien '{deleted_name}' (node terakhir) berhasil dihapus."}

    def hapus_by_id(self, id_pasien: str) -> dict:
        """
        Hapus Node berdasarkan ID — Algoritma Jurnal (gabungan):
        1. Menemukan Node: Gunakan id_pasien sebagai kunci pencarian,
           lintasi DLL dari awal hingga ditemukan.
        2. Jika node adalah HEAD → hapus head.
        3. Jika node adalah TAIL → hapus tail.
        4. Jika node di tengah:
           - Ubah next dari node sebelum ke node setelah node yang dihapus.
           - Ubah prev dari node setelah ke node sebelum node yang dihapus.
        """
        if self.head is None:
            return {"success": False, "message": "Linked list kosong. Tidak ada data untuk dihapus."}

        # Langkah 1: Cari node target
        target = self._find_node(id_pasien)
        if target is None:
            return {"success": False, "message": f"Pasien dengan ID '{id_pasien}' tidak ditemukan."}

        deleted_name = target.nama

        # Langkah 2: Node adalah HEAD
        if target == self.head:
            return self.hapus_depan()

        # Langkah 3: Node adalah TAIL
        if target == self.tail:
            return self.hapus_belakang()

        # Langkah 4: Node di tengah
        target.prev.next = target.next   # next dari node sebelum → node setelah
        target.next.prev = target.prev   # prev dari node setelah → node sebelum

        return {"success": True, "message": f"Pasien '{deleted_name}' (ID: {id_pasien}) berhasil dihapus."}

    # =========================================================================
    # C. TRAVERSAL (Tampil Data & Navigasi)
    # =========================================================================

    def display_all(self) -> list:
        """
        Traversal dari depan ke belakang.
        Melintasi DLL dari head → tail, mengumpulkan data setiap node
        ke dalam list of dictionary.
        """
        result = []
        current = self.head
        while current is not None:
            result.append(current.to_dict())
            current = current.next
        return result

    def count(self) -> int:
        """Hitung jumlah total node dalam DLL."""
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
        """
        node = self._find_node(id_pasien)
        if node is not None:
            return node.to_dict()
        return None



# =============================================================================
# GLOBAL STATE
# =============================================================================
# Instance DLL disimpan dalam variabel global agar state tersimpan in-memory
# selama server Flask berjalan.
dll = DoubleLinkedList()

# Current pointer untuk navigasi 2 arah (Prev/Next)
current_pointer = None


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
# ENTRYPOINT
# =============================================================================
if __name__ == "__main__":
    app.run(debug=True, port=5000)
