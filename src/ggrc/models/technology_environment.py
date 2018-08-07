# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""TechnologyEnvironment model."""

from ggrc import db
from ggrc.access_control.roleable import Roleable
from ggrc.fulltext.mixin import Indexed
from ggrc.models.comment import Commentable
from ggrc.models import mixins
from ggrc.models.object_document import PublicDocumentable
from ggrc.models.object_person import Personable
from ggrc.models.relationship import Relatable
from ggrc.models import track_object_state


class TechnologyEnvironment(mixins.CustomAttributable,
                            Personable,
                            Roleable,
                            Relatable,
                            PublicDocumentable,
                            track_object_state.HasObjectState,
                            Commentable,
                            mixins.TestPlanned,
                            mixins.LastDeprecatedTimeboxed,
                            mixins.base.ContextRBAC,
                            mixins.BusinessObject,
                            mixins.Folderable,
                            db.Model,
                            Indexed):
  """Representation for TechnologyEnvironment model."""
  __tablename__ = 'technology_environments'
