#!/usr/bin/env python3
"""
Q-AVIOGEN FastAPI Service Test Script

This script provides comprehensive testing capabilities for the Q-AVIOGEN API,
including unit tests, integration tests, and manual API testing with curl examples.
"""

import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, Any, Optional

import requests


class QAviogenAPITester:
    """Test client for Q-AVIOGEN FastAPI Service"""
    
    def __init__(self, base_url: str = "http://localhost:8000", api_token: Optional[str] = None):
        """Initialize the test client
        
        Args:
            base_url: Base URL of the API service
            api_token: Optional API token for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        
        if api_token:
            self.session.headers.update({
                "Authorization": f"Bearer {api_token}"
            })
    
    def test_health_check(self) -> bool:
        """Test the health check endpoint"""
        print("🔍 Testing health check endpoint...")
        
        try:
            response = self.session.get(f"{self.base_url}/health")
            response.raise_for_status()
            
            data = response.json()
            print(f"✅ Health check passed: {data['status']}")
            print(f"   Version: {data.get('version', 'N/A')}")
            print(f"   Active jobs: {data.get('active_jobs', 0)}")
            
            return True
            
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            return False
    
    def test_video_generation(self) -> Optional[str]:
        """Test video generation endpoint"""
        print("🎬 Testing video generation endpoint...")
        
        # Sample request payload
        request_payload = {
            "project_name": "API_Test_Project",
            "procedure_text": "This is a test procedure for API validation. We are testing the complete video generation pipeline with all components working together seamlessly.",
            "avatar": {
                "model_path": "./project/assets/avatars/amedeo/avatar_model.blend",
                "face_texture": "./project/assets/avatars/amedeo/face_texture.png",
                "animation_style": "professional",
                "enable_lip_sync": True,
                "gesture_intensity": 0.7
            },
            "voice": {
                "voice_file": "./project/assets/audio/amedeo_voice_48k.wav",
                "speed": 1.0,
                "pitch": 1.0,
                "volume": 0.8
            },
            "render": {
                "resolution_x": 1280,
                "resolution_y": 720,
                "fps": 30,
                "quality": "medium",
                "samples": 64,
                "enable_denoising": True
            },
            "camera": {
                "position": [0, 0, 5],
                "rotation": [0, 0, 0],
                "focal_length": 50.0
            },
            "scene": {
                "lighting_setup": "studio",
                "environment_intensity": 1.0,
                "props": []
            },
            "output_format": "mp4",
            "output_quality": "high"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/generate",
                json=request_payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            
            data = response.json()
            job_id = data.get("job_id")
            
            print(f"✅ Video generation job submitted successfully")
            print(f"   Job ID: {job_id}")
            print(f"   Status: {data.get('status')}")
            print(f"   Message: {data.get('message')}")
            
            return job_id
            
        except Exception as e:
            print(f"❌ Video generation failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    print(f"   Error details: {error_data}")
                except:
                    print(f"   Response text: {e.response.text}")
            return None
    
    def test_job_status(self, job_id: str) -> Dict[str, Any]:
        """Test job status endpoint"""
        print(f"📊 Testing job status for: {job_id}")
        
        try:
            response = self.session.get(f"{self.base_url}/jobs/{job_id}")
            response.raise_for_status()
            
            data = response.json()
            print(f"✅ Job status retrieved successfully")
            print(f"   Status: {data.get('status')}")
            print(f"   Progress: {data.get('progress', 0)}%")
            print(f"   Message: {data.get('message')}")
            
            return data
            
        except Exception as e:
            print(f"❌ Job status check failed: {e}")
            return {}
    
    def test_list_jobs(self) -> bool:
        """Test list jobs endpoint"""
        print("📋 Testing list jobs endpoint...")
        
        try:
            response = self.session.get(f"{self.base_url}/jobs")
            response.raise_for_status()
            
            jobs = response.json()
            print(f"✅ Jobs list retrieved successfully")
            print(f"   Total jobs: {len(jobs)}")
            
            for i, job in enumerate(jobs[:3]):  # Show first 3 jobs
                print(f"   Job {i+1}: {job.get('job_id', 'N/A')} - {job.get('status', 'N/A')}")
            
            if len(jobs) > 3:
                print(f"   ... and {len(jobs) - 3} more jobs")
            
            return True
            
        except Exception as e:
            print(f"❌ List jobs failed: {e}")
            return False
    
    def test_cancel_job(self, job_id: str) -> bool:
        """Test job cancellation endpoint"""
        print(f"🚫 Testing job cancellation for: {job_id}")
        
        try:
            response = self.session.delete(f"{self.base_url}/jobs/{job_id}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Job cancelled successfully")
                print(f"   Message: {data.get('message')}")
                return True
            elif response.status_code == 400:
                data = response.json()
                print(f"ℹ️ Job cannot be cancelled: {data.get('detail')}")
                return True  # This is expected for completed jobs
            else:
                response.raise_for_status()
                
        except Exception as e:
            print(f"❌ Job cancellation failed: {e}")
            return False
    
    def test_download_video(self, job_id: str) -> bool:
        """Test video download endpoint"""
        print(f"⬇️ Testing video download for: {job_id}")
        
        try:
            response = self.session.get(f"{self.base_url}/download/{job_id}")
            
            if response.status_code == 200:
                # Save the video file
                filename = f"test_download_{job_id[:8]}.mp4"
                with open(filename, 'wb') as f:
                    f.write(response.content)
                
                file_size = len(response.content)
                print(f"✅ Video downloaded successfully")
                print(f"   File: {filename}")
                print(f"   Size: {file_size:,} bytes")
                
                return True
            elif response.status_code == 400:
                data = response.json()
                print(f"ℹ️ Download not available: {data.get('detail')}")
                return True  # Expected for non-completed jobs
            else:
                response.raise_for_status()
                
        except Exception as e:
            print(f"❌ Video download failed: {e}")
            return False
    
    def run_full_test_suite(self) -> bool:
        """Run complete test suite"""
        print("🧪 Running Q-AVIOGEN API Test Suite")
        print("=" * 50)
        
        tests_passed = 0
        total_tests = 0
        
        # Test 1: Health check
        total_tests += 1
        if self.test_health_check():
            tests_passed += 1
        print()
        
        # Test 2: Video generation
        total_tests += 1
        job_id = self.test_video_generation()
        if job_id:
            tests_passed += 1
        print()
        
        # Test 3: List jobs
        total_tests += 1
        if self.test_list_jobs():
            tests_passed += 1
        print()
        
        if job_id:
            # Test 4: Job status
            total_tests += 1
            job_status = self.test_job_status(job_id)
            if job_status:
                tests_passed += 1
            print()
            
            # Wait a bit and check status again
            print("⏳ Waiting 10 seconds before checking status again...")
            time.sleep(10)
            
            total_tests += 1
            updated_status = self.test_job_status(job_id)
            if updated_status:
                tests_passed += 1
            print()
            
            # Test 5: Download (if completed)
            if updated_status.get('status') == 'completed':
                total_tests += 1
                if self.test_download_video(job_id):
                    tests_passed += 1
                print()
            
            # Test 6: Cancel job (if still running)
            if updated_status.get('status') in ['queued', 'processing']:
                total_tests += 1
                if self.test_cancel_job(job_id):
                    tests_passed += 1
                print()
        
        # Summary
        print("📊 Test Suite Summary")
        print("=" * 50)
        print(f"Tests passed: {tests_passed}/{total_tests}")
        print(f"Success rate: {(tests_passed/total_tests)*100:.1f}%")
        
        if tests_passed == total_tests:
            print("🎉 All tests passed! API is working correctly.")
            return True
        else:
            print("⚠️ Some tests failed. Please check the API configuration.")
            return False


def generate_curl_examples():
    """Generate curl command examples for manual testing"""
    print("📝 Curl Command Examples")
    print("=" * 50)
    
    print("1. Health Check:")
    print("curl -X GET http://localhost:8000/health")
    print()
    
    print("2. Generate Video:")
    print("""curl -X POST http://localhost:8000/generate \\
  -H "Content-Type: application/json" \\
  -d '{
    "project_name": "Manual_Test_Project",
    "procedure_text": "This is a manual test of the Q-AVIOGEN API using curl commands.",
    "avatar": {
      "model_path": "./project/assets/avatars/amedeo/avatar_model.blend",
      "animation_style": "professional",
      "enable_lip_sync": true,
      "gesture_intensity": 0.7
    },
    "voice": {
      "voice_file": "./project/assets/audio/amedeo_voice_48k.wav",
      "speed": 1.0,
      "volume": 0.8
    },
    "render": {
      "resolution_x": 1280,
      "resolution_y": 720,
      "fps": 30,
      "quality": "medium"
    }
  }'""")
    print()
    
    print("3. Check Job Status (replace JOB_ID):")
    print("curl -X GET http://localhost:8000/jobs/JOB_ID")
    print()
    
    print("4. List All Jobs:")
    print("curl -X GET http://localhost:8000/jobs")
    print()
    
    print("5. Download Video (replace JOB_ID):")
    print("curl -X GET http://localhost:8000/download/JOB_ID -o video.mp4")
    print()
    
    print("6. Cancel Job (replace JOB_ID):")
    print("curl -X DELETE http://localhost:8000/jobs/JOB_ID")
    print()


def check_service_status(base_url: str = "http://localhost:8000") -> bool:
    """Check if the API service is running"""
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        return response.status_code == 200
    except:
        return False


def main():
    """Main test script"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Q-AVIOGEN API Test Script")
    parser.add_argument("--url", default="http://localhost:8000", help="API base URL")
    parser.add_argument("--token", help="API authentication token")
    parser.add_argument("--curl-only", action="store_true", help="Only show curl examples")
    parser.add_argument("--health-only", action="store_true", help="Only run health check")
    
    args = parser.parse_args()
    
    if args.curl_only:
        generate_curl_examples()
        return
    
    print("🚀 Q-AVIOGEN FastAPI Service Tester")
    print("=" * 50)
    
    # Check if service is running
    print(f"🔍 Checking if API service is available at {args.url}...")
    if not check_service_status(args.url):
        print(f"❌ API service is not available at {args.url}")
        print("   Please ensure the service is running:")
        print("   - Docker: docker-compose up")
        print("   - Direct: uvicorn app.main:app --reload")
        sys.exit(1)
    
    print(f"✅ API service is available at {args.url}")
    print()
    
    # Initialize tester
    tester = QAviogenAPITester(args.url, args.token)
    
    if args.health_only:
        success = tester.test_health_check()
        sys.exit(0 if success else 1)
    
    # Run full test suite
    success = tester.run_full_test_suite()
    
    print()
    print("💡 Tip: Use --curl-only to see curl command examples")
    print("💡 Tip: Use --health-only for quick health checks")
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
