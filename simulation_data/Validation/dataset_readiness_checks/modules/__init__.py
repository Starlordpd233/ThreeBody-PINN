from .correspondence import validate_correspondence
from .file_format import validate_ic_format, validate_brutus_format
from .completeness import validate_completeness
from .metadata import validate_metadata
from .physics import validate_ic_physics
from .parameters import validate_parameters
from .metrics import validate_metrics
from .blacklist import validate_against_blacklist

# Enhanced modules
from .coverage import validate_coverage
from .curriculum import validate_curriculum
# from .duplicates import validate_duplicates # Not per-file
from .temporal import validate_temporal