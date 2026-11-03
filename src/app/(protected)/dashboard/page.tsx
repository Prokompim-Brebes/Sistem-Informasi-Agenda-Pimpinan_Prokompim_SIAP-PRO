import Link from 'next/link';
import Image from 'next/image';
import nextDynamic from 'next/dynamic';
import { CalendarDays, CheckCircle2, CalendarCheck2 } from 'lucide-react';
import type { ReactNode } from 'react';
import { existsSync } from 'fs';
import path from 'path';
import { prisma } from '@/lib/prisma';
import { getCurrentUser } from '@/lib/auth';
import { hitungProgressDokumen } from '@/lib/constants/status-dokumen';
import DashboardYearSelect from './dashboard-year-select';

export const dynamic = 'force-dynamic';

const DashboardCharts = nextDynamic(() => import('./dashboard-charts'), {
  loading: () => <div className="h-[240px] bg-slate-50 animate-pulse rounded-xl" />,
});

const DashboardStats = nextDynamic(() => import('./dashboard-stats'), {
  loading: () => <div className="h-[200px] bg-slate-50 animate-pulse rounded-xl" />,
});

interface DashboardPageProps {
  searchParams?: Promise<{ tahun?: string }>;
}

export default async function DashboardPage({ searchParams }: DashboardPageProps) {
  try {
    const resolvedParams = searchParams ? await searchParams : {};
    const user = await getCurrentUser();
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);

    const startOfMonth = new Date(today.getFullYear(), today.getMonth(), 1);
    const endOfMonth = new Date(today.getFullYear(), today.getMonth() + 1, 0, 23, 59, 59, 999);

    const currentYear = today.getFullYear();
    const parsedYear = resolvedParams?.tahun ? parseInt(resolvedParams.tahun, 10) : NaN;
    const selectedYear = !isNaN(parsedYear) && parsedYear >= 2000 && parsedYear <= 2100 ? parsedYear : currentYear;

    const yearStart = new Date(Date.UTC(selectedYear, 0, 1, 0, 0, 0, 0));
    const yearEnd = new Date(Date.UTC(selectedYear, 11, 31, 23, 59, 59, 999));

    // Hero: pakai foto gedung KPT hanya jika file sudah ada di public/
    const showHeroFoto = existsSync(path.join(process.cwd(), 'public', 'gedung-kpt.jpg'));

    const [
      bulanIniCount,
      hariIniCount,
      sudahCount,
      belumCount,
      tahunSelectedCount,
      statusKegiatanRaw,
      upcoming,
      chartDataRaw,
      topSektorRaw,
      kegiatanWithDokumen,
      tahunAgg,
    ] = await Promise.all([
      prisma.kegiatan.count({ where: { tanggal: { gte: startOfMonth, lte: endOfMonth } } }),
      prisma.kegiatan.count({ where: { tanggal: { gte: today, lt: tomorrow } } }),
      prisma.kegiatan.count({ where: { statusSambutan: 'SUDAH' } }),
      prisma.kegiatan.count({ where: { statusSambutan: 'BELUM' } }),
      prisma.kegiatan.count({ where: { tanggal: { gte: yearStart, lte: yearEnd } } }),
      prisma.kegiatan.groupBy({
        by: ['statusKegiatan'],
        where: { tanggal: { gte: yearStart, lte: yearEnd } },
        _count: true,
      }),
      prisma.kegiatan.findMany({
        where: { tanggal: { gte: today } },
        orderBy: { tanggal: 'asc' },
        take: 5,
      }),
      prisma.kegiatan.findMany({
        where: { tanggal: { gte: yearStart, lte: yearEnd } },
        select: { tanggal: true },
      }),
      prisma.kegiatan.groupBy({
        by: ['leadingSectorId'],
        where: {
          leadingSectorId: { not: null },
          tanggal: { gte: yearStart, lte: yearEnd },
        },
        _count: true,
        orderBy: { _count: { leadingSectorId: 'desc' } },
        take: 10,
      }),
      prisma.kegiatan.findMany({
        where: { tanggal: { gte: yearStart, lte: yearEnd } },
        select: { id: true, namaKegiatan: true, dokumen: { select: { status: true } } },
      }),
      prisma.kegiatan.aggregate({
        _min: { tanggal: true },
        _max: { tanggal: true },
      }),
    ]);

    // Opsi tahun untuk dropdown selector
    const minDbYear = tahunAgg._min.tanggal ? new Date(tahunAgg._min.tanggal).getFullYear() : currentYear;
    const maxDbYear = tahunAgg._max.tanggal ? new Date(tahunAgg._max.tanggal).getFullYear() : currentYear;
    const tahunSet = new Set<number>([currentYear, selectedYear, minDbYear, maxDbYear]);
    tahunSet.add(currentYear - 1);
    tahunSet.add(currentYear + 1);
    for (let y = minDbYear; y <= maxDbYear; y++) {
      tahunSet.add(y);
    }
    const tahunOptions = Array.from(tahunSet).sort((a, b) => b - a);

    // Format 12 bulan (Januari - Desember) untuk tahun yang dipilih
    const NAMA_BULAN_PENDEK = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'];
    const NAMA_BULAN_PANJANG = [
      'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
      'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember',
    ];

    const chartData = NAMA_BULAN_PENDEK.map((shortName, monthIdx) => ({
      bulan: shortName,
      fullBulan: `${NAMA_BULAN_PANJANG[monthIdx]} ${selectedYear}`,
      jumlah: 0,
    }));

    chartDataRaw.forEach((k) => {
      const d = new Date(k.tanggal);
      const m = d.getUTCMonth();
      if (m >= 0 && m < 12) {
        chartData[m].jumlah += 1;
      }
    });

    // --- Progress dokumen per kegiatan (tahun yang dipilih) ---
    let progressLengkap = 0;
    let progressBelum = 0;
    const perluPerhatianList: string[] = [];
    kegiatanWithDokumen.forEach((k) => {
      const pct = hitungProgressDokumen(k.dokumen);
      if (pct === 100) {
        progressLengkap++;
      } else {
        progressBelum++;
        perluPerhatianList.push(k.namaKegiatan);
      }
    });

    // --- Status Pelaksanaan Kegiatan (tahun yang dipilih) ---
    const statusCounts: Record<string, number> = {
      ACARA_MASUK: 0,
      MENUNGGU_PENUGASAN: 0,
      KEGIATAN_SELESAI: 0,
      SPJ_SELESAI: 0,
    };
    statusKegiatanRaw.forEach((s) => {
      if (s.statusKegiatan in statusCounts) {
        statusCounts[s.statusKegiatan] = s._count;
      }
    });
    const selesaiCount = statusCounts.KEGIATAN_SELESAI + statusCounts.SPJ_SELESAI;

    // --- Top 5 leading sector ---
    const topSektorIds = topSektorRaw.map((t) => t.leadingSectorId).filter((id): id is string => Boolean(id));
    const sektorNama = topSektorIds.length > 0
      ? await prisma.leadingSector.findMany({
        where: {
          id: { in: topSektorIds },
          nama: { not: '-' },
        },
        select: { id: true, nama: true },
      })
      : [];
    const topSektorData = topSektorRaw
      .map((t) => {
        const s = sektorNama.find((x) => x.id === t.leadingSectorId);
        if (!s || !s.nama || s.nama.trim() === '-') return null;
        return { nama: s.nama, count: t._count };
      })
      .filter((item): item is { nama: string; count: number } => item !== null)
      .slice(0, 5);

    type Stat = {
      label: string;
      value: number;
      icon: ReactNode;
      tone: 'default' | 'success' | 'warning';
      sub?: ReactNode;
    };

    const stats: Stat[] = [
      { label: 'Kegiatan bulan ini', value: bulanIniCount, icon: <CalendarDays size={18} />, tone: 'default' as const },
      { label: 'Kegiatan hari ini', value: hariIniCount, icon: <CalendarDays size={18} />, tone: 'default' as const },
      { 
        label: 'Total Sambutan', 
        value: sudahCount + belumCount, 
        icon: <CheckCircle2 size={18} />, 
        tone: 'success', 
        sub: ( 
          <div className='flex gap-4 mt-1 text-xs'>
            <span>
              <span className='text-green-600 font-semibold'>{sudahCount}</span> sudah </span>
            <span>
              <span className='text-amber-600 font-semibold'>{belumCount}</span> belum </span>
          </div>
         ), 
      },
      { 
        label: `Kegiatan ${selectedYear}`, 
        value: tahunSelectedCount, 
        icon: <CalendarCheck2 size={18} />, 
        tone: 'default',
        sub: (
          <div className='flex gap-2 mt-1 text-xs'>
            <span className='text-muted'>
              <span className='text-navy font-semibold'>{selesaiCount}</span> telah terlaksana
            </span>
          </div>
        ),
      },
    ];

    const toneClass = { default: 'bg-app text-navy', success: 'badge-sudah', warning: 'badge-belum' };

    return (
      <div className="space-y-6">
        {/* Hero Banner */}
        <div className='relative overflow-hidden rounded-2xl bg-navy text-white shadow-sm'>
          {showHeroFoto && (
            <div className='absolute inset-0 opacity-40'>
              <Image
                src="/gedung-kpt.jpg"
                alt="Gedung KPT"
                fill
                priority
                className="object-cover object-center"
                sizes="(max-width: 768px) 100vw, 1200px"
                quality={75}
              />
            </div>
          )}
          <div className='absolute inset-0 bg-gradient-to-r from-navy via-navy/85 to-navy/30 pointer-events-none' />
          <div className='relative z-10 p-5 sm:p-8'>
            <p className='text-gold text-xs font-semibold uppercase tracking-wider'>Sistem Manajemen SPJ · Prokompim</p>
            <h1 className='font-display text-2xl sm:text-3xl font-semibold mt-1'>
              Selamat datang, {user?.nama ?? 'Pengguna'}
            </h1>
            <p className='text-white/80 text-sm mt-2'>
              Pantau agenda kegiatan, status sambutan, dan kelengkapan dokumen SPJ.
            </p>
          </div>
        </div>

        {/* Header Ringkasan & Filter Tahun */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
          <div>
            <h2 className="font-display text-lg font-bold text-navy">Ringkasan Kegiatan</h2>
            <p className="text-xs text-muted">Statistik agenda dan kegiatan pimpinan Pemerintah Kabupaten Brebes</p>
          </div>
          <div className="flex items-center gap-2 self-start sm:self-auto">
            <span className="text-xs font-semibold text-muted">Filter Tahun:</span>
            <DashboardYearSelect selectedYear={selectedYear} tahunOptions={tahunOptions} id="dashboard-year-select-top" />
          </div>
        </div>

        {/* --- Status cards --- */}
        <div className='grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4'>
          {stats.map((s) => (
            <div key={s.label} className='bg-white rounded-2xl border border-app p-5 flex items-center justify-between shadow-sm'>
              <div>
                <p className='text-muted text-xs mb-1'>{s.label}</p>
                <p className='font-display text-3xl font-semibold text-navy'>{s.value}</p>
                {s.sub && <div>{s.sub}</div>}
              </div>
              <div className={`rounded-full p-2.5 ${toneClass[s.tone]}`}>{s.icon}</div>
            </div>
          ))}
        </div>

        {/* --- Row: grafik bulanan + kegiatan terdekat --- */}
        <div className="grid grid-cols-1 lg:grid-cols-5 gap-4">
          <div className="lg:col-span-3 bg-white rounded-2xl border border-app p-5 shadow-sm">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-4">
              <div>
                <h3 className="font-display text-base font-semibold text-navy">Jumlah Kegiatan per Bulan</h3>
                <p className="text-xs text-muted">Distribusi 12 bulan pada tahun {selectedYear}</p>
              </div>
              <DashboardYearSelect selectedYear={selectedYear} tahunOptions={tahunOptions} id="dashboard-year-select-chart" />
            </div>
            <DashboardCharts data={chartData} />
          </div>
          <div className="lg:col-span-2 bg-white rounded-2xl border border-app p-5 shadow-sm">
            <h3 className="font-display text-base font-semibold text-navy mb-4">Kegiatan Terdekat</h3>
            {upcoming.length === 0 ? (
              <p className="text-sm text-muted">Belum ada kegiatan mendatang.</p>
            ) : (
              <ul className="space-y-3">
                {upcoming.map((k) => (
                  <li key={k.id}>
                    <Link
                      href="/worksheet"
                      className="flex items-start gap-3 text-sm rounded-lg p-1.5 -m-1.5 hover:bg-app transition-colors"
                    >
                      <div className="font-mono text-xs bg-app rounded-md px-2 py-1 text-navy flex-shrink-0 mt-0.5">
                        {new Date(k.tanggal).toLocaleDateString('id-ID', { day: '2-digit', month: 'short' })}
                      </div>
                      <div className="min-w-0">
                        <p className="font-medium truncate">{k.namaKegiatan}</p>
                        <p className="text-muted text-xs truncate">{k.tempat}</p>
                      </div>
                    </Link>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>

        {/* --- Row 3: Progress Dokumen & Top Sektor --- */}
        <DashboardStats
          progressLengkap={progressLengkap}
          progressBelum={progressBelum}
          topSektor={topSektorData}
          perluPerhatian={perluPerhatianList}
        />
      </div>
    );
  } catch (error) {
    console.error('[DASHBOARD_PAGE_ERROR]', error);
    return (
      <div className="p-6 text-center text-red-600 bg-red-50 rounded-lg border border-red-100">
        <p className="font-medium">Gagal memuat dashboard.</p>
        <p className="text-sm mt-1">Silakan muat ulang halaman atau hubungi administrator.</p>
      </div>
    );
  }
}
