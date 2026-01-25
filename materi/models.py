from django.db import models

# --- PILIHAN UMUM (Bisa dipakai di model mana saja) ---

# 1. Update Prodi sesuai request (4 Prodi + MKU)
PRODI_CHOICES = [
    ('PTIK', 'Pendidikan Teknik Informatika dan Komputer'),
    ('PTE', 'Pendidikan Teknik Elektro'),
    ('TE', 'Teknik Elektro'),
    ('TK', 'Teknik Komputer'),
    ('MKU', 'Mata Kuliah Umum'),
]

STATUS_CHOICES = [
    ('pending', 'Menunggu Review'),
    ('approved', 'Disetujui'),
    ('rejected', 'Ditolak'),
]

SEMESTER_CHOICES = [
    (1, 'Semester 1'),
    (2, 'Semester 2'),
    (3, 'Semester 3'),
    (4, 'Semester 4'),
    (5, 'Semester 5'),
    (6, 'Semester 6'),
    (7, 'Semester 7'),
    (8, 'Semester 8'),
]

# --- MODEL 1: MATERI PERKULIAHAN ---
class Materi(models.Model):
    # Data Pengupload
    nama_pengupload = models.CharField(max_length=100)
    email = models.EmailField(help_text="Email untuk notifikasi jika materi diterima/ditolak")
    
    # Data Akademik
    prodi = models.CharField(max_length=50, choices=PRODI_CHOICES)
    semester = models.IntegerField(choices=SEMESTER_CHOICES)
    mata_kuliah = models.CharField(max_length=100)

    # Data File
    judul = models.CharField(max_length=200)
    deskripsi = models.TextField(blank=True, null=True)
    link_materi = models.URLField(help_text="Masukkan Link Google Drive (Pastikan akses Public/Anyone with link)")
    
    # System
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    tanggal_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.judul} - {self.mata_kuliah}"


# --- MODEL 2: PRESTASI (ELEKTRO BANGGA) ---
# Diupdate Besar-besaran Sesuai Request
class Prestasi(models.Model):
    # Pilihan Dropdown Baru
    JENIS_CHOICES = [
        ('Sains', 'Sains & Teknologi'),
        ('Olahraga', 'Olahraga'),
        ('Seni', 'Seni & Budaya'),
        ('Lainnya', 'Lainnya'),
    ]
    
    TINGKAT_CHOICES = [
        ('Internasional', 'Internasional'),
        ('Nasional', 'Nasional'),
        ('Provinsi', 'Provinsi'),
        ('Kota', 'Kota/Kabupaten'),
        ('Kampus', 'Internal Kampus'),
    ]

    KATEGORI_CHOICES = [
        ('Individu', 'Individu'),
        ('Kelompok', 'Kelompok/Tim'),
    ]

    # --- A. DATA MAHASISWA ---
    nama_mahasiswa = models.CharField("Nama & NIM", max_length=200, help_text="Format: Nama Lengkap (NIM)")
    prodi = models.CharField(max_length=50, choices=PRODI_CHOICES)
    no_hp = models.CharField("No HP / WA", max_length=20, blank=True, null=True)

    # --- B. DATA PERLOMBAAN ---
    nama_lomba = models.CharField(max_length=200)
    penyelenggara = models.CharField(max_length=200)
    url_penyelenggara = models.URLField("Website/Sosmed Penyelenggara", blank=True, null=True)
    
    jenis_lomba = models.CharField(max_length=20, choices=JENIS_CHOICES, default='Sains')
    tingkat = models.CharField(max_length=20, choices=TINGKAT_CHOICES, default='Nasional')
    kategori = models.CharField(max_length=20, choices=KATEGORI_CHOICES, default='Individu')
    
    juara = models.CharField(max_length=100, help_text="Contoh: Juara 1, Medali Emas, Best Speaker")
    
    # Detail Pelaksanaan
    tempat_tanggal = models.CharField("Tempat & Tanggal", max_length=200, help_text="Contoh: Semarang, 1-4 September 2025")
    no_sk = models.CharField("No. SK / Surat Tugas", max_length=100, blank=True, null=True)

    # --- C. BUKTI DUKUNG ---
    # Foto Diri (ImageField) agar bisa tampil langsung di Beranda/Card
    foto_diri = models.ImageField(upload_to='foto_prestasi/', help_text="Upload foto terbaik (Formal/Bebas Sopan)", blank=True, null=True)
    
    # Link Drive untuk berkas berat (Sertifikat/Dokumentasi)
    link_sertifikat = models.URLField("Link Drive (Sertifikat & Foto Kegiatan)", help_text="Pastikan link Google Drive bersifat Public")
    
    # Persetujuan
    is_public = models.BooleanField("Bersedia Diposting?", default=True)

    # System
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.juara} - {self.nama_mahasiswa}"


# --- MODEL 3: KARYA MAHASISWA ---
class Karya(models.Model):
    judul_karya = models.CharField(max_length=200)
    pembuat = models.CharField("Nama Pembuat", max_length=200)
    prodi = models.CharField(max_length=50, choices=PRODI_CHOICES)
    deskripsi = models.TextField()
    
    link_demo = models.URLField("Link Video/Demo", blank=True, null=True)
    
    # System
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.judul_karya


# --- MODEL 4: INFO LOMBA ---
class InfoLomba(models.Model):
    judul = models.CharField(max_length=200)
    penyelenggara = models.CharField(max_length=100)
    tanggal_pelaksanaan = models.DateField()
    
    # Field upload gambar pamflet
    pamflet = models.ImageField(upload_to='pamflet_lomba/', blank=True, null=True)
    
    # Field deskripsi panjang
    deskripsi_lengkap = models.TextField(blank=True, null=True)
    
    link_pendaftaran = models.URLField(blank=True, null=True, help_text="Link Google Form / Website Lomba")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.judul