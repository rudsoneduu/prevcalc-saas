"""
Script de Geração do PDF da Documentação Master do Sistema PrevCalc SaaS Legal Tech
Converte o Relatório Geral do Sistema em um PDF executivo de alto padrão visual.
"""

import os
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

class MasterNumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))

        self.drawString(36, 20, "PrevCalc SaaS Legal Tech • Relatório de Arquitetura e Manual do Sistema")
        page_text = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(576, 20, page_text)

        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(36, 30, 576, 30)

        self.restoreState()


def gerar_pdf_master(output_filepath: str):
    doc = SimpleDocTemplate(
        output_filepath,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=42
    )

    styles = getSampleStyleSheet()

    titulo_style = ParagraphStyle(
        'TituloRelatorio',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=colors.HexColor('#ffffff'),
        alignment=0
    )

    subtitulo_style = ParagraphStyle(
        'SubTituloRelatorio',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#93c5fd'),
        alignment=0
    )

    secao_style = ParagraphStyle(
        'SecaoHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=12,
        spaceAfter=6
    )

    normal_style = ParagraphStyle(
        'NormalBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor('#334155')
    )

    bullet_style = ParagraphStyle(
        'BulletBody',
        parent=normal_style,
        leftIndent=12,
        spaceAfter=3
    )

    elements = []

    # 1. HEADER BANNER
    header_table_data = [
        [
            Paragraph("<b>RELATÓRIO MASTER E MANUAL DO SISTEMA PREVCALC</b>", titulo_style),
            Paragraph("<font color='#38bdf8'><b>PREVCALC LEGAL TECH</b></font>", ParagraphStyle('HBadge', parent=subtitulo_style, alignment=2, fontName='Helvetica-Bold', fontSize=9))
        ],
        [
            Paragraph("Documentação Técnica da Arquitetura, Motores de Cálculo, CNIS Parser e Auditoria", subtitulo_style),
            Paragraph("Versão 3.0 • 2026", ParagraphStyle('HDate', parent=subtitulo_style, alignment=2, textColor=colors.HexColor('#cbd5e1')))
        ]
    ]
    header_table = Table(header_table_data, colWidths=[380, 160])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#0f172a')),
        ('PADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(header_table)
    elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#2563eb'), spaceBefore=0, spaceAfter=12))

    # 2. SEÇÃO 1: VISÃO GERAL
    elements.append(Paragraph("1. VISÃO GERAL E ARQUITETURA DO SISTEMA", secao_style))
    elements.append(Paragraph("O <b>PrevCalc SaaS Legal Tech</b> é uma plataforma de engenharia de software previdenciária desenvolvida para advogados, peritos e consultores. O sistema combina uma engine matemática de alta precisão em Python (FastAPI) a um dashboard web interativo em React/Next.js 14, permitindo a automação do diagnóstico do CNIS, recomendação de regras de aposentadoria e geração de laudos jurídicos.", normal_style))
    elements.append(Spacer(1, 8))

    # 3. SEÇÃO 2: MÓDULOS DO SISTEMA
    elements.append(Paragraph("2. PRINCIPAIS MÓDULOS E FUNCIONALIDADES", secao_style))

    modulos = [
        ("<b>2.1. Módulo de Transição Monetária (1978 – 2026):</b>", "Suporte a 6 moedas históricas (Cr$, Cz$, NCz$, Cr$, CR$, R$). Fator divisor cumulativo de 2,75 Trilhões para salários de 1978 e aplicação da URV de 30/06/1994 (CR$ 2.750,00). Precisão via decimal.Decimal(28)."),
        ("<b>2.2. Engine de Extração Inteligente do CNIS PDF:</b>", "Parser via pypdf que extrai Nome, CPF, NIT, Data de Nascimento, Idade (Anos e Meses) e Mãe. Filtro de CNPJ que isola estabelecimentos da coluna de Remuneração Real. Apuração de tempo de serviço com fusão de períodos concomitantes."),
        ("<b>2.3. Motor de Decisão & Recomendador de Regras:</b>", "Diagnóstico automatizado que indica a regra mais vantajosa (Aposentadoria por Idade EC 103/2019, Revisão da Vida Toda STF Tema 1102, Indenização de Atrasados Art. 45-A) com parecer jurídico."),
        ("<b>2.4. Módulo de Auditoria & Guia de Complementação (PREC-MENOR-MIN):</b>", "Identificação de contribuições abaixo do Salário Mínimo e apuração da Guia/DARF de complementação (alíquotas de 20% para autônomos de 1998 e 11% para cooperativas/LC 123). Totalizador exato de R$ 475,57."),
        ("<b>2.5. Dashboard Web Interativo (React 18 / Next.js 14):</b>", "Planilha Data Grid com conversão de moedas em tempo real, botões de preenchimento em lote e ícones interativos de ajuda (?) com tooltips ao passar o mouse."),
        ("<b>2.6. Gerador de Laudos e Pareceres em PDF:</b>", "Exportação de parecer corporativo de alto nível em formato pt-BR (R$ 1.518,00) com demonstrativo de complementação e memória mês a mês."),
        ("<b>2.7. Automação de Inicialização Windows:</b>", "Script iniciar_sistema.bat para inicialização simultânea do backend FastAPI (:8000) e frontend Next.js (:3000).")
    ]

    for m_titulo, m_desc in modulos:
        elements.append(Paragraph(f"• {m_titulo} {m_desc}", bullet_style))

    elements.append(Spacer(1, 10))

    # 4. TABELA RESUMO DE COMPONENTES
    elements.append(Paragraph("3. RESUMO DOS COMPONENTES E TECNOLOGIAS", secao_style))

    comp_data = [
        [Paragraph("<b>Componente</b>", normal_style), Paragraph("<b>Tecnologia</b>", normal_style), Paragraph("<b>Função Principal</b>", normal_style)],
        [Paragraph("Backend API", normal_style), Paragraph("FastAPI / Python 3.14", normal_style), Paragraph("Engine de cálculo RMI e REST Endpoints", normal_style)],
        [Paragraph("Frontend Web", normal_style), Paragraph("Next.js 14 / React 18", normal_style), Paragraph("Dashboard interativo e planilha Data Grid", normal_style)],
        [Paragraph("CNIS Parser", normal_style), Paragraph("pypdf + Regex Avançado", normal_style), Paragraph("Leitura de cabeçalho, vínculos e salários", normal_style)],
        [Paragraph("PDF Generator", normal_style), Paragraph("ReportLab Engine", normal_style), Paragraph("Laudos executivos e guias de complementação", normal_style)],
        [Paragraph("Precisão Numérica", normal_style), Paragraph("Decimal(28)", normal_style), Paragraph("Zero erro flutuante em conversões monetárias", normal_style)],
    ]
    table_comp = Table(comp_data, colWidths=[120, 140, 280])
    table_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e293b')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 4),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#f8fafc')),
        ('BACKGROUND', (0,3), (-1,3), colors.HexColor('#f8fafc')),
        ('BACKGROUND', (0,5), (-1,5), colors.HexColor('#f8fafc')),
    ]))
    elements.append(table_comp)
    elements.append(Spacer(1, 15))

    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1'), spaceBefore=5, spaceAfter=8))
    elements.append(Paragraph("<i>Documentação gerada automaticamente pela Plataforma PrevCalc SaaS Legal Tech. Todos os direitos reservados.</i>", subtitulo_style))

    doc.build(elements, canvasmaker=MasterNumberedCanvas)

if __name__ == '__main__':
    target = r"d:\Area de Trabalho\PROJETOS ANTIGRAVIT\PROJETO INSS\relatorio_geral_sistema_prevcalc.pdf"
    gerar_pdf_master(target)
    print("PDF Master gerado com sucesso em:", target)
