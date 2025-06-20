"""
Narration Generator - Text-to-Speech for procedure narration
Generador de narración usando diferentes motores de síntesis de voz
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod
from dataclasses import dataclass
import hashlib

@dataclass
class VoiceConfig:
    """Voice configuration settings"""
    voice_id: str = "default"
    language: str = "es-ES"
    speed: float = 1.0
    pitch: float = 1.0
    volume: float = 1.0
    
@dataclass
class AudioOutput:
    """Audio output configuration"""
    file_path: str
    format: str = "wav"
    sample_rate: int = 22050
    bit_depth: int = 16

class TTSEngine(ABC):
    """Abstract base class for TTS engines"""
    
    @abstractmethod
    def synthesize(self, text: str, output_path: str, voice_config: VoiceConfig) -> bool:
        """Synthesize text to speech and save to file"""
        pass
    
    @abstractmethod
    def get_available_voices(self) -> List[str]:
        """Get list of available voices"""
        pass

class PyttsxEngine(TTSEngine):
    """Offline TTS using pyttsx3"""
    
    def __init__(self):
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            self.available = True
        except ImportError:
            print("⚠️ pyttsx3 no está instalado. Use: pip install pyttsx3")
            self.available = False
        except Exception as e:
            print(f"⚠️ Error inicializando pyttsx3: {e}")
            self.available = False
    
    def synthesize(self, text: str, output_path: str, voice_config: VoiceConfig) -> bool:
        """Synthesize text using pyttsx3"""
        if not self.available:
            return False
        
        try:
            # Configure voice properties
            voices = self.engine.getProperty('voices')
            if voices:
                # Try to find Spanish voice
                spanish_voice = None
                for voice in voices:
                    if 'spanish' in voice.name.lower() or 'es' in voice.id.lower():
                        spanish_voice = voice
                        break
                
                if spanish_voice:
                    self.engine.setProperty('voice', spanish_voice.id)
            
            # Set speech rate and volume
            self.engine.setProperty('rate', int(200 * voice_config.speed))
            self.engine.setProperty('volume', voice_config.volume)
            
            # Save to file
            self.engine.save_to_file(text, output_path)
            self.engine.runAndWait()
            
            return os.path.exists(output_path)
            
        except Exception as e:
            print(f"❌ Error en síntesis pyttsx3: {e}")
            return False
    
    def get_available_voices(self) -> List[str]:
        """Get available voices from pyttsx3"""
        if not self.available:
            return []
        
        try:
            voices = self.engine.getProperty('voices')
            return [voice.name for voice in voices] if voices else []
        except:
            return []

class PollyEngine(TTSEngine):
    """AWS Polly TTS engine"""
    
    def __init__(self, region_name: str = 'us-east-1'):
        try:
            import boto3
            self.client = boto3.client('polly', region_name=region_name)
            self.available = True
        except ImportError:
            print("⚠️ boto3 no está instalado. Use: pip install boto3")
            self.available = False
        except Exception as e:
            print(f"⚠️ Error inicializando AWS Polly: {e}")
            self.available = False
    
    def synthesize(self, text: str, output_path: str, voice_config: VoiceConfig) -> bool:
        """Synthesize text using AWS Polly"""
        if not self.available:
            return False
        
        try:
            # Map language to Polly voice
            voice_mapping = {
                'es-ES': 'Conchita',
                'es-MX': 'Mia',
                'en-US': 'Matthew',
                'en-GB': 'Brian'
            }
            
            voice_id = voice_mapping.get(voice_config.language, 'Conchita')
            
            # Request synthesis
            response = self.client.synthesize_speech(
                Text=text,
                OutputFormat='mp3',
                VoiceId=voice_id,
                Engine='standard'
            )
            
            # Save audio stream to file
            with open(output_path, 'wb') as f:
                f.write(response['AudioStream'].read())
            
            return True
            
        except Exception as e:
            print(f"❌ Error en síntesis AWS Polly: {e}")
            return False
    
    def get_available_voices(self) -> List[str]:
        """Get available voices from AWS Polly"""
        if not self.available:
            return []
        
        try:
            response = self.client.describe_voices()
            return [voice['Id'] for voice in response['Voices']]
        except:
            return ['Conchita', 'Mia', 'Matthew', 'Brian']  # Default list

class ElevenLabsEngine(TTSEngine):
    """ElevenLabs TTS engine"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('ELEVENLABS_API_KEY')
        if not self.api_key:
            print("⚠️ ElevenLabs API key no encontrada. Configure ELEVENLABS_API_KEY")
            self.available = False
        else:
            try:
                import requests
                self.available = True
            except ImportError:
                print("⚠️ requests no está instalado. Use: pip install requests")
                self.available = False
    
    def synthesize(self, text: str, output_path: str, voice_config: VoiceConfig) -> bool:
        """Synthesize text using ElevenLabs"""
        if not self.available:
            return False
        
        try:
            import requests
            
            # ElevenLabs API endpoint
            voice_id = voice_config.voice_id or "21m00Tcm4TlvDq8ikWAM"  # Default voice
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.api_key
            }
            
            data = {
                "text": text,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.5,
                    "style": 0.5,
                    "use_speaker_boost": True
                }
            }
            
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                return True
            else:
                print(f"❌ Error ElevenLabs: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error en síntesis ElevenLabs: {e}")
            return False
    
    def get_available_voices(self) -> List[str]:
        """Get available voices from ElevenLabs"""
        if not self.available:
            return []
        
        try:
            import requests
            
            url = "https://api.elevenlabs.io/v1/voices"
            headers = {"xi-api-key": self.api_key}
            
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                voices = response.json()
                return [voice['voice_id'] for voice in voices.get('voices', [])]
            else:
                return ["21m00Tcm4TlvDq8ikWAM"]  # Default voice
                
        except:
            return ["21m00Tcm4TlvDq8ikWAM"]  # Default voice

class NarrationGenerator:
    """Main narration generator class"""
    
    def __init__(self, engine: str = "pyttsx3", voice_config: Optional[VoiceConfig] = None):
        self.engine_name = engine
        self.voice_config = voice_config or VoiceConfig()
        self.cache_dir = Path("output/audio_cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize TTS engine
        self.engine = self._init_engine(engine)
        
    def _init_engine(self, engine_name: str) -> TTSEngine:
        """Initialize the specified TTS engine"""
        if engine_name == "pyttsx3":
            return PyttsxEngine()
        elif engine_name == "polly":
            return PollyEngine()
        elif engine_name == "elevenlabs":
            return ElevenLabsEngine()
        else:
            print(f"⚠️ Motor TTS desconocido: {engine_name}. Usando pyttsx3")
            return PyttsxEngine()
    
    def generate_narration(self, procedure_data: Dict[str, Any]) -> List[str]:
        """Generate narration audio files for all steps"""
        audio_files = []
        
        print(f"🗣️ Generando narración con {self.engine_name}")
        
        for step in procedure_data.get('steps', []):
            audio_file = self._generate_step_audio(step)
            if audio_file:
                audio_files.append(audio_file)
        
        return audio_files
    
    def _generate_step_audio(self, step: Dict[str, Any]) -> Optional[str]:
        """Generate audio for a single step"""
        step_id = step.get('id', 'unknown')
        narration_text = step.get('narration', step.get('description', ''))
        
        if not narration_text:
            print(f"⚠️ Sin texto de narración para {step_id}")
            return None
        
        # Check cache first
        cache_key = self._get_cache_key(narration_text)
        cached_file = self.cache_dir / f"{cache_key}.wav"
        
        if cached_file.exists():
            print(f"📦 Usando audio cacheado para {step_id}")
            # Copy to final location
            output_file = f"output/audio/{step_id}.wav"
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            import shutil
            shutil.copy2(cached_file, output_file)
            return output_file
        
        # Generate new audio
        output_file = f"output/audio/{step_id}.wav"
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        print(f"🎵 Generando audio para {step_id}: {narration_text[:50]}...")
        
        success = self.engine.synthesize(
            text=narration_text,
            output_path=output_file,
            voice_config=self.voice_config
        )
        
        if success:
            # Cache the result
            import shutil
            shutil.copy2(output_file, cached_file)
            print(f"✅ Audio generado: {output_file}")
            return output_file
        else:
            print(f"❌ Error generando audio para {step_id}")
            return None
    
    def _get_cache_key(self, text: str) -> str:
        """Generate cache key for text"""
        # Include voice config in hash for proper caching
        cache_content = f"{text}_{self.engine_name}_{self.voice_config.language}_{self.voice_config.voice_id}"
        return hashlib.md5(cache_content.encode()).hexdigest()
    
    def set_voice_config(self, voice_config: VoiceConfig) -> None:
        """Update voice configuration"""
        self.voice_config = voice_config
    
    def get_available_voices(self) -> List[str]:
        """Get list of available voices from current engine"""
        return self.engine.get_available_voices()
    
    def test_engine(self) -> bool:
        """Test if the current engine is working"""
        test_text = "Prueba de síntesis de voz."
        test_file = "output/audio/test.wav"
        
        os.makedirs(os.path.dirname(test_file), exist_ok=True)
        
        success = self.engine.synthesize(
            text=test_text,
            output_path=test_file,
            voice_config=self.voice_config
        )
        
        if success and os.path.exists(test_file):
            os.remove(test_file)  # Clean up
            return True
        
        return False

# Example usage and testing
if __name__ == "__main__":
    # Test different engines
    engines_to_test = ["pyttsx3"]  # Start with offline engine
    
    for engine_name in engines_to_test:
        print(f"\n🧪 Probando motor: {engine_name}")
        
        try:
            narration_gen = NarrationGenerator(engine=engine_name)
            
            # Test engine
            if narration_gen.test_engine():
                print(f"✅ Motor {engine_name} funcionando correctamente")
                
                # Get available voices
                voices = narration_gen.get_available_voices()
                print(f"🎙️ Voces disponibles: {len(voices)}")
                if voices:
                    print(f"   Ejemplos: {voices[:3]}")
                
                # Test with sample data
                sample_step = {
                    'id': 'test_step',
                    'narration': 'Esta es una prueba de generación de narración para procedimientos técnicos aeroespaciales.'
                }
                
                audio_file = narration_gen._generate_step_audio(sample_step)
                if audio_file:
                    print(f"🎵 Audio de prueba generado: {audio_file}")
                
            else:
                print(f"❌ Motor {engine_name} no funciona correctamente")
                
        except Exception as e:
            print(f"❌ Error probando {engine_name}: {e}")
    
    print("\n✅ Pruebas de narración completadas")
