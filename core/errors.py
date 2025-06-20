"""
Q-AVIOGEN Error Management System - Enhanced
Sistema avanzado de gestión de errores y logging para producción.
Incluye excepciones personalizadas, códigos de error, logging JSON, y decoradores.
Version: 2.0 - Enterprise Grade
"""

import logging
import json
import traceback
from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional, Callable, List
from functools import wraps
from pathlib import Path
import sys
import os

class ErrorCode(Enum):
    """Códigos de error estándar para Q-AVIOGEN."""
    # Errores generales
    UNKNOWN_ERROR = "QAV-0001"
    CONFIGURATION_ERROR = "QAV-0002"
    VALIDATION_ERROR = "QAV-0003"
    FILE_NOT_FOUND = "QAV-0004"
    PERMISSION_ERROR = "QAV-0005"
    
    # Errores de renderizado
    BLENDER_NOT_FOUND = "QAV-1001"
    RENDER_FAILED = "QAV-1002"
    SCENE_SETUP_ERROR = "QAV-1003"
    ASSET_LOADING_ERROR = "QAV-1004"
    MATERIAL_ERROR = "QAV-1005"
    ANIMATION_ERROR = "QAV-1006"
    CAMERA_ERROR = "QAV-1007"
    LIGHTING_ERROR = "QAV-1008"
    
    # Errores de parsing
    MARKDOWN_PARSE_ERROR = "QAV-2001"
    YAML_PARSE_ERROR = "QAV-2002"
    JSON_PARSE_ERROR = "QAV-2003"
    SCHEMA_VALIDATION_ERROR = "QAV-2004"
    
    # Errores de TTS
    TTS_ENGINE_ERROR = "QAV-3001"
    AUDIO_GENERATION_ERROR = "QAV-3002"
    AUDIO_FORMAT_ERROR = "QAV-3003"
    
    # Errores de sistema
    MEMORY_ERROR = "QAV-4001"
    GPU_ERROR = "QAV-4002"
    DISK_SPACE_ERROR = "QAV-4003"
    NETWORK_ERROR = "QAV-4004"
    
    # Códigos de compatibilidad (legacy)
    ASSET_NOT_FOUND = "QAV-1004"  # Alias para ASSET_LOADING_ERROR
    ASSET_IMPORT_FAILED = "QAV-1004"
    INVALID_ASSET_FORMAT = "QAV-1004"
    INVALID_SCENE_CONFIG = "QAV-0002"
    MISSING_CAMERA_CONFIG = "QAV-1007"
    INVALID_ANIMATION_TARGET = "QAV-1006"
    BLENDER_NOT_AVAILABLE = "QAV-1001"
    GPU_NOT_AVAILABLE = "QAV-4002"
    INSUFFICIENT_MEMORY = "QAV-4001"
    AUDIO_FILE_NOT_FOUND = "QAV-3002"
    AUDIO_SYNC_FAILED = "QAV-3002"
    TTS_ENGINE_FAILED = "QAV-3001"
    OUTPUT_DIR_NOT_WRITABLE = "QAV-0005"
    DISK_SPACE_INSUFFICIENT = "QAV-4003"
    PYTHON_VERSION_INCOMPATIBLE = "QAV-4001"
    DEPENDENCY_MISSING = "QAV-4001"

class ErrorLevel(Enum):
    """Error severity levels"""
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class QAviongenError(Exception):
    """Excepción base para todas las excepciones de Q-AVIOGEN."""
    
    def __init__(
        self,
        message: str,
        error_code: ErrorCode = ErrorCode.UNKNOWN_ERROR,
        context: Optional[Dict[str, Any]] = None,
        original_exception: Optional[Exception] = None
    ):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.context = context or {}
        self.original_exception = original_exception
        self.timestamp = datetime.now()
        
    def to_dict(self) -> Dict[str, Any]:
        """Convierte la excepción a diccionario para logging."""
        return {
            "error_code": self.error_code.value,
            "message": self.message,
            "context": self.context,
            "timestamp": self.timestamp.isoformat(),
            "original_exception": str(self.original_exception) if self.original_exception else None,
            "traceback": traceback.format_exc() if self.original_exception else None
        }


class ConfigurationError(QAviongenError):
    """Error de configuración."""
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None):
        super().__init__(message, ErrorCode.CONFIGURATION_ERROR, context)


class ValidationError(QAviongenError):
    """Error de validación de datos."""
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None):
        super().__init__(message, ErrorCode.VALIDATION_ERROR, context)


class RenderError(QAviongenError):
    """Error de renderizado."""
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None):
        super().__init__(message, ErrorCode.RENDER_FAILED, context)


class BlenderError(QAviongenError):
    """Error específico de Blender."""
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None):
        super().__init__(message, ErrorCode.BLENDER_NOT_FOUND, context)


class AssetError(QAviongenError):
    """Error de carga de assets."""
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None):
        super().__init__(message, ErrorCode.ASSET_LOADING_ERROR, context)


class ParseError(QAviongenError):
    """Error de parsing de documentos."""
    def __init__(self, message: str, error_code: ErrorCode, context: Optional[Dict[str, Any]] = None):
        super().__init__(message, error_code, context)


class TTSError(QAviongenError):
    """Error de Text-to-Speech."""
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None):
        super().__init__(message, ErrorCode.TTS_ENGINE_ERROR, context)


class QAviongenJSONFormatter(logging.Formatter):
    """Formateador JSON para logs de Q-AVIOGEN."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Formatea el record de log como JSON."""
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "thread": record.thread,
            "process": record.process
        }
        
        # Agregar contexto extra si existe
        if hasattr(record, 'context'):
            log_data['context'] = record.context
        
        # Agregar información de excepción si existe
        if record.exc_info:
            log_data['exception'] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": self.formatException(record.exc_info)
            }
        
        # Agregar información específica de Q-AVIOGEN si es una QAviongenError
        if hasattr(record, 'qav_error') and isinstance(record.qav_error, QAviongenError):
            log_data['qav_error'] = record.qav_error.to_dict()
        
        return json.dumps(log_data, ensure_ascii=False, indent=None)


class QAviongenLogger:
    """Logger avanzado para Q-AVIOGEN con soporte para JSON y contexto."""
    
    def __init__(self, name: str = "Q-AVIOGEN"):
        self.logger = logging.getLogger(name)
        self.setup_logger()
    
    def setup_logger(self):
        """Configura el logger con formateadores apropiados."""
        if self.logger.handlers:
            return  # Ya configurado
        
        self.logger.setLevel(logging.DEBUG)
        
        # Handler para consola (formato humano)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # Handler para archivo JSON
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        file_handler = logging.FileHandler(
            log_dir / f"qaviongen_{datetime.now().strftime('%Y%m%d')}.json",
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(QAviongenJSONFormatter())
        self.logger.addHandler(file_handler)
    
    def debug(self, message: str, context: Optional[Dict[str, Any]] = None):
        """Log debug con contexto."""
        extra = {'context': context} if context else {}
        self.logger.debug(message, extra=extra)
    
    def info(self, message: str, context: Optional[Dict[str, Any]] = None):
        """Log info con contexto."""
        extra = {'context': context} if context else {}
        self.logger.info(message, extra=extra)
    
    def warning(self, message: str, context: Optional[Dict[str, Any]] = None):
        """Log warning con contexto."""
        extra = {'context': context} if context else {}
        self.logger.warning(message, extra=extra)
    
    def error(self, message: str, context: Optional[Dict[str, Any]] = None, exception: Optional[Exception] = None):
        """Log error con contexto y excepción."""
        extra = {'context': context} if context else {}
        if exception and isinstance(exception, QAviongenError):
            extra['qav_error'] = exception
        self.logger.error(message, extra=extra, exc_info=exception is not None)
    
    def critical(self, message: str, context: Optional[Dict[str, Any]] = None, exception: Optional[Exception] = None):
        """Log critical con contexto y excepción."""
        extra = {'context': context} if context else {}
        if exception and isinstance(exception, QAviongenError):
            extra['qav_error'] = exception
        self.logger.critical(message, extra=extra, exc_info=exception is not None)
    
    def log_render_start(self, scene_name: str, output_path: str):
        """Log especializado para inicio de renderizado."""
        self.info("Render started", {
            "scene_name": scene_name,
            "output_path": output_path,
            "action": "render_start"
        })
    
    def log_render_complete(self, scene_name: str, output_path: str, duration: float, frame_count: int):
        """Log especializado para finalización de renderizado."""
        self.info("Render completed", {
            "scene_name": scene_name,
            "output_path": output_path,
            "duration_seconds": duration,
            "frame_count": frame_count,
            "fps": frame_count / duration if duration > 0 else 0,
            "action": "render_complete"
        })
    
    def log_asset_loaded(self, asset_path: str, asset_type: str):
        """Log especializado para carga de assets."""
        self.debug("Asset loaded", {
            "asset_path": asset_path,
            "asset_type": asset_type,
            "action": "asset_load"
        })
    
    def log_validation_error(self, errors: List[str], config_path: Optional[str] = None):
        """Log especializado para errores de validación."""
        self.error("Validation failed", {
            "errors": errors,
            "config_path": config_path,
            "action": "validation_failed"
        })


# Instancia global del logger
logger = QAviongenLogger()


def handle_exceptions(
    error_code: ErrorCode = ErrorCode.UNKNOWN_ERROR,
    reraise: bool = True,
    log_level: str = "error"
):
    """
    Decorador para manejo automático de excepciones.
    
    Args:
        error_code: Código de error a asignar si no es una QAviongenError
        reraise: Si True, relanza la excepción después de loggear
        log_level: Nivel de log a usar
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except QAviongenError as e:
                # Ya es una excepción de Q-AVIOGEN, solo loggear
                getattr(logger, log_level)(
                    f"Error in {func.__name__}: {e.message}",
                    context={"function": func.__name__, "args": str(args)[:200]},
                    exception=e
                )
                if reraise:
                    raise
                return None
            except Exception as e:
                # Envolver en QAviongenError
                qav_error = QAviongenError(
                    f"Unexpected error in {func.__name__}: {str(e)}",
                    error_code=error_code,
                    context={"function": func.__name__, "args": str(args)[:200]},
                    original_exception=e
                )
                getattr(logger, log_level)(
                    f"Unexpected error in {func.__name__}",
                    context={"function": func.__name__},
                    exception=qav_error
                )
                if reraise:
                    raise qav_error
                return None
        return wrapper
    return decorator


def log_performance(log_args: bool = False):
    """
    Decorador para logging de rendimiento.
    
    Args:
        log_args: Si True, incluye argumentos en el log
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = datetime.now()
            
            context = {
                "function": func.__name__,
                "start_time": start_time.isoformat()
            }
            
            if log_args:
                context["args"] = str(args)[:200]
                context["kwargs"] = str(kwargs)[:200]
            
            logger.debug(f"Starting {func.__name__}", context)
            
            try:
                result = func(*args, **kwargs)
                
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                
                logger.debug(f"Completed {func.__name__}", {
                    **context,
                    "end_time": end_time.isoformat(),
                    "duration_seconds": duration,
                    "success": True
                })
                
                return result
                
            except Exception as e:
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                
                logger.error(f"Failed {func.__name__}", {
                    **context,
                    "end_time": end_time.isoformat(),
                    "duration_seconds": duration,
                    "success": False,
                    "error": str(e)
                }, exception=e)
                
                raise
        
        return wrapper
    return decorator


def validate_input(validation_func: Callable[[Any], bool], error_message: str = "Invalid input"):
    """
    Decorador para validación de entrada.
    
    Args:
        validation_func: Función que retorna True si la entrada es válida
        error_message: Mensaje de error si la validación falla
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not validation_func(*args, **kwargs):
                raise ValidationError(
                    f"{error_message} in {func.__name__}",
                    context={"function": func.__name__, "args": str(args)[:200]}
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator


def require_blender(func: Callable) -> Callable:
    """Decorador que verifica que Blender esté disponible."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            import bpy
        except ImportError:
            raise BlenderError(
                f"Blender not available for {func.__name__}",
                context={"function": func.__name__}
            )
        return func(*args, **kwargs)
    return wrapper


def safe_file_operation(func: Callable) -> Callable:
    """Decorador para operaciones de archivo seguras."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as e:
            raise QAviongenError(
                f"File not found in {func.__name__}: {str(e)}",
                ErrorCode.FILE_NOT_FOUND,
                context={"function": func.__name__, "original_error": str(e)}
            )
        except PermissionError as e:
            raise QAviongenError(
                f"Permission denied in {func.__name__}: {str(e)}",
                ErrorCode.PERMISSION_ERROR,
                context={"function": func.__name__, "original_error": str(e)}
            )
        except OSError as e:
            raise QAviongenError(
                f"OS error in {func.__name__}: {str(e)}",
                ErrorCode.UNKNOWN_ERROR,
                context={"function": func.__name__, "original_error": str(e)}
            )
    return wrapper


class ErrorCollector:
    """Colector de errores para operaciones batch."""
    
    def __init__(self):
        self.errors: List[QAviongenError] = []
        self.warnings: List[str] = []
    
    def add_error(self, error: QAviongenError):
        """Agrega un error al colector."""
        self.errors.append(error)
        logger.error(error.message, exception=error)
    
    def add_warning(self, warning: str, context: Optional[Dict[str, Any]] = None):
        """Agrega un warning al colector."""
        self.warnings.append(warning)
        logger.warning(warning, context)
    
    def has_errors(self) -> bool:
        """Retorna True si hay errores."""
        return len(self.errors) > 0
    
    def has_warnings(self) -> bool:
        """Retorna True si hay warnings."""
        return len(self.warnings) > 0
    
    def get_summary(self) -> Dict[str, Any]:
        """Retorna un resumen de errores y warnings."""
        return {
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "errors": [e.to_dict() for e in self.errors],
            "warnings": self.warnings
        }
    
    def clear(self):
        """Limpia todos los errores y warnings."""
        self.errors.clear()
        self.warnings.clear()


# Utilidades de logging rápido
def log_debug(message: str, **kwargs):
    """Logging debug rápido."""
    logger.debug(message, kwargs if kwargs else None)

def log_info(message: str, **kwargs):
    """Logging info rápido."""
    logger.info(message, kwargs if kwargs else None)

def log_warning(message: str, **kwargs):
    """Logging warning rápido."""
    logger.warning(message, kwargs if kwargs else None)

def log_error(message: str, exception: Optional[Exception] = None, **kwargs):
    """Logging error rápido."""
    logger.error(message, kwargs if kwargs else None, exception)

def log_critical(message: str, exception: Optional[Exception] = None, **kwargs):
    """Logging critical rápido."""
    logger.critical(message, kwargs if kwargs else None, exception)
