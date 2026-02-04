import os
import jsbeautifier
import cssbeautifier
from bs4 import BeautifulSoup

class CodeFormatter:
    @staticmethod
    def beautify_js(input_path: str, output_dir: str) -> str:
        """Beautify/prettify JavaScript code"""
        filename = os.path.basename(input_path)
        name, ext = os.path.splitext(filename)
        output_path = os.path.join(output_dir, f"{name}_formatted{ext}")
        
        with open(input_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        opts = jsbeautifier.default_options()
        opts.indent_size = 2
        formatted = jsbeautifier.beautify(code, opts)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(formatted)
        
        return output_path
    
    @staticmethod
    def minify_js(input_path: str, output_dir: str) -> str:
        """Minify JavaScript code (basic)"""
        filename = os.path.basename(input_path)
        name, ext = os.path.splitext(filename)
        output_path = os.path.join(output_dir, f"{name}.min{ext}")
        
        with open(input_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Basic minification: remove comments and extra whitespace
        lines = [line.strip() for line in code.split('\n') if line.strip() and not line.strip().startswith('//')]
        minified = ' '.join(lines)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(minified)
        
        return output_path
    
    @staticmethod
    def beautify_css(input_path: str, output_dir: str) -> str:
        """Beautify/prettify CSS code"""
        filename = os.path.basename(input_path)
        name, ext = os.path.splitext(filename)
        output_path = os.path.join(output_dir, f"{name}_formatted{ext}")
        
        with open(input_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        opts = cssbeautifier.default_options()
        opts.indent_size = 2
        formatted = cssbeautifier.beautify(code, opts)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(formatted)
        
        return output_path
    
    @staticmethod
    def minify_css(input_path: str, output_dir: str) -> str:
        """Minify CSS code (basic)"""
        filename = os.path.basename(input_path)
        name, ext = os.path.splitext(filename)
        output_path = os.path.join(output_dir, f"{name}.min{ext}")
        
        with open(input_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Basic minification: remove comments and extra whitespace
        import re
        minified = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        minified = re.sub(r'\s+', ' ', minified)
        minified = minified.replace(' {', '{').replace('{ ', '{')
        minified = minified.replace(' }', '}').replace('} ', '}')
        minified = minified.replace(': ', ':').replace('; ', ';')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(minified)
        
        return output_path
    
    @staticmethod
    def beautify_html(input_path: str, output_dir: str) -> str:
        """Beautify/prettify HTML code"""
        filename = os.path.basename(input_path)
        name, ext = os.path.splitext(filename)
        output_path = os.path.join(output_dir, f"{name}_formatted{ext}")
        
        with open(input_path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        soup = BeautifulSoup(html, 'html.parser')
        formatted = soup.prettify()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(formatted)
        
        return output_path
    
    @staticmethod
    def minify_html(input_path: str, output_dir: str) -> str:
        """Minify HTML code"""
        filename = os.path.basename(input_path)
        name, ext = os.path.splitext(filename)
        output_path = os.path.join(output_dir, f"{name}.min{ext}")
        
        with open(input_path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        # Basic minification
        import re
        minified = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
        minified = re.sub(r'\s+', ' ', minified)
        minified = minified.replace('> <', '><')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(minified)
        
        return output_path
