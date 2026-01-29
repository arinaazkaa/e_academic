from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from datetime import date

from .models import Materi, Prestasi, Karya, InfoLomba, AgendaKalender, FileKalender
from .forms import MateriForm, KaryaForm, PrestasiForm

# --- 1. HOMEPAGE ---
def home(request):
    prestasi_list = Prestasi.objects.filter(status='approved').order_by('-created_at')[:6]
    today = date.today()

    info_lomba_list = InfoLomba.objects.filter(
        Q(tanggal_deadline__gte=today) | Q(tanggal_deadline__isnull=True)
    ).order_by('tanggal_deadline')[:3]

    karya_list = Karya.objects.filter(status='approved').order_by('-created_at')[:4]
    
    agenda_list = AgendaKalender.objects.filter(
        tanggal_mulai__gte=today
    ).order_by('tanggal_mulai')[:4]

    return render(request, 'materi/home.html', {
        'prestasi_list': prestasi_list,
        'info_lomba_list': info_lomba_list,
        'karya_list': karya_list, 
        'agenda_list': agenda_list, 
    })


# --- 2. INPUT MATERI ---
def input_materi(request):
    if request.method == 'POST':
        form = MateriForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            messages.success(request, 'Terima kasih! Materi berhasil dikirim dan menunggu verifikasi Admin.')
            return redirect('list_materi')
        else:
            messages.error(request, 'Ada kesalahan input/ukuran file. Mohon periksa kembali.')
    else:
        form = MateriForm()

    return render(request, 'materi/input_materi.html', {'form': form})


# --- 3. INPUT PRESTASI ---
def input_prestasi(request):
    if request.method == "POST":
        form = PrestasiForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data Prestasi berhasil dikirim! Menunggu verifikasi admin.')
            return redirect('list_prestasi')
        else:
            messages.error(request, 'Gagal mengirim. Periksa kembali isian form atau ukuran foto.')
    else:
        form = PrestasiForm()

    return render(request, 'materi/input_prestasi.html', {'form': form})


# --- 4. INPUT KARYA ---
def input_karya(request):
    if request.method == 'POST':
        form = KaryaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Keren! Karya kamu sudah masuk antrian verifikasi.')
            return redirect('list_karya')
        else:
             messages.error(request, 'Gagal upload. Pastikan ukuran foto maksimal 2MB.')
    else:
        form = KaryaForm()

    return render(request, 'materi/input_karya.html', {'form': form})


# --- 5. E-LIBRARY (LIST MATERI) ---
def list_materi(request):
    materi_list = Materi.objects.filter(status='approved').order_by('-tanggal_upload')

    keyword = request.GET.get('keyword')
    prodi = request.GET.get('prodi')
    semester = request.GET.get('semester')
    
    if keyword:
        materi_list = materi_list.filter(
            Q(judul__icontains=keyword) | 
            Q(mata_kuliah__icontains=keyword)
        )
    if prodi:
        materi_list = materi_list.filter(prodi=prodi)
    if semester:
        materi_list = materi_list.filter(semester=semester)

    paginator = Paginator(materi_list, 12) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'materi/list_materi.html', {
        'materi': page_obj,
        'filter_prodi': prodi,
        'filter_semester': semester,
    })


# --- 6. GALERI KARYA ---
def list_karya(request):
    karya_list = Karya.objects.filter(status='approved')

    query = request.GET.get('q')
    if query:
        karya_list = karya_list.filter(
            Q(judul_karya__icontains=query) | 
            Q(pembuat__icontains=query)
        )

    sort_by = request.GET.get('sort', 'terbaru')
    if sort_by == 'terlama':
        karya_list = karya_list.order_by('created_at')
    else:
        karya_list = karya_list.order_by('-created_at')

    paginator = Paginator(karya_list, 16)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'materi/list_karya.html', {'karya_list': page_obj})


# --- 7. DETAIL KARYA ---
def detail_karya(request, id):
    karya = get_object_or_404(Karya, id=id)
    return render(request, 'materi/detail_karya.html', {'karya': karya})


# --- 8. PRESTASI (HALL OF FAME) ---
def list_prestasi(request):
    prestasi_list = Prestasi.objects.filter(status='approved').order_by('-created_at')

    keyword = request.GET.get('keyword')
    prodi = request.GET.get('prodi')

    if keyword:
        prestasi_list = prestasi_list.filter(
            Q(nama_mahasiswa__icontains=keyword) | 
            Q(nama_lomba__icontains=keyword)
        )
    if prodi:
        prestasi_list = prestasi_list.filter(prodi=prodi)

    paginator = Paginator(prestasi_list, 16) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'materi/list_prestasi.html', {
        'prestasi_list': page_obj,
        'filter_prodi': prodi
    })


# --- 9. DETAIL PRESTASI ---
def detail_prestasi(request, id):
    item = get_object_or_404(Prestasi, id=id)
    return render(request, 'materi/detail_prestasi.html', {'prestasi': item})


# --- 10. KALENDER AKADEMIK ---
def kalender(request):
    agenda_list = AgendaKalender.objects.all().order_by('tanggal_mulai')
    file_kalender = FileKalender.objects.last()

    return render(request, 'materi/kalender.html', {
        'agenda_list': agenda_list,
        'file_kalender': file_kalender
    })


# --- 11. LIST LOMBA ---
def list_lomba(request):
    lomba_list = InfoLomba.objects.all()

    query = request.GET.get('q')
    if query:
        lomba_list = lomba_list.filter(
            Q(judul__icontains=query) | 
            Q(penyelenggara__icontains=query)
        )

    sort_by = request.GET.get('sort')
    if sort_by == 'deadline':
        lomba_list = lomba_list.order_by('tanggal_deadline')
    elif sort_by == 'terbaru':
        lomba_list = lomba_list.order_by('-id')
    else:
        lomba_list = lomba_list.order_by('tanggal_deadline')

    return render(request, 'materi/list_lomba.html', {'lomba_list': lomba_list})


# --- 12. DETAIL LOMBA ---
def detail_lomba(request, id):
    lomba = get_object_or_404(InfoLomba, id=id)
    return render(request, 'materi/detail_lomba.html', {'lomba': lomba})