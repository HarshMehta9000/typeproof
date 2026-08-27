import Link from 'next/link';

export default function About() {
  return (
    <main className="about-page">
      <header className="about-header">
        <Link href="/" className="about-brand"><span className="brand-mark">{'{'}<b>✓</b>{'}'}</span><b>Typeproof</b></Link>
        <Link href="/">← return to workbench</Link>
      </header>
      <section className="about-content">
        <div className="eyebrow">about / architecture</div>
        <h1>Structured output should earn its way into your app.</h1>
        <p className="about-lede">Typeproof is a small, inspectable extraction agent: every model response is treated as untrusted input, parsed, validated, persisted when it fails, and only returned once it satisfies a real Pydantic schema.</p>
        <div className="about-grid">
          <div><span className="eyebrow">engine</span><pre>{`received → request → parse → validate → success\n                         ↘ failure → persist → repair → retry`}</pre></div>
          <div><span className="eyebrow">local run</span><pre>{`pip install -r requirements.txt\nuvicorn typeproof.api:app --reload\n\n# deterministic demo\ncurl -X POST localhost:8000/extract`}</pre></div>
        </div>
        <div className="about-notes"><span>FastAPI</span><span>Pydantic v2</span><span>SQLite</span><span>structlog</span><span>OpenAI-compatible</span></div>
      </section>
    </main>
  );
}
