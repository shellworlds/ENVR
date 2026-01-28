import SupportAnalysis from '../components/SupportAnalysis';
import PrimeVisualization from '../components/PrimeVisualization';
import TopologyDiagram from '../components/TopologyDiagram';

export default function Home() {
  return (
    <div className="container">
      <header>
        <h1>SLK8 Problem Analysis</h1>
        <p>Support of M = ℚ/ℤ over integers ℤ</p>
      </header>
      
      <main>
        <section className="problem-statement">
          <h2>Problem Statement</h2>
          <p>
            Let ℤ be the ring of integers, ℚ the rational numbers, 
            and set M := ℚ/ℤ. Find the support Supp(M), 
            and show that it's not Zariski closed.
          </p>
        </section>
        
        <section className="analysis-section">
          <SupportAnalysis />
        </section>
        
        <section className="visualization-section">
          <PrimeVisualization maxPrime={50} />
        </section>
        
        <section className="mathematical-details">
          <h2>Mathematical Details</h2>
          <TopologyDiagram />
          
          <div className="proof">
            <h3>Proof Sketch</h3>
            <ol>
              <li>M = ℚ/ℤ is a torsion ℤ-module</li>
              <li>Localization at (0): M_(0) = 0 (torsion disappears)</li>
              <li>Localization at (p): M_(p) = ℤ[1/p]/ℤ ≠ 0 (p-torsion survives)</li>
              <li>Thus Supp(M) = {"{"}(p) | p prime{"}"}</li>
              <li>In Spec(ℤ), closed sets are finite or whole space</li>
              <li>Support is infinite but ≠ Spec(ℤ) → not closed</li>
            </ol>
          </div>
        </section>
        
        <section className="implementations">
          <h2>Multi-language Implementations</h2>
          <div className="language-grid">
            {['Python', 'JavaScript', 'Java', 'C++', 'Go', 'Rust', 
              'TypeScript', 'React', 'Next.js', 'Shell'].map(lang => (
              <div key={lang} className="language-card">
                {lang}
              </div>
            ))}
          </div>
        </section>
      </main>
      
      <footer>
        <p>Implemented by shellworlds | Mathematical Analysis: SLK8 Problem</p>
      </footer>
    </div>
  );
}
