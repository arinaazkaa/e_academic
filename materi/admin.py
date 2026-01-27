from django.contrib import admin
from .models import Materi, Prestasi, Karya, InfoLomba, AgendaKalender, FileKalender

# --- 1. CONFIG ADMIN UNTUK MATERI ---
class MateriAdmin(admin.ModelAdmin):
    list_display = ('judul', 'nama_pengupload', 'prodi', 'semester', 'mata_kuliah', 'status', 'tanggal_upload')
    list_filter = ('status', 'prodi', 'semester', 'tanggal_upload')
    search_fields = ('judul', 'mata_kuliah', 'nama_pengupload')
    readonly_fields = ('tanggal_upload',)
    actions = ['setujui_data', 'tolak_data']

    @admin.action(description='Setujui Data Terpilih (Approve)')
    def setujui_data(self, request, queryset):
        queryset.update(status='approved')

    @admin.action(description='Tolak Data Terpilih (Reject)')
    def tolak_data(self, request, queryset):
        queryset.update(status='rejected')


# --- 2. CONFIG ADMIN UNTUK PRESTASI ---
class PrestasiAdmin(admin.ModelAdmin):
    list_display = ('nama_mahasiswa', 'nama_lomba', 'juara', 'prodi', 'status', 'created_at')
    list_filter = ('status', 'prodi', 'tingkat')
    search_fields = ('nama_mahasiswa', 'nama_lomba', 'penyelenggara')
    actions = ['setujui_data', 'tolak_data']

    @admin.action(description='Setujui Prestasi')
    def setujui_data(self, request, queryset):
        queryset.update(status='approved')

    @admin.action(description='Tolak Prestasi')
    def tolak_data(self, request, queryset):
        queryset.update(status='rejected')


# --- 3. CONFIG ADMIN UNTUK KARYA ---
class KaryaAdmin(admin.ModelAdmin):
    list_display = ('judul_karya', 'pembuat', 'prodi', 'status', 'created_at')
    list_filter = ('status', 'prodi')
    search_fields = ('judul_karya', 'pembuat')
    actions = ['setujui_data', 'tolak_data']

    @admin.action(description='Setujui Karya')
    def setujui_data(self, request, queryset):
        queryset.update(status='approved')

    @admin.action(description='Tolak Karya')
    def tolak_data(self, request, queryset):
        queryset.update(status='rejected')


# --- 4. CONFIG ADMIN UNTUK INFO LOMBA (UPDATE) ---
class InfoLombaAdmin(admin.ModelAdmin):
    list_display = ('judul', 'penyelenggara', 'kategori', 'tanggal_deadline', 'status_aktif')
    list_filter = ('kategori', 'tanggal_deadline')
    search_fields = ('judul', 'penyelenggara')
    
    # Menampilkan status apakah lomba masih buka atau sudah tutup di tabel admin
    def status_aktif(self, obj):
        return obj.is_active
    status_aktif.boolean = True # Agar muncul ikon centang/silang
    status_aktif.short_description = "Masih Buka?"


# --- 5. CONFIG ADMIN UNTUK KALENDER (BARU) ---
class AgendaAdmin(admin.ModelAdmin):
    list_display = ('kegiatan', 'tanggal_mulai', 'tanggal_selesai', 'warna')
    ordering = ['tanggal_mulai'] # Urutkan dari tanggal terdekat
    search_fields = ('kegiatan',)

class FileKalenderAdmin(admin.ModelAdmin):
    list_display = ('nama_file', 'updated_at')


# --- AKHIRNYA: DAFTARKAN SEMUA KE PANEL ADMIN ---
admin.site.register(Materi, MateriAdmin)
admin.site.register(Prestasi, PrestasiAdmin)
admin.site.register(Karya, KaryaAdmin)
admin.site.register(InfoLomba, InfoLombaAdmin)
admin.site.register(AgendaKalender, AgendaAdmin)
admin.site.register(FileKalender, FileKalenderAdmin)