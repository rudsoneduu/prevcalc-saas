'use client'

import React from 'react'

interface AuditoriaModalProps {
  isOpen: boolean
  onClose: () => void
  onDownloadPdf: () => void
}

export function AuditoriaModal({ isOpen, onClose, onDownloadPdf }: AuditoriaModalProps) {
  if (!isOpen) return null

  return (
    <div style={{ position: 'fixed', inset: 0, backgroundColor: 'rgba(15, 23, 42, 0.85)', backdropFilter: 'blur(8px)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 50, padding: '1rem' }}>
      <div className="card-panel" style={{ maxWidth: '850px', width: '100%', maxHeight: '90vh', overflowY: 'auto', border: '1px solid #3b82f6', boxShadow: '0 20px 50px rgba(0, 0, 0, 0.5)' }}>
        
        {/* CABEÇALHO DO PAINEL DE AUDITORIA */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #334155', paddingBottom: '1rem', marginBottom: '1.25rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <div style={{ width: '2.5rem', height: '2.5rem', borderRadius: '0.5rem', backgroundColor: 'rgba(59, 130, 246, 0.2)', border: '1px solid rgba(59, 130, 246, 0.4)', color: '#60a5fa', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.25rem', fontWeight: 700 }}>
              🛡️
            </div>
            <div>
              <h2 style={{ fontSize: '1.2rem', fontWeight: 800, color: '#f8fafc', margin: 0 }}>
                Auditoria Previdenciária & Conformidade Numérica
              </h2>
              <p style={{ fontSize: '0.75rem', color: '#94a3b8', margin: 0 }}>
                Parecer Técnico Online de Validação das Regras do INSS, STF (Tema 1102) e STJ
              </p>
            </div>
          </div>

          <button onClick={onClose} style={{ background: 'transparent', border: 'none', color: '#94a3b8', fontSize: '1.25rem', padding: '0.2rem 0.5rem' }}>
            ✕
          </button>
        </div>

        {/* MÉTRICAS DE CONFORMIDADE */}
        <div className="grid-4" style={{ marginBottom: '1.25rem' }}>
          <div style={{ backgroundColor: '#0f172a', border: '1px solid rgba(52, 211, 153, 0.3)', borderRadius: '0.75rem', padding: '0.85rem' }}>
            <div style={{ fontSize: '0.65rem', color: '#34d399', textTransform: 'uppercase', fontWeight: 700 }}>Precisão Numérica</div>
            <div style={{ fontSize: '1.1rem', fontWeight: 800, color: '#f8fafc', marginTop: '0.2rem' }}>Decimal(28)</div>
            <div style={{ fontSize: '0.65rem', color: '#94a3b8', marginTop: '0.2rem' }}>Sem erros IEEE 754</div>
          </div>

          <div style={{ backgroundColor: '#0f172a', border: '1px solid rgba(59, 130, 246, 0.3)', borderRadius: '0.75rem', padding: '0.85rem' }}>
            <div style={{ fontSize: '0.65rem', color: '#60a5fa', textTransform: 'uppercase', fontWeight: 700 }}>Divisor 1978</div>
            <div style={{ fontSize: '1.1rem', fontWeight: 800, color: '#f8fafc', marginTop: '0.2rem' }}>2,75 Trilhões</div>
            <div style={{ fontSize: '0.65rem', color: '#94a3b8', marginTop: '0.2rem' }}>Cadeia exata 6 moedas</div>
          </div>

          <div style={{ backgroundColor: '#0f172a', border: '1px solid rgba(251, 191, 36, 0.3)', borderRadius: '0.75rem', padding: '0.85rem' }}>
            <div style={{ fontSize: '0.65rem', color: '#fbbf24', textTransform: 'uppercase', fontWeight: 700 }}>IRSM 02/1994</div>
            <div style={{ fontSize: '1.1rem', fontWeight: 800, color: '#f8fafc', marginTop: '0.2rem' }}>39,67% Aplicado</div>
            <div style={{ fontSize: '0.65rem', color: '#94a3b8', marginTop: '0.2rem' }}>Lei 10.999/2004</div>
          </div>

          <div style={{ backgroundColor: '#0f172a', border: '1px solid rgba(168, 85, 247, 0.3)', borderRadius: '0.75rem', padding: '0.85rem' }}>
            <div style={{ fontSize: '0.65rem', color: '#c084fc', textTransform: 'uppercase', fontWeight: 700 }}>Regra STJ Atrasados</div>
            <div style={{ fontSize: '1.1rem', fontWeight: 800, color: '#f8fafc', marginTop: '0.2rem' }}>Súmula 45 AGU</div>
            <div style={{ fontSize: '0.65rem', color: '#94a3b8', marginTop: '0.2rem' }}>Isento pré-10/1996</div>
          </div>
        </div>

        {/* DETALHAMENTO DOS PONTOS AUDITADOS */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem', marginBottom: '1.5rem' }}>
          
          <div style={{ backgroundColor: '#0f172a', border: '1px solid #334155', borderRadius: '0.75rem', padding: '1rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.35rem' }}>
              <span style={{ color: '#34d399' }}>✓</span>
              <strong style={{ fontSize: '0.85rem', color: '#f8fafc' }}>1. Tabela de Transição Monetária (1978 – 2026)</strong>
            </div>
            <p style={{ fontSize: '0.75rem', color: '#94a3b8', margin: 0, lineHeight: 1.4 }}>
              Validação das 6 moedas históricas (<code style={{ color: '#60a5fa' }}>Cr$</code>, <code style={{ color: '#60a5fa' }}>Cz$</code>, <code style={{ color: '#60a5fa' }}>NCz$</code>, <code style={{ color: '#60a5fa' }}>Cr$</code>, <code style={{ color: '#60a5fa' }}>CR$</code>, <code style={{ color: '#60a5fa' }}>R$</code>) com divisor cumulativo exato de 2,75 trilhões para salários de 1978 e aplicação da URV de 30/06/1994 (CR$ 2.750,00).
            </p>
          </div>

          <div style={{ backgroundColor: '#0f172a', border: '1px solid #334155', borderRadius: '0.75rem', padding: '1rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.35rem' }}>
              <span style={{ color: '#34d399' }}>✓</span>
              <strong style={{ fontSize: '0.85rem', color: '#f8fafc' }}>2. Aposentadoria Comum vs Revisão da Vida Toda (Tema 1102 STF)</strong>
            </div>
            <p style={{ fontSize: '0.75rem', color: '#94a3b8', margin: 0, lineHeight: 1.4 }}>
              Na Aposentadoria Comum (EC 103/2019), o PBC é restrito aos salários pós-07/1994 com 100% da média. Na Revisão da Vida Toda, o PBC é expandido de 1978 a 2026 com aplicação do IRSM de 02/1994 (39,67%) e descarte automático dos 20% menores salários.
            </p>
          </div>

          <div style={{ backgroundColor: '#0f172a', border: '1px solid #334155', borderRadius: '1rem', padding: '1rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.35rem' }}>
              <span style={{ color: '#34d399' }}>✓</span>
              <strong style={{ fontSize: '0.85rem', color: '#f8fafc' }}>3. Penalidades de Atrasados (Art. 45-A da Lei 8.212/91)</strong>
            </div>
            <p style={{ fontSize: '0.75rem', color: '#94a3b8', margin: 0, lineHeight: 1.4 }}>
              Isenção absoluta de juros moratórios e multa para contribuições anteriores a 11/10/1996 (Jurisprudência pacificada no STJ e Súmula 45 AGU). Incidência de Multa (10%) e SELIC apenas pós-10/1996.
            </p>
          </div>

        </div>

        {/* RODAPÉ DO MODAL COM BOTÃO DE DOWNLOAD */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderTop: '1px solid #334155', paddingTop: '1rem' }}>
          <button onClick={onClose} className="btn-secondary">
            Fechar Painel
          </button>

          <button onClick={onDownloadPdf} className="btn-primary" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span>📥</span> Baixar Parecer de Auditoria Completo (PDF)
          </button>
        </div>

      </div>
    </div>
  )
}
