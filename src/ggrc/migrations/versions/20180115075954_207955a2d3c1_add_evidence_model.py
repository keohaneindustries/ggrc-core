# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Add Evidence model

Create Date: 2018-01-15 07:59:54.664574
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '207955a2d3c1'
down_revision = 'e4403da2933a'


def create_evidence_table():
  """Create evidence table in DB"""
  op.create_table(
      'evidence',
      sa.Column('id', sa.Integer(), nullable=False),
      sa.Column('link', sa.String(length=250), nullable=False),
      sa.Column('source_gdrive_id', sa.String(length=250),
                nullable=False, default=u""),
      sa.Column('gdrive_id', sa.String(length=250),
                nullable=False, default=u""),
      sa.Column('description', sa.Text(), nullable=False),
      sa.Column('kind', sa.Enum('URL', 'FILE'),
                nullable=False),
      sa.Column('title', sa.String(length=250), nullable=False),
      sa.Column('slug', sa.String(length=250), nullable=False),
      sa.Column('updated_at', sa.DateTime(), nullable=False),
      sa.Column('modified_by_id', sa.Integer(), nullable=True),
      sa.Column('created_at', sa.DateTime(), nullable=False),
      sa.Column('last_deprecated_date', sa.Date),
      sa.Column('context_id', sa.Integer(), nullable=True),
      sa.Column('status', sa.String(length=250), nullable=False,
                server_default='Active'),
      sa.Column('recipients', sa.String(length=250), nullable=True),
      sa.Column('send_by_default', sa.Boolean(), nullable=True),
      sa.ForeignKeyConstraint(['context_id'], ['contexts.id']),
      sa.PrimaryKeyConstraint('id'),
      sa.UniqueConstraint('slug', name='uq_control_evidence')
  )
  op.create_index('fk_evidence_contexts', 'evidence',
                  ['context_id'], unique=False)
  op.create_index('ix_evidence_updated_at', 'evidence',
                  ['updated_at'], unique=False)


def add_evidence_admin_role():
  """Add Evidence Admin roles"""
  add_evidence_admin = """
    INSERT INTO access_control_roles (
        name,
        object_type,
        access_control_roles.delete,
        created_at,
        updated_at,
        mandatory,
        default_to_current_user,
        non_editable
    )
    VALUES (
        'Admin',
        'Evidence',
        0,
        NOW(),
        NOW(),
        1,
        1,
        1
    )
  """
  op.execute(add_evidence_admin)


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  create_evidence_table()
  add_evidence_admin_role()


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  op.drop_table('evidence')
