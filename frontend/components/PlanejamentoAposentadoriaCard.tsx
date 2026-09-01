'use client'

import React from 'react'

export interface PlanejamentoProps {
  nomeSegurado: string
  idadeAtual: number
  tempoAtual: number
  sexo: string
  dataNascimento: string
  teses: any[]
}

export function PlanejamentoAposentadoriaCard({
  nomeSegurado,
  idadeAtual,
  tempoAtual,
  sexo,
  dataNascimento,
  teses
}: PlanejamentoProps) {
  
  const sexoUpper = sexo ? sexo.toUpperCase() : 'M'
  const isMulher = sexoUpper === 'F'
  const idadeMinimaGeral = isMulher ? 62 : 65
  const tempoMinimoGeral = isMulher ? 15 : 20

  const idadeFaltante = Math.max(0, idadeMinimaGeral - idadeAtual)
  const tempoFaltante = Math.max(0, tempoMinimoGeral - tempoAtual)

  let anoNasc = 1993
  try {
    const parts = dataNascimento.split('-')
    if (parts.length === 3) anoNasc = parseInt(parts[0])
  } catch (e) {}

  const anoAposentadoria = anoNasc + idadeMinimaGeral
  const dataEstimadaStr = `21/06/${anoAposentadoria}`

  return (
    <div className="card-panel" style={{ border: '1px solid rgba(59, 130, 246, 0.4)', backgroundColor: '#0f172a' }}>
      
      {/* CABEÇALHO DO CARD */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem', borderBottom: '1px solid #334155', paddingBottom: '0.85rem' }}>
        <div>
          <h2 style={{ fontSize: '1rem', fontWeight: 800, color: '#f8fafc', textTransform: 'uppercase', letterSpacing: '0.05em', margin: 0, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span>🎯</span> PLANEJAMENTO PREVIDENCIÁRIO: O QUE FALTA PARA APOSENTAR?
          </h2>
          <p style={{ fontSize: '0.75rem', color: '#94a3b8', marginTop: '0.25rem' }}>
            Diagnóstico do tempo restante, idade faltante e estimativa da Data Provável da Aposentadoria (DIB Futura) para {nomeSegurado}
          </p>
        </div>

        <div style={{ backgroundColor: 'rgba(59, 130, 246, 0.15)', border: '1px solid rgba(59, 130, 246, 0.4)', borderRadius: '0.75rem', padding: '0.5rem 1rem', textAlign: 'right' }}>
          <div style={{ fontSize: '0.65rem', textTransform: 'uppercase', fontWeight: 700, color: '#93c5fd' }}>PREVISÃO DA APOSENTADORIA</div>
          <div className="font-mono" style={{ fontSize: '1.2rem', fontWeight: 800, color: '#38bdf8' }}>
            {dataEstimadaStr}
          </div>
        </div>
      </div>

      {/* METRICAS FALTANTES EM CARDS HERO */}
      <div className="grid-3" style={{ marginBottom: '1.25rem' }}>
        
        {/* TEMPO DE CONTRIBUIÇÃO FALTANTE */}
        <div style={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '0.85rem', padding: '1rem' }}>
          <div style={{ fontSize: '0.7rem', color: '#94a3b8', textTransform: 'uppercase', fontWeight: 700 }}>
            ⌛ Tempo de Contribuição Faltante
          </div>
          <div className="font-mono" style={{ fontSize: '1.6rem', fontWeight: 800, color: tempoFaltante > 0 ? '#fbbf24' : '#34d399', marginTop: '0.35rem' }}>
            {tempoFaltante > 0 ? `${tempoFaltante} Anos` : 'Cumprido ✓'}
          </div>
          <div style={{ fontSize: '0.65rem', color: '#94a3b8', marginTop: '0.25rem' }}>
            Possui {tempoAtual}a de contribuição (Exige {tempoMinimoGeral}a)
          </div>
        </div>

        {/* IDADE FALTANTE */}
        <div style={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '0.85rem', padding: '1rem' }}>
          <div style={{ fontSize: '0.7rem', color: '#94a3b8', textTransform: 'uppercase', fontWeight: 700 }}>
            🎂 Idade Regulamentar Faltante
          </div>
          <div className="font-mono" style={{ fontSize: '1.6rem', fontWeight: 800, color: idadeFaltante > 0 ? '#60a5fa' : '#34d399', marginTop: '0.35rem' }}>
            {idadeFaltante > 0 ? `${idadeFaltante} Anos` : 'Atingida ✓'}
          </div>
          <div style={{ fontSize: '0.65rem', color: '#94a3b8', marginTop: '0.25rem' }}>
            Idade atual: {idadeAtual} anos (Idade mínima: {idadeMinimaGeral} anos)
          </div>
        </div>

        {/* PONTUAÇÃO FALTANTE */}
        <div style={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '0.85rem', padding: '1rem' }}>
          <div style={{ fontSize: '0.7rem', color: '#94a3b8', textTransform: 'uppercase', fontWeight: 700 }}>
            📊 Pontuação Faltante (EC 103)
          </div>
          <div className="font-mono" style={{ fontSize: '1.6rem', fontWeight: 800, color: '#f87171', marginTop: '0.35rem' }}>
            {Math.max(0, (isMulher ? 93 : 103) - (idadeAtual + tempoAtual))} Pontos
          </div>
          <div style={{ fontSize: '0.65rem', color: '#94a3b8', marginTop: '0.25rem' }}>
            Pontuação atual: {idadeAtual + tempoAtual} pts (Exige {isMulher ? 93 : 103} pts em 2026)
          </div>
        </div>

      </div>

      {/* QUADRO DE ORIENTAÇÃO AO CLIENTE */}
      <div style={{ backgroundColor: 'rgba(59, 130, 246, 0.1)', border: '1px solid rgba(59, 130, 246, 0.3)', borderRadius: '0.75rem', padding: '0.85rem 1.15rem' }}>
        <div style={{ fontSize: '0.75rem', fontWeight: 700, color: '#60a5fa', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.25rem' }}>
          💡 Orientação do Advogado para o Cliente:
        </div>
        <div style={{ fontSize: '0.8rem', color: '#e2e8f0', lineHeight: 1.4 }}>
          {tempoFaltante > 0
            ? `O segurado precisará manter contribuições contínuas ao INSS por mais ${tempoFaltante} anos para atingir a carência mínima de ${tempoMinimoGeral} anos até o alcance da idade de ${idadeMinimaGeral} anos em ${dataEstimadaStr}.`
            : `Requisito de tempo cumprido! Aguardando o alcance da idade mínima de ${idadeMinimaGeral} anos em ${dataEstimadaStr}.`}
        </div>
      </div>

    </div>
  )
}
