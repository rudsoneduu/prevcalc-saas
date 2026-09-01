'use client'

import React from 'react'

export interface ItemComplementacaoProps {
  competencia_periodo: string
  salario_minimo_epoca: number
  valor_pago: number
  diferenca_base: number
  aliquota_pct: number
  valor_complementar: number
}

interface ComplementacaoTableProps {
  itens?: ItemComplementacaoProps[]
  totalDarf?: number
}

export function ComplementacaoTable({ itens, totalDarf }: ComplementacaoTableProps) {
  const itensExibidos = itens && itens.length > 0 ? itens : []
  const total = totalDarf !== undefined ? totalDarf : (itensExibidos.reduce((a, b) => a + b.valor_complementar, 0))

  return (
    <div className="card-panel" style={{ border: '1px solid rgba(239, 68, 68, 0.3)', backgroundColor: '#0f172a' }}>
      
      {/* HEADER DO CARD DE COMPLEMENTAÇÃO */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', borderBottom: '1px solid #334155', paddingBottom: '0.75rem' }}>
        <div>
          <h2 style={{ fontSize: '0.85rem', fontWeight: 700, color: '#f8fafc', textTransform: 'uppercase', letterSpacing: '0.05em', margin: 0, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span style={{ color: '#f87171' }}>⚠️</span> DEMONSTRATIVO DE COMPLEMENTAÇÃO DE SALÁRIO MÍNIMO (PREC-MENOR-MIN)
          </h2>
          <p style={{ fontSize: '0.75rem', color: '#94a3b8', marginTop: '0.25rem' }}>
            Discriminação da diferença exata por competência para emissão de DARF/Guia (Art. 195, §14 CF/88 e EC 103/2019)
          </p>
        </div>

        <div style={{ backgroundColor: 'rgba(239, 68, 68, 0.15)', border: '1px solid rgba(239, 68, 68, 0.4)', borderRadius: '0.75rem', padding: '0.5rem 1rem', textAlign: 'right' }}>
          <div style={{ fontSize: '0.65rem', textTransform: 'uppercase', fontWeight: 700, color: '#fca5a5' }}>TOTAL A COMPLEMENTAR</div>
          <div className="font-mono" style={{ fontSize: '1.25rem', fontWeight: 800, color: '#f87171' }}>
            R$ {total.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
          </div>
        </div>
      </div>

      {itensExibidos.length === 0 ? (
        <div style={{ padding: '1.5rem', textAlign: 'center', color: '#34d399', fontSize: '0.85rem', fontWeight: 600, backgroundColor: 'rgba(52, 211, 153, 0.1)', borderRadius: '0.75rem', border: '1px solid rgba(52, 211, 153, 0.3)' }}>
          ✓ Nenhuma contribuição abaixo do Salário Mínimo detectada para este segurado. Todas as competências foram recolhidas em conformidade.
        </div>
      ) : (
        /* TABELA DISCRIMINADA POR PERÍODO */
        <div style={{ overflowX: 'auto', maxHeight: '280px' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.75rem' }}>
            <thead>
              <tr style={{ backgroundColor: '#1e293b', color: '#94a3b8', textAlign: 'left' }}>
                <th style={{ padding: '0.6rem 0.75rem', fontWeight: 700 }}>ANO / MÊS</th>
                <th style={{ padding: '0.6rem 0.75rem', fontWeight: 700 }}>SALÁRIO MÍNIMO</th>
                <th style={{ padding: '0.6rem 0.75rem', fontWeight: 700 }}>VALOR PAGO</th>
                <th style={{ padding: '0.6rem 0.75rem', fontWeight: 700 }}>DIFERENÇA BASE</th>
                <th style={{ padding: '0.6rem 0.75rem', fontWeight: 700 }}>ALÍQUOTA</th>
                <th style={{ padding: '0.6rem 0.75rem', fontWeight: 700 }}>VALOR A COMPLEMENTAR</th>
              </tr>
            </thead>
            <tbody>
              {itensExibidos.map((item, idx) => (
                <tr key={idx} style={{ borderBottom: '1px solid #1e293b', color: '#f8fafc' }}>
                  <td style={{ padding: '0.5rem 0.75rem', fontWeight: 600 }}>{item.competencia_periodo}</td>
                  <td style={{ padding: '0.5rem 0.75rem' }} className="font-mono">R$ {item.salario_minimo_epoca.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</td>
                  <td style={{ padding: '0.5rem 0.75rem' }} className="font-mono">R$ {item.valor_pago.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</td>
                  <td style={{ padding: '0.5rem 0.75rem', color: '#fbbf24', fontWeight: 600 }} className="font-mono">R$ {item.diferenca_base.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}/mês</td>
                  <td style={{ padding: '0.5rem 0.75rem' }}><span className="badge-ok" style={{ fontSize: '0.65rem' }}>{item.aliquota_pct}%</span></td>
                  <td style={{ padding: '0.5rem 0.75rem', color: '#f87171', fontWeight: 700 }} className="font-mono">R$ {item.valor_complementar.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

    </div>
  )
}
