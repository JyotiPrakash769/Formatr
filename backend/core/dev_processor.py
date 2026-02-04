import os
import json
import yaml
import xmltodict
import base64
import markdown
from xhtml2pdf import pisa

class DevProcessor:
    @staticmethod
    def convert_config(input_path: str, target_format: str, output_dir: str) -> str:
        """
        Convert between JSON, YAML, and XML.
        """
        filename = os.path.basename(input_path)
        name, _ = os.path.splitext(filename)
        output_path = os.path.join(output_dir, f"{name}.{target_format}")
        
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse Input
        data = None
        try:
            # Try parsing as JSON
            data = json.loads(content)
        except json.JSONDecodeError:
            try:
                # Try parsing as YAML
                data = yaml.safe_load(content)
            except yaml.YAMLError:
                try:
                    # Try parsing as XML
                    data = xmltodict.parse(content)
                    # xmltodict usually wraps root, unwrap if needed or keep consistent
                    if len(data) == 1:
                        key = list(data.keys())[0]
                        # Optional: unwrap root if converting to JSON/YAML for cleaner structure?
                        # For now keep it raw to ensure reversibility
                except Exception:
                    pass
        
        if data is None:
            raise ValueError("Could not parse input file. Ensure it is valid JSON, YAML, or XML.")

        # Write Output
        with open(output_path, 'w', encoding='utf-8') as f:
            if target_format == 'json':
                json.dump(data, f, indent=2)
            elif target_format == 'yaml':
                yaml.dump(data, f, default_flow_style=False)
            elif target_format == 'xml':
                # wrap in root if not present (xml must has single root)
                if len(data) > 1:
                    data = {'root': data}
                xmltodict.unparse(data, f, pretty=True)
            else:
                raise ValueError(f"Unsupported target format: {target_format}")
                
        return output_path

    @staticmethod
    def base64_encode(input_path: str, output_dir: str) -> str:
        """
        Encode file content to Base64 text file.
        """
        filename = os.path.basename(input_path)
        output_path = os.path.join(output_dir, f"{filename}.b64.txt")
        
        with open(input_path, 'rb') as f:
            encoded = base64.b64encode(f.read()).decode('utf-8')
            
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(encoded)
            
        return output_path

    @staticmethod
    def base64_decode(input_path: str, output_dir: str) -> str:
        """
        Decode Base64 text file back to original.
        """
        filename = os.path.basename(input_path)
        # Remove .b64.txt or .txt suffix
        name = filename.replace('.b64.txt', '').replace('.txt', '')
        # If we don't know extension, default to .bin, but user usually converts "image.png.b64.txt" -> "image.png"
        output_path = os.path.join(output_dir, name)
        
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            
        with open(output_path, 'wb') as f:
            f.write(base64.b64decode(content))
            
        return output_path

    @staticmethod
    def md_to_pdf(input_path: str, output_dir: str) -> str:
        """
        Convert Markdown to PDF.
        """
        filename = os.path.basename(input_path)
        name, _ = os.path.splitext(filename)
        output_path = os.path.join(output_dir, f"{name}.pdf")
        
        with open(input_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
            
        # Convert MD to HTML
        html_content = markdown.markdown(md_content, extensions=['extra', 'codehilite', 'tables'])
        
        # Add basic styling for PDF
        styled_html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Helvetica, Arial, sans-serif; font-size: 12pt; line-height: 1.5; }}
                h1, h2, h3 {{ color: #333; }}
                code {{ background: #f4f4f4; padding: 2px 5px; border-radius: 3px; font-family: monospace; }}
                pre {{ background: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        # Convert HTML to PDF
        with open(output_path, "wb") as f:
            pisa_status = pisa.CreatePDF(styled_html, dest=f)
            
        if pisa_status.err:
            raise Exception("PDF generation failed")
            
        return output_path
