from django.contrib import admin
from .models import Materi, Prestasi, Karya, InfoLomba

# --- 1. CONFIG ADMIN UNTUK MATERI ---
class MateriAdmin(admin.ModelAdmin):
    # Kolom apa saja yang muncul di tabel list admin
    list_display = ('judul', 'nama_pengupload', 'prodi', 'semester', 'mata_kuliah', 'status', 'tanggal_upload')
    
    # Menu Filter di sebelah kanan (Penting buat sortir Prodi/Status)
    list_filter = ('status', 'prodi', 'semester', 'tanggal_upload')
    
    # Kolom pencarian
    search_fields = ('judul', 'mata_kuliah', 'nama_pengupload')
    
    # Agar tanggal upload tidak bisa diedit manual (otomatis dari sistem)
    readonly_fields = ('tanggal_upload',)
    
    # Menambahkan tombol aksi massal (Bulk Actions)
    actions = ['setujui_data', 'tolak_data']

    # --- FUNGSI TOMBOL AKSI ---
    @admin.action(description='Setujui Data Terpilih (Approve)')
    def setujui_data(self, request, queryset):
        # Mengubah status data yang dicentang menjadi 'approved'
        queryset.update(status='approved')

    @admin.action(description='Tolak Data Terpilih (Reject)')
    def tolak_data(self, request, queryset):
        # Mengubah status data yang dicentang menjadi 'rejected'
        queryset.update(status='rejected')


# --- 2. CONFIG ADMIN UNTUK PRESTASI ---
class PrestasiAdmin(admin.ModelAdmin):
    list_display = ('nama_mahasiswa', 'nama_lomba', 'juara', 'prodi', 'status')
    list_filter = ('status', 'prodi', 'tingkat')
    search_fields = ('nama_mahasiswa', 'nama_lomba')
    actions = ['setujui_data', 'tolak_data']

    # Kita reuse fungsi yang sama biar ga ngetik ulang logic-nya
    @admin.action(description='Setujui Prestasi')
    def setujui_data(self, request, queryset):
        queryset.update(status='approved')

    @admin.action(description='Tolak Prestasi')
    def tolak_data(self, request, queryset):
        queryset.update(status='rejected')


# --- 3. CONFIG ADMIN UNTUK KARYA ---
class KaryaAdmin(admin.ModelAdmin):
    list_display = ('judul_karya', 'pembuat', 'prodi', 'status')
    list_filter = ('status', 'prodi')
    search_fields = ('judul_karya', 'pembuat')
    actions = ['setujui_data', 'tolak_data']

    @admin.action(description='Setujui Karya')
    def setujui_data(self, request, queryset):
        queryset.update(status='approved')

    @admin.action(description='Tolak Karya')
    def tolak_data(self, request, queryset):
        queryset.update(status='rejected')


# --- AKHIRNYA: DAFTARKAN SEMUA KE PANEL ADMIN ---
admin.site.register(Materi, MateriAdmin)
admin.site.register(Prestasi, PrestasiAdmin)
admin.site.register(Karya, KaryaAdmin)
admin.site.register(InfoLomba)