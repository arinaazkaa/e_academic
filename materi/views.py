from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages  # Untuk notifikasi
from django.db.models import Q       # Untuk pencarian
from django.core.paginator import Paginator # <--- JANGAN LUPA IMPORT INI DI ATAS

# Import Models
from .models import Materi, Prestasi, Karya, InfoLomba
# Import Form (Hanya untuk Materi & Karya yang simpel)
from .forms import MateriForm, KaryaForm 

# --- 1. HOMEPAGE ("ELEKTRO BANGGA") ---
def home(request):
    # Ambil 6 prestasi terbaru (approved)
    prestasi_list = Prestasi.objects.filter(status='approved').order_by('-created_at')[:6]
    
    # Ambil 3 info lomba terbaru (urut berdasarkan tanggal pelaksanaan terdekat)
    info_lomba_list = InfoLomba.objects.order_by('tanggal_pelaksanaan')[:3]
    
    return render(request, 'materi/home.html', {
        'prestasi_list': prestasi_list,
        'info_lomba_list': info_lomba_list,
    })


# --- 2. LOGIC INPUT MATERI ---
def input_materi(request):
    if request.method == 'POST':
        form = MateriForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Terima kasih! Materi berhasil dikirim dan menunggu verifikasi Admin.')
            return redirect('list_materi')
        else:
            messages.error(request, 'Ada kesalahan input. Mohon periksa kembali.')
    else:
        form = MateriForm()

    return render(request, 'materi/input_materi.html', {'form': form})


# --- 3. LOGIC INPUT PRESTASI (MANUAL + VALIDASI FOTO) ---
def input_prestasi(request):
    if request.method == "POST":
        try:
            # 1. Tangkap Data Teks
            nama_mahasiswa = request.POST.get('nama_mahasiswa')
            prodi = request.POST.get('prodi')
            no_hp = request.POST.get('no_hp')
            
            nama_lomba = request.POST.get('nama_lomba')
            penyelenggara = request.POST.get('penyelenggara')
            url_penyelenggara = request.POST.get('url_penyelenggara')
            jenis_lomba = request.POST.get('jenis_lomba')
            tingkat = request.POST.get('tingkat')
            kategori = request.POST.get('kategori')
            juara = request.POST.get('juara')
            
            tempat_tanggal = request.POST.get('tempat_tanggal')
            no_sk = request.POST.get('no_sk')
            link_sertifikat = request.POST.get('link_sertifikat')
            
            # Checkbox
            is_public = request.POST.get('is_public') == 'on'

            # 2. Tangkap File Foto (WAJIB pakai request.FILES)
            foto_diri = request.FILES.get('foto_diri')

            # --- VALIDASI FOTO (BARU) ---
            if foto_diri:
                # Cek Ukuran File (Maksimal 2MB)
                # 2 * 1024 * 1024 bytes = 2MB
                if foto_diri.size > 2 * 1024 * 1024:
                    messages.error(request, 'Ukuran foto terlalu besar! Maksimal 2MB agar hemat penyimpanan.')
                    return redirect('input_prestasi') # Kembali ke form
                
                # Cek Tipe File (Harus Gambar)
                if not foto_diri.content_type.startswith('image/'):
                    messages.error(request, 'File yang diupload bukan gambar. Harap upload format JPG/PNG.')
                    return redirect('input_prestasi') # Kembali ke form

            # 3. Simpan ke Database
            Prestasi.objects.create(
                nama_mahasiswa=nama_mahasiswa,
                prodi=prodi,
                no_hp=no_hp,
                nama_lomba=nama_lomba,
                penyelenggara=penyelenggara,
                url_penyelenggara=url_penyelenggara,
                jenis_lomba=jenis_lomba,
                tingkat=tingkat,
                kategori=kategori,
                juara=juara,
                tempat_tanggal=tempat_tanggal,
                no_sk=no_sk,
                link_sertifikat=link_sertifikat,
                is_public=is_public,
                foto_diri=foto_diri,
                status='pending'
            )

            messages.success(request, 'Data Prestasi berhasil dikirim! Menunggu verifikasi admin.')
            return redirect('list_prestasi')

        except Exception as e:
            messages.error(request, f'Terjadi kesalahan: {e}')
            return redirect('input_prestasi')

    return render(request, 'materi/input_prestasi.html')


# --- 4. LOGIC INPUT KARYA ---
def input_karya(request):
    if request.method == 'POST':
        form = KaryaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Keren! Karya kamu sudah masuk antrian verifikasi.')
            return redirect('list_karya')
    else:
        form = KaryaForm()

    return render(request, 'materi/input_karya.html', {'form': form})


# --- 5. PERPUSTAKAAN (LIST MATERI) ---

def list_materi(request):
    # 1. Ambil semua data (Queryset)
    materi_list = Materi.objects.filter(status='approved').order_by('-tanggal_upload')

    # 2. Filter & Search Logic (Tetap Sama)
    cari_judul = request.GET.get('keyword')
    prodi = request.GET.get('prodi')
    semester = request.GET.get('semester')
    
    if cari_judul:
        materi_list = materi_list.filter(
            Q(judul__icontains=cari_judul) | 
            Q(mata_kuliah__icontains=cari_judul)
        )
    if prodi and prodi != '':
        materi_list = materi_list.filter(prodi=prodi)
    if semester and semester != '':
        materi_list = materi_list.filter(semester=semester)

    # 3. PAGINATION LOGIC (BARU)
    # Tampilkan 16 materi per halaman (4 kolom x 4 baris)
    paginator = Paginator(materi_list, 16) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'materi': page_obj, # Sekarang kita kirim 'page_obj', bukan list biasa
        'filter_prodi': prodi,
        'filter_semester': semester,
    }

    return render(request, 'materi/list_materi.html', context)

# --- 6. HALAMAN LIST KARYA ---
def list_karya(request):
    karya_list = Karya.objects.filter(status='approved').order_by('-created_at')
    return render(request, 'materi/list_karya.html', {'karya_list': karya_list})


# --- 7. HALAMAN LIST PRESTASI (HALL OF FAME) ---
def list_prestasi(request):
    # Ambil data approved
    prestasi_list = Prestasi.objects.filter(status='approved').order_by('-created_at')

    # --- FITUR SEARCH PRESTASI ---
    keyword = request.GET.get('keyword')
    prodi = request.GET.get('prodi')

    if keyword:
        # Cari berdasarkan nama mahasiswa ATAU nama lomba
        prestasi_list = prestasi_list.filter(
            Q(nama_mahasiswa__icontains=keyword) | 
            Q(nama_lomba__icontains=keyword)
        )
    
    if prodi and prodi != '':
        prestasi_list = prestasi_list.filter(prodi=prodi)

    return render(request, 'materi/list_prestasi.html', {'prestasi_list': prestasi_list})


# --- 8. KALENDER AKADEMIK ---
def kalender(request):
    return render(request, 'materi/kalender.html')


# --- 9. DETAIL INFO LOMBA ---
def detail_lomba(request, id_lomba):
    lomba = get_object_or_404(InfoLomba, id=id_lomba)
    return render(request, 'materi/detail_lomba.html', {'lomba': lomba})


# --- 10. DETAIL PRESTASI ---
def detail_prestasi(request, id_prestasi):
    # Ambil data prestasi berdasarkan ID
    p = get_object_or_404(Prestasi, id=id_prestasi)
    return render(request, 'materi/detail_prestasi.html', {'p': p})