'use client'

import React from 'react'

interface JobProgressBarProps {
  percent: number
  mensagem: string
  status: string
}

export function JobProgressBar({ percent, mensagem, status }: JobProgressBarProps) {
  if (percent === 0 || status === 'COMPLETED') return null

  return (
    <div style={{ backgroundColor: '#0f172a', border: '1px solid #334155', borderRadius: '0.85rem', padding: '0.85rem 1.25rem', margin: '0.75rem 0' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.4rem' }}>
        <div style={{ fontSize: '0.75rem', fontWeight: 600, color: '#60a5fa', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
          <span>⏳</span> {mensagem}
        </div>
        <div className="font-mono" style={{ fontSize: '0.75rem', fontWeight: 700, color: '#34d399' }}>
          {percent}%
        </div>
      </div>

      <div style={{ width: '100%', height: '8px', backgroundColor: '#1e293b', borderRadius: '9999px', overflow: 'hidden', border: '1px solid #334155' }}>
        <div
          style={{
            width: `${percent}%`,
            height: '100%',
            backgroundColor: status === 'FAILED' ? '#f87171' : '#3b82f6',
            borderRadius: '9999px',
            transition: 'width 0.3s ease'
          }}
        />
      </div>
    </div>
  )
}
