from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1837047c988'
down_revision = 'c7f31d60e36e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('game', sa.Column('turn_order', sa.String(length=50), nullable=True))
    op.add_column('game', sa.Column('notes', sa.Text(), nullable=True))


def downgrade():
    op.drop_column('game', 'turn_order')
    op.drop_column('game', 'notes')





