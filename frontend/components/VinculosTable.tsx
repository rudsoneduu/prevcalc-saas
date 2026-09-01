'use client'

import React from 'react'

export interface VinculoItem {
  seq: number
  cnpj_cpf: string
  empregador: string
  data_inicio: string
  data_fim?: string | null
  tipo_vinculo: string
  qtd_salarios: number
}

interface VinculosTableProps {
  vinculos: VinculoItem[]
}

export function VinculosTable({ vinculos }: VinculosTableProps) {
  if (!vinculos || vinculos.length === 0) return null

  return (
    <div className="card-panel">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', borderBottom: '1px solid #334155', paddingBottom: '0.75rem' }}>
        <div>
          <h2 style={{ fontSize: '0.9rem', fontWeight: 700, color: '#f8fafc', textTransform: 'uppercase', letterSpacing: '0.05em', margin: 0, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span>🏢</span> Vínculos Empregatícios Extraídos do CNIS ({vinculos.length})
          </h2>
          <p style={{ fontSize: '0.75rem', color: '#94a3b8', marginTop: '0.25rem' }}>
            Histórico completo de empresas, períodos de trabalho e recolhimentos
          </p>
        </div>
      </div>

      <div className="spreadsheet-container">
        <table>
          <thead>
            <tr>
              <th style={{ width: '40px', textAlign: 'center' }}>Seq</th>
              <th style={{ width: '150px' }}>CNPJ / CPF</th>
              <th>Razão Social / Empregador</th>
              <th style={{ width: '110px' }}>Início</th>
              <th style={{ width: '110px' }}>Fim</th>
              <th style={{ width: '190px' }}>Tipo Vínculo</th>
              <th style={{ width: '90px', textAlign: 'center' }}>Salários</th>
            </tr>
          </thead>
          <tbody>
            {vinculos.map((v) => (
              <tr key={v.seq}>
                <td style={{ textAlign: 'center', color: '#64748b', fontWeight: 600 }}>{v.seq}</td>
                <td className="font-mono" style={{ fontSize: '0.75rem', color: '#94a3b8' }}>{v.cnpj_cpf}</td>
                <td style={{ fontWeight: 600, color: '#f8fafc' }}>{v.empregador}</td>
                <td className="font-mono" style={{ color: '#34d399' }}>{v.data_inicio}</td>
                <td className="font-mono" style={{ color: v.data_fim ? '#e2e8f0' : '#fbbf24' }}>
                  {v.data_fim || 'Em Aberto'}
                </td>
                <td>
                  <span className="badge-ok" style={{ fontSize: '0.65rem' }}>{v.tipo_vinculo}</span>
                </td>
                <td style={{ textAlign: 'center', fontWeight: 700, color: '#60a5fa' }}>{v.qtd_salarios}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
