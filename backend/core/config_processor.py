import os
import json
try:
    import tomllib  # Python 3.11+
except ImportError:
    import tomli as tomllib
import yaml

class ConfigProcessor:
    @staticmethod
    def toml_to_json(input_path: str, output_dir: str) -> str:
        """Convert TOML to JSON"""
        filename = os.path.basename(input_path)
        name, _ = os.path.splitext(filename)
        output_path = os.path.join(output_dir, f"{name}.json")
        
        with open(input_path, 'rb') as f:
            data = tomllib.load(f)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        return output_path
    
    @staticmethod
    def toml_to_yaml(input_path: str, output_dir: str) -> str:
        """Convert TOML to YAML"""
        filename = os.path.basename(input_path)
        name, _ = os.path.splitext(filename)
        output_path = os.path.join(output_dir, f"{name}.yaml")
        
        with open(input_path, 'rb') as f:
            data = tomllib.load(f)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
        
        return output_path
    
    @staticmethod
    def env_to_json(input_path: str, output_dir: str) -> str:
        """Convert .env file to JSON"""
        filename = os.path.basename(input_path)
        name, _ = os.path.splitext(filename)
        output_path = os.path.join(output_dir, f"{name}.json")
        
        env_vars = {}
        
        with open(input_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                
                # Parse KEY=VALUE
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Remove quotes if present
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    
                    env_vars[key] = value
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(env_vars, f, indent=2)
        
        return output_path
    
    @staticmethod
    def json_to_env(input_path: str, output_dir: str) -> str:
        """Convert JSON to .env file"""
        filename = os.path.basename(input_path)
        name, _ = os.path.splitext(filename)
        output_path = os.path.join(output_dir, f"{name}.env")
        
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Generated from JSON\n\n")
            
            for key, value in data.items():
                # Quote values with spaces
                if isinstance(value, str) and ' ' in value:
                    f.write(f'{key}="{value}"\n')
                else:
                    f.write(f'{key}={value}\n')
        
        return output_path
    
    @staticmethod
    def validate_env(input_path: str, output_dir: str) -> str:
        """Validate .env file and report issues"""
        filename = os.path.basename(input_path)
        name, _ = os.path.splitext(filename)
        output_path = os.path.join(output_dir, f"{name}_validation.txt")
        
        issues = []
        seen_keys = {}
        
        with open(input_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                original_line = line
                line = line.strip()
                
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                
                # Check for = sign
                if '=' not in line:
                    issues.append(f"Line {line_num}: Missing '=' sign: {original_line.strip()}")
                    continue
                
                key, value = line.split('=', 1)
                key = key.strip()
                
                # Check for duplicate keys
                if key in seen_keys:
                    issues.append(f"Line {line_num}: Duplicate key '{key}' (first seen on line {seen_keys[key]})")
                else:
                    seen_keys[key] = line_num
                
                # Check for empty keys
                if not key:
                    issues.append(f"Line {line_num}: Empty key name")
                
                # Check for spaces in keys
                if ' ' in key:
                    issues.append(f"Line {line_num}: Key contains spaces: '{key}'")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"ENV File Validation Report\n")
            f.write(f"{'='*50}\n\n")
            f.write(f"File: {filename}\n")
            f.write(f"Total variables: {len(seen_keys)}\n\n")
            
            if issues:
                f.write(f"Issues found: {len(issues)}\n\n")
                for issue in issues:
                    f.write(f"⚠️  {issue}\n")
            else:
                f.write("✅ No issues found!\n")
        
        return output_path
