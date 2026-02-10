from django.db import models
import re # Menggunakan regex untuk ekstraksi ID file yang lebih akurat

# --- PILIHAN UMUM ---
PRODI_CHOICES = [
    ('PTIK', 'PTIK'),
    ('PTE', 'PTE'),
    ('TE', 'TE'),
    ('TEKKOM', 'TEKKOM'),
    ('MKU', 'MKU'),
]

STATUS_CHOICES = [
    ('pending', '⏳ Pending'),
    ('approved', '✅ Approved'),
    ('rejected', '❌ Rejected'),
]

# --- FUNGSI HELPER: CONVERTER GOOGLE DRIVE ---
def convert_to_direct_link(url):
    """Mengubah link pratinjau Drive menjadi link langsung (Direct Link)."""
    if url and "drive.google.com" in url:
        # Mencari ID file (biasanya 25+ karakter acak)
        match = re.search(r'[-\w]{25,}', url)
        if match:
            file_id = match.group()
            return f"https://drive.google.com/uc?export=view&id={file_id}"
    return url

# --- 1. MODEL MATERI ---
class Materi(models.Model):
    prodi = models.CharField(max_length=10, choices=PRODI_CHOICES)
    semester = models.IntegerField(null=True, blank=True)
    mata_kuliah = models.CharField(max_length=200)
    judul = models.CharField(max_length=255)
    link_google_drive = models.URLField(max_length=500, null=True, blank=True)
    tanggal_upload = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Materi"

    def save(self, *args, **kwargs):
        self.link_google_drive = convert_to_direct_link(self.link_google_drive)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.mata_kuliah} - {self.judul}"

# --- 2. MODEL PRESTASI ---
class Prestasi(models.Model):
    nama_mahasiswa = models.CharField(max_length=200)
    prodi = models.CharField(max_length=10, choices=PRODI_CHOICES)
    nama_lomba = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    link_foto = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Prestasi"

    def save(self, *args, **kwargs):
        self.link_foto = convert_to_direct_link(self.link_foto)
        super().save(*args, **kwargs)

# --- 3. MODEL KARYA INOVASI ---
class Karya(models.Model):
    judul_karya = models.CharField(max_length=255)
    pembuat = models.CharField(max_length=255)
    prodi = models.CharField(max_length=10, choices=PRODI_CHOICES, default='PTIK') 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Karya"

# --- 4. MODEL INFO LOMBA ---
class InfoLomba(models.Model):
    judul = models.CharField(max_length=255)
    penyelenggara = models.CharField(max_length=200)
    kategori = models.CharField(max_length=100, default="UMUM")
    
    link_poster = models.URLField(max_length=500, blank=True, null=True, help_text="Link poster dari Google Drive/Imgur")
    link_pendaftaran = models.URLField(max_length=500, blank=True, null=True)
    link_sosmed = models.URLField(max_length=500, blank=True, null=True)
    link_booklet = models.URLField(max_length=500, blank=True, null=True)
    
    deskripsi = models.TextField(blank=True, null=True)
    tanggal_deadline = models.DateField(null=True, blank=True)
    tanggal_pelaksanaan = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Info Lomba"

    def save(self, *args, **kwargs):
        self.link_poster = convert_to_direct_link(self.link_poster)
        self.link_booklet = convert_to_direct_link(self.link_booklet)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.judul

# --- 5. MODEL AGENDA AKADEMIK (UPDATED: DATE RANGE) ---
class AgendaAkademik(models.Model):
    WARNA_CHOICES = [
        ('primary', 'Biru (Umum)'), 
        ('danger', 'Merah (Penting)'), 
        ('warning', 'Kuning (Pengingat)'), 
        ('success', 'Hijau (Opsional)')
    ]
    kegiatan = models.CharField(max_length=255)
    tanggal_mulai = models.DateField()
    # Field baru untuk menampung batas akhir agenda
    tanggal_selesai = models.DateField(null=True, blank=True, help_text="Kosongkan jika hanya satu hari")
    warna = models.CharField(max_length=10, choices=WARNA_CHOICES, default='primary')

    class Meta:
        verbose_name_plural = "Agenda Akademik"
        ordering = ['tanggal_mulai'] # Agar otomatis urut berdasarkan waktu terdekat di Admin

    def __str__(self):
        return self.kegiatan

# --- 6. MODEL FILE KALENDER ---
class KalenderPDF(models.Model):
    nama_file = models.CharField(max_length=255, default="Kalender Akademik")
    link_google_drive = models.URLField(max_length=500)
    tanggal_update = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.link_google_drive = convert_to_direct_link(self.link_google_drive)
        super().save(*args, **kwargs)