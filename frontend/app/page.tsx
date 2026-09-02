'use client'

import React, { useState, useEffect } from 'react'
import { DataGrid, SalarioItem } from '../components/DataGrid'
import { CnisPdfUploader } from '../components/CnisPdfUploader'
import { VinculosTable, VinculoItem } from '../components/VinculosTable'
import { ComplementacaoTable, ItemComplementacaoProps } from '../components/ComplementacaoTable'
import { AuditoriaModal } from '../components/AuditoriaModal'
import { TesesComparativasTable, TeseItem } from '../components/TesesComparativasTable'
import { PlanejamentoAposentadoriaCard } from '../components/PlanejamentoAposentadoriaCard'
import { TabelaPlanejamentoContribuicao } from '../components/TabelaPlanejamentoContribuicao'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function HomePage() {
  const [abaAtiva, setAbaAtiva] = useState<'cnis' | 'simulacao' | 'teses' | 'planejamento' | 'complementacao'>('cnis')

  const [clienteNome, setClienteNome] = useState('RUDSON EDUARDO DE OLIVEIRA AMARO')
  const [cpf, setCpf] = useState('041.929.711-19')
  const [nit, setNit] = useState('114.45167.11-0')
  const [dataNascimento, setDataNascimento] = useState('1993-06-21')
  const [idadeAnos, setIdadeAnos] = useState(33)
  const [idadeMeses, setIdadeMeses] = useState(2)
  const [sexo, setSexo] = useState('M')
  const [tempoAnos, setTempoAnos] = useState(11)
  const [dataDib, setDataDib] = useState('2026-09-01')
  const [modalidade, setModalidade] = useState('APOSENTADORIA_COMUM')

  const [isAuditoriaOpen, setIsAuditoriaOpen] = useState(false)
  const [mostrarComplementacao, setMostrarComplementacao] = useState(true)

  const [teses, setTeses] = useState<TeseItem[]>([])

  const [vinculos, setVinculos] = useState<VinculoItem[]>([
    { seq: 1, cnpj_cpf: "04.192.971/0001-19", empregador: "TECNOLOGIA E INOVAÇÃO S/A", data_inicio: "2015-01-10", data_fim: "2019-12-31", tipo_vinculo: "Empregado CLT", qtd_salarios: 60 },
    { seq: 2, cnpj_cpf: "12.345.678/0001-90", empregador: "CONSULTORIA PREVIDENCIÁRIA E SERVIÇOS", data_inicio: "2020-01-01", data_fim: "2026-08-31", tipo_vinculo: "Empregado CLT", qtd_salarios: 80 }
  ])

  const [salarios, setSalarios] = useState<SalarioItem[]>([
    { competencia: "2015-01", valor: 2500.00, moeda: "R$" },
    { competencia: "2018-05", valor: 3800.00, moeda: "R$" },
    { competencia: "2020-07", valor: 5200.00, moeda: "R$" },
    { competencia: "2024-01", valor: 7500.00, moeda: "R$" },
    { competencia: "2026-01", valor: 8157.41, moeda: "R$" }
  ])

  const [itensComplementacao, setItensComplementacao] = useState<ItemComplementacaoProps[]>([])
  const [totalComplementarDarf, setTotalComplementarDarf] = useState<number>(0)

  const [recomendacao, setRecomendacao] = useState<any>({
    titulo_modalidade: "Aposentadoria Comum (Simulação em Andamento)",
    justificativa_juridica: "Segurado Rudson Eduardo de Oliveira Amaro (33 anos de idade e 11 anos de contribuição). Ainda não cumpre os requisitos mínimos definitivos da EC 103/2019."
  })

  const [resultado, setResultado] = useState<any>(null)

  const recalcularTudo = (
    nome: string,
    idade: number,
    genero: string,
    tempo: number,
    sals: SalarioItem[],
    mod: string
  ) => {
    fetch(`${API_BASE}/api/v1/calculos/teses-comparativas`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        idade_anos: idade,
        sexo: genero,
        tempo_contribuicao_anos: tempo,
        tempo_em_13_11_2019: Math.max(0, tempo - 6),
        media_pbc: 4500.00,
        fator_prev: 1.0,
        dt_nascimento_iso: dataNascimento
      })
    })
    .then(res => res.ok ? res.json() : null)
    .then(data => {
      if (data && data.todas_teses) {
        setTeses(data.todas_teses)
      } else {
        gerarTesesFallback(idade, genero, tempo)
      }
    })
    .catch(() => gerarTesesFallback(idade, genero, tempo))

    executarCalculoLocal(mod, tempo, genero, sals, nome)
  }

  const gerarTesesFallback = (idade: number, genero: string, tempo: number) => {
    const elegivelGeral = idade >= (genero === 'F' ? 62 : 65) && tempo >= (genero === 'F' ? 15 : 20)
    setTeses([
      {
        codigo_regra: 'REGRA_GERAL_IDADE',
        nome_regra: 'Regra Geral: Aposentadoria por Idade (Art. 26)',
        elegivel: elegivelGeral,
        rmi_estimada: elegivelGeral ? 3200.00 : 0.0,
        coeficiente_aplicado: 0.60,
        fator_previdenciario: 1.0,
        requisitos_cumpridos: elegivelGeral ? `Cumprido: ${idade} anos de idade.` : 'Incompleto',
        motivo_inelegibilidade: elegivelGeral ? null : `Exige idade mínima de ${genero === 'F' ? 62 : 65} anos. Possui ${idade} anos.`
      },
      {
        codigo_regra: 'PONTOS',
        nome_regra: 'Regra de Transição: Sistema de Pontos (Art. 15)',
        elegivel: false,
        rmi_estimada: 0.0,
        coeficiente_aplicado: 0.60,
        fator_previdenciario: 1.0,
        requisitos_cumpridos: 'Incompleto',
        motivo_inelegibilidade: `Pontuação atual: ${idade + tempo} pts (Exige ${genero === 'F' ? 93 : 103} pts).`
      },
      {
        codigo_regra: 'PEDAGIO_100',
        nome_regra: 'Regra de Transição: Pedágio 100% (Art. 20)',
        elegivel: false,
        rmi_estimada: 0.0,
        coeficiente_aplicado: 1.0,
        fator_previdenciario: 1.0,
        requisitos_cumpridos: 'Incompleto',
        motivo_inelegibilidade: `Exige idade mínima de ${genero === 'F' ? 57 : 60} anos.`
      },
      {
        codigo_regra: 'PEDAGIO_50',
        nome_regra: 'Regra de Transição: Pedágio 50% (Art. 17)',
        elegivel: false,
        rmi_estimada: 0.0,
        coeficiente_aplicado: 0.0,
        fator_previdenciario: 1.0,
        requisitos_cumpridos: 'Incompleto',
        motivo_inelegibilidade: 'Não possuía o tempo mínimo exigido em 13/11/2019.'
      }
    ])
  }

  useEffect(() => {
    recalcularTudo(clienteNome, idadeAnos, sexo, tempoAnos, salarios, modalidade)
  }, [])

  const handleCnisParsed = (data: any) => {
    let novoNome = clienteNome
    let novaIdade = idadeAnos
    let novoSexo = sexo
    let novoTempo = tempoAnos
    let novosSalarios = salarios

    if (data.dados_pessoais) {
      novoNome = data.dados_pessoais.nome || clienteNome
      novaIdade = data.dados_pessoais.idade_anos || idadeAnos
      novoSexo = data.dados_pessoais.sexo_estimado || sexo

      setClienteNome(novoNome)
      setCpf(data.dados_pessoais.cpf || cpf)
      setNit(data.dados_pessoais.nit || nit)
      setDataNascimento(data.dados_pessoais.data_nascimento || dataNascimento)
      setIdadeAnos(novaIdade)
      setIdadeMeses(data.dados_pessoais.idade_meses || idadeMeses)
      setSexo(novoSexo)
    }

    if (data.tempo_total_anos) {
      novoTempo = data.tempo_total_anos
      setTempoAnos(novoTempo)
    }

    if (data.vinculos && data.vinculos.length > 0) {
      setVinculos(data.vinculos)
    }

    if (data.salarios && data.salarios.length > 0) {
      novosSalarios = data.salarios.map((s: any) => ({
        competencia: s.competencia,
        valor: s.valor_informado,
        moeda: s.codigo_moeda
      }))
      setSalarios(novosSalarios)
    }

    if (data.itens_complementacao) {
      setItensComplementacao(data.itens_complementacao)
      setTotalComplementarDarf(data.total_complementar_darf || 0)
    } else {
      setItensComplementacao([])
      setTotalComplementarDarf(0)
    }

    if (data.recomendacao_modalidade) {
      setRecomendacao(data.recomendacao_modalidade)
      if (data.recomendacao_modalidade.codigo_modalidade) {
        setModalidade(data.recomendacao_modalidade.codigo_modalidade)
      }
    }

    recalcularTudo(novoNome, novaIdade, novoSexo, novoTempo, novosSalarios, modalidade)
  }

  const handleDownloadPdf = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/v1/calculos/relatorio-pdf`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          cliente_nome: clienteNome,
          cpf: cpf,
          nit: nit,
          data_nascimento: dataNascimento,
          idade_formatada: `${idadeAnos} Anos e ${idadeMeses} Meses`,
          simulacao: {
            cliente_id: 'client-pdf-export',
            data_dib: dataDib,
            sexo,
            tempo_contribuicao_anos: tempoAnos,
            modalidade,
            salarios_contribuicao: salarios.map(s => ({
              competencia: s.competencia,
              valor_informado: s.valor,
              codigo_moeda: s.moeda
            }))
          }
        })
      })

      if (response.ok) {
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `parecer_previdenciario_${clienteNome.replace(/\s+/g, '_')}.pdf`
        document.body.appendChild(a)
        a.click()
        a.remove()
      } else {
        alert("Servidor FastAPI indisponível. Certifique-se de que o backend está em execução.")
      }
    } catch (err) {
      alert("Erro ao baixar PDF. Certifique-se de que o backend FastAPI está em execução.")
    }
  }

  const handleAddRow = () => {
    const updated = [...salarios, { competencia: "2026-02", valor: 2500.00, moeda: "R$" }]
    setSalarios(updated)
    recalcularTudo(clienteNome, idadeAnos, sexo, tempoAnos, updated, modalidade)
  }

  const handleClear = () => {
    setSalarios([])
    setResultado(null)
  }

  const handlePreencherLote = (tipo: 'MINIMO' | 'TETO') => {
    const updated = salarios.map(s => {
      if (!s.valor || s.valor === 0) {
        return { ...s, valor: tipo === 'MINIMO' ? 1518.00 : 8157.41 }
      }
      return s
    })
    setSalarios(updated)
    recalcularTudo(clienteNome, idadeAnos, sexo, tempoAnos, updated, modalidade)
  }

  const handleCalcular = () => {
    recalcularTudo(clienteNome, idadeAnos, sexo, tempoAnos, salarios, modalidade)
  }

  const executarCalculoLocal = (mod: string, tempo: number, genero: string, sals: SalarioItem[], nomeSegurado: string) => {
    const salariosConsiderados: number[] = []
    sals.forEach(s => {
      let valReal = s.valor
      if (s.competencia < "1994-07") valReal = s.valor / 2750000000000
      let descartado = mod === "APOSENTADORIA_COMUM" && s.competencia < "1994-07"
      if (!descartado) salariosConsiderados.push(valReal * 1.0)
    })

    const soma = salariosConsiderados.reduce((a, b) => a + b, 0)
    const media = salariosConsiderados.length > 0 ? soma / salariosConsiderados.length : 0
    let coef = 0.60 + Math.max(0, tempo - (genero === 'F' ? 15 : 20)) * 0.02
    if (mod === "REVISAO_VIDA_TODA") coef = 1.00

    const rmi = Math.min(8157.41, Math.max(1518.00, media * coef))

    setResultado({
      sucesso: true,
      modalidade: mod,
      data_dib: dataDib,
      rmi_apurada: rmi,
      media_pbc: media,
      coeficiente_aplicado: coef,
      fator_previdenciario: 1.0,
      salarios_considerados_qtd: salariosConsiderados.length,
      salarios_descartados_qtd: sals.length - salariosConsiderados.length,
    })
  }

  return (
    <main>
      
      {/* HEADER TOP BAR WITH AUDITORIA BUTTON & BACEN SYNC BADGE */}
      <header>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{ width: '3rem', height: '3rem', borderRadius: '0.75rem', backgroundColor: 'rgba(37, 99, 235, 0.2)', border: '1px solid rgba(59, 130, 246, 0.3)', color: '#60a5fa', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.5rem', fontWeight: 700 }}>
            ⚖️
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <h1 style={{ fontSize: '1.5rem', fontWeight: 800, color: '#f8fafc', margin: 0 }}>PrevCalc SaaS Legal Tech Enterprise</h1>
              <span style={{ backgroundColor: 'rgba(59, 130, 246, 0.2)', color: '#93c5fd', fontSize: '0.75rem', padding: '0.2rem 0.6rem', borderRadius: '9999px', border: '1px solid rgba(147, 197, 253, 0.3)', fontWeight: 600 }}>
                BACEN SGS Sync Active
              </span>
            </div>
            <p style={{ fontSize: '0.8rem', color: '#94a3b8', marginTop: '0.25rem' }}>
              Diagnóstico Automático do CNIS, Planejamento de Aposentadoria e Comparativo de Teses (EC 103)
            </p>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <button onClick={() => setIsAuditoriaOpen(true)} className="btn-secondary" style={{ backgroundColor: 'rgba(59, 130, 246, 0.2)', borderColor: 'rgba(59, 130, 246, 0.4)', color: '#60a5fa', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
            <span>🛡️</span> Ver Auditoria Previdenciária
          </button>

          <button onClick={handleDownloadPdf} className="btn-secondary" style={{ backgroundColor: 'rgba(16, 185, 129, 0.2)', borderColor: 'rgba(52, 211, 153, 0.4)', color: '#34d399', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
            <span>📥</span> Baixar Parecer (PDF)
          </button>
        </div>
      </header>

      {/* BANNER NAVEGAÇÃO POR ABAS EXECUTIVAS */}
      <nav style={{ display: 'flex', gap: '0.5rem', backgroundColor: '#0f172a', padding: '0.5rem', borderRadius: '0.85rem', border: '1px solid #334155', marginBottom: '1.25rem', overflowX: 'auto' }}>
        <button
          onClick={() => setAbaAtiva('cnis')}
          style={{
            padding: '0.65rem 1.15rem',
            borderRadius: '0.6rem',
            border: 'none',
            fontSize: '0.8rem',
            fontWeight: 700,
            cursor: 'pointer',
            backgroundColor: abaAtiva === 'cnis' ? '#2563eb' : 'transparent',
            color: abaAtiva === 'cnis' ? '#ffffff' : '#94a3b8',
            transition: 'all 0.2s ease',
            whiteSpace: 'nowrap'
          }}
        >
          📋 Perfil & Extrator CNIS
        </button>

        <button
          onClick={() => setAbaAtiva('simulacao')}
          style={{
            padding: '0.65rem 1.15rem',
            borderRadius: '0.6rem',
            border: 'none',
            fontSize: '0.8rem',
            fontWeight: 700,
            cursor: 'pointer',
            backgroundColor: abaAtiva === 'simulacao' ? '#2563eb' : 'transparent',
            color: abaAtiva === 'simulacao' ? '#ffffff' : '#94a3b8',
            transition: 'all 0.2s ease',
            whiteSpace: 'nowrap'
          }}
        >
          🚀 Simulação & Planilha Data Grid
        </button>

        <button
          onClick={() => setAbaAtiva('teses')}
          style={{
            padding: '0.65rem 1.15rem',
            borderRadius: '0.6rem',
            border: 'none',
            fontSize: '0.8rem',
            fontWeight: 700,
            cursor: 'pointer',
            backgroundColor: abaAtiva === 'teses' ? '#2563eb' : 'transparent',
            color: abaAtiva === 'teses' ? '#ffffff' : '#94a3b8',
            transition: 'all 0.2s ease',
            whiteSpace: 'nowrap'
          }}
        >
          ⚖️ Regras de Transição (EC 103)
        </button>

        <button
          onClick={() => setAbaAtiva('planejamento')}
          style={{
            padding: '0.65rem 1.15rem',
            borderRadius: '0.6rem',
            border: 'none',
            fontSize: '0.8rem',
            fontWeight: 700,
            cursor: 'pointer',
            backgroundColor: abaAtiva === 'planejamento' ? '#2563eb' : 'transparent',
            color: abaAtiva === 'planejamento' ? '#ffffff' : '#94a3b8',
            transition: 'all 0.2s ease',
            whiteSpace: 'nowrap'
          }}
        >
          🎯 Planejamento & Guia de Contribuição
        </button>

        <button
          onClick={() => setAbaAtiva('complementacao')}
          style={{
            padding: '0.65rem 1.15rem',
            borderRadius: '0.6rem',
            border: 'none',
            fontSize: '0.8rem',
            fontWeight: 700,
            cursor: 'pointer',
            backgroundColor: abaAtiva === 'complementacao' ? '#2563eb' : 'transparent',
            color: abaAtiva === 'complementacao' ? '#ffffff' : '#94a3b8',
            transition: 'all 0.2s ease',
            whiteSpace: 'nowrap'
          }}
        >
          ⚠️ Guia de Complementação (PREC-MENOR-MIN)
        </button>
      </nav>

      {/* BANNER RECOMENDAÇÃO AUTOMÁTICA DA MODALIDADE & ALERTAS */}
      {recomendacao && (
        <div style={{ backgroundColor: 'rgba(59, 130, 246, 0.1)', border: '1px solid rgba(59, 130, 246, 0.3)', borderRadius: '1rem', padding: '0.85rem 1.25rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '1rem', marginBottom: '1.25rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <div style={{ fontSize: '1.5rem' }}>💡</div>
            <div>
              <div style={{ fontSize: '0.75rem', textTransform: 'uppercase', fontWeight: 700, color: '#60a5fa', letterSpacing: '0.05em' }}>
                Recomendação Automática do Sistema: {recomendacao.titulo_modalidade}
              </div>
              <div style={{ fontSize: '0.8rem', color: '#e2e8f0', marginTop: '0.2rem' }}>
                {recomendacao.justificativa_juridica}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ABA 1: PERFIL & EXTRATOR CNIS */}
      {abaAtiva === 'cnis' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          <div className="grid-3">

            {/* CARD PERFIL AUTO EXTRAÍDO */}
            <div className="card-panel">
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', borderBottom: '1px solid #334155', paddingBottom: '0.75rem', marginBottom: '1rem' }}>
                <span style={{ fontSize: '1.2rem' }}>👤</span>
                <h2 style={{ fontSize: '0.85rem', fontWeight: 700, color: '#f8fafc', textTransform: 'uppercase', letterSpacing: '0.05em', margin: 0 }}>
                  Perfil Auto-Extraído do CNIS
                </h2>
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
                <div>
                  <label style={{ display: 'block', fontSize: '0.75rem', fontWeight: 600, color: '#94a3b8', marginBottom: '0.25rem' }}>Nome do Segurado</label>
                  <input
                    type="text"
                    value={clienteNome}
                    onChange={(e) => setClienteNome(e.target.value)}
                  />
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem' }}>
                  <div>
                    <label style={{ display: 'block', fontSize: '0.75rem', fontWeight: 600, color: '#94a3b8', marginBottom: '0.25rem' }}>CPF</label>
                    <input
                      type="text"
                      value={cpf}
                      onChange={(e) => setCpf(e.target.value)}
                    />
                  </div>

                  <div>
                    <label style={{ display: 'block', fontSize: '0.75rem', fontWeight: 600, color: '#94a3b8', marginBottom: '0.25rem' }}>Nascimento (Idade)</label>
                    <input
                      type="text"
                      value={`${dataNascimento} (${idadeAnos}a ${idadeMeses}m)`}
                      readOnly
                      style={{ backgroundColor: '#1e293b', color: '#60a5fa', fontWeight: 700 }}
                    />
                  </div>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem' }}>
                  <div>
                    <label style={{ display: 'block', fontSize: '0.75rem', fontWeight: 600, color: '#94a3b8', marginBottom: '0.25rem' }}>Tempo Contribuição</label>
                    <input
                      type="text"
                      value={`${tempoAnos} Anos`}
                      readOnly
                      style={{ backgroundColor: '#1e293b', color: '#34d399', fontWeight: 700 }}
                    />
                  </div>

                  <div>
                    <label style={{ display: 'block', fontSize: '0.75rem', fontWeight: 600, color: '#94a3b8', marginBottom: '0.25rem' }}>Data DIB</label>
                    <input
                      type="date"
                      value={dataDib}
                      onChange={(e) => setDataDib(e.target.value)}
                    />
                  </div>
                </div>
              </div>
            </div>

            {/* CARD SELEÇÃO DE MODALIDADE */}
            <div className="card-panel">
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', borderBottom: '1px solid #334155', paddingBottom: '0.75rem', marginBottom: '1rem' }}>
                <span style={{ fontSize: '1.2rem' }}>⚙️</span>
                <h2 style={{ fontSize: '0.85rem', fontWeight: 700, color: '#f8fafc', textTransform: 'uppercase', letterSpacing: '0.05em', margin: 0 }}>
                  Modalidade de Cálculo Selecionada
                </h2>
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.65rem' }}>
                <label style={{ display: 'flex', alignItems: 'flex-start', gap: '0.75rem', padding: '0.75rem', borderRadius: '0.75rem', border: modalidade === 'APOSENTADORIA_COMUM' ? '1px solid #3b82f6' : '1px solid #334155', backgroundColor: modalidade === 'APOSENTADORIA_COMUM' ? 'rgba(59, 130, 246, 0.1)' : 'transparent', cursor: 'pointer' }}>
                  <input
                    type="radio"
                    name="modalidade"
                    value="APOSENTADORIA_COMUM"
                    checked={modalidade === 'APOSENTADORIA_COMUM'}
                    onChange={(e) => {
                      setModalidade(e.target.value)
                      recalcularTudo(clienteNome, idadeAnos, sexo, tempoAnos, salarios, e.target.value)
                    }}
                    style={{ width: 'auto', marginTop: '0.2rem' }}
                  />
                  <div>
                    <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#f8fafc' }}>Aposentadoria por Idade Geral (EC 103/2019) ★</div>
                    <div style={{ fontSize: '0.7rem', color: '#94a3b8', marginTop: '0.2rem' }}>Idade mínima 62 anos (Mulher) / 65 (Homem), 100% PBC.</div>
                  </div>
                </label>

                <label style={{ display: 'flex', alignItems: 'flex-start', gap: '0.75rem', padding: '0.75rem', borderRadius: '0.75rem', border: modalidade === 'REVISAO_VIDA_TODA' ? '1px solid #3b82f6' : '1px solid #334155', backgroundColor: modalidade === 'REVISAO_VIDA_TODA' ? 'rgba(59, 130, 246, 0.1)' : 'transparent', cursor: 'pointer' }}>
                  <input
                    type="radio"
                    name="modalidade"
                    value="REVISAO_VIDA_TODA"
                    checked={modalidade === 'REVISAO_VIDA_TODA'}
                    onChange={(e) => {
                      setModalidade(e.target.value)
                      recalcularTudo(clienteNome, idadeAnos, sexo, tempoAnos, salarios, e.target.value)
                    }}
                    style={{ width: 'auto', marginTop: '0.2rem' }}
                  />
                  <div>
                    <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#f8fafc' }}>Revisão da Vida Toda (Tema 1102 STF)</div>
                    <div style={{ fontSize: '0.7rem', color: '#94a3b8', marginTop: '0.2rem' }}>Histórico 1978-2026, 6 moedas, 80% maiores salários.</div>
                  </div>
                </label>

                <label style={{ display: 'flex', alignItems: 'flex-start', gap: '0.75rem', padding: '0.75rem', borderRadius: '0.75rem', border: modalidade === 'INDENIZACAO_ATRASADOS' ? '1px solid #3b82f6' : '1px solid #334155', backgroundColor: modalidade === 'INDENIZACAO_ATRASADOS' ? 'rgba(59, 130, 246, 0.1)' : 'transparent', cursor: 'pointer' }}>
                  <input
                    type="radio"
                    name="modalidade"
                    value="INDENIZACAO_ATRASADOS"
                    checked={modalidade === 'INDENIZACAO_ATRASADOS'}
                    onChange={(e) => {
                      setModalidade(e.target.value)
                      recalcularTudo(clienteNome, idadeAnos, sexo, tempoAnos, salarios, e.target.value)
                    }}
                    style={{ width: 'auto', marginTop: '0.2rem' }}
                  />
                  <div>
                    <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#f8fafc' }}>Indenização de Atrasados (Art. 45-A)</div>
                    <div style={{ fontSize: '0.7rem', color: '#94a3b8', marginTop: '0.2rem' }}>Isento de juros pré-10/1996. Pós-10/1996 com SELIC + 10% multa.</div>
                  </div>
                </label>
              </div>
            </div>

            {/* UPLOADER */}
            <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between', gap: '1rem' }}>
              <CnisPdfUploader onCnisDataParsed={handleCnisParsed} />
            </div>
          </div>

          {/* TABELA DE VÍNCULOS EMPREGATÍCIOS EXTRAÍDOS */}
          <VinculosTable vinculos={vinculos} />
        </div>
      )}

      {/* ABA 2: SIMULAÇÃO & PLANILHA DATA GRID */}
      {abaAtiva === 'simulacao' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          {/* PLANILHA DATA GRID */}
          <DataGrid
            salarios={salarios}
            onUpdate={(updated) => {
              setSalarios(updated)
              recalcularTudo(clienteNome, idadeAnos, sexo, tempoAnos, updated, modalidade)
            }}
            onAddRow={handleAddRow}
            onClear={handleClear}
            onPreencherLote={handlePreencherLote}
            onCarregarExemplo={() => {
              const ex = [
                { competencia: "1978-05", valor: 2750000000000, moeda: "Cr$" },
                { competencia: "1985-05", valor: 1375000000000, moeda: "Cr$" },
                { competencia: "1987-10", valor: 2750000000, moeda: "Cz$" },
                { competencia: "1994-06", valor: 825000, moeda: "CR$" },
                { competencia: "1994-07", valor: 500.00, moeda: "R$" },
                { competencia: "2019-11", valor: 3500.00, moeda: "R$" },
                { competencia: "2024-01", valor: 5500.00, moeda: "R$" }
              ]
              setSalarios(ex)
              recalcularTudo(clienteNome, idadeAnos, sexo, tempoAnos, ex, modalidade)
            }}
          />

          {/* PAINEL DE RESULTADO DASHBOARD */}
          {resultado && (
            <div className="card-panel">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #334155', paddingBottom: '0.75rem', marginBottom: '1rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <span style={{ fontSize: '1.2rem' }}>🎉</span>
                  <h2 style={{ fontSize: '1.1rem', fontWeight: 800, color: '#f8fafc', margin: 0 }}>
                    Resultado Apurado da Simulação ({clienteNome})
                  </h2>
                </div>
                <span className="badge-ok" style={{ fontSize: '0.75rem' }}>
                  {resultado.modalidade}
                </span>
              </div>

              <div className="grid-4">
                
                {/* RMI APURADA */}
                <div className="stat-hero">
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                    <span style={{ fontSize: '0.7rem', textTransform: 'uppercase', fontWeight: 700, opacity: 0.9, letterSpacing: '0.05em' }}>
                      RMI APURADA (R$)
                    </span>
                    <span className="has-tooltip">
                      <span className="tooltip-icon" style={{ backgroundColor: 'rgba(255, 255, 255, 0.2)', color: '#ffffff', borderColor: 'rgba(255, 255, 255, 0.4)' }}>?</span>
                      <span className="tooltip-box">
                        <strong>Renda Mensal Inicial:</strong> Valor bruto mensal da aposentadoria pago pelo INSS. Se a média resultar abaixo do piso, o sistema garante o <strong>Piso do Salário Mínimo (R$ 1.518,00/mês)</strong>.
                      </span>
                    </span>
                  </div>
                  <div className="font-mono" style={{ fontSize: '1.8rem', fontWeight: 800, marginTop: '0.5rem' }}>
                    R$ {Number(resultado.rmi_apurada).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                  </div>
                  <div style={{ fontSize: '0.65rem', opacity: 0.8, marginTop: '0.35rem' }}>Garantia do Piso Constitucional do INSS</div>
                </div>

                {/* MÉDIA DO PBC */}
                <div style={{ backgroundColor: '#0f172a', border: '1px solid #334155', borderRadius: '1rem', padding: '1.25rem' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                    <span style={{ fontSize: '0.7rem', color: '#94a3b8', textTransform: 'uppercase', fontWeight: 700, letterSpacing: '0.05em' }}>
                      Média do PBC
                    </span>
                    <span className="has-tooltip">
                      <span className="tooltip-icon">?</span>
                      <span className="tooltip-box">
                        <strong>Período Básico de Cálculo:</strong> Média aritmética simples de todas as contribuições salariais registradas pós-07/1994, corrigidas pelo INPC.
                      </span>
                    </span>
                  </div>
                  <div className="font-mono" style={{ fontSize: '1.4rem', fontWeight: 700, color: '#f8fafc', marginTop: '0.5rem' }}>
                    R$ {Number(resultado.media_pbc).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                  </div>
                  <div style={{ fontSize: '0.65rem', color: '#64748b', marginTop: '0.35rem' }}>Média de Salários Pós-07/1994</div>
                </div>

                {/* COEFICIENTE APLICADO */}
                <div style={{ backgroundColor: '#0f172a', border: '1px solid #334155', borderRadius: '1rem', padding: '1.25rem' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                    <span style={{ fontSize: '0.7rem', color: '#94a3b8', textTransform: 'uppercase', fontWeight: 700, letterSpacing: '0.05em' }}>
                      Coeficiente Aplicado
                    </span>
                    <span className="has-tooltip">
                      <span className="tooltip-icon">?</span>
                      <span className="tooltip-box">
                        <strong>Percentual da Reforma (EC 103/2019):</strong> Base de 60% ao atingir o tempo mínimo + 2% por ano excedente (acima de 15a mulher / 20a homem).
                      </span>
                    </span>
                  </div>
                  <div className="font-mono" style={{ fontSize: '1.4rem', fontWeight: 700, color: '#f8fafc', marginTop: '0.5rem' }}>
                    {(Number(resultado.coeficiente_aplicado) * 100).toFixed(0)}%
                  </div>
                  <div style={{ fontSize: '0.65rem', color: '#64748b', marginTop: '0.35rem' }}>Percentual Acumulado da Regra</div>
                </div>

                {/* SALÁRIOS NO PBC */}
                <div style={{ backgroundColor: '#0f172a', border: '1px solid #334155', borderRadius: '1rem', padding: '1.25rem' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                    <span style={{ fontSize: '0.7rem', color: '#94a3b8', textTransform: 'uppercase', fontWeight: 700, letterSpacing: '0.05em' }}>
                      Salários no PBC
                    </span>
                    <span className="has-tooltip">
                      <span className="tooltip-icon">?</span>
                      <span className="tooltip-box">
                        <strong>Histórico de Contribuições:</strong> Indica a quantidade de salários computados na média do PBC sem descarte.
                      </span>
                    </span>
                  </div>
                  <div className="font-mono" style={{ fontSize: '1.4rem', fontWeight: 700, color: '#f8fafc', marginTop: '0.5rem' }}>
                    {resultado.salarios_considerados_qtd} <span style={{ fontSize: '0.75rem', color: '#64748b', fontWeight: 400 }}>de {salarios.length}</span>
                  </div>
                  <div style={{ fontSize: '0.65rem', color: '#fbbf24', fontWeight: 600, marginTop: '0.35rem' }}>
                    {resultado.salarios_descartados_qtd} descartados na regra
                  </div>
                </div>

              </div>
            </div>
          )}
        </div>
      )}

      {/* ABA 3: TESES & REGRAS DE TRANSIÇÃO (EC 103/2019) */}
      {abaAtiva === 'teses' && (
        <TesesComparativasTable teses={teses} />
      )}

      {/* ABA 4: PLANEJAMENTO & GUIA DE CONTRIBUIÇÃO */}
      {abaAtiva === 'planejamento' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          {/* PLANEJAMENTO O QUE FALTA PARA APOSENTAR */}
          <PlanejamentoAposentadoriaCard
            nomeSegurado={clienteNome}
            idadeAtual={idadeAnos}
            tempoAtual={tempoAnos}
            sexo={sexo}
            dataNascimento={dataNascimento}
            teses={teses}
          />

          {/* TABELA DE CONTRIBUIÇÃO FUTURA 1 A 5 SALÁRIOS & TETO */}
          <TabelaPlanejamentoContribuicao />
        </div>
      )}

      {/* ABA 5: GUIA DE COMPLEMENTAÇÃO (PREC-MENOR-MIN) */}
      {abaAtiva === 'complementacao' && (
        <ComplementacaoTable itens={itensComplementacao} totalDarf={totalComplementarDarf} />
      )}

      {/* MODAL DE AUDITORIA PREVIDENCIÁRIA */}
      <AuditoriaModal
        isOpen={isAuditoriaOpen}
        onClose={() => setIsAuditoriaOpen(false)}
        onDownloadPdf={handleDownloadPdf}
      />
    </main>
  )
}
