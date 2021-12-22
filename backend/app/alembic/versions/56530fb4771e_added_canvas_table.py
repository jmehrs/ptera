"""added Canvas table

Revision ID: 56530fb4771e
Revises: a1cce7a733d6
Create Date: 2021-11-22 02:17:46.169868

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from app.models.model_base import JSONBType

# revision identifiers, used by Alembic.
revision = "56530fb4771e"
down_revision = "a1cce7a733d6"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "canvas",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=True),
        sa.Column("canvas", JSONBType(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_canvas")),
    )
    op.create_table(
        "scheduleentry",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=True),
        sa.Column("canvas_id", sa.Integer(), nullable=True),
        sa.Column("interval_id", sa.Integer(), nullable=True),
        sa.Column("crontab_id", sa.Integer(), nullable=True),
        sa.Column("enabled", sa.Boolean(), nullable=True),
        sa.Column("last_run_at", sa.DateTime(), nullable=True),
        sa.Column("total_run_count", sa.Integer(), nullable=True),
        sa.Column("date_changed", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["crontab_id"],
            ["crontabschedule.id"],
            name=op.f("fk_scheduleentry_crontab_id_crontabschedule"),
        ),
        sa.ForeignKeyConstraint(
            ["interval_id"],
            ["intervalschedule.id"],
            name=op.f("fk_scheduleentry_interval_id_intervalschedule"),
        ),
        sa.ForeignKeyConstraint(
            ["canvas_id"],
            ["canvas.id"],
            name=op.f("fk_scheduleentry_canvas_id_canvas"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_scheduleentry")),
    )
    op.drop_table("canvasscheduleentry")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "canvasscheduleentry",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("name", sa.VARCHAR(length=255), autoincrement=False, nullable=True),
        sa.Column(
            "signature",
            JSONBType(),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("interval_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("crontab_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("enabled", sa.BOOLEAN(), autoincrement=False, nullable=True),
        sa.Column(
            "last_run_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.Column("total_run_count", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column(
            "date_changed", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["crontab_id"],
            ["crontabschedule.id"],
            name="fk_canvasscheduleentry_crontab_id_crontabschedule",
        ),
        sa.ForeignKeyConstraint(
            ["interval_id"],
            ["intervalschedule.id"],
            name="fk_canvasscheduleentry_interval_id_intervalschedule",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_canvasscheduleentry"),
    )
    op.drop_table("scheduleentry")
    op.drop_table("canvas")
    # ### end Alembic commands ###
