from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7f31d60e36e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'game',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=120), nullable=False),
        sa.Column('colors', sa.String(length=255)),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('sr_turn1', sa.Boolean()),
        sa.Column('result', sa.String(length=50)),
        sa.Column('turns', sa.Integer()),
        sa.Column('end_condition', sa.String(length=255)),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id']),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('game')
