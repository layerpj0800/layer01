from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "plans",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("channel_id", sa.Integer, sa.ForeignKey("channels.id", ondelete="CASCADE"), nullable=False),
        sa.Column("price", sa.Integer, nullable=False),
        sa.Column("interval", sa.String(20), nullable=False, server_default="month"),
        sa.Column("trial_days", sa.Integer, nullable=False, server_default="0"),
    )

    op.create_table(
        "subscriptions",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("plan_id", sa.Integer, sa.ForeignKey("plans.id", ondelete="CASCADE"), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="active"),
        sa.Column("current_period_end", sa.DateTime(timezone=True), nullable=False),
        sa.Column("merchant_uid", sa.String(255), nullable=False, unique=True),
    )
    op.create_index(
        "ix_subscriptions_user_status_end",
        "subscriptions",
        ["user_id", "status", "current_period_end"],
    )

    op.create_table(
        "payment_events",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("provider", sa.String(50), nullable=False),
        sa.Column("type", sa.String(50), nullable=False),
        sa.Column("payload_json", sa.JSON(), nullable=False),
        sa.Column("subscription_id", sa.Integer, sa.ForeignKey("subscriptions.id")),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("payment_events")
    op.drop_index("ix_subscriptions_user_status_end", table_name="subscriptions")
    op.drop_table("subscriptions")
    op.drop_table("plans")
