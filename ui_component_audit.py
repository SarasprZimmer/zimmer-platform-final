#!/usr/bin/env python3
"""
Comprehensive UI Component and Page Audit
Identifies missing pages, broken components, and non-functional UI elements
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple
from datetime import datetime

class UIComponentAuditor:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.user_panel_path = self.project_root / "zimmer_user_panel"
        self.admin_panel_path = self.project_root / "zimmermanagement" / "zimmer-admin-dashboard"
        
        # Results storage
        self.missing_pages = []
        self.broken_components = []
        self.non_functional_buttons = []
        self.missing_routes = []
        self.undefined_links = []
        self.incomplete_components = []
        
    def audit_user_panel_pages(self):
        """Audit user panel pages for missing routes and functionality"""
        print("🔍 Auditing User Panel Pages...")
        
        pages_dir = self.user_panel_path / "pages"
        if not pages_dir.exists():
            print("❌ Pages directory not found")
            return
            
        # Get all page files
        page_files = list(pages_dir.glob("*.tsx")) + list(pages_dir.glob("**/*.tsx"))
        
        # Expected pages based on navigation and common patterns
        expected_pages = [
            "dashboard", "profile", "settings", "purchase", "payment", 
            "automations", "support", "notifications", "billing", "usage",
            "tickets", "help", "documentation", "api", "integrations"
        ]
        
        # Check for missing pages
        existing_pages = set()
        for page_file in page_files:
            # Handle directory-based routes like /payment/index.tsx
            if page_file.name == "index.tsx":
                # Get the parent directory name as the page name
                parent_dir = page_file.parent.name
                if parent_dir != "pages":  # Not in root pages directory
                    existing_pages.add(parent_dir)
            else:
                page_name = page_file.stem
                if page_name not in ["_app", "index"]:
                    existing_pages.add(page_name)
        
        for expected in expected_pages:
            if expected not in existing_pages:
                self.missing_pages.append({
                    "page": expected,
                    "type": "missing_page",
                    "severity": "high",
                    "description": f"Page /{expected} is referenced but not implemented"
                })
        
        print(f"✅ Found {len(existing_pages)} existing pages")
        print(f"❌ Found {len(self.missing_pages)} missing pages")
        
    def audit_components(self):
        """Audit UI components for missing functionality"""
        print("🔍 Auditing UI Components...")
        
        components_dir = self.user_panel_path / "components"
        if not components_dir.exists():
            print("❌ Components directory not found")
            return
            
        # Get all component files
        component_files = list(components_dir.glob("**/*.tsx"))
        
        for component_file in component_files:
            self._audit_component_file(component_file)
            
        print(f"✅ Audited {len(component_files)} component files")
        
    def _audit_component_file(self, component_file: Path):
        """Audit individual component file"""
        try:
            with open(component_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            component_name = component_file.stem
            
            # Check for common issues
            issues = []
            
            # Check for TODO comments
            todo_matches = re.findall(r'//\s*TODO[:\s]*(.+)', content, re.IGNORECASE)
            if todo_matches:
                issues.extend([{"type": "todo", "message": todo.strip()} for todo in todo_matches])
            
            # Check for FIXME comments
            fixme_matches = re.findall(r'//\s*FIXME[:\s]*(.+)', content, re.IGNORECASE)
            if fixme_matches:
                issues.extend([{"type": "fixme", "message": fixme.strip()} for fixme in fixme_matches])
            
            # Check for placeholder text
            placeholder_matches = re.findall(r'placeholder=["\']([^"\']+)["\']', content)
            if placeholder_matches:
                issues.extend([{"type": "placeholder", "message": f"Placeholder text: {placeholder}"} for placeholder in placeholder_matches])
            
            # Check for disabled buttons
            disabled_buttons = re.findall(r'<button[^>]*disabled[^>]*>([^<]+)</button>', content, re.IGNORECASE)
            if disabled_buttons:
                issues.extend([{"type": "disabled_button", "message": f"Disabled button: {button.strip()}"} for button in disabled_buttons])
            
            # Check for empty onClick handlers
            empty_onclick = re.findall(r'onClick=\{[^}]*\s*//\s*TODO|onClick=\{\s*\(\)\s*=>\s*\{\s*\}\s*\}', content)
            if empty_onclick:
                issues.append({"type": "empty_onclick", "message": "Empty or placeholder onClick handler"})
            
            # Check for hardcoded text that suggests incomplete implementation
            hardcoded_issues = re.findall(r'["\'](Coming Soon|Not Implemented|TODO|Placeholder|Test|Mock)[^"\']*["\']', content, re.IGNORECASE)
            if hardcoded_issues:
                issues.extend([{"type": "hardcoded_placeholder", "message": f"Hardcoded placeholder: {text}"} for text in hardcoded_issues])
            
            if issues:
                self.incomplete_components.append({
                    "component": component_name,
                    "file": str(component_file.relative_to(self.project_root)),
                    "issues": issues
                })
                
        except Exception as e:
            print(f"❌ Error auditing {component_file}: {e}")
            
    def audit_navigation_links(self):
        """Audit navigation links for broken routes"""
        print("🔍 Auditing Navigation Links...")
        
        # Check sidebar navigation
        sidebar_file = self.user_panel_path / "components" / "Sidebar.tsx"
        if sidebar_file.exists():
            self._audit_navigation_file(sidebar_file, "Sidebar")
            
        # Check topbar navigation
        topbar_file = self.user_panel_path / "components" / "Topbar.tsx"
        if topbar_file.exists():
            self._audit_navigation_file(topbar_file, "Topbar")
            
        # Check dashboard components for links
        dashboard_dir = self.user_panel_path / "components" / "dashboard"
        if dashboard_dir.exists():
            for component_file in dashboard_dir.glob("*.tsx"):
                self._audit_navigation_file(component_file, f"Dashboard/{component_file.stem}")
                
    def _audit_navigation_file(self, file_path: Path, component_name: str):
        """Audit navigation file for broken links"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Find all href and router.push references
            href_matches = re.findall(r'href=["\']([^"\']+)["\']', content)
            router_matches = re.findall(r'router\.push\(["\']([^"\']+)["\']', content)
            link_matches = re.findall(r'Link.*href=["\']([^"\']+)["\']', content)
            
            all_links = href_matches + router_matches + link_matches
            
            for link in all_links:
                if link.startswith('/') and not link.startswith('/api'):
                    # Check if the page exists
                    page_name = link.strip('/')
                    if page_name and page_name != 'dashboard':
                        # Check for both direct file and directory-based routes
                        page_file = self.user_panel_path / "pages" / f"{page_name}.tsx"
                        page_dir = self.user_panel_path / "pages" / page_name / "index.tsx"
                        
                        if not page_file.exists() and not page_dir.exists():
                            self.undefined_links.append({
                                "component": component_name,
                                "link": link,
                                "type": "missing_page",
                                "severity": "high"
                            })
                            
        except Exception as e:
            print(f"❌ Error auditing navigation in {file_path}: {e}")
            
    def audit_api_integrations(self):
        """Audit API integrations for missing endpoints"""
        print("🔍 Auditing API Integrations...")
        
        # Check API client files
        api_files = [
            self.user_panel_path / "lib" / "api.ts",
            self.user_panel_path / "lib" / "apiClient.ts"
        ]
        
        for api_file in api_files:
            if api_file.exists():
                self._audit_api_file(api_file)
                
    def _audit_api_file(self, api_file: Path):
        """Audit API file for missing endpoints"""
        try:
            with open(api_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Find API endpoint definitions
            endpoint_matches = re.findall(r'["\']([^"\']*api[^"\']*)["\']', content)
            
            for endpoint in endpoint_matches:
                if endpoint.startswith('/api/'):
                    # Check if this endpoint is actually implemented in backend
                    # This would require backend analysis, so we'll just note it
                    pass
                    
        except Exception as e:
            print(f"❌ Error auditing API file {api_file}: {e}")
            
    def audit_forms_and_inputs(self):
        """Audit forms and inputs for missing functionality"""
        print("🔍 Auditing Forms and Inputs...")
        
        # Check all page files for forms
        pages_dir = self.user_panel_path / "pages"
        if pages_dir.exists():
            for page_file in pages_dir.glob("*.tsx"):
                self._audit_form_in_page(page_file)
                
    def _audit_form_in_page(self, page_file: Path):
        """Audit forms in a specific page"""
        try:
            with open(page_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Find form elements
            form_matches = re.findall(r'<form[^>]*>', content, re.IGNORECASE)
            input_matches = re.findall(r'<input[^>]*>', content, re.IGNORECASE)
            button_matches = re.findall(r'<button[^>]*>([^<]+)</button>', content, re.IGNORECASE)
            
            page_name = page_file.stem
            
            # Check for forms without onSubmit handlers
            if form_matches:
                has_onsubmit = 'onSubmit' in content
                if not has_onsubmit:
                    self.broken_components.append({
                        "component": f"Form in {page_name}",
                        "file": str(page_file.relative_to(self.project_root)),
                        "issue": "Form without onSubmit handler",
                        "severity": "medium"
                    })
            
            # Check for buttons without onClick handlers
            for button_text in button_matches:
                if button_text.strip() and 'onClick' not in content:
                    self.non_functional_buttons.append({
                        "component": f"Button in {page_name}",
                        "file": str(page_file.relative_to(self.project_root)),
                        "button_text": button_text.strip(),
                        "issue": "Button without onClick handler"
                    })
                    
        except Exception as e:
            print(f"❌ Error auditing forms in {page_file}: {e}")
            
    def generate_report(self):
        """Generate comprehensive audit report"""
        print("\n" + "="*60)
        print("🎯 UI COMPONENT AUDIT REPORT")
        print("="*60)
        
        # Summary
        total_issues = (len(self.missing_pages) + len(self.broken_components) + 
                       len(self.non_functional_buttons) + len(self.undefined_links) + 
                       len(self.incomplete_components))
        
        print(f"📊 SUMMARY:")
        print(f"   Missing Pages: {len(self.missing_pages)}")
        print(f"   Broken Components: {len(self.broken_components)}")
        print(f"   Non-functional Buttons: {len(self.non_functional_buttons)}")
        print(f"   Undefined Links: {len(self.undefined_links)}")
        print(f"   Incomplete Components: {len(self.incomplete_components)}")
        print(f"   Total Issues: {total_issues}")
        
        # Detailed reports
        if self.missing_pages:
            print(f"\n❌ MISSING PAGES ({len(self.missing_pages)}):")
            for page in self.missing_pages:
                print(f"   • /{page['page']} - {page['description']}")
                
        if self.undefined_links:
            print(f"\n🔗 UNDEFINED LINKS ({len(self.undefined_links)}):")
            for link in self.undefined_links:
                print(f"   • {link['component']}: {link['link']} -> Missing page")
                
        if self.non_functional_buttons:
            print(f"\n🔘 NON-FUNCTIONAL BUTTONS ({len(self.non_functional_buttons)}):")
            for button in self.non_functional_buttons:
                print(f"   • {button['component']}: '{button['button_text']}' - {button['issue']}")
                
        if self.broken_components:
            print(f"\n🔧 BROKEN COMPONENTS ({len(self.broken_components)}):")
            for component in self.broken_components:
                print(f"   • {component['component']} - {component['issue']}")
                
        if self.incomplete_components:
            print(f"\n⚠️  INCOMPLETE COMPONENTS ({len(self.incomplete_components)}):")
            for component in self.incomplete_components:
                print(f"   • {component['component']} ({component['file']}):")
                for issue in component['issues']:
                    print(f"     - {issue['type'].upper()}: {issue['message']}")
        
        # Save detailed report
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "missing_pages": len(self.missing_pages),
                "broken_components": len(self.broken_components),
                "non_functional_buttons": len(self.non_functional_buttons),
                "undefined_links": len(self.undefined_links),
                "incomplete_components": len(self.incomplete_components),
                "total_issues": total_issues
            },
            "missing_pages": self.missing_pages,
            "broken_components": self.broken_components,
            "non_functional_buttons": self.non_functional_buttons,
            "undefined_links": self.undefined_links,
            "incomplete_components": self.incomplete_components
        }
        
        with open("ui_audit_report.json", "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
            
        print(f"\n📄 Detailed report saved to: ui_audit_report.json")
        
        return report_data
        
    def run_full_audit(self):
        """Run complete UI audit"""
        print("🚀 Starting Comprehensive UI Component Audit...")
        print("="*60)
        
        self.audit_user_panel_pages()
        self.audit_components()
        self.audit_navigation_links()
        self.audit_api_integrations()
        self.audit_forms_and_inputs()
        
        return self.generate_report()

def main():
    """Main function"""
    project_root = "."
    auditor = UIComponentAuditor(project_root)
    report = auditor.run_full_audit()
    
    print(f"\n✅ Audit completed! Found {report['summary']['total_issues']} issues to address.")
    
    # Create priority action items
    high_priority = [item for item in report['missing_pages'] + report['undefined_links'] 
                    if item.get('severity') == 'high']
    
    if high_priority:
        print(f"\n🎯 HIGH PRIORITY ACTIONS ({len(high_priority)}):")
        for item in high_priority:
            if 'page' in item:
                print(f"   1. Create page: /{item['page']}")
            elif 'link' in item:
                print(f"   2. Fix broken link: {item['link']} in {item['component']}")

if __name__ == "__main__":
    main()
