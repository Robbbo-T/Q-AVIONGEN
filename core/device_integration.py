"""
Q-AVIOGEN Device Integration Framework
====================================

Provides seamless integration with external devices, sensors, and systems.
Supports real-time data streaming, device control, and automated video generation
based on device events and data patterns.

Features:
- Universal device connectivity (USB, Bluetooth, WiFi, Serial, Network)
- Real-time sensor data streaming and processing
- Device event-driven video generation
- Multi-protocol support (MQTT, WebSocket, REST, gRPC)
- Device discovery and auto-configuration
- Health monitoring and diagnostics
- Security and authentication
- Edge computing capabilities

Author: Q-AVIOGEN Team
Version: 1.0.0
Date: 2025-01-21
License: Q-AVIOGEN Enterprise
"""

from typing import Dict, List, Optional, AsyncGenerator, Union, Any, Callable
from dataclasses import dataclass, field
from enum import Enum, auto
import asyncio
import json
import uuid
import time
from datetime import datetime, timezone
import logging
import hashlib
import aiohttp
import websockets
from pathlib import Path
import numpy as np

# Import Q-AVIOGEN core modules
import sys
sys.path.append(str(Path(__file__).parent.parent))

from core.types_v2_1_clean import (
    SceneDescription, AnimationKeyframe, RenderConfig,
    VideoMetadata, QualityLevel, OutputFormat
)

# ============================================================================
# Device Integration Types and Enums
# ============================================================================

class DeviceType(Enum):
    """Supported device types"""
    SENSOR = "sensor"
    ACTUATOR = "actuator"
    CAMERA = "camera"
    MICROPHONE = "microphone"
    CONTROLLER = "controller"
    DISPLAY = "display"
    IOT_DEVICE = "iot_device"
    AIRCRAFT_SYSTEM = "aircraft_system"
    GROUND_EQUIPMENT = "ground_equipment"
    TEST_EQUIPMENT = "test_equipment"
    MOBILE_DEVICE = "mobile_device"
    COMPUTER = "computer"
    NETWORK_DEVICE = "network_device"

class ConnectionType(Enum):
    """Device connection protocols"""
    USB = "usb"
    BLUETOOTH = "bluetooth"
    WIFI = "wifi"
    ETHERNET = "ethernet"
    SERIAL = "serial"
    MQTT = "mqtt"
    WEBSOCKET = "websocket"
    REST_API = "rest_api"
    GRPC = "grpc"
    MODBUS = "modbus"
    CAN_BUS = "can_bus"
    ARINC_429 = "arinc_429"
    MILSTD_1553 = "milstd_1553"

class DeviceStatus(Enum):
    """Device operational status"""
    ONLINE = "online"
    OFFLINE = "offline"
    CONNECTING = "connecting"
    ERROR = "error"
    MAINTENANCE = "maintenance"
    CALIBRATING = "calibrating"
    DEGRADED = "degraded"
    UNKNOWN = "unknown"

class DataType(Enum):
    """Data types from devices"""
    NUMERIC = "numeric"
    TEXT = "text"
    BINARY = "binary"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    JSON = "json"
    XML = "xml"
    CUSTOM = "custom"

@dataclass
class DeviceData:
    """Standardized device data structure"""
    device_id: str
    timestamp: datetime
    data_type: DataType
    value: Any
    unit: Optional[str] = None
    quality: float = 1.0  # 0.0 to 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        return {
            'device_id': self.device_id,
            'timestamp': self.timestamp.isoformat(),
            'data_type': self.data_type.value,
            'value': self.value,
            'unit': self.unit,
            'quality': self.quality,
            'metadata': self.metadata
        }

@dataclass
class DeviceConfiguration:
    """Device configuration and capabilities"""
    device_id: str
    name: str
    device_type: DeviceType
    connection_type: ConnectionType
    endpoint: str  # Connection endpoint (URL, IP, port, etc.)
    capabilities: List[str] = field(default_factory=list)
    data_schema: Dict[str, Any] = field(default_factory=dict)
    polling_interval: float = 1.0  # seconds
    authentication: Optional[Dict[str, str]] = None
    settings: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        return {
            'device_id': self.device_id,
            'name': self.name,
            'device_type': self.device_type.value,
            'connection_type': self.connection_type.value,
            'endpoint': self.endpoint,
            'capabilities': self.capabilities,
            'data_schema': self.data_schema,
            'polling_interval': self.polling_interval,
            'authentication': self.authentication,
            'settings': self.settings,
            'enabled': self.enabled
        }

@dataclass
class DeviceEvent:
    """Device event for triggering actions"""
    event_id: str
    device_id: str
    event_type: str
    data: DeviceData
    severity: str = "info"  # info, warning, error, critical
    triggers_video: bool = False
    video_template: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class VideoGenerationRequest:
    """Request for video generation based on device data"""
    request_id: str
    device_event: DeviceEvent
    template_name: str
    scene_data: Dict[str, Any]
    output_path: str
    priority: int = 5  # 1-10 scale
    metadata: Dict[str, Any] = field(default_factory=dict)

# ============================================================================
# Device Interface Classes
# ============================================================================

class DeviceInterface:
    """Base class for device interfaces"""
    
    def __init__(self, config: DeviceConfiguration):
        self.config = config
        self.status = DeviceStatus.OFFLINE
        self.last_data = None
        self.error_count = 0
        self.logger = logging.getLogger(f"device.{config.device_id}")
        
    async def connect(self) -> bool:
        """Connect to the device"""
        raise NotImplementedError
        
    async def disconnect(self) -> bool:
        """Disconnect from the device"""
        raise NotImplementedError
        
    async def read_data(self) -> Optional[DeviceData]:
        """Read data from the device"""
        raise NotImplementedError
        
    async def write_data(self, data: Any) -> bool:
        """Write data to the device"""
        raise NotImplementedError
        
    async def get_status(self) -> DeviceStatus:
        """Get device status"""
        return self.status
        
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check"""
        return {
            'device_id': self.config.device_id,
            'status': self.status.value,
            'last_data_time': self.last_data.timestamp.isoformat() if self.last_data else None,
            'error_count': self.error_count
        }

class HTTPDevice(DeviceInterface):
    """HTTP/REST API device interface"""
    
    def __init__(self, config: DeviceConfiguration):
        super().__init__(config)
        self.session = None
        
    async def connect(self) -> bool:
        """Connect to HTTP device"""
        try:
            self.session = aiohttp.ClientSession()
            
            # Test connection with health endpoint
            health_url = f"{self.config.endpoint}/health"
            async with self.session.get(health_url) as response:
                if response.status == 200:
                    self.status = DeviceStatus.ONLINE
                    self.logger.info(f"Connected to HTTP device {self.config.device_id}")
                    return True
                    
        except Exception as e:
            self.logger.error(f"Failed to connect to HTTP device {self.config.device_id}: {e}")
            self.status = DeviceStatus.ERROR
            self.error_count += 1
            
        return False
        
    async def disconnect(self) -> bool:
        """Disconnect from HTTP device"""
        if self.session:
            await self.session.close()
            self.session = None
            
        self.status = DeviceStatus.OFFLINE
        return True
        
    async def read_data(self) -> Optional[DeviceData]:
        """Read data from HTTP device"""
        if not self.session or self.status != DeviceStatus.ONLINE:
            return None
            
        try:
            data_url = f"{self.config.endpoint}/data"
            headers = {}
            
            # Add authentication if configured
            if self.config.authentication:
                if 'api_key' in self.config.authentication:
                    headers['Authorization'] = f"Bearer {self.config.authentication['api_key']}"
                    
            async with self.session.get(data_url, headers=headers) as response:
                if response.status == 200:
                    raw_data = await response.json()
                    
                    # Parse based on device schema
                    device_data = DeviceData(
                        device_id=self.config.device_id,
                        timestamp=datetime.now(timezone.utc),
                        data_type=DataType.JSON,
                        value=raw_data,
                        metadata={'source': 'http_api'}
                    )
                    
                    self.last_data = device_data
                    return device_data
                    
        except Exception as e:
            self.logger.error(f"Error reading from HTTP device {self.config.device_id}: {e}")
            self.error_count += 1
            
        return None

class WebSocketDevice(DeviceInterface):
    """WebSocket device interface"""
    
    def __init__(self, config: DeviceConfiguration):
        super().__init__(config)
        self.websocket = None
        
    async def connect(self) -> bool:
        """Connect to WebSocket device"""
        try:
            self.websocket = await websockets.connect(self.config.endpoint)
            self.status = DeviceStatus.ONLINE
            self.logger.info(f"Connected to WebSocket device {self.config.device_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to connect to WebSocket device {self.config.device_id}: {e}")
            self.status = DeviceStatus.ERROR
            self.error_count += 1
            return False
            
    async def disconnect(self) -> bool:
        """Disconnect from WebSocket device"""
        if self.websocket:
            await self.websocket.close()
            self.websocket = None
            
        self.status = DeviceStatus.OFFLINE
        return True
        
    async def read_data(self) -> Optional[DeviceData]:
        """Read data from WebSocket device"""
        if not self.websocket or self.status != DeviceStatus.ONLINE:
            return None
            
        try:
            # Read with timeout
            raw_message = await asyncio.wait_for(
                self.websocket.recv(), 
                timeout=self.config.polling_interval
            )
            
            # Parse JSON message
            message_data = json.loads(raw_message)
            
            device_data = DeviceData(
                device_id=self.config.device_id,
                timestamp=datetime.now(timezone.utc),
                data_type=DataType.JSON,
                value=message_data,
                metadata={'source': 'websocket'}
            )
            
            self.last_data = device_data
            return device_data
            
        except asyncio.TimeoutError:
            # Timeout is normal for polling
            return None
        except Exception as e:
            self.logger.error(f"Error reading from WebSocket device {self.config.device_id}: {e}")
            self.error_count += 1
            
        return None

class MQTTDevice(DeviceInterface):
    """MQTT device interface"""
    
    def __init__(self, config: DeviceConfiguration):
        super().__init__(config)
        self.client = None
        self.data_queue = asyncio.Queue()
        
    async def connect(self) -> bool:
        """Connect to MQTT device"""
        try:
            import aiomqtt
            
            # Parse MQTT broker details
            broker_parts = self.config.endpoint.split(':')
            host = broker_parts[0]
            port = int(broker_parts[1]) if len(broker_parts) > 1 else 1883
            
            self.client = aiomqtt.Client(hostname=host, port=port)
            await self.client.__aenter__()
            
            # Subscribe to device topic
            topic = f"devices/{self.config.device_id}/data"
            await self.client.subscribe(topic)
            
            self.status = DeviceStatus.ONLINE
            self.logger.info(f"Connected to MQTT device {self.config.device_id}")
            
            # Start message listener
            asyncio.create_task(self._mqtt_listener())
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to connect to MQTT device {self.config.device_id}: {e}")
            self.status = DeviceStatus.ERROR
            self.error_count += 1
            return False
            
    async def disconnect(self) -> bool:
        """Disconnect from MQTT device"""
        if self.client:
            await self.client.__aexit__(None, None, None)
            self.client = None
            
        self.status = DeviceStatus.OFFLINE
        return True
        
    async def _mqtt_listener(self):
        """Listen for MQTT messages"""
        try:
            async for message in self.client.messages:
                # Parse message payload
                payload = json.loads(message.payload.decode())
                
                device_data = DeviceData(
                    device_id=self.config.device_id,
                    timestamp=datetime.now(timezone.utc),
                    data_type=DataType.JSON,
                    value=payload,
                    metadata={'source': 'mqtt', 'topic': str(message.topic)}
                )
                
                await self.data_queue.put(device_data)
                
        except Exception as e:
            self.logger.error(f"MQTT listener error for device {self.config.device_id}: {e}")
            
    async def read_data(self) -> Optional[DeviceData]:
        """Read data from MQTT device"""
        try:
            # Non-blocking queue read
            device_data = self.data_queue.get_nowait()
            self.last_data = device_data
            return device_data
            
        except asyncio.QueueEmpty:
            return None

# ============================================================================
# Device Manager
# ============================================================================

class DeviceManager:
    """Manages all device connections and data streams"""
    
    def __init__(self, config_file: str = "config/devices.json"):
        self.config_file = Path(config_file)
        self.devices: Dict[str, DeviceInterface] = {}
        self.device_configs: Dict[str, DeviceConfiguration] = {}
        self.data_callbacks: List[Callable] = []
        self.event_callbacks: List[Callable] = []
        self.logger = logging.getLogger(__name__)
        self.running = False
        
        # Load device configurations
        self.load_device_configs()
        
    def load_device_configs(self):
        """Load device configurations from file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    config_data = json.load(f)
                    
                for device_data in config_data.get('devices', []):
                    config = DeviceConfiguration(
                        device_id=device_data['device_id'],
                        name=device_data['name'],
                        device_type=DeviceType(device_data['device_type']),
                        connection_type=ConnectionType(device_data['connection_type']),
                        endpoint=device_data['endpoint'],
                        capabilities=device_data.get('capabilities', []),
                        data_schema=device_data.get('data_schema', {}),
                        polling_interval=device_data.get('polling_interval', 1.0),
                        authentication=device_data.get('authentication'),
                        settings=device_data.get('settings', {}),
                        enabled=device_data.get('enabled', True)
                    )
                    
                    self.device_configs[config.device_id] = config
                    
                self.logger.info(f"Loaded {len(self.device_configs)} device configurations")
                
        except Exception as e:
            self.logger.error(f"Error loading device configurations: {e}")
            
    def save_device_configs(self):
        """Save device configurations to file"""
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            
            config_data = {
                'devices': [config.to_dict() for config in self.device_configs.values()]
            }
            
            with open(self.config_file, 'w') as f:
                json.dump(config_data, f, indent=2)
                
            self.logger.info("Saved device configurations")
            
        except Exception as e:
            self.logger.error(f"Error saving device configurations: {e}")
            
    def add_device(self, config: DeviceConfiguration):
        """Add a new device configuration"""
        self.device_configs[config.device_id] = config
        self.save_device_configs()
        
        if config.enabled and self.running:
            # Auto-connect if manager is running
            asyncio.create_task(self.connect_device(config.device_id))
            
    def remove_device(self, device_id: str):
        """Remove a device configuration"""
        if device_id in self.device_configs:
            # Disconnect if connected
            if device_id in self.devices:
                asyncio.create_task(self.disconnect_device(device_id))
                
            del self.device_configs[device_id]
            self.save_device_configs()
            
    def get_device_interface(self, config: DeviceConfiguration) -> DeviceInterface:
        """Create appropriate device interface"""
        if config.connection_type == ConnectionType.REST_API:
            return HTTPDevice(config)
        elif config.connection_type == ConnectionType.WEBSOCKET:
            return WebSocketDevice(config)
        elif config.connection_type == ConnectionType.MQTT:
            return MQTTDevice(config)
        else:
            raise NotImplementedError(f"Connection type {config.connection_type} not implemented")
            
    async def connect_device(self, device_id: str) -> bool:
        """Connect to a specific device"""
        if device_id not in self.device_configs:
            self.logger.error(f"Device {device_id} not configured")
            return False
            
        config = self.device_configs[device_id]
        if not config.enabled:
            self.logger.info(f"Device {device_id} is disabled")
            return False
            
        try:
            device_interface = self.get_device_interface(config)
            
            if await device_interface.connect():
                self.devices[device_id] = device_interface
                self.logger.info(f"Connected to device {device_id}")
                return True
                
        except Exception as e:
            self.logger.error(f"Error connecting to device {device_id}: {e}")
            
        return False
        
    async def disconnect_device(self, device_id: str) -> bool:
        """Disconnect from a specific device"""
        if device_id in self.devices:
            try:
                await self.devices[device_id].disconnect()
                del self.devices[device_id]
                self.logger.info(f"Disconnected from device {device_id}")
                return True
                
            except Exception as e:
                self.logger.error(f"Error disconnecting from device {device_id}: {e}")
                
        return False
        
    async def start(self):
        """Start the device manager"""
        self.running = True
        self.logger.info("Starting device manager")
        
        # Connect to all enabled devices
        connect_tasks = []
        for device_id, config in self.device_configs.items():
            if config.enabled:
                connect_tasks.append(self.connect_device(device_id))
                
        if connect_tasks:
            await asyncio.gather(*connect_tasks, return_exceptions=True)
            
        # Start data collection
        asyncio.create_task(self._data_collection_loop())
        
    async def stop(self):
        """Stop the device manager"""
        self.running = False
        self.logger.info("Stopping device manager")
        
        # Disconnect all devices
        disconnect_tasks = []
        for device_id in list(self.devices.keys()):
            disconnect_tasks.append(self.disconnect_device(device_id))
            
        if disconnect_tasks:
            await asyncio.gather(*disconnect_tasks, return_exceptions=True)
            
    async def _data_collection_loop(self):
        """Main data collection loop"""
        while self.running:
            try:
                # Read data from all connected devices
                for device_id, device_interface in self.devices.items():
                    try:
                        data = await device_interface.read_data()
                        if data:
                            # Process data through callbacks
                            for callback in self.data_callbacks:
                                try:
                                    await callback(data)
                                except Exception as e:
                                    self.logger.error(f"Data callback error: {e}")
                                    
                    except Exception as e:
                        self.logger.error(f"Error reading from device {device_id}: {e}")
                        
                # Sleep before next collection cycle
                await asyncio.sleep(0.1)  # 10Hz collection rate
                
            except Exception as e:
                self.logger.error(f"Data collection loop error: {e}")
                await asyncio.sleep(1.0)
                
    def add_data_callback(self, callback: Callable):
        """Add callback for device data"""
        self.data_callbacks.append(callback)
        
    def add_event_callback(self, callback: Callable):
        """Add callback for device events"""
        self.event_callbacks.append(callback)
        
    async def get_device_status(self, device_id: str) -> Optional[Dict]:
        """Get status of a specific device"""
        if device_id in self.devices:
            return await self.devices[device_id].health_check()
        return None
        
    async def get_all_device_status(self) -> Dict[str, Dict]:
        """Get status of all devices"""
        status_map = {}
        
        for device_id in self.device_configs:
            if device_id in self.devices:
                status_map[device_id] = await self.devices[device_id].health_check()
            else:
                status_map[device_id] = {
                    'device_id': device_id,
                    'status': 'offline',
                    'last_data_time': None,
                    'error_count': 0
                }
                
        return status_map

# ============================================================================
# Event Processing and Video Integration
# ============================================================================

class EventProcessor:
    """Processes device events and triggers video generation"""
    
    def __init__(self, device_manager: DeviceManager):
        self.device_manager = device_manager
        self.event_rules: List[Dict] = []
        self.video_queue: asyncio.Queue = asyncio.Queue()
        self.logger = logging.getLogger(__name__)
        
        # Load event rules
        self.load_event_rules()
        
        # Register as data callback
        self.device_manager.add_data_callback(self.process_device_data)
        
    def load_event_rules(self):
        """Load event processing rules"""
        try:
            rules_file = Path("config/event_rules.json")
            if rules_file.exists():
                with open(rules_file, 'r') as f:
                    self.event_rules = json.load(f).get('rules', [])
                    
                self.logger.info(f"Loaded {len(self.event_rules)} event rules")
                
        except Exception as e:
            self.logger.error(f"Error loading event rules: {e}")
            
    async def process_device_data(self, data: DeviceData):
        """Process device data and check for events"""
        try:
            # Check each rule against the data
            for rule in self.event_rules:
                if self._evaluate_rule(rule, data):
                    # Create event
                    event = DeviceEvent(
                        event_id=str(uuid.uuid4()),
                        device_id=data.device_id,
                        event_type=rule['event_type'],
                        data=data,
                        severity=rule.get('severity', 'info'),
                        triggers_video=rule.get('triggers_video', False),
                        video_template=rule.get('video_template'),
                        metadata=rule.get('metadata', {})
                    )
                    
                    # Process event
                    await self._process_event(event)
                    
        except Exception as e:
            self.logger.error(f"Error processing device data: {e}")
            
    def _evaluate_rule(self, rule: Dict, data: DeviceData) -> bool:
        """Evaluate if a rule matches the data"""
        try:
            # Device filter
            if 'device_id' in rule and rule['device_id'] != data.device_id:
                return False
                
            # Data type filter
            if 'data_type' in rule and rule['data_type'] != data.data_type.value:
                return False
                
            # Value conditions
            if 'conditions' in rule:
                for condition in rule['conditions']:
                    if not self._evaluate_condition(condition, data):
                        return False
                        
            return True
            
        except Exception as e:
            self.logger.error(f"Error evaluating rule: {e}")
            return False
            
    def _evaluate_condition(self, condition: Dict, data: DeviceData) -> bool:
        """Evaluate a single condition"""
        try:
            field = condition['field']
            operator = condition['operator']
            value = condition['value']
            
            # Get field value from data
            if field == 'value':
                data_value = data.value
            elif field == 'quality':
                data_value = data.quality
            elif field.startswith('metadata.'):
                metadata_key = field[9:]  # Remove 'metadata.' prefix
                data_value = data.metadata.get(metadata_key)
            else:
                return False
                
            # Evaluate condition
            if operator == 'eq':
                return data_value == value
            elif operator == 'ne':
                return data_value != value
            elif operator == 'gt':
                return data_value > value
            elif operator == 'gte':
                return data_value >= value
            elif operator == 'lt':
                return data_value < value
            elif operator == 'lte':
                return data_value <= value
            elif operator == 'contains':
                return value in str(data_value)
            elif operator == 'in':
                return data_value in value
                
        except Exception as e:
            self.logger.error(f"Error evaluating condition: {e}")
            
        return False
        
    async def _process_event(self, event: DeviceEvent):
        """Process a triggered event"""
        try:
            self.logger.info(f"Event triggered: {event.event_type} from device {event.device_id}")
            
            # Trigger callbacks
            for callback in self.device_manager.event_callbacks:
                try:
                    await callback(event)
                except Exception as e:
                    self.logger.error(f"Event callback error: {e}")
                    
            # Queue video generation if requested
            if event.triggers_video and event.video_template:
                video_request = VideoGenerationRequest(
                    request_id=str(uuid.uuid4()),
                    device_event=event,
                    template_name=event.video_template,
                    scene_data=self._build_scene_data(event),
                    output_path=f"output/device_videos/{event.event_id}.mp4",
                    metadata={
                        'event_type': event.event_type,
                        'device_id': event.device_id,
                        'timestamp': event.data.timestamp.isoformat()
                    }
                )
                
                await self.video_queue.put(video_request)
                
        except Exception as e:
            self.logger.error(f"Error processing event: {e}")
            
    def _build_scene_data(self, event: DeviceEvent) -> Dict[str, Any]:
        """Build scene data for video generation"""
        return {
            'device_data': event.data.to_dict(),
            'event_type': event.event_type,
            'severity': event.severity,
            'timestamp': event.data.timestamp.isoformat(),
            'device_id': event.device_id
        }

# ============================================================================
# Video Integration
# ============================================================================

class DeviceVideoIntegration:
    """Integrates device events with Q-AVIOGEN video generation"""
    
    def __init__(self, event_processor: EventProcessor):
        self.event_processor = event_processor
        self.logger = logging.getLogger(__name__)
        self.running = False
        
    async def start(self):
        """Start video integration processing"""
        self.running = True
        self.logger.info("Starting device video integration")
        
        # Start video generation loop
        asyncio.create_task(self._video_generation_loop())
        
    async def stop(self):
        """Stop video integration processing"""
        self.running = False
        self.logger.info("Stopping device video integration")
        
    async def _video_generation_loop(self):
        """Main video generation loop"""
        while self.running:
            try:
                # Wait for video requests
                request = await asyncio.wait_for(
                    self.event_processor.video_queue.get(),
                    timeout=1.0
                )
                
                # Process video generation request
                await self._generate_video(request)
                
            except asyncio.TimeoutError:
                # Timeout is normal for queue polling
                continue
            except Exception as e:
                self.logger.error(f"Video generation loop error: {e}")
                await asyncio.sleep(1.0)
                
    async def _generate_video(self, request: VideoGenerationRequest):
        """Generate video based on device event"""
        try:
            self.logger.info(f"Generating video for event {request.device_event.event_type}")
            
            # Load template
            template_path = Path(f"templates/device/{request.template_name}.md")
            if not template_path.exists():
                self.logger.error(f"Template not found: {template_path}")
                return
                
            # Import Q-AVIOGEN modules for video generation
            from parser.md_parser import MarkdownParser
            from parser.scene_builder import SceneBuilder
            from tts.narration import NarrationGenerator
            from blender.simulated_renderer import get_renderer_class
            
            # Parse template with device data
            parser = MarkdownParser()
            
            # Inject device data into template context
            template_context = {
                'device_data': request.scene_data,
                'event': request.device_event,
                'timestamp': datetime.now().isoformat()
            }
            
            parsed_content = parser.parse_file(str(template_path), context=template_context)
            
            # Build scene
            scene_builder = SceneBuilder()
            scene = scene_builder.build_scene(parsed_content)
            
            # Generate narration
            narration_gen = NarrationGenerator()
            audio_path = await narration_gen.generate_narration(
                parsed_content.get('narration', ''),
                f"temp/device_audio_{request.request_id}.wav"
            )
            
            # Render video
            renderer_class = get_renderer_class()
            renderer = renderer_class()
            
            output_path = Path(request.output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            await renderer.render_scene(
                scene=scene,
                audio_path=audio_path,
                output_path=str(output_path),
                quality=QualityLevel.HIGH
            )
            
            self.logger.info(f"Video generated successfully: {output_path}")
            
        except Exception as e:
            self.logger.error(f"Error generating video: {e}")

# ============================================================================
# Device Discovery
# ============================================================================

class DeviceDiscovery:
    """Automatic device discovery service"""
    
    def __init__(self, device_manager: DeviceManager):
        self.device_manager = device_manager
        self.logger = logging.getLogger(__name__)
        
    async def discover_network_devices(self) -> List[DeviceConfiguration]:
        """Discover devices on the network"""
        discovered = []
        
        try:
            # Network scan for common device ports
            common_ports = [80, 443, 8080, 8443, 1883, 8765]
            
            # Simple network discovery (can be enhanced)
            import ipaddress
            import socket
            
            # Get local network
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            network = ipaddress.IPv4Network(f"{local_ip}/24", strict=False)
            
            for ip in network:
                for port in common_ports:
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(0.1)
                        result = sock.connect_ex((str(ip), port))
                        
                        if result == 0:
                            # Potential device found
                            device_config = DeviceConfiguration(
                                device_id=f"discovered_{ip}_{port}",
                                name=f"Network Device {ip}:{port}",
                                device_type=DeviceType.NETWORK_DEVICE,
                                connection_type=ConnectionType.REST_API if port in [80, 443, 8080, 8443] else ConnectionType.MQTT,
                                endpoint=f"http://{ip}:{port}" if port in [80, 8080] else f"https://{ip}:{port}" if port in [443, 8443] else f"{ip}:{port}",
                                enabled=False  # Require manual enablement
                            )
                            discovered.append(device_config)
                            
                        sock.close()
                        
                    except Exception:
                        pass
                        
        except Exception as e:
            self.logger.error(f"Network discovery error: {e}")
            
        return discovered
        
    async def discover_usb_devices(self) -> List[DeviceConfiguration]:
        """Discover USB devices"""
        discovered = []
        
        try:
            import serial.tools.list_ports
            
            ports = serial.tools.list_ports.comports()
            for port in ports:
                device_config = DeviceConfiguration(
                    device_id=f"usb_{port.device.replace('/', '_')}",
                    name=f"USB Device {port.device}",
                    device_type=DeviceType.SENSOR,
                    connection_type=ConnectionType.SERIAL,
                    endpoint=port.device,
                    settings={
                        'baudrate': 9600,
                        'description': port.description,
                        'manufacturer': port.manufacturer
                    },
                    enabled=False
                )
                discovered.append(device_config)
                
        except ImportError:
            self.logger.warning("pyserial not available for USB discovery")
        except Exception as e:
            self.logger.error(f"USB discovery error: {e}")
            
        return discovered

# ============================================================================
# Main Integration Class
# ============================================================================

class QAviogenDeviceIntegration:
    """Main Q-AVIOGEN device integration orchestrator"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self.device_manager = DeviceManager(str(self.config_dir / "devices.json"))
        self.event_processor = EventProcessor(self.device_manager)
        self.video_integration = DeviceVideoIntegration(self.event_processor)
        self.discovery = DeviceDiscovery(self.device_manager)
        
        self.logger = logging.getLogger(__name__)
        
    async def start(self):
        """Start the complete integration system"""
        self.logger.info("Starting Q-AVIOGEN Device Integration")
        
        # Start components in order
        await self.device_manager.start()
        await self.video_integration.start()
        
        self.logger.info("Q-AVIOGEN Device Integration started successfully")
        
    async def stop(self):
        """Stop the complete integration system"""
        self.logger.info("Stopping Q-AVIOGEN Device Integration")
        
        # Stop components
        await self.video_integration.stop()
        await self.device_manager.stop()
        
        self.logger.info("Q-AVIOGEN Device Integration stopped")
        
    async def discover_devices(self) -> List[DeviceConfiguration]:
        """Discover available devices"""
        self.logger.info("Starting device discovery")
        
        network_devices = await self.discovery.discover_network_devices()
        usb_devices = await self.discovery.discover_usb_devices()
        
        all_discovered = network_devices + usb_devices
        
        self.logger.info(f"Discovered {len(all_discovered)} devices")
        
        return all_discovered
        
    def add_device(self, config: DeviceConfiguration):
        """Add a new device"""
        self.device_manager.add_device(config)
        
    def remove_device(self, device_id: str):
        """Remove a device"""
        self.device_manager.remove_device(device_id)
        
    async def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status"""
        device_status = await self.device_manager.get_all_device_status()
        
        return {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'devices': device_status,
            'total_devices': len(self.device_manager.device_configs),
            'online_devices': len([s for s in device_status.values() if s['status'] == 'online']),
            'event_queue_size': self.event_processor.video_queue.qsize()
        }

# ============================================================================
# Example Usage and Testing
# ============================================================================

async def main():
    """Example usage of the device integration system"""
    
    # Initialize logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Initialize integration system
    integration = QAviogenDeviceIntegration()
    
    try:
        # Discover devices
        discovered = await integration.discover_devices()
        print(f"Discovered {len(discovered)} devices")
        
        # Add example device configurations
        example_devices = [
            DeviceConfiguration(
                device_id="weather_station_001",
                name="Weather Station #1",
                device_type=DeviceType.SENSOR,
                connection_type=ConnectionType.REST_API,
                endpoint="http://192.168.1.100:8080",
                capabilities=["temperature", "humidity", "pressure", "wind"],
                polling_interval=5.0,
                enabled=True
            ),
            DeviceConfiguration(
                device_id="aircraft_telemetry_001",
                name="Aircraft Telemetry System",
                device_type=DeviceType.AIRCRAFT_SYSTEM,
                connection_type=ConnectionType.WEBSOCKET,
                endpoint="ws://telemetry.aircraft.local:8765",
                capabilities=["position", "altitude", "speed", "fuel"],
                polling_interval=1.0,
                enabled=True
            )
        ]
        
        for device in example_devices:
            integration.add_device(device)
            
        # Start the integration system
        await integration.start()
        
        # Run for a period
        print("Integration system running... Press Ctrl+C to stop")
        
        try:
            while True:
                # Get system status
                status = await integration.get_system_status()
                print(f"System Status: {status['online_devices']}/{status['total_devices']} devices online")
                
                await asyncio.sleep(10)
                
        except KeyboardInterrupt:
            print("\nShutting down...")
            
    finally:
        # Stop the integration system
        await integration.stop()

if __name__ == "__main__":
    asyncio.run(main())
