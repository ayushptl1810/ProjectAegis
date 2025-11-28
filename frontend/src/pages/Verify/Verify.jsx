import { useState } from 'react'
import './Verify.css'

function Verify() {
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    
    // TODO: Implement API call
    setTimeout(() => {
      setLoading(false)
      setResult({ message: "Verification in progress..." })
    }, 1000)
  }

  return (
    <div className="verify-page">
      <h1>Verify Content</h1>
      <form onSubmit={handleSubmit}>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Enter text, URL, or upload media..."
          rows={5}
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Verifying...' : 'Verify'}
        </button>
      </form>
      {result && (
        <div className="result">
          <p>{result.message}</p>
        </div>
      )}
    </div>
  )
}

export default Verify