"""
Create minimal valid .mo files for Django translations
"""
import struct
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
LOCALE_DIR = BASE_DIR / 'voske_dzerq' / 'locale'

def create_minimal_mo_file(mo_path):
    """Create a minimal valid .mo file"""
    # Minimal .mo file structure
    # Magic number: 0x950412de (little-endian)
    # Version: 0
    # Number of strings: 0 (empty file is valid)
    
    with open(mo_path, 'wb') as f:
        # Header
        magic = 0x950412de
        version = 0
        num_strings = 0
        
        # Write header (28 bytes)
        f.write(struct.pack('<I', magic))  # Magic number
        f.write(struct.pack('<I', version))  # Version
        f.write(struct.pack('<I', num_strings))  # Number of strings
        f.write(struct.pack('<I', 28))  # Offset of original string table (after header)
        f.write(struct.pack('<I', 28))  # Offset of translation string table
        f.write(struct.pack('<I', 0))  # Size of hashing table
        f.write(struct.pack('<I', 0))  # Offset of hashing table
        
        # Empty string tables (since num_strings = 0, no data needed)

if __name__ == '__main__':
    for lang in ['hy', 'ru', 'en']:
        mo_file = LOCALE_DIR / lang / 'LC_MESSAGES' / 'django.mo'
        print(f"Creating minimal .mo file: {mo_file}")
        create_minimal_mo_file(mo_file)
    
    print("\nMinimal .mo files created.")
    print("Note: These are empty files. Django will use .po files for translations.")
    print("For production, install gettext and run: python manage.py compilemessages")

