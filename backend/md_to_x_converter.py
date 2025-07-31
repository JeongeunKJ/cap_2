import tempfile
import os
from markdown2 import markdown
import pdfkit  # PDF 변환용, wkhtmltopdf 필요
import pandas as pd

def convert_markdown_to_format(md_content: str, fmt: str) -> str:
    tmp_dir = tempfile.gettempdir()

    if fmt == "html":
        html_content = markdown(md_content)
        output_path = os.path.join(tmp_dir, "output.html")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

    elif fmt == "pdf":
        html_content = markdown(md_content)
        html_path = os.path.join(tmp_dir, "temp.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        output_path = os.path.join(tmp_dir, "output.pdf")
        pdfkit.from_file(html_path, output_path)

    elif fmt == "csv":
        # 아주 단순한 마크다운 테이블 처리 예시
        from io import StringIO
        import pandas as pd
        lines = [line for line in md_content.splitlines() if '|' in line]
        if len(lines) < 2:
            raise ValueError("유효한 마크다운 테이블이 아닙니다.")
        table = "\n".join(lines)
        df = pd.read_csv(StringIO(table), sep="|", engine="python", skipinitialspace=True)
        output_path = os.path.join(tmp_dir, "output.csv")
        df.to_csv(output_path, index=False)

    elif fmt == "json":
        # 마크다운을 직접 JSON으로 파싱하는 건 구조 따라 다름, 필요 시 커스터마이징
        raise NotImplementedError("마크다운 → JSON 변환은 추가 구현 필요")

    else:
        raise ValueError("지원하지 않는 포맷")

    return output_path