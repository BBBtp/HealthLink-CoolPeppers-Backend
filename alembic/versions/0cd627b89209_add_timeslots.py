"""add timeslots

Revision ID: 0cd627b89209
Revises: b285de58b65a
Create Date: 2025-03-20 10:13:57.729906

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '0cd627b89209'
down_revision: Union[str, None] = 'b285de58b65a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('appointment_slots',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('doctor_id', sa.Integer(), nullable=True),
    sa.Column('slot_time', sa.DateTime(), nullable=False),
    sa.Column('status', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['doctor_id'], ['doctors.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_appointment_slots_id'), 'appointment_slots', ['id'], unique=False)
    op.add_column('appointments', sa.Column('appointment_slot_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'appointments', 'appointment_slots', ['appointment_slot_id'], ['id'])
    op.drop_column('appointments', 'date')
    op.drop_column('appointments', 'time')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('appointments', sa.Column('time', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('appointments', sa.Column('date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'appointments', type_='foreignkey')
    op.drop_column('appointments', 'appointment_slot_id')
    op.drop_index(op.f('ix_appointment_slots_id'), table_name='appointment_slots')
    op.drop_table('appointment_slots')
    # ### end Alembic commands ###
