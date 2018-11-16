# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Add missing roles for scope objects

Create Date: 2018-11-12 12:45:24.412395
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

from alembic import op
from sqlalchemy import text
from ggrc.migrations import utils


# revision identifiers, used by Alembic.
revision = 'e3bbe8b7b0c9'
down_revision = '9beabcd92f34'


SCOPING_OBJECTS = [
    ("AccessGroup", "access_groups"),
    ("DataAsset", "data_assets"),
    ("Facility", "facilities"),
    ("Market", "markets"),
    ("Metric", "metrics"),
    ("OrgGroup", "org_groups"),
    ("Process", "systems"),
    ("Product", "products"),
    ("ProductGroup", "product_groups"),
    ("Project", "projects"),
    ("System", "systems"),
    ("TechnologyEnvironment", "technology_environments"),
    ("Vendor", "vendors")
]


ROLE_TYPES = [
    "Admin",
    "Assignee",
    "Verifier"
]


def load_scope_object_data(conn, scope_object_type, scope_table, role_id):
  """Load all necessary data for migration"""

  specific_condition = ""
  if scope_object_type == "Process":
    specific_condition = "AND is_biz_process IS TRUE"
  elif scope_object_type == "System":
    specific_condition = "AND is_biz_process IS FALSE"

  sql = """
    SELECT so.id as obj_id, rev.modified_by_id as creator_id
    FROM {} so
    LEFT JOIN access_control_list acl
    ON so.id = acl.object_id AND
      acl.object_type=:scope_object AND
      acl.ac_role_id =:role_id
    LEFT JOIN revisions rev
    ON rev.resource_type=:scope_object AND
      rev.action = 'created' AND
      rev.resource_id = so.id
    WHERE acl.id IS NULL AND rev.id IS NOT NULL {}
    GROUP BY so.id
  """.format(scope_table, specific_condition)

  return conn.execute(
      text(sql),
      scope_object=scope_object_type,
      role_id=role_id
  ).fetchall()


def create_acl_record(conn, acr_id, object_id, object_type):
  """Create new acl record in data base"""

  sql = """
    INSERT INTO access_control_list (
      ac_role_id,
      object_id,
      object_type,
      created_at,
      updated_at
    ) VALUES (
      :ac_role_id,
      :object_id,
      :object_type,
      NOW(),
      NOW()
    );
  """

  conn.execute(
      text(sql),
      ac_role_id=acr_id,
      object_id=object_id,
      object_type=object_type
  )

  return utils.last_insert_id(conn)


def create_acp_record(conn, person_id, modified_by_id):
  """Create new acp record in database"""

  sql = """
    INSERT INTO access_control_people (
      person_id,
      ac_list_id,
      updated_at,
      created_at
    ) VALUES (
      :person_id,
      :modified_by_id,
      NOW(),
      NOW()
    );
  """
  return conn.execute(
      text(sql),
      person_id=person_id,
      modified_by_id=modified_by_id
  )


def get_role_id(conn, object_type, role_type):
  """ Get role ID base-on type and object"""

  sql = """
    SELECT id FROM access_control_roles
    WHERE name =:role_type AND object_type=:object_type
  """
  return conn.execute(
      text(sql),
      object_type=object_type,
      role_type=role_type
  ).fetchone()['id']


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""

  conn = op.get_bind()
  for so in SCOPING_OBJECTS:
    scope_object_type = so[0]
    scope_table = so[1]
    for role in ROLE_TYPES:
      role_id = get_role_id(conn, scope_object_type, role)
      scope_objects = load_scope_object_data(
          conn,
          scope_object_type,
          scope_table,
          role_id
      )
      for scope_object in scope_objects:
        object_id = scope_object[0]
        creator_id = scope_object[1]
        acl_record_id = create_acl_record(
            conn,
            role_id,
            object_id,
            scope_object_type
        )
        create_acp_record(conn, creator_id, acl_record_id)


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
