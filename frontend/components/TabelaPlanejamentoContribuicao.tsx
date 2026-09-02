'use client'

import React from 'react'

interface PerfilOpcao {
  faixa: string
  multiplicador_sm: number
  base_contribuicao: number
  guia_20_pct: number      // Autônomo Código 1007
  guia_11_pct?: number     // Simplificado Código 1163 (Apenas no Salário Mínimo)
  rmi_estimada: number
  perfil_recomendado: string
}

export function TabelaPlanejamentoContribuicao() {
  const salarioMinimo = 1518.00
  const tetoInss = 8157.41

  const opcoes: PerfilOpcao[] = [
    {
      faixa: '1 Salário Mínimo (Piso Nacional)',
      multiplicador_sm: 1,
      base_contribuicao: 1518.00,
      guia_20_pct: 303.60,
      guia_11_pct: 166.98,
      rmi_estimada: 1518.00,
      perfil_recomendado: 'Ideal para orçamentos enxutos ou segurados que buscam a proteção básica do INSS.'
    },
    {
      faixa: '2 Salários Mínimos',
      multiplicador_sm: 2,
      base_contribuicao: 3036.00,
      guia_20_pct: 607.20,
      rmi_estimada: 3036.00,
      perfil_recomendado: 'Aposentadoria confortável com excelente relação custo-benefício mensal.'
    },
    {
      faixa: '3 Salários Mínimos (Recomendado ★)',
      multiplicador_sm: 3,
      base_contribuicao: 4554.00,
      guia_20_pct: 910.80,
      rmi_estimada: 4554.00,
      perfil_recomendado: 'Aposentadoria Saudável: Garante ótimo poder de compra mantendo o orçamento equilibrado.'
    },
    {
      faixa: '4 Salários Mínimos',
      multiplicador_sm: 4,
      base_contribuicao: 6072.00,
      guia_20_pct: 1214.40,
      rmi_estimada: 6072.00,
      perfil_recomendado: 'Para quem busca padrão de vida elevado e possui margem financeira mensal.'
    },
    {
      faixa: 'Teto Máximo do INSS (~5.3 SM)',
      multiplicador_sm: 5.37,
      base_contribuicao: 8157.41,
      guia_20_pct: 1631.48,
      rmi_estimada: 8157.41,
      perfil_recomendado: 'Aposentadoria de Elite: Retorno máximo permitido pela legislação previdenciária.'
    }
  ]

  return (
    <div className="card-panel" style={{ border: '1px solid rgba(52, 211, 153, 0.3)', backgroundColor: '#0f172a' }}>
      
      {/* CABEÇALHO DA TABELA DE PLANEJAMENTO */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem', borderBottom: '1px solid #334155', paddingBottom: '0.85rem' }}>
        <div>
          <h2 style={{ fontSize: '0.95rem', fontWeight: 800, color: '#f8fafc', textTransform: 'uppercase', letterSpacing: '0.05em', margin: 0, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span>📈</span> TABELA DE PLANEJAMENTO DE CONTRIBUIÇÃO FUTURA (1 A 5 SALÁRIOS & TETO)
          </h2>
          <p style={{ fontSize: '0.75rem', color: '#94a3b8', marginTop: '0.25rem' }}>
            Compare o valor mensal da guia (GPS/DARF) a pagar versus a Aposentadoria Estimada para escolher o perfil ideal do seu cliente
          </p>
        </div>

        <span className="badge-ok" style={{ fontSize: '0.75rem', backgroundColor: 'rgba(52, 211, 153, 0.2)', color: '#34d399', borderColor: 'rgba(52, 211, 153, 0.4)' }}>
          Valores Oficiais 2026
        </span>
      </div>

      {/* TABELA COMPARATIVA DE OPÇÕES DE CONTRIBUIÇÃO */}
      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.75rem' }}>
          <thead>
            <tr style={{ backgroundColor: '#1e293b', color: '#94a3b8', textAlign: 'left' }}>
              <th style={{ padding: '0.75rem', fontWeight: 700 }}>PERFIL / FAIXA</th>
              <th style={{ padding: '0.75rem', fontWeight: 700 }}>BASE DE CÁLCULO</th>
              <th style={{ padding: '0.75rem', fontWeight: 700 }}>GUIA MENSAL (20% GPS)</th>
              <th style={{ padding: '0.75rem', fontWeight: 700 }}>PLANO SIMPLIFICADO (11%)</th>
              <th style={{ padding: '0.75rem', fontWeight: 700 }}>APOSENTADORIA ESTIMADA</th>
              <th style={{ padding: '0.75rem', fontWeight: 700 }}>INDICAÇÃO PREVIDENCIÁRIA</th>
            </tr>
          </thead>
          <tbody>
            {opcoes.map((o, idx) => {
              const isRecomendada = o.faixa.includes('Recomendado')
              return (
                <tr
                  key={idx}
                  style={{
                    borderBottom: '1px solid #1e293b',
                    backgroundColor: isRecomendada ? 'rgba(59, 130, 246, 0.1)' : 'transparent',
                    color: '#f8fafc'
                  }}
                >
                  <td style={{ padding: '0.75rem', fontWeight: 700, color: isRecomendada ? '#60a5fa' : '#f8fafc' }}>
                    {o.faixa}
                  </td>
                  <td style={{ padding: '0.75rem' }} className="font-mono">
                    R$ {o.base_contribuicao.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                  </td>
                  <td style={{ padding: '0.75rem', color: '#fbbf24', fontWeight: 700 }} className="font-mono">
                    R$ {o.guia_20_pct.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}/mês
                  </td>
                  <td style={{ padding: '0.75rem', color: o.guia_11_pct ? '#34d399' : '#64748b' }} className="font-mono">
                    {o.guia_11_pct ? `R$ ${o.guia_11_pct.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}/mês` : 'Não se aplica'}
                  </td>
                  <td style={{ padding: '0.75rem', color: '#34d399', fontWeight: 800, fontSize: '0.85rem' }} className="font-mono">
                    R$ {o.rmi_estimada.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}/mês
                  </td>
                  <td style={{ padding: '0.75rem', color: '#94a3b8', fontSize: '0.7rem', lineHeight: 1.3 }}>
                    {o.perfil_recomendado}
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>

    </div>
  )
}
