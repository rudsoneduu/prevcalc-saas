import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'PrevCalc SaaS Legal Tech Enterprise - Cálculos Previdenciários (1978-2026)',
  description: 'Sistema Web de Alta Precisão para RMI, Revisão da Vida Toda, Planejamento e Atrasados',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="pt-BR" className="dark" style={{ backgroundColor: '#0f172a', color: '#f8fafc' }}>
      <body className="bg-slate-900 text-slate-100 antialiased min-h-screen" style={{ backgroundColor: '#0f172a', color: '#f8fafc' }}>
        {children}
      </body>
    </html>
  )
}
