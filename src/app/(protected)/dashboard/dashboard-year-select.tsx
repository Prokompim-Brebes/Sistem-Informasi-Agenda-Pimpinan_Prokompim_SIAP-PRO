'use client';

import { useTransition } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { Calendar, ChevronDown, Loader2 } from 'lucide-react';

interface DashboardYearSelectProps {
  selectedYear: number;
  tahunOptions: number[];
  className?: string;
  id?: string;
}

export default function DashboardYearSelect({
  selectedYear,
  tahunOptions,
  className = '',
  id = 'dashboard-year-select',
}: DashboardYearSelectProps) {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [isPending, startTransition] = useTransition();

  const handleYearChange = (newYear: number) => {
    if (newYear === selectedYear) return;
    const params = new URLSearchParams(searchParams?.toString() ?? '');
    params.set('tahun', String(newYear));
    startTransition(() => {
      router.push(`/dashboard?${params.toString()}`);
    });
  };

  return (
    <div className={`relative inline-flex items-center ${className}`}>
      <div className="relative">
        <select
          id={id}
          value={selectedYear}
          disabled={isPending}
          onChange={(e) => handleYearChange(Number(e.target.value))}
          className="appearance-none bg-white border border-app rounded-xl pl-9 pr-9 py-2 text-sm font-semibold text-navy hover:border-navy/40 focus:outline-none focus:ring-2 focus:ring-navy/20 cursor-pointer disabled:opacity-60 transition-all shadow-sm"
          aria-label="Pilih Tahun Dashboard"
        >
          {tahunOptions.map((year) => (
            <option key={year} value={year}>
              Tahun {year}
            </option>
          ))}
        </select>
        <div className="absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none text-navy/60">
          <Calendar size={15} />
        </div>
        <div className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-navy/60">
          {isPending ? (
            <Loader2 size={15} className="animate-spin text-navy" />
          ) : (
            <ChevronDown size={15} />
          )}
        </div>
      </div>
    </div>
  );
}
