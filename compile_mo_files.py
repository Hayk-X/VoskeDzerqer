"""
Compile .po files to .mo files without gettext
This creates proper binary .mo files from .po files
"""
import struct
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
LOCALE_DIR = BASE_DIR / 'voske_dzerq' / 'locale'

def unescape_po_string(s):
    """Unescape PO file string"""
    # Handle escape sequences
    s = s.replace('\\n', '\n')
    s = s.replace('\\t', '\t')
    s = s.replace('\\r', '\r')
    s = s.replace('\\"', '"')
    s = s.replace('\\\\', '\\')
    return s

def extract_string_value(line):
    """Extract string value from a quoted line"""
    # Remove leading/trailing quotes and unescape
    if line.startswith('"') and line.endswith('"'):
        return unescape_po_string(line[1:-1])
    return ""

def parse_po_file(po_file):
    """Parse .po file and return dictionary of translations"""
    messages = {}
    msgid = None
    msgstr = None
    
    with open(po_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split into message blocks (separated by empty lines)
    blocks = re.split(r'\n\n+', content)
    
    for block in blocks:
        block = block.strip()
        if not block or block.startswith('#'):
            continue
        
        lines = block.split('\n')
        msgid_parts = []
        msgstr_parts = []
        in_msgid = False
        in_msgstr = False
        
        for line in lines:
            line_stripped = line.strip()
            
            # Skip comments
            if line_stripped.startswith('#'):
                continue
            
            # Start of msgid
            if line_stripped.startswith('msgid '):
                in_msgid = True
                in_msgstr = False
                match = re.match(r'msgid\s+"(.*)"', line_stripped)
                if match:
                    msgid_parts.append(match.group(1))
                else:
                    # Empty msgid
                    match = re.match(r'msgid\s+""', line_stripped)
                    if match:
                        msgid_parts.append("")
            
            # Start of msgstr
            elif line_stripped.startswith('msgstr '):
                in_msgid = False
                in_msgstr = True
                match = re.match(r'msgstr\s+"(.*)"', line_stripped)
                if match:
                    msgstr_parts.append(match.group(1))
                else:
                    # Empty msgstr
                    match = re.match(r'msgstr\s+""', line_stripped)
                    if match:
                        msgstr_parts.append("")
            
            # Continuation line (starts with quote)
            elif line_stripped.startswith('"') and line_stripped.endswith('"'):
                if in_msgid:
                    msgid_parts.append(line_stripped[1:-1])
                elif in_msgstr:
                    msgstr_parts.append(line_stripped[1:-1])
        
        # Process collected msgid and msgstr
        if msgid_parts:
            msgid = unescape_po_string(''.join(msgid_parts))
        
        if msgstr_parts and msgid:
            msgstr = unescape_po_string(''.join(msgstr_parts))
            # Only add non-empty translations
            if msgid and msgstr:
                messages[msgid] = msgstr
    
    return messages

def create_mo_file(messages, mo_file):
    """Create binary .mo file from messages dictionary"""
    # Sort messages by msgid for consistent output
    sorted_items = sorted(messages.items())
    
    num_strings = len(sorted_items)
    if num_strings == 0:
        # Create empty but valid .mo file
        with open(mo_file, 'wb') as f:
            magic = 0x950412de
            version = 0
            f.write(struct.pack('<I', magic))
            f.write(struct.pack('<I', version))
            f.write(struct.pack('<I', 0))
            f.write(struct.pack('<I', 28))
            f.write(struct.pack('<I', 28))
            f.write(struct.pack('<I', 0))
            f.write(struct.pack('<I', 0))
        return
    
    # Calculate offsets
    header_size = 28
    # Each entry: 2 uint32 (length, offset) = 8 bytes
    # Original strings table: num_strings * 8
    # Translation strings table: num_strings * 8
    original_table_offset = header_size
    translation_table_offset = original_table_offset + (num_strings * 8)
    
    # Calculate string data offset
    string_data_offset = translation_table_offset + (num_strings * 8)
    
    # Build string data
    string_data = b''
    original_offsets = []
    translation_offsets = []
    
    for msgid, msgstr in sorted_items:
        # Original string (msgid)
        msgid_bytes = msgid.encode('utf-8') + b'\x00'
        original_offsets.append((len(msgid_bytes), len(string_data)))
        string_data += msgid_bytes
        
        # Translation string (msgstr)
        msgstr_bytes = msgstr.encode('utf-8') + b'\x00'
        translation_offsets.append((len(msgstr_bytes), len(string_data)))
        string_data += msgstr_bytes
    
    # Write .mo file
    with open(mo_file, 'wb') as f:
        # Header
        magic = 0x950412de
        version = 0
        f.write(struct.pack('<I', magic))
        f.write(struct.pack('<I', version))
        f.write(struct.pack('<I', num_strings))
        f.write(struct.pack('<I', original_table_offset))
        f.write(struct.pack('<I', translation_table_offset))
        f.write(struct.pack('<I', 0))  # hashing table size
        f.write(struct.pack('<I', 0))  # hashing table offset
        
        # Original strings table
        current_offset = string_data_offset
        for length, offset in original_offsets:
            f.write(struct.pack('<I', length))
            f.write(struct.pack('<I', current_offset + offset))
        
        # Translation strings table
        for length, offset in translation_offsets:
            f.write(struct.pack('<I', length))
            f.write(struct.pack('<I', current_offset + offset))
        
        # String data
        f.write(string_data)

def main():
    """Compile all .po files"""
    for lang in ['hy', 'ru', 'en']:
        lc_messages_dir = LOCALE_DIR / lang / 'LC_MESSAGES'
        po_file = lc_messages_dir / 'django.po'
        mo_file = lc_messages_dir / 'django.mo'
        
        if po_file.exists():
            print(f"Compiling {po_file.name}...")
            try:
                messages = parse_po_file(po_file)
                create_mo_file(messages, mo_file)
                print(f"  [OK] Created {mo_file.name} with {len(messages)} translations")
            except Exception as e:
                print(f"  [ERROR] Error: {e}")
        else:
            print(f"  ⚠ {po_file} not found")
    
    print("\n[SUCCESS] Compilation complete!")

if __name__ == '__main__':
    main()

