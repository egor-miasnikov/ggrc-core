# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Utility class for handling revisions."""

from logging import getLogger

from ggrc import db
from ggrc.login import get_current_user_id
from ggrc.models import all_models

logger = getLogger(__name__)


def _get_new_objects():
  """Returns list of new objects"""
  result = db.session.execute("""
      SELECT obj_id, obj_type, action FROM objects_without_revisions
  """).fetchall()
  return result


def _get_new_objects_count():
  """Returns count of new objects"""
  return db.session.execute("SELECT count(*) "
                            "FROM objects_without_revisions").scalar()


def _get_chunks(objects, size):
  """Yield sized chunks from objects."""
  for i in xrange(0, len(objects), size):
    yield objects[i:i + size]


def build_revision_body(obj_id, obj_type, obj_content, event_id, action):
  """Build revision body"""
  return {
      "resource_id": obj_id,
      "resource_type": obj_type,
      "resource_slug": obj_content.get("slug"),
      "event_id": event_id,
      "action": action,
      "content": obj_content,
      "context_id": obj_content.get("context_id"),
      "modified_by_id": (obj_content.get("modified_by_id") or
                         get_current_user_id()),
      "source_type": obj_content.get("source_type"),
      "source_id": obj_content.get("source_id"),
      "destination_type": obj_content.get("destination_type"),
      "destination_id": obj_content.get("destination_id")
  }


def do_missing_revisions():
  """Crate 'created/modified' revisions.

  Iterate thought objects in objects_without_revisions
  table and create revisions
  """
  event = all_models.Event(action="BULK")
  db.session.add(event)
  db.session.commit()
  revisions_table = all_models.Revision.__table__
  count = _get_new_objects_count()
  chunk_size = 100
  logger.info("Crating revision content...")
  for index, chunk in enumerate(_get_chunks(_get_new_objects(),
                                            chunk_size), 1):
    logger.info("Processing chunk %s of %s", index, count / chunk_size + 1)
    revisions = []
    for obj_id, obj_type, action in chunk:
      model = getattr(all_models, obj_type, None)
      if not model:
        logger.warning("Failed to update revisions"
                       " for invalid model: %s", obj_type)
        continue

      if not hasattr(model, "log_json"):
        logger.warning("Model '%s' has no log_json method,"
                       " revision generation skipped", obj_type)
        continue
      obj = model.query.get(obj_id)
      if not obj and action == u"deleted":
        obj_content = get_last_revision_content(obj_type, obj_id)
        if not obj_content:
          logger.info("Revision for Object '%s' with id '%s' does't exists,"
                      " 'deleted' revision generation skipped",
                      obj_type, obj_id)
          continue
        revisions.append(build_revision_body(
            obj_id, obj_type, obj_content, event.id, action
        ))
      elif not obj:
        logger.info("Object '%s' with id '%s' does't exists,"
                    " revision generation skipped", obj_type, obj_id)
        continue
      else:
        obj_content = obj.log_json()
        revisions.append(build_revision_body(
            obj_id, obj_type, obj_content, event.id, action
        ))
    db.session.execute(revisions_table.insert(), revisions)
    db.session.commit()
  db.session.execute("truncate objects_without_revisions")


def get_last_revision_content(obj_type, obj_id):
  """Create 'deleted' revision content

   we need to get content of latest known revision
   """
  content = None
  last_revision = all_models.Revision.query.filter_by(
      resource_type=obj_type, resource_id=obj_id
  ).order_by(all_models.Revision.created_at.desc()).first()
  if last_revision and last_revision.action == u"deleted":
    logger.info("Deleted revision already logged for Object '%s' "
                "with id '%s', 'deleted' revision generation skipped",
                obj_type, obj_id)
  else:
    content = last_revision.content if last_revision else None
  return content
