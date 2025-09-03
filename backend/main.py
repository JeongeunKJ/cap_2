from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import os
import tempfile
import uuid
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

OUTPUT_DIR = "./output"
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_MD_PATH = os.path.join(OUTPUT_DIR, "output.md")


@app.post("/api/convert")
async def convert_file(file: UploadFile = File(...)):
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

        # ✅ 변환된 md를 서버에 저장
        with open(OUTPUT_MD_PATH, "w", encoding="utf-8") as f:
            f.write(markdown)

    finally:
        os.remove(tmp_path)

    return JSONResponse(content={"markdown": markdown})


@app.get("/api/download")
def download_file():
    """서버에 저장된 md 파일 다운로드"""
    if not os.path.exists(OUTPUT_MD_PATH):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(
        path=OUTPUT_MD_PATH, 
        filename="converted.md", 
        media_type="application/octet-stream")


@app.post("/api/export")
async def export_file(format: str = Form(...)):
    """
    서버에 저장된 output.md 파일을 다른 포맷으로 변환
    """
    if not os.path.exists(OUTPUT_MD_PATH):
        raise HTTPException(status_code=404, detail="Markdown 파일이 존재하지 않습니다.")

    if format not in ["html", "pdf", "csv", "json", "docx", "xlsx"]:
        raise HTTPException(status_code=400, detail="지원하지 않는 포맷입니다.")

    try:
        # 저장된 md 파일을 읽어서 변환
        with open(OUTPUT_MD_PATH, "r", encoding="utf-8") as f:
            markdown = f.read()

        output_path = convert_markdown_to_format(markdown, format)
        filename = os.path.basename(output_path)


        return FileResponse(path=output_path, filename=filename, media_type="application/octet-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def read_root():
    return {"message": "Markdown Viewer API is running"}

