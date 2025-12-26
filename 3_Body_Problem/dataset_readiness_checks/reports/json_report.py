"""
JSON report generator.
"""

import json
from pathlib import Path
from dataclasses import asdict
from ..datastructures import ValidationReport

class ReportEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return super().default(obj)
        except TypeError:
            if hasattr(obj, 'value'): # Enum
                return obj.value
            return str(obj)

def generate_json_report(report: ValidationReport, output_path: Path):
    """
    Generate a JSON report from validation results.
    """
    data = asdict(report)
    
    # Convert Enums to strings manually or use custom encoder
    # dataclasses.asdict doesn't handle Enums by default in older python or specific ways?
    # Actually asdict keeps the Enum object.
    
    with open(output_path, 'w') as f:
        json.dump(data, f, cls=ReportEncoder, indent=2)
