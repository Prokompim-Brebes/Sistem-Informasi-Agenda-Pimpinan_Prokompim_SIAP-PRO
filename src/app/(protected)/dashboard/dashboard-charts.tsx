'use client';

import { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, ResponsiveContainer, Tooltip, CartesianGrid } from 'recharts';

interface AxisTickProps {
  x?: number;
  y?: number;
  payload?: {
    value?: string;
  };
}

export default function DashboardCharts({
  data,
}: {
  data: { bulan: string; fullBulan?: string; jumlah: number }[];
}) {
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 640);
    };
    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  const totalKegiatan = data.reduce((acc, curr) => acc + curr.jumlah, 0);

  return (
    <div>
      <div style={{ height: isMobile ? 250 : 240 }}>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={data}
            margin={{
              top: 12,
              right: isMobile ? 8 : 12,
              left: isMobile ? -14 : -10,
              bottom: isMobile ? 6 : 4,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#E2E5EA" vertical={false} />
            <XAxis
              dataKey="bulan"
              interval={0}
              height={isMobile ? 38 : 24}
              axisLine={false}
              tickLine={false}
              tick={(props: AxisTickProps) => {
                const { x = 0, y = 0, payload } = props;
                return (
                  <g transform={`translate(${x},${y})`}>
                    <text
                      x={0}
                      y={0}
                      dy={isMobile ? 10 : 12}
                      textAnchor={isMobile ? 'end' : 'middle'}
                      fill="#6B7280"
                      fontSize={isMobile ? 10 : 11}
                      transform={isMobile ? 'rotate(-45)' : undefined}
                    >
                      {payload?.value}
                    </text>
                  </g>
                );
              }}
            />
            <YAxis
              width={32}
              allowDecimals={false}
              tick={{ fontSize: 11, fill: '#6B7280' }}
              axisLine={false}
              tickLine={false}
            />
            <Tooltip
              cursor={{ fill: '#F3F1EC' }}
              formatter={(value) => [`${value ?? 0} kegiatan`, 'Jumlah']}
              labelFormatter={(label, payload) => {
                const item = payload?.[0]?.payload;
                return item?.fullBulan || label;
              }}
            />
            <Bar
              dataKey="jumlah"
              fill="#16294D"
              radius={isMobile ? [3, 3, 0, 0] : [5, 5, 0, 0]}
              maxBarSize={28}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
      {totalKegiatan === 0 && (
        <p className="text-xs text-muted text-center mt-2 italic">
          Belum ada agenda kegiatan yang tercatat pada tahun ini.
        </p>
      )}
    </div>
  );
}
