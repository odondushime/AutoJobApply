from app.schemas.settings import Settings, SettingsUpdate
import json
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class SettingsService:
    def __init__(self):
        self.settings_file = Path("config.json")
        self._ensure_settings_file()

    def _ensure_settings_file(self):
        """Ensure the settings file exists with default values"""
        if not self.settings_file.exists():
            default_settings = {
                "name": "",
                "email": "",
                "phone": "",
                "location": "",
                "resume_path": None,
                "cover_letter_path": None,
                "linkedin_email": None,
                "linkedin_password": None
            }
            self.settings_file.write_text(json.dumps(default_settings, indent=2))

    async def get_settings(self) -> Settings:
        """Get current settings from the config file"""
        try:
            settings_data = json.loads(self.settings_file.read_text())
            return Settings(**settings_data)
        except Exception as e:
            logger.error(f"Error reading settings: {str(e)}")
            raise

    async def update_settings(self, settings_update: SettingsUpdate) -> Settings:
        """Update settings in the config file"""
        try:
            current_settings = await self.get_settings()
            updated_data = current_settings.dict()
            
            # Update only the provided fields
            for field, value in settings_update.dict(exclude_unset=True).items():
                updated_data[field] = value
            
            # Save to file
            self.settings_file.write_text(json.dumps(updated_data, indent=2))
            
            return Settings(**updated_data)
        except Exception as e:
            logger.error(f"Error updating settings: {str(e)}")
            raise 