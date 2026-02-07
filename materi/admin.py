from django.contrib import admin
from django.utils.html import format_html
from .models import Materi, Prestasi, Karya, InfoLomba, AgendaAkademik, KalenderPDF

# --- 1. CONFIG ADMIN UNTUK MATERI (E-LIBRARY) ---
@admin.register(Materi)
class MateriAdmin(admin.ModelAdmin):
    list_display = ('mata_kuliah', 'prodi', 'semester_display', 'tanggal_upload', 'view_drive_link')
    list_filter = ('prodi', 'semester', 'tanggal_upload')
    search_fields = ('mata_kuliah', 'judul')
    ordering = ('-tanggal_upload',)
    list_per_page = 20

    fieldsets = (
        ('Info Akademik', {
            'fields': ('prodi', 'semester', 'mata_kuliah')
        }),
        ('Konten Materi (Google Drive)', {
            'fields': ('judul', 'link_google_drive'),
            'description': 'Pastikan link Google Drive sudah diatur ke "Public" agar mahasiswa dapat mengaksesnya.'
        }),
    )

    def semester_display(self, obj):
        return f"Semester {obj.semester}" if obj.semester else "MKU (Tanpa Semester)"
    semester_display.short_description = 'Semester'

    def view_drive_link(self, obj):
        if obj.link_google_drive:
            return format_html('<a href="{}" target="_blank" style="font-weight:bold; color:#0d6efd;">Buka Drive</a>', obj.link_google_drive)
        return "-"
    view_drive_link.short_description = 'Cek Materi'


# --- 2. CONFIG ADMIN UNTUK PRESTASI (HEMAT STORAGE) ---
@admin.register(Prestasi)
class PrestasiAdmin(admin.ModelAdmin):
    list_display = ('preview_foto', 'nama_mahasiswa', 'nama_lomba', 'prodi', 'status_label')
    list_filter = ('status', 'prodi', 'created_at')
    search_fields = ('nama_mahasiswa', 'nama_lomba')
    actions = ['setujui_data', 'tolak_data']

    def preview_foto(self, obj):
        if obj.link_foto:
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 8px; object-fit:cover; border: 1px solid #ddd;" />', obj.link_foto)
        return format_html('<span style="color: #999; font-size: 0.8rem;">No Photo</span>')
    preview_foto.short_description = "Foto"

    def status_label(self, obj):
        color = '#10b981' if obj.status == 'approved' else '#ef4444' if obj.status == 'rejected' else '#f59e0b'
        return format_html('<b style="color: {};">{}</b>', color, obj.get_status_display())
    status_label.short_description = 'Status'

    @admin.action(description='✅ Setujui Data Terpilih')
    def setujui_data(self, request, queryset):
        queryset.update(status='approved')

    @admin.action(description='❌ Tolak Data Terpilih')
    def tolak_data(self, request, queryset):
        queryset.update(status='rejected')


# --- 3. CONFIG ADMIN UNTUK KARYA INOVASI ---
@admin.register(Karya)
class KaryaAdmin(admin.ModelAdmin):
    list_display = ('judul_karya', 'pembuat', 'prodi', 'status_label')
    list_filter = ('status', 'prodi', 'created_at')
    search_fields = ('judul_karya', 'pembuat')
    actions = ['setujui_data', 'tolak_data']

    def status_label(self, obj):
        color = '#10b981' if obj.status == 'approved' else '#ef4444' if obj.status == 'rejected' else '#f59e0b'
        return format_html('<b style="color: {};">{}</b>', color, obj.get_status_display())
    status_label.short_description = 'Status'

    @admin.action(description='✅ Setujui Karya Terpilih')
    def setujui_data(self, request, queryset):
        queryset.update(status='approved')

    @admin.action(description='❌ Tolak Karya Terpilih')
    def tolak_data(self, request, queryset):
        queryset.update(status='rejected')


# --- 4. CONFIG ADMIN UNTUK INFO LOMBA (UPDATE: LINK POSTER KEMBALI) ---
@admin.register(InfoLomba)
class InfoLombaAdmin(admin.ModelAdmin):
    list_display = ('judul', 'penyelenggara', 'kategori', 'tanggal_deadline', 'is_active', 'view_poster_link')
    list_filter = ('is_active', 'kategori', 'tanggal_deadline')
    search_fields = ('judul', 'penyelenggara')
    date_hierarchy = 'tanggal_deadline'
    
    fieldsets = (
        ('Informasi Dasar', {
            'fields': ('judul', 'penyelenggara', 'kategori', 'deskripsi')
        }),
        ('Link Eksternal (Hemat Storage)', {
            'fields': ('link_poster', 'link_pendaftaran', 'link_sosmed', 'link_booklet'),
            'description': 'Simpan gambar di Google Drive/Imgur dan tempel linknya di sini untuk menghemat ruang server.'
        }),
        ('Waktu & Status', {
            'fields': ('tanggal_deadline', 'tanggal_pelaksanaan', 'is_active')
        }),
    )

    def view_poster_link(self, obj):
        if obj.link_poster:
            return format_html('<a href="{}" target="_blank" style="font-weight:bold; color:#0d6efd;">Lihat Poster</a>', obj.link_poster)
        return "-"
    view_poster_link.short_description = 'Cek Poster'


# --- 5. CONFIG ADMIN UNTUK AGENDA AKADEMIK (UPDATED: RANGE TANGGAL) ---
@admin.register(AgendaAkademik)
class AgendaAdmin(admin.ModelAdmin):
    # Menampilkan tanggal mulai dan selesai di daftar tabel
    list_display = ('kegiatan', 'tanggal_mulai', 'tanggal_selesai', 'color_preview')
    ordering = ['tanggal_mulai']
    search_fields = ('kegiatan',)

    fieldsets = (
        (None, {
            'fields': ('kegiatan', 'warna')
        }),
        ('Rentang Waktu Kegiatan', {
            # Mengelompokkan tanggal mulai dan selesai dalam satu baris agar rapi
            'fields': (('tanggal_mulai', 'tanggal_selesai'),),
            'description': 'Jika kegiatan hanya berlangsung satu hari, biarkan Tanggal Selesai kosong.'
        }),
    )

    def color_preview(self, obj):
        color_map = {
            'primary': '#3b82f6', 
            'warning': '#f59e0b', 
            'success': '#10b981', 
            'danger': '#ef4444',  
        }
        hex_color = color_map.get(obj.warna, '#6c757d')
        return format_html('<div style="width: 18px; height: 18px; background-color: {}; border-radius: 50%; box-shadow: 0 0 5px rgba(0,0,0,0.1);"></div>', hex_color)
    color_preview.short_description = "Warna"


# --- 6. CONFIG ADMIN UNTUK FILE KALENDER PDF ---
@admin.register(KalenderPDF)
class KalenderPDFAdmin(admin.ModelAdmin):
    list_display = ('nama_file', 'tanggal_update', 'view_pdf_link')
    
    def view_pdf_link(self, obj):
        return format_html('<a href="{}" target="_blank" style="font-weight:bold; color:#10b981;">Buka PDF</a>', obj.link_google_drive)
    view_pdf_link.short_description = 'Cek Dokumen'