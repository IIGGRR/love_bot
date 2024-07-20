"""nullable photo name

Revision ID: 5e1c66fe6243
Revises: 16547be8789f
Create Date: 2024-07-20 12:47:11.614946

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5e1c66fe6243"
down_revision: Union[str, None] = "16547be8789f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
