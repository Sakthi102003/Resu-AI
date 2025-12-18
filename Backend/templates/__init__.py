"""Resume Templates Package"""

from .auto_cv import AutoCVTemplate
from .anti_cv import AntiCVTemplate
from .ethan_template import EthanTemplate
from .rendercv_classic import RenderCVClassicTemplate
from .rendercv_engineering import RenderCVEngineeringTemplate
from .rendercv_sb2nov import RenderCVSb2novTemplate
from .yuan_template import YuanTemplate

__all__ = [
    'AutoCVTemplate',
    'AntiCVTemplate',
    'EthanTemplate',
    'RenderCVClassicTemplate',
    'RenderCVEngineeringTemplate',
    'RenderCVSb2novTemplate',
    'YuanTemplate'
]

# Template registry
TEMPLATES = {
    'auto_cv': AutoCVTemplate,
    'anti_cv': AntiCVTemplate,
    'ethan': EthanTemplate,
    'rendercv_classic': RenderCVClassicTemplate,
    'rendercv_engineering': RenderCVEngineeringTemplate,
    'rendercv_sb2nov': RenderCVSb2novTemplate,
    'yuan': YuanTemplate,
}
