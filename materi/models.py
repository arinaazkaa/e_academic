from django.db import models
from datetime import date 

# --- PILIHAN UMUM (Bisa dipakai di model mana saja) ---

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
    
    # --- PEMISAHAN LINK & FILE ---
    link_google_drive = models.URLField(
        blank=True, null=True, 
        help_text="Isi jika materi ada di Google Drive (Pastikan akses Public)"
    )
    file_materi = models.FileField(
        upload_to='dokumen_materi/', 
        blank=True, null=True, 
        help_text="Upload file PDF/PPT langsung ke server (Opsional)"
    )
    
    # System
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    tanggal_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.judul} - {self.mata_kuliah}"


# --- MODEL 2: PRESTASI (ELEKTRO BANGGA) ---
class Prestasi(models.Model):
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
    foto_diri = models.ImageField(
        upload_to='foto_prestasi/', 
        help_text="Upload foto terbaik (Formal/Bebas Sopan). Maksimal 2MB.", 
        blank=True, null=True
    )
    
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
    
    # --- FOTO COVER KARYA ---
    gambar_cover = models.ImageField(
        upload_to='cover_karya/', 
        blank=True, null=True, 
        help_text="Upload Foto Alat/Karya (Maksimal 2MB)"
    )
    
    link_video = models.URLField(
        "Link Google Drive Video", 
        blank=True, null=True,
        help_text="Paste link Google Drive Video Demo di sini (Pastikan akses 'Public')"
    )
    
    # System
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.judul_karya


# --- MODEL 4: INFO LOMBA ---
class InfoLomba(models.Model):
    # Pilihan untuk Kategori/Tingkatan Lomba
    TINGKAT_LOMBA_CHOICES = [
        ('Internasional', 'Internasional'),
        ('Nasional', 'Nasional'),
        ('Provinsi', 'Provinsi'),
        ('Kota', 'Kota/Kabupaten'),
        ('Kampus', 'Internal Kampus'),
        ('Umum', 'Umum'),
    ]

    judul = models.CharField(max_length=200)
    penyelenggara = models.CharField(max_length=100)
    
    # UPDATE 1: Kategori menggunakan Choices agar konsisten
    kategori = models.CharField(
        max_length=50, 
        choices=TINGKAT_LOMBA_CHOICES, 
        default='Nasional', 
        help_text="Pilih tingkatan lomba untuk label (Badge)"
    )

    # Waktu
    tanggal_buka_pendaftaran = models.DateField(null=True, blank=True)
    tanggal_deadline = models.DateField(null=True, blank=True, help_text="Batas akhir pendaftaran") 
    tanggal_pelaksanaan = models.DateField(help_text="Tanggal Lomba Dimulai")
    
    poster = models.ImageField(upload_to='poster_lomba/', blank=True, null=True) 
    
    # Deskripsi
    deskripsi_lengkap = models.TextField(blank=True, null=True)
    
    # Link Pendaftaran (Google Form, dll)
    link_pendaftaran = models.URLField(blank=True, null=True, help_text="Link untuk mendaftar (Tombol Daftar)")
    
    # UPDATE 2: Link Info Tambahan (Sosmed/Web Penyelenggara)
    url_penyelenggara = models.URLField(
        "Link Info/Sosmed", 
        blank=True, null=True, 
        help_text="Link Website, Instagram, atau Guidebook Lomba (Untuk tombol More Info)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.judul

    # --- LOGIKA OTOMATIS STATUS (BUKA/TUTUP) ---
    @property
    def is_active(self):
        if self.tanggal_deadline:
            return date.today() <= self.tanggal_deadline
        return True


# --- MODEL 5: KALENDER AKADEMIK (BARU) ---
class AgendaKalender(models.Model):
    kegiatan = models.CharField(max_length=200)
    tanggal_mulai = models.DateField()
    tanggal_selesai = models.DateField(blank=True, null=True)
    
    # Warna label agar cantik di tampilan (Hijau, Biru, Kuning, Merah)
    WARNA_CHOICES = [
        ('primary', 'Biru (Normal)'),
        ('success', 'Hijau (Penting)'),
        ('warning', 'Kuning (Warning)'),
        ('danger', 'Merah (Libur/Deadline)'),
    ]
    warna = models.CharField(max_length=20, choices=WARNA_CHOICES, default='primary')
    
    def __str__(self):
        return self.kegiatan

class FileKalender(models.Model):
    nama_file = models.CharField(max_length=100, default="Kalender Akademik PDF")
    file_pdf = models.FileField(upload_to='dokumen_kalender/', help_text="Upload PDF Kalender Akademik Resmi di sini")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama_file