"""create user table

Revision ID: 820b3bd13910
Revises: 
Create Date: 2021-10-10 15:56:50.736142

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '820b3bd13910'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("full_name", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("hashed_password", sa.String(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("is_superuser", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("user")
