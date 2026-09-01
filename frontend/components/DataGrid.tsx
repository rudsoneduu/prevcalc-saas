'use client'

import React from 'react'

export interface SalarioItem {
  competencia: string
  valor: number
  moeda: string
}

interface DataGridProps {
  salarios: SalarioItem[]
  onUpdate: (updated: SalarioItem[]) => void
  onAddRow: () => void
  onClear: () => void
  onPreencherLote: (tipo: 'MINIMO' | 'TETO') => void
  onCarregarExemplo: () => void
}

export function DataGrid({
  salarios,
  onUpdate,
  onAddRow,
  onClear,
  onPreencherLote,
  onCarregarExemplo,
}: DataGridProps) {

  const identificarMoeda = (comp: string) => {
    if (comp < "1986-02") return "Cr$"
    if (comp <= "1989-01") return "Cz$"
    if (comp <= "1990-03") return "NCz$"
    if (comp <= "1993-07") return "Cr$"
    if (comp <= "1994-06") return "CR$"
    return "R$"
  }

  const converterParaReal = (valor: number, comp: string) => {
    if (comp >= "1994-07") return valor
    if (comp < "1986-02") return valor / 2750000000000
    if (comp <= "1989-01") return valor / 2750000000
    if (comp <= "1990-03") return valor / 2750000
    if (comp <= "1993-07") return valor / 2750000
    if (comp <= "1994-06") return valor / 2750
    return valor
  }

  const handleFieldChange = (index: number, field: keyof SalarioItem, value: any) => {
    const copy = [...salarios]
    copy[index] = { ...copy[index], [field]: value }
    if (field === 'competencia') {
      copy[index].moeda = identificarMoeda(value)
    }
    onUpdate(copy)
  }

  const handleRemoveRow = (index: number) => {
    const copy = salarios.filter((_, i) => i !== index)
    onUpdate(copy)
  }

  return (
    <div className="card-panel">
      {/* BARRA SUPERIOR DA PLANILHA */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem', borderBottom: '1px solid #334155', paddingBottom: '1rem' }}>
        <div>
          <h2 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#f8fafc', margin: 0, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span>📊</span> Data Grid — Planilha de Salários (1978 – 2026)
          </h2>
          <p style={{ fontSize: '0.75rem', color: '#94a3b8', marginTop: '0.25rem' }}>
            {salarios.length} competências cadastradas com conversão monetária em tempo real
          </p>
        </div>

        {/* BOTOES DE ACAO EM LOTE */}
        <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
          <button onClick={() => onPreencherLote('MINIMO')} className="btn-secondary">
            ⚡ Salário Mínimo Lote
          </button>

          <button onClick={() => onPreencherLote('TETO')} className="btn-secondary">
            ⚡ Teto INSS Lote
          </button>

          <button onClick={onAddRow} className="btn-secondary">
            ➕ Adicionar Mês
          </button>

          <button onClick={onCarregarExemplo} className="btn-secondary">
            💡 Exemplo 1978-2026
          </button>

          <button onClick={onClear} style={{ backgroundColor: 'rgba(239, 68, 68, 0.15)', color: '#f87171', border: '1px solid rgba(248, 113, 113, 0.3)', padding: '0.5rem 0.85rem', fontSize: '0.75rem' }}>
            🗑️ Limpar
          </button>
        </div>
      </div>

      {/* PLANILHA DATA GRID */}
      <div className="spreadsheet-container">
        <table>
          <thead>
            <tr>
              <th style={{ width: '40px', textAlign: 'center' }}>#</th>
              <th style={{ width: '150px' }}>Competência</th>
              <th style={{ width: '110px', textAlign: 'center' }}>Moeda Época</th>
              <th>Valor Informado na Época</th>
              <th>Valor em Real (R$ Convertido)</th>
              <th style={{ width: '120px', textAlign: 'center' }}>Situação</th>
              <th style={{ width: '60px', textAlign: 'center' }}>Ações</th>
            </tr>
          </thead>
          <tbody>
            {salarios.map((item, index) => {
              const valorReal = converterParaReal(item.valor, item.competencia)
              return (
                <tr key={index}>
                  <td style={{ textAlign: 'center', color: '#64748b', fontFamily: 'monospace' }}>{index + 1}</td>
                  <td>
                    <input
                      type="month"
                      value={item.competencia}
                      onChange={(e) => handleFieldChange(index, 'competencia', e.target.value)}
                    />
                  </td>
                  <td style={{ textAlign: 'center' }}>
                    <span className="badge-moeda">{item.moeda}</span>
                  </td>
                  <td>
                    <input
                      type="number"
                      step="any"
                      value={item.valor}
                      onChange={(e) => handleFieldChange(index, 'valor', parseFloat(e.target.value) || 0)}
                      style={{ fontWeight: 600 }}
                    />
                  </td>
                  <td style={{ color: '#34d399', fontWeight: 700, fontFamily: 'JetBrains Mono, monospace' }}>
                    R$ {valorReal.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                  </td>
                  <td style={{ textAlign: 'center' }}>
                    <span className="badge-ok">✓ OK</span>
                  </td>
                  <td style={{ textAlign: 'center' }}>
                    <button
                      onClick={() => handleRemoveRow(index)}
                      style={{ background: 'transparent', border: 'none', color: '#f87171', fontSize: '1rem', padding: '0.2rem 0.5rem' }}
                    >
                      ✕
                    </button>
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
