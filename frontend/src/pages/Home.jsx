import { useState } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import MarkdownViewer from '../components/MarkdownViewer';

function Home() {
  const [markdown, setMarkdown] = useState('');
  const [loading, setLoading] = useState(false);
  const [selectedFormat, setSelectedFormat] = useState('pdf');

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    setLoading(true);
    try {
      const res = await axios.post('http://localhost:8000/api/convert', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      setMarkdown(res.data.markdown);
    } catch (err) {
      alert('업로드 실패!');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async () => {
    try {
      const formData = new FormData();
      formData.append('markdown', markdown);
      formData.append('format', selectedFormat);

      const res = await axios.post(
        `http://localhost:8000/api/export`,  // ✅ export 엔드포인트로 수정
        formData,
        { responseType: 'blob' } // 파일 다운로드
      );

      const blob = new Blob([res.data], { type: res.headers['content-type'] });
      const url = window.URL.createObjectURL(blob);

      const a = document.createElement('a');
      a.href = url;
      a.download = `converted.${selectedFormat}`;
      document.body.appendChild(a);
      a.click();
      a.remove();

      window.URL.revokeObjectURL(url);
    } catch (err) {
      alert('다운로드 실패!');
      console.error(err);
    }
  };

  return (
    <div style={{ padding: 40, maxWidth: 800, margin: 'auto' }}>
      <h2>📄 파일 업로드 → 📘 Markdown 변환기</h2>
      <input type="file" accept=".csv,.xlsx,.json" onChange={handleFileChange} />
      {loading && <p>⏳ 변환 중...</p>}

      {/* 작성된 내용 표시 */}
      <div style={{ marginTop: 30, border: '1px solid #ddd', padding: 20 }}>
        <ReactMarkdown>{markdown}</ReactMarkdown>
      </div>

      <MarkdownViewer content={markdown} />

      {markdown && (
        <div style={{ marginTop: 20 }}>
          <label>
            변환 포맷:
            <select
              value={selectedFormat}
              onChange={(e) => setSelectedFormat(e.target.value)}
              style={{ marginLeft: 10 }}
            >
              <option value="pdf">PDF</option>
              <option value="html">HTML</option>
              <option value="docx">docx</option>
              <option value="csv">CSV</option>
              <option value="json">JSON</option>
            </select>
          </label>
          <button onClick={handleDownload} style={{ marginLeft: 20 }}>
            다운로드
          </button>
        </div>
      )}
    </div>
  );
}

export default Home;