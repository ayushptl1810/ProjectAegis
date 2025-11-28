"""
Orchestrator Agent
Coordinates workflow between different agents
"""

import logging
from trend_scanner_agent import TrendScannerAgent
from claim_verifier_agent import ClaimVerifierAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OrchestratorAgent:
    """Orchestrates multi-agent workflows"""
    
    def __init__(self):
        """Initialize orchestrator"""
        self.trend_scanner = TrendScannerAgent()
        self.claim_verifier = ClaimVerifierAgent()
        logger.info("OrchestratorAgent initialized")
    
    def run_pipeline(self):
        """Run the complete verification pipeline"""
        logger.info("Starting verification pipeline")
        
        # Step 1: Scan trends
        trends = self.trend_scanner.scan_trends()
        
        # Step 2: Verify claims
        verified_claims = []
        for post in trends.get("trending_posts", []):
            if "claim" in post:
                result = self.claim_verifier.verify_claim(post["claim"])
                verified_claims.append(result)
        
        return {
            "timestamp": "2024-01-15T10:30:00",
            "total_posts": len(verified_claims),
            "posts": verified_claims
        }

if __name__ == "__main__":
    orchestrator = OrchestratorAgent()
    result = orchestrator.run_pipeline()
    print(result)