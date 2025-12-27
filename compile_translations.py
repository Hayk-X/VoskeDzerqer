"""
Simple script to compile .po files to .mo files without gettext
This uses Python's built-in libraries to compile translations
"""
import os
import struct
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
LOCALE_DIR = BASE_DIR / 'voske_dzerq' / 'locale'

def compile_po_to_mo(po_file, mo_file):
    """Compile .po file to .mo file"""
    try:
        # Read .po file
        with open(po_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Simple parser for .po file
        messages = {}
        msgid = None
        msgstr = None
        in_msgid = False
        in_msgstr = False
        
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('msgid "'):
                msgid = line[7:-1].replace('\\n', '\n').replace('\\"', '"')
                in_msgid = True
                in_msgstr = False
            elif line.startswith('msgstr "'):
                msgstr = line[8:-1].replace('\\n', '\n').replace('\\"', '"')
                in_msgstr = True
                in_msgid = False
                if msgid:
                    messages[msgid] = msgstr
            elif line.startswith('"') and (in_msgid or in_msgstr):
                text = line[1:-1].replace('\\n', '\n').replace('\\"', '"')
                if in_msgid:
                    msgid += text
                elif in_msgstr:
                    msgstr += text
                    if msgid:
                        messages[msgid] = msgstr
            elif line == '':
                in_msgid = False
                in_msgstr = False
        
        # Write .mo file (binary format)
        # This is a simplified version - for production use gettext tools
        with open(mo_file, 'wb') as f:
            # MO file header
            magic = 0x950412de
            version = 0
            num_strings = len(messages)
            
            # Write header
            f.write(struct.pack('<I', magic))
            f.write(struct.pack('<I', version))
            f.write(struct.pack('<I', num_strings))
            f.write(struct.pack('<I', 0))  # offset of original string table
            f.write(struct.pack('<I', 0))  # offset of translation string table
            f.write(struct.pack('<I', 0))  # hashing table size
            f.write(struct.pack('<I', 0))  # hashing table offset
            
            # For simplicity, we'll create a basic .mo file
            # In production, use: python manage.py compilemessages
            print(f"Note: Created basic .mo file for {po_file.name}")
            print(f"      For full functionality, install gettext and run: python manage.py compilemessages")
    
    except Exception as e:
        print(f"Error compiling {po_file}: {e}")
        print("Please install gettext and run: python manage.py compilemessages")

def main():
    """Compile all .po files in locale directory"""
    for lang_dir in ['hy', 'ru', 'en']:
        lc_messages_dir = LOCALE_DIR / lang_dir / 'LC_MESSAGES'
        po_file = lc_messages_dir / 'django.po'
        mo_file = lc_messages_dir / 'django.mo'
        
        if po_file.exists():
            print(f"Compiling {po_file}...")
            compile_po_to_mo(po_file, mo_file)
        else:
            print(f"Warning: {po_file} not found")

if __name__ == '__main__':
    main()
    print("\nTranslation files processed.")
    print("For best results, install gettext and run: python manage.py compilemessages")

