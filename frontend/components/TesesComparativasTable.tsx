'use client'

import React from 'react'

export interface TeseItem {
  codigo_regra: string
  nome_regra: string
  elegivel: boolean
  rmi_estimada: number
  coeficiente_aplicado: number
  fator_previdenciario: number
  requisitos_cumpridos: string
  motivo_inelegibilidade?: string | null
}

interface TesesComparativasTableProps {
  teses: TeseItem[]
}

export function TesesComparativasTable({ teses }: TesesComparativasTableProps) {
  if (!teses || teses.length === 0) return null

  return (
    <div className="card-panel" style={{ border: '1px solid rgba(59, 130, 246, 0.3)', backgroundColor: '#0f172a' }}>
      
      {/* CABEÇALHO DO CARD */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', borderBottom: '1px solid #334155', paddingBottom: '0.75rem' }}>
        <div>
          <h2 style={{ fontSize: '0.9rem', fontWeight: 700, color: '#f8fafc', textTransform: 'uppercase', letterSpacing: '0.05em', margin: 0, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span>⚖️</span> Comparativo das 4 Regras de Transição (EC 103/2019)
          </h2>
          <p style={{ fontSize: '0.75rem', color: '#94a3b8', marginTop: '0.25rem' }}>
            Análise simultânea de teses para instrução de Petição Inicial e escolha da RMI mais vantajosa
          </p>
        </div>
      </div>

      {/* GRADE COMPARATIVA DAS REGRAS */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '1rem' }}>
        {teses.map((t, idx) => {
          const isVantajosa = t.codigo_regra === 'PEDAGIO_100' || idx === 0
          return (
            <div
              key={t.codigo_regra}
              style={{
                backgroundColor: t.elegivel ? (isVantajosa ? 'rgba(16, 185, 129, 0.1)' : '#1e293b') : '#1e293b',
                border: t.elegivel ? (isVantajosa ? '1px solid #34d399' : '1px solid #3b82f6') : '1px solid #334155',
                borderRadius: '0.85rem',
                padding: '1rem',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between',
                opacity: t.elegivel ? 1 : 0.65
              }}
            >
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                  <span className="badge-ok" style={{ fontSize: '0.65rem', backgroundColor: t.elegivel ? 'rgba(52, 211, 153, 0.2)' : 'rgba(239, 68, 68, 0.2)', color: t.elegivel ? '#34d399' : '#f87171', borderColor: t.elegivel ? 'rgba(52, 211, 153, 0.4)' : 'rgba(239, 68, 68, 0.4)' }}>
                    {t.elegivel ? 'Elegível ✓' : 'Inelegível ✕'}
                  </span>

                  {isVantajosa && t.elegivel && (
                    <span style={{ fontSize: '0.65rem', fontWeight: 700, color: '#34d399', backgroundColor: 'rgba(52, 211, 153, 0.15)', padding: '0.15rem 0.45rem', borderRadius: '0.375rem', border: '1px solid rgba(52, 211, 153, 0.3)' }}>
                      Mais Vantajosa ★
                    </span>
                  )}
                </div>

                <div style={{ fontSize: '0.825rem', fontWeight: 700, color: '#f8fafc', marginBottom: '0.5rem' }}>
                  {t.nome_regra}
                </div>

                <div style={{ fontSize: '0.7rem', color: '#94a3b8', marginBottom: '0.75rem', lineHeight: 1.35 }}>
                  {t.requisitos_cumpridos}
                  {t.motivo_inelegibilidade && (
                    <div style={{ color: '#f87171', marginTop: '0.25rem' }}>{t.motivo_inelegibilidade}</div>
                  )}
                </div>
              </div>

              <div style={{ borderTop: '1px solid #334155', paddingTop: '0.5rem', marginTop: '0.5rem' }}>
                <div style={{ fontSize: '0.65rem', color: '#94a3b8', textTransform: 'uppercase', fontWeight: 600 }}>RMI Estimada</div>
                <div className="font-mono" style={{ fontSize: '1.25rem', fontWeight: 800, color: t.elegivel ? '#34d399' : '#94a3b8' }}>
                  {t.elegivel ? `R$ ${t.rmi_estimada.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}` : '—'}
                </div>
              </div>
            </div>
          )
        })}
      </div>

    </div>
  )
}
