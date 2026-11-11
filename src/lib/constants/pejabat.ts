export const STANDARD_PEJABAT_OPTIONS: string[] = [
  'Bupati',
  'Wakil Bupati',
  'Bupati & Wakil Bupati',
  '-',
  'Belum Ditentukan',
];

export const PEJABAT_OPTIONS: string[] = [
  ...STANDARD_PEJABAT_OPTIONS,
  'Lainnya',
];

export type PejabatOption = string;
