import React, { useEffect, useState } from 'react';

function AdminDashboard() {
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(false);
  const [filter, setFilter] = useState('pending');
  const [error, setError] = useState('');

  const load = async (status = filter) => {
    try {
      setLoading(true);
      const qs = status ? `?status=${status}` : '';
      const res = await fetch(`http://localhost:8000/api/admin/join-requests${qs}`);
      const data = await res.json();
      setRequests(data.projects || []);
    } catch (e) {
      setError('목록을 불러오지 못했습니다.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(filter); }, []);

  const updateStatus = async (id, reviewStatus) => {
    try {
      setLoading(true);
      await fetch(`http://localhost:8000/api/admin/join-requests/${id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ reviewStatus })
      });
      await load(filter);
    } catch (e) {
      setError('상태 업데이트 실패');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 24 }}>
      <h2>관리자: 결합 요청 관리</h2>
      <div style={{ display: 'flex', gap: 8, margin: '12px 0' }}>
        {['pending','approved','rejected','all'].map(s => (
          <button key={s} onClick={() => { setFilter(s === 'all' ? '' : s); load(s === 'all' ? '' : s); }}>
            {s}
          </button>
        ))}
      </div>
      {loading && <div>로딩 중…</div>}
      {error && <div style={{ color: 'red' }}>{error}</div>}
      <div style={{ display: 'grid', gap: 12 }}>
        {requests.map(r => (
          <div key={r.id} style={{ border: '1px solid #e5e7eb', borderRadius: 8, padding: 12, background: '#fff' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <div>
                <div style={{ fontWeight: 600 }}>{r.projectName}</div>
                <div style={{ fontSize: 12, color: '#6b7280' }}>ID: {r.id} • 생성일: {r.createdAt}</div>
                <div style={{ fontSize: 12, color: '#6b7280' }}>파일: {(r.files||[]).join(', ')}</div>
                <div style={{ fontSize: 12, color: '#6b7280' }}>현재상태: {r.review?.status} / 표시상태: {r.status}</div>
              </div>
              <div style={{ display: 'flex', gap: 8 }}>
                <button onClick={() => updateStatus(r.id, 'approved')} disabled={r.review?.status==='approved'}>승인</button>
                <button onClick={() => updateStatus(r.id, 'rejected')} disabled={r.review?.status==='rejected'}>반려</button>
              </div>
            </div>
          </div>
        ))}
        {(!loading && requests.length===0) && <div>표시할 요청이 없습니다.</div>}
      </div>
    </div>
  );
}

export default AdminDashboard;
