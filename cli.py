#!/usr/bin/env python3
"""
Q-AVIOGEN Management CLI
Comprehensive command-line interface for managing the Q-AVIOGEN system
"""

import sys
import os
import argparse
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.errors import create_logger
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.panel import Panel
from rich.syntax import Syntax

console = Console()
logger = create_logger(__name__)

class QAviogenCLI:
    """Main CLI class for Q-AVIOGEN management"""
    
    def __init__(self):
        self.project_root = project_root
        self.logger = logger
        self.console = console
    
    def create_parser(self) -> argparse.ArgumentParser:
        """Create the main argument parser"""
        parser = argparse.ArgumentParser(
            description="Q-AVIOGEN Management CLI - Comprehensive aerospace video generation",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  %(prog)s generate --input procedure.md --output ./videos/
  %(prog)s batch --config batch_config.yaml
  %(prog)s test --suite integration
  %(prog)s deploy --environment staging
  %(prog)s status --verbose
        """
        )
        
        # Global options
        parser.add_argument('--verbose', '-v', action='store_true',
                          help='Enable verbose output')
        parser.add_argument('--debug', action='store_true',
                          help='Enable debug logging')
        parser.add_argument('--config', '-c', 
                          help='Configuration file path')
        
        # Subcommands
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Generate command
        self._add_generate_parser(subparsers)
        
        # Batch command
        self._add_batch_parser(subparsers)
        
        # Test command
        self._add_test_parser(subparsers)
        
        # Deploy command
        self._add_deploy_parser(subparsers)
        
        # Status command
        self._add_status_parser(subparsers)
        
        # Validate command
        self._add_validate_parser(subparsers)
        
        # Setup command
        self._add_setup_parser(subparsers)
        
        # Monitor command
        self._add_monitor_parser(subparsers)
        
        return parser
    
    def _add_generate_parser(self, subparsers):
        """Add generate command parser"""
        generate_parser = subparsers.add_parser(
            'generate', help='Generate video from procedure'
        )
        
        # Input options
        input_group = generate_parser.add_mutually_exclusive_group(required=True)
        input_group.add_argument('--input', '-i', 
                               help='Input Markdown file (.md)')
        input_group.add_argument('--yaml', '-y', 
                               help='Input YAML configuration file')
        
        # Output options
        generate_parser.add_argument('--output', '-o', 
                                   default='output/videos/',
                                   help='Output directory')
        generate_parser.add_argument('--format', '-f', 
                                   choices=['mp4', 'webm', 'mov', 'avi'],
                                   default='mp4',
                                   help='Output video format')
        
        # Quality options
        generate_parser.add_argument('--resolution', 
                                   choices=['720p', '1080p', '4k'],
                                   default='1080p',
                                   help='Video resolution')
        generate_parser.add_argument('--quality', 
                                   choices=['low', 'medium', 'high', 'ultra'],
                                   default='high',
                                   help='Rendering quality')
        
        # TTS options
        generate_parser.add_argument('--tts-engine', 
                                   choices=['pyttsx3', 'aws_polly', 'elevenlabs'],
                                   default='pyttsx3',
                                   help='Text-to-speech engine')
        generate_parser.add_argument('--voice', 
                                   help='Voice selection for TTS')
        
        # Processing options
        generate_parser.add_argument('--preview', action='store_true',
                                   help='Generate preview quality (faster)')
        generate_parser.add_argument('--parallel', type=int, default=1,
                                   help='Number of parallel render processes')
        generate_parser.add_argument('--skip-audio', action='store_true',
                                   help='Skip audio generation')
        generate_parser.add_argument('--skip-render', action='store_true',
                                   help='Skip 3D rendering (use simulated)')
    
    def _add_batch_parser(self, subparsers):
        """Add batch command parser"""
        batch_parser = subparsers.add_parser(
            'batch', help='Batch process multiple procedures'
        )
        
        batch_parser.add_argument('--config', '-c', required=True,
                                help='Batch configuration file')
        batch_parser.add_argument('--parallel', type=int, default=2,
                                help='Number of parallel processes')
        batch_parser.add_argument('--resume', action='store_true',
                                help='Resume interrupted batch job')
        batch_parser.add_argument('--dry-run', action='store_true',
                                help='Show what would be processed without running')
    
    def _add_test_parser(self, subparsers):
        """Add test command parser"""
        test_parser = subparsers.add_parser(
            'test', help='Run test suites'
        )
        
        test_parser.add_argument('--suite', '-s', 
                               choices=['unit', 'integration', 'all'],
                               default='all',
                               help='Test suite to run')
        test_parser.add_argument('--coverage', action='store_true',
                               help='Generate coverage report')
        test_parser.add_argument('--report-format', 
                               choices=['json', 'html', 'console'],
                               default='console',
                               help='Test report format')
        test_parser.add_argument('--output-dir', 
                               default='test_reports/',
                               help='Test report output directory')
    
    def _add_deploy_parser(self, subparsers):
        """Add deploy command parser"""
        deploy_parser = subparsers.add_parser(
            'deploy', help='Deploy to various environments'
        )
        
        deploy_parser.add_argument('--environment', '-e', 
                                 choices=['development', 'staging', 'production'],
                                 required=True,
                                 help='Target environment')
        deploy_parser.add_argument('--platform', '-p', 
                                 choices=['docker', 'kubernetes', 'local'],
                                 default='docker',
                                 help='Deployment platform')
        deploy_parser.add_argument('--build', action='store_true',
                                 help='Build before deploying')
        deploy_parser.add_argument('--tag', 
                                 help='Docker image tag')
        deploy_parser.add_argument('--dry-run', action='store_true',
                                 help='Show deployment commands without executing')
    
    def _add_status_parser(self, subparsers):
        """Add status command parser"""
        status_parser = subparsers.add_parser(
            'status', help='Show system status and health'
        )
        
        status_parser.add_argument('--verbose', '-v', action='store_true',
                                 help='Show detailed status information')
        status_parser.add_argument('--json', action='store_true',
                                 help='Output status in JSON format')
        status_parser.add_argument('--watch', '-w', action='store_true',
                                 help='Watch status continuously')
        status_parser.add_argument('--interval', type=int, default=5,
                                 help='Watch interval in seconds')
    
    def _add_validate_parser(self, subparsers):
        """Add validate command parser"""
        validate_parser = subparsers.add_parser(
            'validate', help='Validate configuration files and procedures'
        )
        
        validate_parser.add_argument('files', nargs='+',
                                   help='Files to validate')
        validate_parser.add_argument('--schema', 
                                   help='JSON schema for validation')
        validate_parser.add_argument('--strict', action='store_true',
                                   help='Enable strict validation')
        validate_parser.add_argument('--fix', action='store_true',
                                   help='Attempt to fix validation errors')
    
    def _add_setup_parser(self, subparsers):
        """Add setup command parser"""
        setup_parser = subparsers.add_parser(
            'setup', help='Setup and configure Q-AVIOGEN system'
        )
        
        setup_parser.add_argument('--install-deps', action='store_true',
                                help='Install dependencies')
        setup_parser.add_argument('--init-project', action='store_true',
                                help='Initialize new project')
        setup_parser.add_argument('--configure', action='store_true',
                                help='Run configuration wizard')
        setup_parser.add_argument('--create-examples', action='store_true',
                                help='Create example files')
        setup_parser.add_argument('--check-system', action='store_true',
                                help='Check system requirements')
    
    def _add_monitor_parser(self, subparsers):
        """Add monitor command parser"""
        monitor_parser = subparsers.add_parser(
            'monitor', help='Monitor system performance and logs'
        )
        
        monitor_parser.add_argument('--logs', action='store_true',
                                  help='Show live logs')
        monitor_parser.add_argument('--performance', action='store_true',
                                  help='Show performance metrics')
        monitor_parser.add_argument('--alerts', action='store_true',
                                  help='Show system alerts')
        monitor_parser.add_argument('--tail', type=int, default=50,
                                  help='Number of log lines to show')
    
    def cmd_generate(self, args) -> int:
        """Handle generate command"""
        self.console.print("🎬 [bold blue]Q-AVIOGEN Video Generation[/bold blue]")
        
        try:
            # Import main generation logic
            from main import main as generate_main
            
            # Prepare arguments for main function
            main_args = [
                '--input' if args.input else '--yaml',
                args.input or args.yaml,
                '--output', args.output,
                '--format', args.format,
                '--resolution', args.resolution,
                '--tts-engine', args.tts_engine
            ]
            
            if args.preview:
                main_args.append('--preview')
            if args.skip_audio:
                main_args.append('--skip-audio')
            if args.skip_render:
                main_args.append('--skip-render')
            if args.verbose:
                main_args.append('--verbose')
            if args.debug:
                main_args.append('--debug')
            
            # Override sys.argv temporarily
            original_argv = sys.argv
            sys.argv = ['main.py'] + main_args
            
            try:
                result = generate_main()
                return 0 if result else 1
            finally:
                sys.argv = original_argv
                
        except Exception as e:
            self.console.print(f"❌ [red]Generation failed: {e}[/red]")
            if args.debug:
                import traceback
                self.console.print(traceback.format_exc())
            return 1
    
    def cmd_batch(self, args) -> int:
        """Handle batch command"""
        self.console.print("📦 [bold blue]Q-AVIOGEN Batch Processing[/bold blue]")
        
        try:
            # Import batch processing logic
            from batch_render import main as batch_main
            
            batch_args = ['--config', args.config]
            if args.parallel:
                batch_args.extend(['--parallel', str(args.parallel)])
            if args.resume:
                batch_args.append('--resume')
            if args.dry_run:
                batch_args.append('--dry-run')
            
            original_argv = sys.argv
            sys.argv = ['batch_render.py'] + batch_args
            
            try:
                result = batch_main()
                return 0 if result else 1
            finally:
                sys.argv = original_argv
                
        except Exception as e:
            self.console.print(f"❌ [red]Batch processing failed: {e}[/red]")
            return 1
    
    def cmd_test(self, args) -> int:
        """Handle test command"""
        self.console.print("🧪 [bold blue]Q-AVIOGEN Test Suite[/bold blue]")
        
        try:
            if args.suite in ['integration', 'all']:
                # Run integration tests
                from integration_test import QAviogenIntegrationTest
                
                test_suite = QAviogenIntegrationTest()
                summary = test_suite.run_all_tests()
                
                # Generate report
                report_dir = Path(args.output_dir)
                report_dir.mkdir(exist_ok=True)
                
                if args.report_format == 'json':
                    report_file = report_dir / "integration_test_report.json"
                    with open(report_file, 'w') as f:
                        json.dump(summary, f, indent=2)
                    self.console.print(f"📊 Report saved: {report_file}")
                
                # Show summary
                self._show_test_summary(summary)
                
                test_suite.cleanup_test_environment()
                
                return 0 if summary['success_rate'] == 100 else 1
            
            if args.suite in ['unit', 'all']:
                # Run unit tests using pytest if available
                try:
                    result = subprocess.run([
                        sys.executable, '-m', 'pytest', 
                        'tests/', '-v'
                    ] + (['--cov=.'] if args.coverage else []),
                    capture_output=True, text=True)
                    
                    self.console.print(result.stdout)
                    if result.stderr:
                        self.console.print(f"[red]{result.stderr}[/red]")
                    
                    return result.returncode
                    
                except FileNotFoundError:
                    self.console.print("⚠️ [yellow]pytest not found, skipping unit tests[/yellow]")
                    return 0
            
        except Exception as e:
            self.console.print(f"❌ [red]Test execution failed: {e}[/red]")
            return 1
    
    def cmd_deploy(self, args) -> int:
        """Handle deploy command"""
        self.console.print("🚀 [bold blue]Q-AVIOGEN Deployment[/bold blue]")
        
        try:
            from deployment_prep import DeploymentPreparation
            
            prep = DeploymentPreparation()
            
            if args.build:
                self.console.print("🔨 Building deployment artifacts...")
                prep.prepare_deployment()
            
            # Run deployment based on platform
            if args.platform == 'docker':
                return self._deploy_docker(args)
            elif args.platform == 'kubernetes':
                return self._deploy_kubernetes(args)
            else:
                self.console.print(f"❌ [red]Unsupported platform: {args.platform}[/red]")
                return 1
                
        except Exception as e:
            self.console.print(f"❌ [red]Deployment failed: {e}[/red]")
            return 1
    
    def cmd_status(self, args) -> int:
        """Handle status command"""
        self.console.print("📊 [bold blue]Q-AVIOGEN System Status[/bold blue]")
        
        try:
            status_info = self._collect_status_info(args.verbose)
            
            if args.json:
                self.console.print(json.dumps(status_info, indent=2))
            else:
                self._display_status_table(status_info)
            
            return 0
            
        except Exception as e:
            self.console.print(f"❌ [red]Status check failed: {e}[/red]")
            return 1
    
    def cmd_validate(self, args) -> int:
        """Handle validate command"""
        self.console.print("✅ [bold blue]Q-AVIOGEN Validation[/bold blue]")
        
        try:
            all_valid = True
            
            for file_path in args.files:
                file_path = Path(file_path)
                
                if not file_path.exists():
                    self.console.print(f"❌ [red]File not found: {file_path}[/red]")
                    all_valid = False
                    continue
                
                # Validate based on file extension
                if file_path.suffix == '.md':
                    valid = self._validate_markdown(file_path, args)
                elif file_path.suffix in ['.yaml', '.yml']:
                    valid = self._validate_yaml(file_path, args)
                elif file_path.suffix == '.json':
                    valid = self._validate_json(file_path, args)
                else:
                    self.console.print(f"⚠️ [yellow]Unknown file type: {file_path}[/yellow]")
                    continue
                
                if valid:
                    self.console.print(f"✅ [green]{file_path}: Valid[/green]")
                else:
                    self.console.print(f"❌ [red]{file_path}: Invalid[/red]")
                    all_valid = False
            
            return 0 if all_valid else 1
            
        except Exception as e:
            self.console.print(f"❌ [red]Validation failed: {e}[/red]")
            return 1
    
    def cmd_setup(self, args) -> int:
        """Handle setup command"""
        self.console.print("⚙️ [bold blue]Q-AVIOGEN Setup[/bold blue]")
        
        try:
            if args.check_system:
                return self._check_system_requirements()
            
            if args.install_deps:
                return self._install_dependencies()
            
            if args.init_project:
                return self._init_project()
            
            if args.configure:
                return self._run_configuration_wizard()
            
            if args.create_examples:
                return self._create_examples()
            
            # Default: run all setup steps
            steps = [
                ("System Requirements", self._check_system_requirements),
                ("Dependencies", self._install_dependencies),
                ("Configuration", self._run_configuration_wizard),
                ("Examples", self._create_examples)
            ]
            
            for step_name, step_func in steps:
                self.console.print(f"🔧 Running: {step_name}")
                result = step_func()
                if result != 0:
                    self.console.print(f"❌ [red]Setup failed at: {step_name}[/red]")
                    return result
            
            self.console.print("✅ [green]Setup completed successfully![/green]")
            return 0
            
        except Exception as e:
            self.console.print(f"❌ [red]Setup failed: {e}[/red]")
            return 1
    
    def cmd_monitor(self, args) -> int:
        """Handle monitor command"""
        self.console.print("📈 [bold blue]Q-AVIOGEN Monitoring[/bold blue]")
        
        try:
            if args.logs:
                return self._show_logs(args.tail)
            
            if args.performance:
                return self._show_performance_metrics()
            
            if args.alerts:
                return self._show_alerts()
            
            # Default: show overview
            self._show_monitoring_overview()
            return 0
            
        except Exception as e:
            self.console.print(f"❌ [red]Monitoring failed: {e}[/red]")
            return 1
    
    # Helper methods for command implementations
    def _show_test_summary(self, summary: Dict[str, Any]):
        """Display test summary table"""
        table = Table(title="Test Summary")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="magenta")
        
        table.add_row("Total Tests", str(summary['total_tests']))
        table.add_row("Passed", str(summary['passed_tests']))
        table.add_row("Failed", str(summary['failed_tests']))
        table.add_row("Success Rate", f"{summary['success_rate']:.1f}%")
        
        self.console.print(table)
    
    def _deploy_docker(self, args) -> int:
        """Deploy using Docker"""
        try:
            tag = args.tag or 'latest'
            
            commands = [
                f"docker build -t q-aviogen:{tag} .",
                f"docker run -d --name q-aviogen-{args.environment} -p 8080:8080 q-aviogen:{tag}"
            ]
            
            for cmd in commands:
                if args.dry_run:
                    self.console.print(f"[dim]Would run: {cmd}[/dim]")
                else:
                    self.console.print(f"🔧 Running: {cmd}")
                    result = subprocess.run(cmd, shell=True)
                    if result.returncode != 0:
                        return result.returncode
            
            self.console.print("✅ [green]Docker deployment completed[/green]")
            return 0
            
        except Exception as e:
            self.console.print(f"❌ [red]Docker deployment failed: {e}[/red]")
            return 1
    
    def _deploy_kubernetes(self, args) -> int:
        """Deploy using Kubernetes"""
        try:
            commands = [
                "kubectl apply -f k8s/",
                "kubectl rollout status deployment/q-aviogen"
            ]
            
            for cmd in commands:
                if args.dry_run:
                    self.console.print(f"[dim]Would run: {cmd}[/dim]")
                else:
                    self.console.print(f"🔧 Running: {cmd}")
                    result = subprocess.run(cmd, shell=True)
                    if result.returncode != 0:
                        return result.returncode
            
            self.console.print("✅ [green]Kubernetes deployment completed[/green]")
            return 0
            
        except Exception as e:
            self.console.print(f"❌ [red]Kubernetes deployment failed: {e}[/red]")
            return 1
    
    def _collect_status_info(self, verbose: bool) -> Dict[str, Any]:
        """Collect system status information"""
        status = {
            "timestamp": datetime.now().isoformat(),
            "system": {
                "python_version": sys.version.split()[0],
                "platform": sys.platform,
                "project_root": str(self.project_root),
            },
            "components": {
                "core": self._check_component_status("core"),
                "parser": self._check_component_status("parser"),
                "blender": self._check_component_status("blender"),
                "tts": self._check_component_status("tts"),
            },
            "files": {
                "input_available": len(list((self.project_root / "input").glob("**/*.*"))),
                "output_size": self._get_directory_size(self.project_root / "output"),
                "cache_size": self._get_directory_size(self.project_root / "cache"),
            }
        }
        
        if verbose:
            status["detailed"] = {
                "dependencies": self._check_dependencies(),
                "configuration": self._check_configuration(),
                "recent_runs": self._get_recent_runs()
            }
        
        return status
    
    def _check_component_status(self, component: str) -> str:
        """Check status of a system component"""
        try:
            if component == "core":
                from core.types import SceneConfig
                from core.errors import RenderingError
                return "operational"
            elif component == "parser":
                from parser.md_parser import MarkdownParser
                return "operational"
            elif component == "blender":
                from blender.simulated_renderer import get_renderer_class
                return "operational"
            elif component == "tts":
                from tts.narration import NarrationGenerator
                return "operational"
            else:
                return "unknown"
        except ImportError:
            return "error"
        except Exception:
            return "warning"
    
    def _display_status_table(self, status_info: Dict[str, Any]):
        """Display status information in a table"""
        # System information
        system_table = Table(title="System Information")
        system_table.add_column("Component", style="cyan")
        system_table.add_column("Status", style="magenta")
        
        for key, value in status_info["system"].items():
            system_table.add_row(key.replace("_", " ").title(), str(value))
        
        self.console.print(system_table)
        
        # Component status
        component_table = Table(title="Component Status")
        component_table.add_column("Component", style="cyan")
        component_table.add_column("Status", style="magenta")
        
        for component, status in status_info["components"].items():
            status_color = "green" if status == "operational" else "red" if status == "error" else "yellow"
            component_table.add_row(component.title(), f"[{status_color}]{status}[/{status_color}]")
        
        self.console.print(component_table)
    
    def _validate_markdown(self, file_path: Path, args) -> bool:
        """Validate Markdown file"""
        try:
            from parser.md_parser import MarkdownParser
            parser = MarkdownParser()
            data = parser.parse_file(str(file_path))
            return bool(data.get("title") and data.get("steps"))
        except Exception:
            return False
    
    def _validate_yaml(self, file_path: Path, args) -> bool:
        """Validate YAML file"""
        try:
            import yaml
            with open(file_path, 'r') as f:
                data = yaml.safe_load(f)
            return isinstance(data, dict)
        except Exception:
            return False
    
    def _validate_json(self, file_path: Path, args) -> bool:
        """Validate JSON file"""
        try:
            with open(file_path, 'r') as f:
                json.load(f)
            return True
        except Exception:
            return False
    
    def _check_system_requirements(self) -> int:
        """Check system requirements"""
        requirements = [
            ("Python 3.8+", sys.version_info >= (3, 8)),
            ("Required directories", all([
                (self.project_root / d).exists() 
                for d in ["input", "output", "core", "parser", "blender", "tts"]
            ])),
            ("Configuration files", (self.project_root / "config.ini").exists()),
        ]
        
        all_met = True
        for req_name, req_met in requirements:
            status = "✅" if req_met else "❌"
            self.console.print(f"{status} {req_name}")
            if not req_met:
                all_met = False
        
        return 0 if all_met else 1
    
    def _install_dependencies(self) -> int:
        """Install system dependencies"""
        try:
            result = subprocess.run([
                sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.console.print("✅ [green]Dependencies installed successfully[/green]")
                return 0
            else:
                self.console.print(f"❌ [red]Dependency installation failed: {result.stderr}[/red]")
                return 1
                
        except Exception as e:
            self.console.print(f"❌ [red]Failed to install dependencies: {e}[/red]")
            return 1
    
    def _init_project(self) -> int:
        """Initialize new project"""
        # Create necessary directories
        dirs = ["input/markdown", "input/yaml", "output/videos", "output/frames", "output/audio", "cache"]
        
        for dir_name in dirs:
            dir_path = self.project_root / dir_name
            dir_path.mkdir(parents=True, exist_ok=True)
            self.console.print(f"📁 Created: {dir_name}")
        
        self.console.print("✅ [green]Project initialized[/green]")
        return 0
    
    def _run_configuration_wizard(self) -> int:
        """Run interactive configuration wizard"""
        self.console.print("🧙 [bold]Configuration Wizard[/bold]")
        self.console.print("This will create a basic configuration file.")
        
        # For now, just copy the template
        template_file = self.project_root / "config_template.ini"
        config_file = self.project_root / "config.ini"
        
        if template_file.exists() and not config_file.exists():
            import shutil
            shutil.copy(template_file, config_file)
            self.console.print(f"✅ [green]Configuration created: {config_file}[/green]")
        else:
            self.console.print("ℹ️ [blue]Configuration already exists or template not found[/blue]")
        
        return 0
    
    def _create_examples(self) -> int:
        """Create example files"""
        examples_created = 0
        
        # Check if examples already exist
        if (self.project_root / "input" / "yaml" / "enhanced_demo_config.yaml").exists():
            examples_created += 1
        
        if (self.project_root / "input" / "markdown" / "Engine_Inspection_Procedure.md").exists():
            examples_created += 1
        
        self.console.print(f"✅ [green]{examples_created} example files available[/green]")
        return 0
    
    def _show_logs(self, tail_lines: int) -> int:
        """Show system logs"""
        log_file = self.project_root / "output.log"
        
        if log_file.exists():
            with open(log_file, 'r') as f:
                lines = f.readlines()
                for line in lines[-tail_lines:]:
                    self.console.print(line.rstrip())
        else:
            self.console.print("ℹ️ [blue]No log file found[/blue]")
        
        return 0
    
    def _show_performance_metrics(self) -> int:
        """Show performance metrics"""
        # Placeholder for performance metrics
        metrics_table = Table(title="Performance Metrics")
        metrics_table.add_column("Metric", style="cyan")
        metrics_table.add_column("Value", style="magenta")
        
        metrics_table.add_row("CPU Usage", "N/A")
        metrics_table.add_row("Memory Usage", "N/A")
        metrics_table.add_row("Disk Usage", "N/A")
        metrics_table.add_row("Active Renders", "0")
        
        self.console.print(metrics_table)
        return 0
    
    def _show_alerts(self) -> int:
        """Show system alerts"""
        self.console.print("🔔 [bold]System Alerts[/bold]")
        self.console.print("ℹ️ [blue]No alerts at this time[/blue]")
        return 0
    
    def _show_monitoring_overview(self):
        """Show monitoring overview"""
        self.console.print("📊 [bold]Monitoring Overview[/bold]")
        self.console.print("Use --logs, --performance, or --alerts for specific views")
    
    def _get_directory_size(self, directory: Path) -> str:
        """Get directory size in human readable format"""
        if not directory.exists():
            return "0 B"
        
        total_size = sum(f.stat().st_size for f in directory.rglob('*') if f.is_file())
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if total_size < 1024.0:
                return f"{total_size:.1f} {unit}"
            total_size /= 1024.0
        
        return f"{total_size:.1f} TB"
    
    def _check_dependencies(self) -> List[str]:
        """Check installed dependencies"""
        try:
            import pkg_resources
            installed_packages = [d.project_name for d in pkg_resources.working_set]
            return installed_packages
        except Exception:
            return []
    
    def _check_configuration(self) -> Dict[str, Any]:
        """Check configuration status"""
        config_file = self.project_root / "config.ini"
        return {
            "config_exists": config_file.exists(),
            "config_size": config_file.stat().st_size if config_file.exists() else 0
        }
    
    def _get_recent_runs(self) -> List[str]:
        """Get recent run information"""
        # Placeholder for recent runs
        return []
    
    def run(self, argv: Optional[List[str]] = None) -> int:
        """Main CLI entry point"""
        parser = self.create_parser()
        args = parser.parse_args(argv)
        
        if args.debug:
            import logging
            logging.basicConfig(level=logging.DEBUG)
        
        # Route to appropriate command handler
        if args.command == 'generate':
            return self.cmd_generate(args)
        elif args.command == 'batch':
            return self.cmd_batch(args)
        elif args.command == 'test':
            return self.cmd_test(args)
        elif args.command == 'deploy':
            return self.cmd_deploy(args)
        elif args.command == 'status':
            return self.cmd_status(args)
        elif args.command == 'validate':
            return self.cmd_validate(args)
        elif args.command == 'setup':
            return self.cmd_setup(args)
        elif args.command == 'monitor':
            return self.cmd_monitor(args)
        else:
            parser.print_help()
            return 1


def main():
    """Main entry point"""
    cli = QAviogenCLI()
    return cli.run()


if __name__ == "__main__":
    sys.exit(main())
