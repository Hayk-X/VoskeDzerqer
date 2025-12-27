"""
Compile .po files to .mo files using polib library
This creates proper binary .mo files compatible with Django
"""
import polib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
LOCALE_DIR = BASE_DIR / 'voske_dzerq' / 'locale'

def compile_po_to_mo(po_file, mo_file):
    """Compile .po file to .mo file using polib"""
    try:
        po = polib.pofile(str(po_file))
        po.save_as_mofile(str(mo_file))
        return len(po)
    except Exception as e:
        print(f"  Error compiling {po_file.name}: {e}")
        return 0

def main():
    """Compile all .po files"""
    total = 0
    for lang in ['hy', 'ru', 'en']:
        po_file = LOCALE_DIR / lang / 'LC_MESSAGES' / 'django.po'
        mo_file = LOCALE_DIR / lang / 'LC_MESSAGES' / 'django.mo'
        
        if po_file.exists():
            print(f"Compiling {lang}...")
            count = compile_po_to_mo(po_file, mo_file)
            if count > 0:
                print(f"  [OK] Created {mo_file.name} with {count} translations")
                total += count
            else:
                print(f"  [ERROR] Failed to compile {po_file.name}")
        else:
            print(f"  [WARNING] {po_file} not found")
    
    print(f"\n[SUCCESS] Compiled {total} translations total!")

if __name__ == '__main__':
    main()

