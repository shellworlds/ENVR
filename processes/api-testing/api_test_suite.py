"""
Comprehensive API Testing Suite for Quantum AI System
Includes performance, security, load, and contract testing
"""
import asyncio
import aiohttp
import pytest
import json
import time
from typing import Dict, List, Optional
from dataclasses import dataclass
import statistics
from security import SecurityScanner

@dataclass
class TestResult:
    endpoint: str
    status_code: int
    response_time: float
    success: bool
    error: Optional[str] = None
    security_scan: Optional[Dict] = None

class QuantumAPITester:
    """Advanced API testing framework for quantum AI services"""
    
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        self.results: List[TestResult] = []
        self.security_scanner = SecurityScanner()
        
    async def test_endpoint(self, endpoint: str, method: str = "GET", 
                          payload: Optional[Dict] = None) -> TestResult:
        """Test individual endpoint with performance tracking"""
        url = f"{self.base_url}{endpoint}"
        start_time = time.time()
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(method, url, json=payload) as response:
                    response_time = time.time() - start_time
                    response_data = await response.json() if response.content else {}
                    
                    # Security scan
                    security_report = self.security_scanner.scan_response(
                        response.headers, response_data
                    )
                    
                    return TestResult(
                        endpoint=endpoint,
                        status_code=response.status,
                        response_time=response_time,
                        success=200 <= response.status < 300,
                        security_scan=security_report
                    )
        except Exception as e:
            return TestResult(
                endpoint=endpoint,
                status_code=0,
                response_time=time.time() - start_time,
                success=False,
                error=str(e)
            )
    
    async def run_performance_test(self, endpoint: str, concurrent_requests: int = 100):
        """Run load testing with concurrent requests"""
        print(f"🚀 Performance testing {endpoint} with {concurrent_requests} requests")
        
        tasks = [self.test_endpoint(endpoint) for _ in range(concurrent_requests)]
        results = await asyncio.gather(*tasks)
        
        # Calculate metrics
        response_times = [r.response_time for r in results if r.success]
        success_rate = sum(1 for r in results if r.success) / len(results) * 100
        
        if response_times:
            metrics = {
                "avg_response_time": statistics.mean(response_times),
                "p95_response_time": statistics.quantiles(response_times, n=20)[18],
                "p99_response_time": statistics.quantiles(response_times, n=100)[98],
                "success_rate": success_rate,
                "total_requests": len(results)
            }
            return metrics
        return {}
    
    async def test_quantum_inference(self):
        """Test quantum AI inference endpoints"""
        print("\n🧪 Testing Quantum Inference API")
        
        endpoints = [
            ("/api/v1/quantum/infer", "POST", {
                "prompt": "Explain quantum superposition",
                "max_tokens": 100
            }),
            ("/api/v1/quantum/embed", "POST", {
                "text": "Quantum machine learning combines quantum algorithms with neural networks"
            }),
            ("/api/v1/rag/query", "POST", {
                "query": "What is quantum entanglement?",
                "top_k": 3
            })
        ]
        
        for endpoint, method, payload in endpoints:
            result = await self.test_endpoint(endpoint, method, payload)
            self.results.append(result)
            print(f"  {endpoint}: {result.status_code} ({result.response_time:.3f}s)")
    
    async def test_security_headers(self):
        """Test API security headers and configurations"""
        print("\n🔒 Testing Security Headers")
        
        security_endpoints = [
            "/api/v1/auth/login",
            "/api/v1/users/profile",
            "/api/v1/admin/config"
        ]
        
        for endpoint in security_endpoints:
            result = await self.test_endpoint(endpoint)
            if result.security_scan:
                vulnerabilities = result.security_scan.get('vulnerabilities', [])
                if vulnerabilities:
                    print(f"  ⚠️  {endpoint}: {len(vulnerabilities)} vulnerabilities found")
                else:
                    print(f"  ✅ {endpoint}: Secure")
    
    def generate_test_report(self):
        """Generate comprehensive test report"""
        print("\n📊 Test Report Summary")
        print("=" * 50)
        
        total_tests = len(self.results)
        successful = sum(1 for r in self.results if r.success)
        success_rate = (successful / total_tests) * 100
        
        print(f"Total Tests: {total_tests}")
        print(f"Successful: {successful}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        # Performance summary
        avg_response_time = statistics.mean([r.response_time for r in self.results])
        print(f"Average Response Time: {avg_response_time:.3f}s")
        
        # Security summary
        security_issues = sum(
            1 for r in self.results 
            if r.security_scan and r.security_scan.get('vulnerabilities')
        )
        print(f"Security Issues Found: {security_issues}")
        
        return {
            "total_tests": total_tests,
            "success_rate": success_rate,
            "avg_response_time": avg_response_time,
            "security_issues": security_issues
        }

# Pytest test suite
@pytest.mark.asyncio
class TestQuantumAPI:
    """Pytest test cases for Quantum AI API"""
    
    @pytest.fixture
    async def api_tester(self):
        return QuantumAPITester()
    
    async def test_health_endpoint(self, api_tester):
        """Test health check endpoint"""
        result = await api_tester.test_endpoint("/health")
        assert result.status_code == 200
        assert result.response_time < 1.0
    
    async def test_inference_endpoint(self, api_tester):
        """Test quantum inference endpoint"""
        payload = {
            "prompt": "What is quantum computing?",
            "temperature": 0.7,
            "max_tokens": 50
        }
        result = await api_tester.test_endpoint(
            "/api/v1/quantum/infer", 
            "POST", 
            payload
        )
        assert result.status_code == 200
        assert "response" in result.security_scan
    
    async def test_rate_limiting(self, api_tester):
        """Test API rate limiting"""
        results = []
        for _ in range(110):  # Exceed typical rate limit
            result = await api_tester.test_endpoint("/api/v1/quantum/infer", "POST", {})
            results.append(result)
        
        # Should get 429 for some requests
        status_codes = [r.status_code for r in results]
        assert 429 in status_codes
    
    async def test_security_headers_present(self, api_tester):
        """Test that security headers are present"""
        result = await api_tester.test_endpoint("/api/v1/auth/login")
        security_scan = result.security_scan
        
        required_headers = ['X-Content-Type-Options', 'X-Frame-Options', 'Strict-Transport-Security']
        for header in required_headers:
            assert header in security_scan.get('headers', {})

# Async main execution
async def main():
    """Run comprehensive API testing suite"""
    print("🚀 Quantum AI API Testing Suite")
    print("=" * 50)
    
    tester = QuantumAPITester()
    
    # Run test suite
    await tester.test_quantum_inference()
    await tester.test_security_headers()
    
    # Performance testing
    print("\n⚡ Performance Testing")
    perf_metrics = await tester.run_performance_test("/api/v1/quantum/infer", 50)
    for metric, value in perf_metrics.items():
        print(f"  {metric}: {value}")
    
    # Generate report
    report = tester.generate_test_report()
    
    # Save report to file
    with open("api_test_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n✅ Test report saved to api_test_report.json")
    return report

if __name__ == "__main__":
    asyncio.run(main())
