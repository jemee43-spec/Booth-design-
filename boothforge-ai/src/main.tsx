import React, { useState } from 'react';
import { createRoot } from 'react-dom/client';
import './style.css';

type Brief = { name: string; width: number; depth: number; height: number; brand: string; requirements: string };
const initial: Brief = { name: 'مشروع جديد', width: 6, depth: 4, height: 3, brand: '', requirements: 'استقبال، شاشة عرض، مخزن' };
const concepts = [
  { name: 'Open Flow', desc: 'واجهة مفتوحة واستقبال أمامي', zones: ['استقبال', 'عرض', 'تخزين'] },
  { name: 'Central Island', desc: 'منطقة تفاعل مركزية', zones: ['عرض', 'تفاعل', 'استقبال'] },
  { name: 'Premium Lounge', desc: 'جلسة ضيافة ومسار زوار', zones: ['ضيافة', 'عرض', 'تخزين'] },
];
function App() {
  const [brief, setBrief] = useState<Brief>(() => {
    try { return { ...initial, ...JSON.parse(localStorage.getItem('boothforge-brief') || '{}') }; }
    catch { return initial; }
  });
  const [selected, setSelected] = useState(0);
  const update = (key: keyof Brief, value: string) => setBrief(p => ({ ...p, [key]: ['width', 'depth', 'height'].includes(key) ? Number(value) : value }));
  const valid = [brief.width, brief.depth, brief.height].every(n => Number.isFinite(n) && n > 0);
  const save = () => { localStorage.setItem('boothforge-brief', JSON.stringify(brief)); alert('تم حفظ المشروع على هذا المتصفح'); };
  const exportJson = () => {
    if (!valid) return;
    const payload = { schemaVersion: '0.1', units: 'm', brief, concept: concepts[selected], status: 'concept-only-not-engineering-approved' };
    const url = URL.createObjectURL(new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' }));
    const a = document.createElement('a'); a.href = url; a.download = 'boothforge-concept.json'; a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  };
  return <main>
    <header><div><small>DESIGN • PLAN • BUILD</small><h1>BOOTHFORGE <span>AI</span></h1><p>استوديو تخطيط أجنحة المعارض — النسخة الأولية</p></div><b>PHASE 01 / MVP</b></header>
    <section className="layout">
      <article className="panel"><h2>مواصفات الجناح</h2>
        <label>اسم المشروع<input value={brief.name} onChange={e => update('name', e.target.value)} /></label>
        <label>العلامة التجارية<input value={brief.brand} onChange={e => update('brand', e.target.value)} placeholder="اسم العميل" /></label>
        <div className="dimensions">{(['width', 'depth', 'height'] as const).map((key, i) => <label key={key}>{['العرض (م)', 'العمق (م)', 'الارتفاع (م)'][i]}<input type="number" min="0.1" step="0.1" value={brief[key]} onChange={e => update(key, e.target.value)} /></label>)}</div>
        <label>المتطلبات<textarea rows={4} value={brief.requirements} onChange={e => update('requirements', e.target.value)} /></label>
        <p className="area">المساحة: {valid ? (brief.width * brief.depth).toFixed(2) : '—'} م²</p>
        {!valid && <p className="error">يجب أن تكون جميع الأبعاد أكبر من صفر.</p>}
        <button disabled={!valid} onClick={save}>حفظ المشروع</button>
      </article>
      <article className="panel preview"><h2>ثلاثة تصورات أولية</h2><p className="muted">مخططات تقسيم مساحات توضيحية، وليست نماذج 3D أو رسومات تنفيذية.</p>
        <div className="tabs">{concepts.map((c, i) => <button className={selected === i ? 'active' : ''} onClick={() => setSelected(i)} key={c.name}>{c.name}</button>)}</div>
        <div className="plan" style={{ aspectRatio: valid ? `${brief.width}/${brief.depth}` : '3/2' }}>{concepts[selected].zones.map((z, i) => <div className={'zone zone' + i} key={z}>{z}</div>)}</div>
        <h3>{concepts[selected].name}</h3><p>{concepts[selected].desc}</p><button disabled={!valid} onClick={exportJson}>تصدير مواصفات JSON</button>
      </article>
    </section><footer>Concept prototype • CAD and realistic rendering are not yet implemented.</footer>
  </main>;
}
createRoot(document.getElementById('root')!).render(<App />);
