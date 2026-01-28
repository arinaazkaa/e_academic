from django import forms
from django.core.exceptions import ValidationError 
from .models import Materi, Prestasi, Karya

# Setting Batas Ukuran File
MAX_IMAGE_SIZE = 2 * 1024 * 1024  # 2MB untuk Foto
MAX_DOC_SIZE = 5 * 1024 * 1024    # 5MB untuk Dokumen

# --- 1. FORM INPUT MATERI ---
class MateriForm(forms.ModelForm):
    class Meta:
        model = Materi
        fields = [
            'prodi', 'semester', 'mata_kuliah', 'dosen',
            'judul', 'link_google_drive', 'file_materi', 'cover'
        ]
        
        widgets = {
            'prodi': forms.Select(attrs={'class': 'form-select'}),
            'semester': forms.Select(attrs={'class': 'form-select'}),
            'mata_kuliah': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: Rangkaian Listrik'}),
            'dosen': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Dosen Pengampu'}),
            'judul': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Judul Materi / Bab'}),
            'link_google_drive': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://drive.google.com/...'}),
            'file_materi': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'cover': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    # Validasi File Materi (PDF/DOC)
    def clean_file_materi(self):
        file = self.cleaned_data.get('file_materi')
        if file:
            if file.size > MAX_DOC_SIZE:
                raise ValidationError("Ukuran file terlalu besar! Maksimal 5MB.")
        return file

# --- 2. FORM INPUT PRESTASI ---
class PrestasiForm(forms.ModelForm):
    class Meta:
        model = Prestasi
        fields = [
            'nama_mahasiswa', 'nim', 'prodi', 'no_hp',
            'nama_lomba', 'penyelenggara', 'url_penyelenggara',
            'jenis_lomba', 'tingkat', 'kategori',
            'juara', 'tempat_tanggal', 'no_sk',
            'foto_diri', 'link_sertifikat', 'is_public'
        ]
        
        widgets = {
            'nama_mahasiswa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Lengkap'}),
            'nim': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'NIM Mahasiswa'}),
            'prodi': forms.Select(attrs={'class': 'form-select'}),
            'no_hp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '08xxxxxxxxxx'}),
            'nama_lomba': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Kompetisi'}),
            'penyelenggara': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pihak Penyelenggara'}),
            'url_penyelenggara': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Link Info Lomba'}),
            'jenis_lomba': forms.Select(attrs={'class': 'form-select'}),
            'tingkat': forms.Select(attrs={'class': 'form-select'}),
            'kategori': forms.Select(attrs={'class': 'form-select'}),
            'juara': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: Juara 1'}),
            'tempat_tanggal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Semarang, 12 Agustus 2025'}),
            'no_sk': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'No. Surat Tugas'}),
            'foto_diri': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'link_sertifikat': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Link GDrive Sertifikat'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    # Validasi Foto Prestasi
    def clean_foto_diri(self):
        foto = self.cleaned_data.get('foto_diri')
        if foto:
            if foto.size > MAX_IMAGE_SIZE:
                raise ValidationError("Ukuran foto terlalu besar! Maksimal 2MB.")
        return foto


# --- 3. FORM INPUT KARYA ---
class KaryaForm(forms.ModelForm):
    class Meta:
        model = Karya
        fields = ['judul_karya', 'pembuat', 'prodi', 'deskripsi', 'gambar_cover', 'link_video']
        
        widgets = {
            'judul_karya': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Alat / Judul Karya'}),
            'pembuat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Pembuat / Tim'}),
            'prodi': forms.Select(attrs={'class': 'form-select'}),
            'deskripsi': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Jelaskan cara kerja alat...'}),
            'gambar_cover': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'link_video': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Link YouTube / Google Drive Video'}),
        }

    # Validasi Foto Cover Karya
    def clean_gambar_cover(self):
        gambar = self.cleaned_data.get('gambar_cover')
        if gambar:
            if gambar.size > MAX_IMAGE_SIZE:
                raise ValidationError("Ukuran gambar terlalu besar! Maksimal 2MB.")
        return gambar