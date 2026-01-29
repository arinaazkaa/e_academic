from django.db import models
from datetime import date 

# --- PILIHAN UMUM ---
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

SEMESTER_CHOICES = [(i, f'Semester {i}') for i in range(1, 9)]

# --- MODEL 1: MATERI PERKULIAHAN ---
class Materi(models.Model):
    nama_pengupload = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    
    prodi = models.CharField(max_length=50, choices=PRODI_CHOICES)
    semester = models.IntegerField(choices=SEMESTER_CHOICES)
    mata_kuliah = models.CharField(max_length=100)
    dosen = models.CharField(max_length=100, blank=True, null=True, verbose_name="Dosen Pengampu")

    judul = models.CharField(max_length=200)
    deskripsi = models.TextField(blank=True, null=True)
    cover = models.ImageField(upload_to='cover_materi/', blank=True, null=True, verbose_name="Cover Materi")

    link_google_drive = models.URLField(blank=True, null=True)
    file_materi = models.FileField(upload_to='dokumen_materi/', blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    tanggal_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.judul} - {self.mata_kuliah}"


# --- MODEL 2: PRESTASI ---
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

    nama_mahasiswa = models.CharField("Nama Lengkap", max_length=200)
    nim = models.CharField("NIM", max_length=20, blank=True, null=True) 
    prodi = models.CharField(max_length=50, choices=PRODI_CHOICES)
    no_hp = models.CharField("No HP / WA", max_length=20, blank=True, null=True)

    nama_lomba = models.CharField(max_length=200)
    penyelenggara = models.CharField(max_length=200)
    url_penyelenggara = models.URLField("Website/Sosmed Penyelenggara", blank=True, null=True)
    
    jenis_lomba = models.CharField(max_length=20, choices=JENIS_CHOICES, default='Sains')
    tingkat = models.CharField(max_length=20, choices=TINGKAT_CHOICES, default='Nasional')
    kategori = models.CharField(max_length=20, choices=KATEGORI_CHOICES, default='Individu')
    
    juara = models.CharField(max_length=100)
    tempat_tanggal = models.CharField("Tempat & Tanggal", max_length=200)
    no_sk = models.CharField("No. SK / Surat Tugas", max_length=100, blank=True, null=True)

    foto_diri = models.ImageField(upload_to='foto_prestasi/', blank=True, null=True)
    link_sertifikat = models.URLField("Link Drive Sertifikat")
    is_public = models.BooleanField("Bersedia Diposting?", default=True)

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
    
    gambar_cover = models.ImageField(upload_to='cover_karya/', blank=True, null=True)
    link_video = models.URLField("Link Video", blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.judul_karya


# --- MODEL 4: INFO LOMBA ---
class InfoLomba(models.Model):
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
    kategori = models.CharField(max_length=50, choices=TINGKAT_LOMBA_CHOICES, default='Nasional')

    tanggal_buka_pendaftaran = models.DateField(null=True, blank=True)
    tanggal_deadline = models.DateField(null=True, blank=True) 
    tanggal_pelaksanaan = models.DateField(null=True, blank=True)
    
    poster = models.ImageField(upload_to='poster_lomba/', blank=True, null=True) 
    deskripsi_lengkap = models.TextField(blank=True, null=True)
    link_pendaftaran = models.URLField(blank=True, null=True)
    url_penyelenggara = models.URLField("Link Info/Sosmed", blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.judul

    @property
    def is_active(self):
        if self.tanggal_deadline:
            return date.today() <= self.tanggal_deadline
        return True


# --- MODEL 5: KALENDER AKADEMIK ---
class AgendaKalender(models.Model):
    kegiatan = models.CharField(max_length=200)
    tanggal_mulai = models.DateField()
    tanggal_selesai = models.DateField(blank=True, null=True)
    
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
    file_pdf = models.FileField(upload_to='dokumen_kalender/')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama_file