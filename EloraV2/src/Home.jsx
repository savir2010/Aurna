import { Link } from "react-router-dom";
//header
import Header from './components/Header';

function Home() {
  return (
    <div style={{ margin: 0, fontFamily: '-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen, Ubuntu, Cantarell, Fira Sans, Droid Sans, Helvetica Neue, sans-serif', backgroundColor: '#2a2a2a', color: '#fff' }}>
      <main>
        <Header />
        
        <section style={{ position: 'relative', textAlign: 'left', padding: '6rem 2rem', color: '#fff' }}>
          <div style={{ maxWidth: '800px', margin: 'auto', textAlign: 'center' }}>
            <h1 style={{ background: 'linear-gradient(90deg, #ff6e6e, #508bf1)', WebkitBackgroundClip: 'text', color: 'transparent', fontSize: '4rem', fontWeight: 'bold' }}>
              BrainSync Analytics
            </h1>
            <p style={{ color: 'white', fontSize: '1.5rem', maxWidth: '700px', margin: 'auto' }}>
              Advanced EEG analysis and brain monitoring solutions. Unlocking the mysteries of neural activity through cutting-edge technology.
            </p>
            <div style={{ marginTop: '3rem' }}>
              <Link to="/signup" style={{ background: '#ff6e6e', color: 'white', padding: '0.95rem 2rem', borderRadius: '6px', textDecoration: 'none', fontWeight: 'bold' }}>Sign Up</Link>
              <Link to="/signin" style={{ border: '2px solid white', color: 'white', marginLeft: '1rem', padding: '0.95rem 2rem', borderRadius: '6px', textDecoration: 'none', fontWeight: 'bold' }}>
                Sign In <span aria-hidden="true">→</span>
              </Link>
            </div>
          </div>
        </section>

        <section style={{ padding: '3rem 2rem', background: '#2a2a2a', textAlign: 'center' }}>
          <h1 style={{ fontSize: "30px" }}>Our Services</h1>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1.8rem', marginTop: '2rem' }}>
            <div style={{ background: '#454545', padding: '4.4rem', borderRadius: '8px', textAlign: 'center' }}>
              <div style={{ fontSize: '5rem' }}>📊</div>
              <h3>EEG Analysis</h3>
              <p>Advanced brain activity monitoring and pattern recognition using state-of-the-art equipment.</p>
            </div>
            <div style={{ background: '#454545', padding: '4.4rem', borderRadius: '8px', textAlign: 'center' }}>
              <div style={{ fontSize: '5rem' }}>🧠</div>
              <h3>Neural Research</h3>
              <p>Cutting-edge research in neural networks and brain-computer interfaces.</p>
            </div>
            <div style={{ background: '#454545', padding: '4.4rem', borderRadius: '8px', textAlign: 'center' }}>
              <div style={{ fontSize: '5rem' }}>💻</div>
              <h3>Data Processing</h3>
              <p>Efficient data processing and analysis for EEG data collected from various sources.</p>
            </div>
          </div>
        </section>

        <footer style={{ background: '#222', padding: '2rem', textAlign: 'center', color: 'white' }}>
          <div>
            <div>
              <Link to="/about" style={{ color: 'white', textDecoration: 'none', margin: '0 1rem' }}>About</Link>
              <Link to="/services" style={{ color: 'white', textDecoration: 'none', margin: '0 1rem' }}>Services</Link>
              <Link to="/contact" style={{ color: 'white', textDecoration: 'none', margin: '0 1rem' }}>Contact</Link>
            </div>
            <p style={{ color: 'white', marginTop: '2rem' }}>© 2024 BrainSync Analytics. All rights reserved.</p>
          </div>
        </footer>
      </main>
    </div>
  );
}

export default Home;