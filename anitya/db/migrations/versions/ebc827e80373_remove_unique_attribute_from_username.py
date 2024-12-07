"""Remove unique attribute from username

Revision ID: ebc827e80373
Revises: 8ba7d4c42044
Create Date: 2024-12-05 16:24:01.098473
"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "ebc827e80373"
down_revision = "8ba7d4c42044"


def upgrade():
    """Alembic migration."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("ix_users_username", "users", type_="unique")
    # ### end Alembic commands ###


def downgrade():
    """Downgrade migration."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint("ix_users_username", "users", ["username"])
    # ### end Alembic commands ###
