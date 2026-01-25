from django import forms
# Kita import semua Model
from .models import Materi, Prestasi, Karya

# --- 1. FORM INPUT MATERI ---
class MateriForm(forms.ModelForm):
    class Meta:
        model = Materi
        # PENTING: Urutan fields menentukan urutan tampilan di web
        fields = [
            'nama_pengupload', 
            'email', 
            'prodi', 
            'semester', 
            'mata_kuliah', 
            'judul', 
            'link_materi', 
            'deskripsi'
        ]
        
        # WIDGETS: Ini "Make-up" nya form biar rapi & ada petunjuk (placeholder)
        widgets = {
            'nama_pengupload': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Lengkap Kamu'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@mahasiswa.ac.id (Untuk notifikasi)'}),
            'prodi': forms.Select(attrs={'class': 'form-select'}),
            'semester': forms.Select(attrs={'class': 'form-select'}),
            'mata_kuliah': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: Rangkaian Listrik'}),
            'judul': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Judul Materi (Misal: PPT Pertemuan 1)'}),
            'link_materi': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Paste Link Google Drive di sini (Pastikan Public)'}),
            'deskripsi': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Keterangan tambahan (Opsional)...'}),
        }

# --- 2. FORM INPUT PRESTASI (Elektro Bangga) ---
class PrestasiForm(forms.ModelForm):
    class Meta:
        model = Prestasi
        fields = ['nama_mahasiswa', 'prodi', 'nama_lomba', 'juara', 'tingkat', 'link_sertifikat']
        
        widgets = {
            'nama_mahasiswa': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Tulis nama lengkap. Jika tim, pisahkan dengan koma.'}),
            'prodi': forms.Select(attrs={'class': 'form-select'}),
            'nama_lomba': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Kompetisi/Lomba'}),
            'juara': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: Juara 1, Gold Medal, Finalis'}),
            'tingkat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nasional / Internasional / Regional'}),
            'link_sertifikat': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Link GDrive Foto Penyerahan Hadiah / Sertifikat'}),
        }

# --- 3. FORM INPUT KARYA ---
class KaryaForm(forms.ModelForm):
    class Meta:
        model = Karya
        fields = ['judul_karya', 'pembuat', 'prodi', 'deskripsi', 'link_demo']
        
        widgets = {
            'judul_karya': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Alat / Judul Karya'}),
            'pembuat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Pembuat'}),
            'prodi': forms.Select(attrs={'class': 'form-select'}),
            'deskripsi': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Jelaskan cara kerja atau fungsi alat ini...'}),
            'link_demo': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Link Video Youtube / Demo'}),
        }