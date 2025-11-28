import { Link } from 'react-router-dom'
import './Home.css'

function Home() {
  return (
    <div className="home">
      <section className="hero">
        <h1>Misinformation Detection Platform</h1>
        <p>Verify claims, images, and videos with AI-powered fact-checking</p>
        <Link to="/verify" className="cta-button">
          Start Verifying
        </Link>
      </section>
    </div>
  )
}

export default Home