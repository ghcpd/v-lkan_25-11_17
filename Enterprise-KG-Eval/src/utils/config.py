"""Configuration manager."""

from typing import Dict, Any, List
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class Config:
    """Configuration manager for the extraction pipeline."""

    def __init__(self, config_dir: str = "config"):
        """Initialize configuration manager.
        
        Args:
            config_dir: Directory containing config files
        """
        self.config_dir = Path(config_dir)
        self.settings: Dict[str, Any] = {}

    def load(self, key: str, value: Any) -> None:
        """Load a configuration setting.
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self.settings[key] = value
        logger.info(f"Loaded config: {key}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        return self.settings.get(key, default)

    def set_batch_mode(self, batch_size: int = 10) -> None:
        """Configure batch processing.
        
        Args:
            batch_size: Number of documents per batch
        """
        self.load("batch_size", batch_size)

    def set_output_dir(self, output_dir: str) -> None:
        """Set output directory.
        
        Args:
            output_dir: Path to output directory
        """
        self.load("output_dir", output_dir)

    def set_logging_level(self, level: str) -> None:
        """Set logging level.
        
        Args:
            level: Logging level (DEBUG, INFO, WARNING, ERROR)
        """
        self.load("logging_level", level)

    def as_dict(self) -> Dict[str, Any]:
        """Get all settings as dictionary.
        
        Returns:
            Dictionary of all settings
        """
        return self.settings.copy()
