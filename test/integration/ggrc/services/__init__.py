# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

from contextlib import contextmanager

from ggrc.models.all_models import register_model
from ggrc.models.all_models import unregister_model
from ggrc.models.inflector import register_inflections
from ggrc.models.inflector import unregister_inflector

# Skip warning for model._inflector protected access
# pylint: disable=protected-access


@contextmanager
def model_registered(model):
  """Make a context where model is correctly registered"""
  # At the moment, model._inflector is registered in its __init__ and is
  # unregistered in ggrc.models.all_models. A possible fix would be to add
  # inflector registration to all_models.register_model or remove inflector
  # unregistration from all_models.unregister_model. As this change may cause
  # incompatibilities, for now the inflector is explicitly (un)registered here
  # for test purposes.
  register_model(model)
  register_inflections(model._inflector)
  yield
  unregister_inflector(model._inflector)
  unregister_model(model)
