"""
Proper .po to .mo compiler without gettext
Uses correct binary format for .mo files
"""
import struct
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
LOCALE_DIR = BASE_DIR / 'voske_dzerq' / 'locale'

def unescape(s):
    """Unescape PO string"""
    return (s.replace('\\n', '\n')
             .replace('\\t', '\t')
             .replace('\\r', '\r')
             .replace('\\"', '"')
             .replace('\\\\', '\\'))

def parse_po(po_path):
    """Parse .po file into msgid->msgstr dictionary"""
    with open(po_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    messages = {}
    header = None
    # Split by double newlines (message blocks)
    blocks = content.split('\n\n')
    
    for block in blocks:
        block = block.strip()
        if not block or (block.startswith('#') and not 'msgid' in block):
            continue
        
        msgid_parts = []
        msgstr_parts = []
        in_msgid = False
        in_msgstr = False
        
        for line in block.split('\n'):
            line = line.rstrip('\r')
            stripped = line.strip()
            
            if not stripped or (stripped.startswith('#') and not stripped.startswith('#:')):
                continue
            
            # msgid line
            if stripped.startswith('msgid '):
                in_msgid = True
                in_msgstr = False
                # Extract content from quotes
                match = re.search(r'msgid\s+"(.*)"', stripped, re.DOTALL)
                if match:
                    msgid_parts = [match.group(1)]
                elif re.match(r'msgid\s+""', stripped):
                    msgid_parts = ['']
            
            # msgstr line
            elif stripped.startswith('msgstr '):
                in_msgid = False
                in_msgstr = True
                match = re.search(r'msgstr\s+"(.*)"', stripped, re.DOTALL)
                if match:
                    msgstr_parts = [match.group(1)]
                elif re.match(r'msgstr\s+""', stripped):
                    msgstr_parts = ['']
            
            # Continuation line (quoted string)
            elif stripped.startswith('"') and stripped.endswith('"'):
                line_content = stripped[1:-1]
                if in_msgid:
                    msgid_parts.append(line_content)
                elif in_msgstr:
                    msgstr_parts.append(line_content)
        
        # Process collected msgid and msgstr
        if msgid_parts and msgstr_parts:
            msgid = unescape(''.join(msgid_parts))
            msgstr = unescape(''.join(msgstr_parts))
            
            # Handle header (empty msgid)
            if not msgid:
                # Create proper header with charset info
                if not header:
                    header = msgstr if msgstr else 'Content-Type: text/plain; charset=UTF-8\n'
                else:
                    header = msgstr
            else:
                # Include all messages
                messages[msgid] = msgstr if msgstr else msgid
    
    # Ensure header has charset info
    if not header or 'charset' not in header.lower():
        header = 'Content-Type: text/plain; charset=UTF-8\n'
    
    return messages, header

def write_mo(messages, mo_path, header=None):
    """Write .mo file in correct binary format"""
    # Always include header entry (empty msgid)
    items = [('', header if header else '')]
    items.extend(sorted(messages.items()))
    num = len(items)
    
    # Build strings
    orig_strings = []
    trans_strings = []
    string_data = b''
    
    for msgid, msgstr in items:
        msgid_bytes = msgid.encode('utf-8') + b'\x00'
        msgstr_bytes = msgstr.encode('utf-8') + b'\x00'
        
        orig_offset = len(string_data)
        string_data += msgid_bytes
        orig_strings.append((len(msgid_bytes), orig_offset))
        
        trans_offset = len(string_data)
        string_data += msgstr_bytes
        trans_strings.append((len(msgstr_bytes), trans_offset))
    
    # Calculate offsets
    header_size = 28
    orig_table_offset = header_size
    trans_table_offset = orig_table_offset + (num * 8)
    string_data_offset = trans_table_offset + (num * 8)
    
    # Adjust offsets
    orig_strings = [(l, o + string_data_offset) for l, o in orig_strings]
    trans_strings = [(l, o + string_data_offset) for l, o in trans_strings]
    
    # Write file
    with open(mo_path, 'wb') as f:
        # Header
        f.write(struct.pack('<I', 0x950412de))  # magic number
        f.write(struct.pack('<I', 0))  # version
        f.write(struct.pack('<I', num))  # number of strings
        f.write(struct.pack('<I', orig_table_offset))  # offset of original strings table
        f.write(struct.pack('<I', trans_table_offset))  # offset of translation strings table
        f.write(struct.pack('<I', 0))  # size of hashing table
        f.write(struct.pack('<I', 0))  # offset of hashing table
        
        # Original strings table
        for length, offset in orig_strings:
            f.write(struct.pack('<I', length))
            f.write(struct.pack('<I', offset))
        
        # Translation strings table
        for length, offset in trans_strings:
            f.write(struct.pack('<I', length))
            f.write(struct.pack('<I', offset))
        
        # String data
        f.write(string_data)

def main():
    for lang in ['hy', 'ru', 'en']:
        po_file = LOCALE_DIR / lang / 'LC_MESSAGES' / 'django.po'
        mo_file = LOCALE_DIR / lang / 'LC_MESSAGES' / 'django.mo'
        
        if po_file.exists():
            print(f"Compiling {lang}...")
            try:
                messages, header = parse_po(po_file)
                write_mo(messages, mo_file, header)
                print(f"  Created {mo_file.name} with {len(messages)} translations")
            except Exception as e:
                print(f"  Error: {e}")
                import traceback
                traceback.print_exc()

if __name__ == '__main__':
    main()

