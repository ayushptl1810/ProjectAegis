import './RumourCard.css'

function RumourCard({ rumour }) {
  const getVerdictColor = (verdict) => {
    switch (verdict) {
      case 'true':
        return 'green'
      case 'false':
        return 'red'
      case 'uncertain':
        return 'orange'
      default:
        return 'gray'
    }
  }

  return (
    <div className="rumour-card">
      <h3>{rumour.title || rumour.claim || 'Untitled'}</h3>
      <p>{rumour.content || rumour.summary || 'No content'}</p>
      {rumour.verdict && (
        <div className={`verdict verdict-${rumour.verdict}`}>
          {rumour.verdict.toUpperCase()}
        </div>
      )}
    </div>
  )
}

export default RumourCard