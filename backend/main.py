from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import os
import tempfile
from x_to_md_converter import convert_table_to_markdown, convert_json_to_markdown
from md_to_x_converter import convert_markdown_to_format 
app = FastAPI()

# CORS 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.get("/")
# async def root():
#     return {"message": "Hello from FastAPI"}

@app.post("/api/convert")
async def convert_file(file: UploadFile = File(...)):
    # 임시 파일 저장
    suffix = os.path.splitext(file.filename)[1]
    if suffix not in [".csv", ".xlsx", ".json"]:
        raise HTTPException(status_code=400, detail="지원하지 않는 파일 형식입니다.")

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        if suffix in [".csv", ".xlsx"]:
            markdown = convert_table_to_markdown(tmp_path)
        elif suffix == ".json":
            markdown = convert_json_to_markdown(tmp_path)
        else:
            raise HTTPException(status_code=400, detail="파일 변환 실패")
    finally:
        os.remove(tmp_path)

    return JSONResponse(content = {"markdown": markdown})

@app.get("/api/download")
def download_file():
    file_path = "./output/output.md"  # 실제 마크다운 파일 경로
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=file_path, filename="converted.md", media_type='text/markdown')

@app.post("/api/export")
async def export_file(markdown: str = Form(...), format: str = Form(...)):
    """
    마크다운 문자열을 원하는 포맷(format)으로 변환하여 파일로 제공
    지원 포맷 예: html, pdf, json, csv 등
    """
    if format not in ["html", "pdf", "csv", "json"]:
        raise HTTPException(status_code=400, detail="지원하지 않는 포맷입니다.")

    try:
        output_path = convert_markdown_to_format(markdown, format)  # 구현 필요
        filename = os.path.basename(output_path)
        return FileResponse(path=output_path, filename=filename, media_type="application/octet-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def read_root():
    return {"message": "Markdown Viewer API is running"}
