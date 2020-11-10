from docx import Document
from docx.shared import Inches
from docx.shared import Pt
from docx.shared import Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn


# author 刘钰
class Report:
    # 生成报告
    def report(self):
        document = Document()  # 实例化Document
        document.styles['Normal'].font.name = u'微软雅黑'
        document.styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), u'微软雅黑')

        # 添加标题
        p = document.add_paragraph()
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        head = "XX年XX月XX日技术分析判断报告"
        font = p.add_run(head).font
        font.size = Pt(22)
        font.bold = True

        # 添加图片
        document.add_picture("D:/aaa/mplfinance.png", width=Inches(6))
        # 图片居中
        last_paragraph = document.paragraphs[-1]
        last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # 创建表格
        table = document.add_table(rows=9, cols=0, style='Table Grid')
        table.add_column(width=Cm(6))
        table.add_column(width=Cm(9.5))
        table.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # 填充表格内容
        header = ["品种名称", "趋势", "N日均线价格穿越情况", "M日、N日均线交叉和穿越情况", "RSI指标", "RSI指标背离情况", "MACD穿越情况", "形态提示", "前期低点、高点是否突破"]
        for i in range(0, len(header)):
            table.cell(i, 0).text = header[i]

        # test
        table.cell(0, 1).text = "未知品种未知品种未知品种未知品种未知品种"

        # 保存docx
        document.save('D:/aaa/result.docx')
