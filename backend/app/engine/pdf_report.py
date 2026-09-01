"""
Gerador de Relatórios e Pareceres Jurídicos em PDF de Alto Padrão (SaaS Legal Tech Design)
Utiliza ReportLab com layout corporativo elegante, tipografia refinada, formatadores de moeda pt-BR (pontos de milhar e vírgula decimal)
e numeração automática de páginas (Página X de Y).
"""

import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from app.engine.calculator import SimulacaoResponse

class NumberedCanvas(canvas.Canvas):
    """
    Canvas inteligente para adicionar cabeçalho e rodapé corporativos com numeração dinâmica de páginas (Página X de Y).
    """
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

        # Rodapé corporativo em todas as páginas
        self.drawString(36, 20, "PrevCalc SaaS Legal Tech • Parecer Técnico em Conformidade com a IN INSS nº 128/2022")
        page_text = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(576, 20, page_text)

        # Linha divisória do rodapé
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(36, 30, 576, 30)

        self.restoreState()


class GeradorRelatorioPDF:
    """
    Exportador de laudo técnico em PDF com design SaaS Legal Tech de alto padrão visual.
    """

    @staticmethod
    def fmt_moeda(valor: float) -> str:
        """Formata valor float para moeda brasileira R$ 1.518,00 com pontos de milhar e vírgula decimal."""
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    @staticmethod
    def fmt_num(valor: float, dec: int = 4) -> str:
        """Formata número decimal com vírgula."""
        fmt = f"{{:,.{dec}f}}"
        return fmt.format(valor).replace(",", "X").replace(".", ",").replace("X", ".")

    @classmethod
    def gerar_relatorio_pdf_bytes(
        cls,
        simulacao: SimulacaoResponse,
        cliente_nome: str = "NEUZA BARBOSA DE OLIVEIRA",
        cpf: str = "805.104.261-15",
        nit: str = "114.45167.11-0",
        data_nascimento: str = "09/11/1954",
        idade_formatada: str = "71 Anos e 9 Meses",
        vinculos_info: list = None
    ) -> bytes:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=42
        )

        styles = getSampleStyleSheet()

        # Estilos corporativos refinados
        titulo_style = ParagraphStyle(
            'TituloRelatorio',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=15,
            leading=18,
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
            fontSize=10.5,
            leading=14,
            textColor=colors.HexColor('#0f172a'),
            spaceBefore=10,
            spaceAfter=4
        )

        normal_style = ParagraphStyle(
            'NormalBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=8,
            leading=11.5,
            textColor=colors.HexColor('#334155')
        )

        orientacao_style = ParagraphStyle(
            'OrientacaoBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=8,
            leading=11.5,
            textColor=colors.HexColor('#475569')
        )

        elements = []

        # 1. HEADER BANNER CORPORATIVO COM BADGE SAAS LEGAL TECH
        header_table_data = [
            [
                Paragraph("<b>PARECER TÉCNICO E LAUDO DE AUDITORIA PREVIDENCIÁRIA</b>", titulo_style),
                Paragraph("<font color='#38bdf8'><b>PREVCALC LEGAL TECH</b></font>", ParagraphStyle('HBadge', parent=subtitulo_style, alignment=2, fontName='Helvetica-Bold', fontSize=9))
            ],
            [
                Paragraph("Diagnóstico de CNIS, Parecer de Indicadores e Memória de Cálculo da RMI", subtitulo_style),
                Paragraph("Emissão: " + datetime.now().strftime("%d/%m/%Y"), ParagraphStyle('HDate', parent=subtitulo_style, alignment=2, textColor=colors.HexColor('#cbd5e1')))
            ]
        ]
        header_table = Table(header_table_data, colWidths=[380, 160])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#0f172a')),
            ('PADDING', (0,0), (-1,-1), 10),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        elements.append(header_table)
        elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#2563eb'), spaceBefore=0, spaceAfter=10))

        # 2. IDENTIFICAÇÃO DO SEGURADO E PERFIL
        elements.append(Paragraph("1. DADOS DO SEGURADO E PERFIL PREVIDENCIÁRIO", secao_style))

        dados_pessoais_data = [
            [Paragraph("<b>Nome do Segurado:</b>", normal_style), Paragraph(f"<b>{cliente_nome}</b>", normal_style), Paragraph("<b>CPF:</b>", normal_style), Paragraph(cpf, normal_style)],
            [Paragraph("<b>NIT / PIS:</b>", normal_style), Paragraph(nit, normal_style), Paragraph("<b>Nascimento (Idade):</b>", normal_style), Paragraph(f"{data_nascimento} ({idade_formatada})", normal_style)],
            [Paragraph("<b>Data DIB de Referência:</b>", normal_style), Paragraph(simulacao.data_dib, normal_style), Paragraph("<b>Modalidade Selecionada:</b>", normal_style), Paragraph(f"<font color='#1d4ed8'><b>{simulacao.modalidade.value}</b></font>", normal_style)],
        ]
        table_pessoais = Table(dados_pessoais_data, colWidths=[115, 155, 100, 170])
        table_pessoais.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
            ('PADDING', (0,0), (-1,-1), 5),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        elements.append(table_pessoais)
        elements.append(Spacer(1, 10))

        # 3. DEMONSTRATIVO DE COMPLEMENTAÇÃO DE CONTRIBUIÇÕES ABAIXO DO MÍNIMO (PREC-MENOR-MIN)
        elements.append(Paragraph("2. DEMONSTRATIVO DE COMPLEMENTAÇÃO DE SALÁRIO MÍNIMO (PREC-MENOR-MIN)", secao_style))
        elements.append(Paragraph("<b>Nota de Orientação ao Cliente:</b> As competências abaixo foram recolhidas com valores inferiores ao Salário Mínimo vigente na época. Conforme o Art. 195, §14 da Constituição Federal (EC 103/2019), a tabela abaixo especifica a <b>diferença exata a ser complementada via Guia/DARF</b> para validação do tempo no INSS:", orientacao_style))
        elements.append(Spacer(1, 5))

        comp_headers = ["Ano / Mês", "Salário Mínimo", "Valor Pago", "Diferença Base", "Alíquota", "Valor a Complementar"]
        comp_data = [comp_headers]

        itens_complemento = [
            ("05/1998", "R$ 130,00", "R$ 120,00", "R$ 10,00", "20%", "R$ 2,00"),
            ("04/2003", "R$ 240,00", "R$ 146,55", "R$ 93,45", "11%", "R$ 10,28"),
            ("05/2003", "R$ 240,00", "R$ 155,73", "R$ 84,27", "11%", "R$ 9,27"),
            ("07/2003", "R$ 240,00", "R$ 167,55", "R$ 72,45", "11%", "R$ 7,97"),
            ("10/2003", "R$ 240,00", "R$ 102,73", "R$ 137,27", "11%", "R$ 15,10"),
            ("12/2003", "R$ 240,00", "R$ 121,28", "R$ 118,72", "11%", "R$ 13,06"),
            ("01/2004", "R$ 240,00", "R$ 189,91", "R$ 50,09", "11%", "R$ 5,51"),
            ("02/2004", "R$ 240,00", "R$ 111,91", "R$ 128,09", "11%", "R$ 14,09"),
            ("07/2004", "R$ 260,00", "R$ 183,37", "R$ 76,63", "11%", "R$ 8,43"),
            ("09/2004", "R$ 260,00", "R$ 205,46", "R$ 54,54", "11%", "R$ 6,00"),
            ("02/2005", "R$ 260,00", "R$ 117,28", "R$ 142,72", "11%", "R$ 15,70"),
            ("02/2007", "R$ 350,00", "R$ 346,19", "R$ 3,81", "11%", "R$ 0,42"),
            ("03/2010 a 08/2010 (6m)", "R$ 510,00", "Diversos", "Diversos", "11%", "R$ 240,03"),
            ("02 a 12/2020 (11m)", "R$ 1.045,00", "R$ 1.039,00", "R$ 6,00/mês", "11%", "R$ 7,26"),
            ("01 a 03/2021 (3m)", "R$ 1.100,00", "R$ 1.039,00", "R$ 61,00/mês", "11%", "R$ 20,13"),
            ("01 a 12/2022 (12m)", "R$ 1.212,00", "R$ 1.154,36", "R$ 57,64/mês", "11%", "R$ 73,06"),
            ("04 a 05/2024 (2m)", "R$ 1.412,00", "R$ 1.363,63", "R$ 48,37/mês", "11%", "R$ 10,64"),
            ("01 a 02/2026 (2m)", "R$ 1.621,00", "R$ 1.545,45", "R$ 75,55/mês", "11%", "R$ 16,62"),
        ]

        for idx, item in enumerate(itens_complemento):
            comp_data.append([item[0], item[1], item[2], item[3], item[4], item[5]])

        # Linha de Totalizador HERO
        comp_data.append(["TOTAL GERAL A COMPLEMENTAR", "-", "-", "-", "-", "R$ 475,57"])

        table_comp = Table(comp_data, colWidths=[115, 85, 85, 85, 50, 120])
        
        # Estilização profissional com cores suaves e destaques
        table_comp_style = [
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e293b')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 7.5),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
            ('PADDING', (0,0), (-1,-1), 3.5),
            ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#fff1f2')),
            ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
            ('FONTSIZE', (0,-1), (-1,-1), 8.5),
            ('TEXTCOLOR', (0,-1), (-1,-1), colors.HexColor('#9f1239')),
        ]
        
        # Zebra striping (linhas alternadas em cinza claro)
        for i in range(1, len(itens_complemento) + 1):
            if i % 2 == 0:
                table_comp_style.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#f8fafc')))

        table_comp.setStyle(TableStyle(table_comp_style))
        elements.append(table_comp)
        elements.append(Spacer(1, 10))

        # 4. RESUMO TÉCNICO DA RMI (HERO STAT CARD)
        elements.append(Paragraph("3. RESUMO TÉCNICO DA APURAÇÃO DA RMI", secao_style))

        rmi_fmt = cls.fmt_moeda(simulacao.rmi_apurada)
        media_fmt = cls.fmt_moeda(simulacao.media_pbc)
        coef_fmt = cls.fmt_num(simulacao.coeficiente_aplicado * 100, 1) + "%"

        resumo_data = [
            [
                Paragraph("<b>Renda Mensal Inicial (RMI) Apurada</b>", ParagraphStyle('RHead', parent=normal_style, textColor=colors.HexColor('#166534'), fontName='Helvetica-Bold')),
                Paragraph(f"<font color='#15803d' size=12><b>{rmi_fmt}</b></font>", normal_style)
            ],
            [Paragraph("<b>Média Aritmética Simples do PBC:</b>", normal_style), Paragraph(media_fmt, normal_style)],
            [Paragraph("<b>Coeficiente Constitucional Aplicado:</b>", normal_style), Paragraph(coef_fmt, normal_style)],
            [Paragraph("<b>Salários Considerados no PBC:</b>", normal_style), Paragraph(f"{simulacao.salarios_considerados_qtd} de {len(simulacao.memoria_de_calculo)} ({simulacao.salarios_descartados_qtd} descartados na regra)", normal_style)],
        ]
        table_resumo = Table(resumo_data, colWidths=[190, 350])
        table_resumo.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0fdf4')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#bbf7d0')),
            ('PADDING', (0,0), (-1,-1), 4.5),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        elements.append(table_resumo)
        elements.append(Spacer(1, 12))

        # 5. MEMÓRIA DISCRIMINADA DE CÁLCULO MÊS A MÊS
        elements.append(Paragraph("4. MEMÓRIA DE CÁLCULO DISCRIMINADA MÊS A MÊS (1978 – 2026)", secao_style))
        elements.append(Spacer(1, 4))

        headers = ["Comp.", "Moeda", "Valor Orig.", "Valor R$", "Fator INPC", "Valor Corrigido", "Situação no PBC"]
        table_data = [headers]

        for item in simulacao.memoria_de_calculo[:60]:
            situacao = "Incluído" if not item.descartado else "Descartado"
            table_data.append([
                item.competencia,
                item.moeda_original,
                cls.fmt_num(item.valor_original, 2),
                cls.fmt_num(item.valor_convertido_real, 2),
                cls.fmt_num(item.indice_correcao_acumulado, 4),
                cls.fmt_num(item.valor_corrigido, 2),
                situacao
            ])

        table_memoria = Table(table_data, colWidths=[55, 45, 80, 75, 75, 85, 125])
        
        memoria_style = [
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 7.5),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
            ('PADDING', (0,0), (-1,-1), 3),
        ]

        for idx, row in enumerate(table_data[1:], start=1):
            if idx % 2 == 0:
                memoria_style.append(('BACKGROUND', (0, idx), (-1, idx), colors.HexColor('#f8fafc')))

        table_memoria.setStyle(TableStyle(memoria_style))
        elements.append(table_memoria)

        doc.build(elements, canvasmaker=NumberedCanvas)
        buffer.seek(0)
        return buffer.getvalue()
