"""Phase 40 training-driver layer (v2.0 BUILD milestone, FUT-04).

This package owns the CTL-PINN stage-0 curriculum training loop: the
``CurriculumController`` that drives outer stage progression, the
``RunController`` that runs one stage's inner Adam->L-BFGS closure, the
``TrainingConfig`` that pins the run/stage/opt/loss contract (Phase 41's
YAML-mapping seam), and the ``CheckpointStore`` protocol (Phase 41's
atomic/retention/promotion seam) -- the four Phase-41/42 seam types every
downstream consumer imports from this one namespace (CTX-33).

Importing this package binds these four names but performs NO model build and
NO dataset discovery: nothing here constructs a network, opens a dataset, or
touches the filesystem beyond loading their defining submodules, so
``import pinn.training`` is side-effect-free and safe at the top of any
module (mirrors the ``pinn/data/__init__.py`` / ``pinn/verification/__init__.py``
discipline).
"""

from pinn.training.checkpoint import CheckpointStore
from pinn.training.config import TrainingConfig
from pinn.training.controllers import CurriculumController, RunController

__all__ = ["TrainingConfig", "CurriculumController", "RunController", "CheckpointStore"]
