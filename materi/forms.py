from django import forms
from .models import Materi, Prestasi, Karya

# --- 1. FORM INPUT MATERI (E-LIBRARY) ---
class MateriForm(forms.ModelForm):
    class Meta:
        model = Materi
        # Field disesuaikan dengan model terbaru (Tanpa file/cover)
        fields = [
            'prodi', 'semester', 'mata_kuliah', 'judul', 'link_google_drive'
        ]
        
        # Widgets minimalis menggunakan Bootstrap
        widgets = {
            'prodi': forms.Select(attrs={'class': 'form-select'}),
            'semester': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: 1', 'min': 1, 'max': 8}),
            'mata_kuliah': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: Dasar Teknik Elektro'}),
            'judul': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: Modul Pertemuan 1'}),
            'link_google_drive': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Tempel link Google Drive di sini...'}),
        }

    # Validasi opsional untuk memastikan link adalah Google Drive
    def clean_link_google_drive(self):
        link = self.cleaned_data.get('link_google_drive')
        if link and "drive.google.com" not in link:
            # Tetap diperbolehkan, tapi memberikan peringatan di console atau pesan
            pass
        return link


# --- 2. FORM PENDATAAN PRESTASI (FOR STUDENTS) ---
class PrestasiForm(forms.ModelForm):
    """Digunakan untuk tombol 'PENDATAAN' di navbar oleh mahasiswa"""
    class Meta:
        model = Prestasi
        fields = ['nama_mahasiswa', 'prodi', 'nama_lomba', 'link_foto']
        
        widgets = {
            'nama_mahasiswa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Lengkap'}),
            'prodi': forms.Select(attrs={'class': 'form-select'}),
            'nama_lomba': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Kompetisi'}),
            'link_foto': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Link Foto (Google Drive/Lainnya)'}),
        }


# --- 3. FORM PENDATAAN KARYA INOVASI ---
class KaryaForm(forms.ModelForm):
    class Meta:
        model = Karya
        fields = ['judul_karya', 'pembuat', 'prodi']
        
        widgets = {
            'judul_karya': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Judul Inovasi'}),
            'pembuat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama-nama Pembuat'}),
            'prodi': forms.Select(attrs={'class': 'form-select'}),
        }