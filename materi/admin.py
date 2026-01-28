from django.contrib import admin
from django.utils.html import format_html
from .models import Materi, Prestasi, Karya, InfoLomba, AgendaKalender, FileKalender

# --- 1. CONFIG ADMIN UNTUK MATERI ---
class MateriAdmin(admin.ModelAdmin):
    list_display = ('judul', 'mata_kuliah', 'prodi', 'semester', 'nama_pengupload', 'status_label', 'tanggal_upload')
    list_filter = ('status', 'prodi', 'semester', 'tanggal_upload')
    search_fields = ('judul', 'mata_kuliah', 'nama_pengupload')
    readonly_fields = ('tanggal_upload',)
    date_hierarchy = 'tanggal_upload'
    list_per_page = 20

    # Mengelompokkan form agar rapi
    fieldsets = (
        ('Info Akademik', {
            'fields': ('prodi', 'semester', 'mata_kuliah', 'dosen')
        }),
        ('Detail Materi', {
            'fields': ('judul', 'file_materi', 'link_google_drive', 'cover')
        }),
        ('Status & User', {
            'fields': ('nama_pengupload', 'status', 'tanggal_upload')
        }),
    )

    # Mewarnai status agar mudah dilihat
    def status_label(self, obj):
        if obj.status == 'approved':
            color = 'green'
        elif obj.status == 'rejected':
            color = 'red'
        else:
            color = 'orange'
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, obj.get_status_display())
    status_label.short_description = 'Status'

    actions = ['setujui_data', 'tolak_data']

    @admin.action(description='✅ Setujui Data Terpilih')
    def setujui_data(self, request, queryset):
        queryset.update(status='approved')

    @admin.action(description='❌ Tolak Data Terpilih')
    def tolak_data(self, request, queryset):
        queryset.update(status='rejected')


# --- 2. CONFIG ADMIN UNTUK PRESTASI ---
class PrestasiAdmin(admin.ModelAdmin):
    list_display = ('preview_foto', 'nama_mahasiswa', 'nama_lomba', 'juara', 'prodi', 'status_label')
    list_filter = ('status', 'prodi', 'tingkat', 'created_at')
    search_fields = ('nama_mahasiswa', 'nama_lomba', 'penyelenggara')
    readonly_fields = ('created_at',)
    list_display_links = ('nama_mahasiswa',)

    fieldsets = (
        ('Identitas Mahasiswa', {
            'fields': ('nama_mahasiswa', 'nim', 'prodi', 'no_hp')
        }),
        ('Detail Lomba', {
            'fields': ('nama_lomba', 'penyelenggara', 'tempat_tanggal', 'tingkat', 'kategori', 'juara')
        }),
        ('Bukti Dukung', {
            'fields': ('no_sk', 'link_sertifikat', 'foto_diri', 'is_public')
        }),
        ('Validasi', {
            'fields': ('status', 'created_at')
        }),
    )

    def preview_foto(self, obj):
        if obj.foto_diri:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 5px;" />', obj.foto_diri.url)
        return "-"
    preview_foto.short_description = "Foto"

    def status_label(self, obj):
        if obj.status == 'approved':
            return format_html('<span style="color: green;">✔ Approved</span>')
        elif obj.status == 'rejected':
            return format_html('<span style="color: red;">✖ Rejected</span>')
        return format_html('<span style="color: orange;">⏳ Pending</span>')
    status_label.short_description = 'Status'

    actions = ['setujui_data', 'tolak_data']

    @admin.action(description='✅ Setujui Prestasi')
    def setujui_data(self, request, queryset):
        queryset.update(status='approved')

    @admin.action(description='❌ Tolak Prestasi')
    def tolak_data(self, request, queryset):
        queryset.update(status='rejected')


# --- 3. CONFIG ADMIN UNTUK KARYA ---
class KaryaAdmin(admin.ModelAdmin):
    list_display = ('preview_cover', 'judul_karya', 'pembuat', 'prodi', 'status_label')
    list_filter = ('status', 'prodi', 'created_at')
    search_fields = ('judul_karya', 'pembuat')
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Info Karya', {
            'fields': ('judul_karya', 'deskripsi', 'pembuat', 'prodi')
        }),
        ('Media & File', {
            'fields': ('gambar_cover', 'link_video')
        }),
        ('Validasi', {
            'fields': ('status', 'created_at')
        }),
    )

    def preview_cover(self, obj):
        if obj.gambar_cover:
            return format_html('<img src="{}" style="width: 60px; height: 40px; object-fit: cover; border-radius: 4px;" />', obj.gambar_cover.url)
        return "-"
    preview_cover.short_description = "Cover"

    def status_label(self, obj):
        color = 'green' if obj.status == 'approved' else 'red' if obj.status == 'rejected' else 'orange'
        return format_html('<b style="color: {};">{}</b>', color, obj.get_status_display())
    status_label.short_description = 'Status'

    actions = ['setujui_data', 'tolak_data']

    @admin.action(description='✅ Setujui Karya')
    def setujui_data(self, request, queryset):
        queryset.update(status='approved')

    @admin.action(description='❌ Tolak Karya')
    def tolak_data(self, request, queryset):
        queryset.update(status='rejected')


# --- 4. CONFIG ADMIN UNTUK INFO LOMBA ---
class InfoLombaAdmin(admin.ModelAdmin):
    list_display = ('judul', 'penyelenggara', 'kategori', 'tanggal_deadline', 'status_aktif')
    list_filter = ('kategori', 'tanggal_deadline')
    search_fields = ('judul', 'penyelenggara')
    date_hierarchy = 'tanggal_deadline'

    fieldsets = (
        ('Info Utama', {
            'fields': ('judul', 'penyelenggara', 'kategori', 'poster')
        }),
        ('Jadwal', {
            'fields': ('tanggal_pelaksanaan', 'tanggal_deadline')
        }),
        ('Detail & Link', {
            'fields': ('deskripsi_lengkap', 'link_pendaftaran', 'url_penyelenggara')
        }),
    )
    
    def status_aktif(self, obj):
        return obj.is_active
    status_aktif.boolean = True
    status_aktif.short_description = "Buka?"


# --- 5. CONFIG ADMIN UNTUK KALENDER ---
class AgendaAdmin(admin.ModelAdmin):
    list_display = ('kegiatan', 'tanggal_mulai', 'tanggal_selesai', 'color_preview')
    ordering = ['tanggal_mulai']
    search_fields = ('kegiatan',)

    def color_preview(self, obj):
        # Menampilkan kotak warna sesuai pilihan user
        color_map = {
            'primary': '#0d6efd', # Biru
            'danger': '#dc3545',  # Merah
            'warning': '#ffc107', # Kuning
            'success': '#198754', # Hijau
            'info': '#0dcaf0'     # Cyan
        }
        hex_color = color_map.get(obj.warna, '#6c757d')
        return format_html('<div style="width: 20px; height: 20px; background-color: {}; border-radius: 50%;"></div>', hex_color)
    color_preview.short_description = "Warna"

class FileKalenderAdmin(admin.ModelAdmin):
    list_display = ('nama_file', 'updated_at')
    readonly_fields = ('updated_at',)


# --- REGISTER ---
admin.site.register(Materi, MateriAdmin)
admin.site.register(Prestasi, PrestasiAdmin)
admin.site.register(Karya, KaryaAdmin)
admin.site.register(InfoLomba, InfoLombaAdmin)
admin.site.register(AgendaKalender, AgendaAdmin)
admin.site.register(FileKalender, FileKalenderAdmin)