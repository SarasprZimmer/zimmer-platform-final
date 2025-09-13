#!/usr/bin/env python3
"""
Script to fix React Hook useEffect dependency warnings
"""
import os
import re
import glob

def fix_dependency_warnings():
    """Fix missing dependencies in useEffect hooks"""
    
    # Files to fix
    files_to_fix = [
        'zimmer_user_panel/pages/automations/[id]/index.tsx',
        'zimmer_user_panel/pages/automations/[id]/purchase.tsx', 
        'zimmer_user_panel/pages/automations/[id]/tokens.tsx',
        'zimmer_user_panel/pages/notifications/index.tsx',
        'zimmer_user_panel/pages/payment/index.tsx',
        'zimmer_user_panel/pages/payment/return.tsx',
        'zimmer_user_panel/components/notifications/NotificationsBell.tsx'
    ]
    
    changes_made = 0
    
    for file_path in files_to_fix:
        if not os.path.exists(file_path):
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Add useCallback import if not present
            if 'useCallback' not in content and 'useEffect' in content:
                content = re.sub(
                    r'import \{ ([^}]+) \} from [\'"]react[\'"]',
                    r'import { \1, useCallback } from \'react\'',
                    content
                )
            
            # Fix specific patterns
            patterns = [
                # Pattern 1: fetchData dependency
                (r'useEffect\(\(\) => \{\s*if \([^)]+\) \{\s*fetchData\(\)\s*\}\s*\}, \[([^\]]+)\]\)', 
                 r'useEffect(() => {\n    if (\1) {\n      fetchData()\n    }\n  }, [\2, fetchData])'),
                
                # Pattern 2: fetchAutomation dependency  
                (r'useEffect\(\(\) => \{\s*if \([^)]+\) \{\s*fetchAutomation\(\)\s*\}\s*\}, \[([^\]]+)\]\)',
                 r'useEffect(() => {\n    if (\1) {\n      fetchAutomation()\n    }\n  }, [\2, fetchAutomation])'),
                
                # Pattern 3: load dependency
                (r'useEffect\(\(\) => \{\s*load\(\)\s*\}, \[([^\]]+)\]\)',
                 r'useEffect(() => {\n    load()\n  }, [\1, load])'),
                
                # Pattern 4: verifyPayment dependency
                (r'useEffect\(\(\) => \{\s*verifyPayment\(\)\s*\}, \[([^\]]+)\]\)',
                 r'useEffect(() => {\n    verifyPayment()\n  }, [\1, verifyPayment])'),
                
                # Pattern 5: loadInitial dependency
                (r'useEffect\(\(\) => \{\s*loadInitial\(\)\s*\}, \[([^\]]+)\]\)',
                 r'useEffect(() => {\n    loadInitial()\n  }, [\1, loadInitial])')
            ]
            
            for pattern, replacement in patterns:
                content = re.sub(pattern, replacement, content, flags=re.MULTILINE | re.DOTALL)
            
            # Only write if content changed
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ Fixed: {file_path}")
                changes_made += 1
            
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
    
    print(f"\n📊 Summary:")
    print(f"   Files changed: {changes_made}")

if __name__ == "__main__":
    fix_dependency_warnings()
