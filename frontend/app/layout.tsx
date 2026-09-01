import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'PrevCalc INSS Web - Sistema de Cálculos Previdenciários (1978-2026)',
  description: 'Sistema Web de Alta Precisão para RMI, Revisão da Vida Toda e Atrasados',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="pt-BR">
      <body className="bg-slate-900 text-slate-100 antialiased min-h-screen">
        {children}
      </body>
    </html>
  )
}
