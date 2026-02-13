"""
WooCommerce database models.
Maps to tables with prefix 8jH_wc_* and 8jH_woocommerce_*
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional
from sqlmodel import SQLModel, Field


class WCOrder(SQLModel, table=True):
    """WooCommerce orders table (8jH_wc_orders)"""
    __tablename__ = "8jH_wc_orders"

    id: Optional[int] = Field(default=None, primary_key=True)
    status: Optional[str] = Field(default=None, max_length=20)
    currency: Optional[str] = Field(default=None, max_length=10)
    type: Optional[str] = Field(default=None, max_length=20)
    tax_amount: Optional[Decimal] = Field(default=None)
    total_amount: Optional[Decimal] = Field(default=None)
    customer_id: Optional[int] = Field(default=None)
    billing_email: Optional[str] = Field(default=None, max_length=320)
    date_created_gmt: Optional[datetime] = Field(default=None)
    date_updated_gmt: Optional[datetime] = Field(default=None)
    parent_order_id: Optional[int] = Field(default=None)
    payment_method: Optional[str] = Field(default=None, max_length=100)
    payment_method_title: Optional[str] = Field(default=None)
    transaction_id: Optional[str] = Field(default=None, max_length=100)
    ip_address: Optional[str] = Field(default=None, max_length=100)
    user_agent: Optional[str] = Field(default=None)
    customer_note: Optional[str] = Field(default=None)


class WCOrderMeta(SQLModel, table=True):
    """WooCommerce order meta table (8jH_wc_orders_meta)"""
    __tablename__ = "8jH_wc_orders_meta"

    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: Optional[int] = Field(default=None, foreign_key="8jH_wc_orders.id")
    meta_key: Optional[str] = Field(default=None, max_length=255)
    meta_value: Optional[str] = Field(default=None)


class WCOrderAddress(SQLModel, table=True):
    """WooCommerce order addresses table (8jH_wc_order_addresses)"""
    __tablename__ = "8jH_wc_order_addresses"

    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="8jH_wc_orders.id")
    address_type: Optional[str] = Field(default=None, max_length=20)
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    company: Optional[str] = Field(default=None)
    address_1: Optional[str] = Field(default=None)
    address_2: Optional[str] = Field(default=None)
    city: Optional[str] = Field(default=None)
    state: Optional[str] = Field(default=None)
    postcode: Optional[str] = Field(default=None)
    country: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None, max_length=320)
    phone: Optional[str] = Field(default=None, max_length=100)


class WCOrderOperationalData(SQLModel, table=True):
    """WooCommerce order operational data (8jH_wc_order_operational_data)"""
    __tablename__ = "8jH_wc_order_operational_data"

    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: Optional[int] = Field(default=None, foreign_key="8jH_wc_orders.id")
    created_via: Optional[str] = Field(default=None, max_length=100)
    woocommerce_version: Optional[str] = Field(default=None, max_length=20)
    prices_include_tax: Optional[bool] = Field(default=None)
    coupon_usages_are_counted: Optional[bool] = Field(default=None)
    download_permission_granted: Optional[bool] = Field(default=None)
    cart_hash: Optional[str] = Field(default=None, max_length=100)
    new_order_email_sent: Optional[bool] = Field(default=None)
    order_key: Optional[str] = Field(default=None, max_length=100)
    order_stock_reduced: Optional[bool] = Field(default=None)
    date_paid_gmt: Optional[datetime] = Field(default=None)
    date_completed_gmt: Optional[datetime] = Field(default=None)
    shipping_tax_amount: Optional[Decimal] = Field(default=None)
    shipping_total_amount: Optional[Decimal] = Field(default=None)
    discount_tax_amount: Optional[Decimal] = Field(default=None)
    discount_total_amount: Optional[Decimal] = Field(default=None)
    recorded_sales: Optional[bool] = Field(default=None)


class WCOrderItem(SQLModel, table=True):
    """WooCommerce order items (8jH_woocommerce_order_items)"""
    __tablename__ = "8jH_woocommerce_order_items"

    order_item_id: Optional[int] = Field(default=None, primary_key=True)
    order_item_name: str = Field(default="")
    order_item_type: str = Field(max_length=200, default="")
    order_id: int = Field(foreign_key="8jH_wc_orders.id")


class WCOrderItemMeta(SQLModel, table=True):
    """WooCommerce order item meta (8jH_woocommerce_order_itemmeta)"""
    __tablename__ = "8jH_woocommerce_order_itemmeta"

    meta_id: Optional[int] = Field(default=None, primary_key=True)
    order_item_id: int = Field(foreign_key="8jH_woocommerce_order_items.order_item_id")
    meta_key: Optional[str] = Field(default=None, max_length=255)
    meta_value: Optional[str] = Field(default=None)


class WCOrderStats(SQLModel, table=True):
    """WooCommerce order stats (8jH_wc_order_stats)"""
    __tablename__ = "8jH_wc_order_stats"

    order_id: int = Field(primary_key=True)
    parent_id: int = Field(default=0)
    date_created: datetime = Field(default_factory=datetime.now)
    date_created_gmt: datetime = Field(default_factory=datetime.now)
    num_items_sold: int = Field(default=0)
    total_sales: float = Field(default=0)
    tax_total: float = Field(default=0)
    shipping_total: float = Field(default=0)
    net_total: float = Field(default=0)
    returning_customer: Optional[bool] = Field(default=None)
    status: str = Field(max_length=20, default="")
    customer_id: int = Field(default=0)
    date_paid: Optional[datetime] = Field(default=None)
    date_completed: Optional[datetime] = Field(default=None)


class WCCustomerLookup(SQLModel, table=True):
    """WooCommerce customer lookup (8jH_wc_customer_lookup)"""
    __tablename__ = "8jH_wc_customer_lookup"

    customer_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="8jH_users.ID")
    username: str = Field(max_length=60, default="")
    first_name: str = Field(max_length=255, default="")
    last_name: str = Field(max_length=255, default="")
    email: Optional[str] = Field(default=None, max_length=100)
    date_last_active: Optional[datetime] = Field(default=None)
    date_registered: Optional[datetime] = Field(default=None)
    country: str = Field(max_length=2, default="")
    postcode: str = Field(max_length=20, default="")
    city: str = Field(max_length=100, default="")
    state: str = Field(max_length=100, default="")


class WCProductMetaLookup(SQLModel, table=True):
    """WooCommerce product meta lookup (8jH_wc_product_meta_lookup)"""
    __tablename__ = "8jH_wc_product_meta_lookup"

    product_id: int = Field(primary_key=True)
    sku: Optional[str] = Field(default="", max_length=100)
    virtual: Optional[bool] = Field(default=False)
    downloadable: Optional[bool] = Field(default=False)
    min_price: Optional[Decimal] = Field(default=None)
    max_price: Optional[Decimal] = Field(default=None)
    onsale: Optional[bool] = Field(default=False)
    stock_quantity: Optional[float] = Field(default=None)
    stock_status: Optional[str] = Field(default="instock", max_length=100)
    rating_count: Optional[int] = Field(default=0)
    average_rating: Optional[Decimal] = Field(default=None)
    total_sales: Optional[int] = Field(default=0)
    tax_status: Optional[str] = Field(default="taxable", max_length=100)
    tax_class: Optional[str] = Field(default="", max_length=100)
    global_unique_id: Optional[str] = Field(default="", max_length=100)


class WCSession(SQLModel, table=True):
    """WooCommerce sessions (8jH_woocommerce_sessions)"""
    __tablename__ = "8jH_woocommerce_sessions"

    session_id: Optional[int] = Field(default=None, primary_key=True)
    session_key: str = Field(max_length=32, default="")
    session_value: str = Field(default="")
    session_expiry: int = Field(default=0)


class WCWebhook(SQLModel, table=True):
    """WooCommerce webhooks (8jH_wc_webhooks)"""
    __tablename__ = "8jH_wc_webhooks"

    webhook_id: Optional[int] = Field(default=None, primary_key=True)
    status: str = Field(max_length=200, default="")
    name: str = Field(default="")
    user_id: int = Field(foreign_key="8jH_users.ID")
    delivery_url: str = Field(default="")
    secret: str = Field(default="")
    topic: str = Field(max_length=200, default="")
    date_created: datetime = Field(default_factory=datetime.now)
    date_created_gmt: datetime = Field(default_factory=datetime.now)
    date_modified: datetime = Field(default_factory=datetime.now)
    date_modified_gmt: datetime = Field(default_factory=datetime.now)
    api_version: int = Field(default=0)
    failure_count: int = Field(default=0)
    pending_delivery: bool = Field(default=False)


class WCApiKey(SQLModel, table=True):
    """WooCommerce API keys (8jH_woocommerce_api_keys)"""
    __tablename__ = "8jH_woocommerce_api_keys"

    key_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="8jH_users.ID")
    description: Optional[str] = Field(default=None, max_length=200)
    permissions: str = Field(max_length=10, default="")
    consumer_key: str = Field(max_length=64, default="")
    consumer_secret: str = Field(max_length=43, default="")
    nonces: Optional[str] = Field(default=None)
    truncated_key: str = Field(max_length=7, default="")
    last_access: Optional[datetime] = Field(default=None)


class WCDownloadableProductPermission(SQLModel, table=True):
    """WooCommerce downloadable product permissions (8jH_woocommerce_downloadable_product_permissions)"""
    __tablename__ = "8jH_woocommerce_downloadable_product_permissions"

    permission_id: Optional[int] = Field(default=None, primary_key=True)
    download_id: str = Field(max_length=36, default="")
    product_id: int = Field(default=0)
    order_id: int = Field(default=0)
    order_key: str = Field(max_length=200, default="")
    user_email: str = Field(max_length=200, default="")
    user_id: Optional[int] = Field(default=None, foreign_key="8jH_users.ID")
    downloads_remaining: Optional[str] = Field(default=None, max_length=9)
    access_granted: datetime = Field(default_factory=datetime.now)
    access_expires: Optional[datetime] = Field(default=None)
    download_count: int = Field(default=0)


class WCPaymentToken(SQLModel, table=True):
    """WooCommerce payment tokens (8jH_woocommerce_payment_tokens)"""
    __tablename__ = "8jH_woocommerce_payment_tokens"

    token_id: Optional[int] = Field(default=None, primary_key=True)
    gateway_id: str = Field(max_length=200, default="")
    token: str = Field(default="")
    user_id: int = Field(default=0, foreign_key="8jH_users.ID")
    type: str = Field(max_length=200, default="")
    is_default: bool = Field(default=False)


class WCPaymentTokenMeta(SQLModel, table=True):
    """WooCommerce payment token meta (8jH_woocommerce_payment_tokenmeta)"""
    __tablename__ = "8jH_woocommerce_payment_tokenmeta"

    meta_id: Optional[int] = Field(default=None, primary_key=True)
    payment_token_id: int = Field(foreign_key="8jH_woocommerce_payment_tokens.token_id")
    meta_key: Optional[str] = Field(default=None, max_length=255)
    meta_value: Optional[str] = Field(default=None)


class WCShippingZone(SQLModel, table=True):
    """WooCommerce shipping zones (8jH_woocommerce_shipping_zones)"""
    __tablename__ = "8jH_woocommerce_shipping_zones"

    zone_id: Optional[int] = Field(default=None, primary_key=True)
    zone_name: str = Field(max_length=200, default="")
    zone_order: int = Field(default=0)


class WCShippingZoneLocation(SQLModel, table=True):
    """WooCommerce shipping zone locations (8jH_woocommerce_shipping_zone_locations)"""
    __tablename__ = "8jH_woocommerce_shipping_zone_locations"

    location_id: Optional[int] = Field(default=None, primary_key=True)
    zone_id: int = Field(foreign_key="8jH_woocommerce_shipping_zones.zone_id")
    location_code: str = Field(max_length=200, default="")
    location_type: str = Field(max_length=40, default="")


class WCShippingZoneMethod(SQLModel, table=True):
    """WooCommerce shipping zone methods (8jH_woocommerce_shipping_zone_methods)"""
    __tablename__ = "8jH_woocommerce_shipping_zone_methods"

    instance_id: Optional[int] = Field(default=None, primary_key=True)
    zone_id: int = Field(foreign_key="8jH_woocommerce_shipping_zones.zone_id")
    method_id: str = Field(max_length=200, default="")
    method_order: int = Field(default=0)
    is_enabled: bool = Field(default=True)


class WCTaxRate(SQLModel, table=True):
    """WooCommerce tax rates (8jH_woocommerce_tax_rates)"""
    __tablename__ = "8jH_woocommerce_tax_rates"

    tax_rate_id: Optional[int] = Field(default=None, primary_key=True)
    tax_rate_country: str = Field(max_length=2, default="")
    tax_rate_state: str = Field(max_length=200, default="")
    tax_rate: str = Field(max_length=8, default="")
    tax_rate_name: str = Field(max_length=200, default="")
    tax_rate_priority: int = Field(default=0)
    tax_rate_compound: int = Field(default=0)
    tax_rate_shipping: int = Field(default=1)
    tax_rate_order: int = Field(default=0)
    tax_rate_class: str = Field(max_length=200, default="")


class WCOrderTaxLookup(SQLModel, table=True):
    """WooCommerce order tax lookup (8jH_wc_order_tax_lookup)"""
    __tablename__ = "8jH_wc_order_tax_lookup"

    order_id: int = Field(primary_key=True)
    tax_rate_id: int = Field(primary_key=True)
    date_created: datetime = Field(default_factory=datetime.now)
    shipping_tax: float = Field(default=0)
    order_tax: float = Field(default=0)
    total_tax: float = Field(default=0)


class WCProductAttributeLookup(SQLModel, table=True):
    """WooCommerce product attribute lookup (8jH_wc_product_attributes_lookup)"""
    __tablename__ = "8jH_wc_product_attributes_lookup"

    product_id: int = Field(primary_key=True)
    product_or_parent_id: int = Field(default=0)
    taxonomy: str = Field(max_length=32, default="")
    term_id: int = Field(default=0)
    is_variation_attribute: bool = Field(default=False)
    in_stock: bool = Field(default=False)


class WCReservedStock(SQLModel, table=True):
    """WooCommerce reserved stock (8jH_wc_reserved_stock)"""
    __tablename__ = "8jH_wc_reserved_stock"

    order_id: int = Field(primary_key=True)
    product_id: int = Field(primary_key=True)
    stock_quantity: float = Field(default=0)
    timestamp: datetime = Field(default_factory=datetime.now)
    expires: datetime = Field(default_factory=datetime.now)


class WCTaxRateClass(SQLModel, table=True):
    """WooCommerce tax rate classes (8jH_wc_tax_rate_classes)"""
    __tablename__ = "8jH_wc_tax_rate_classes"

    tax_rate_class_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=200, default="")
    slug: str = Field(max_length=200, default="")


class WCProductDownloadDirectory(SQLModel, table=True):
    """WooCommerce product download directories (8jH_wc_product_download_directories)"""
    __tablename__ = "8jH_wc_product_download_directories"

    url_id: Optional[int] = Field(default=None, primary_key=True)
    url: str = Field(max_length=256, default="")
    enabled: bool = Field(default=False)


class WCRateLimit(SQLModel, table=True):
    """WooCommerce rate limits (8jH_wc_rate_limits)"""
    __tablename__ = "8jH_wc_rate_limits"

    rate_limit_id: Optional[int] = Field(default=None, primary_key=True)
    rate_limit_key: str = Field(max_length=200, default="")
    rate_limit_expiry: int = Field(default=0)
    rate_limit_remaining: int = Field(default=0)


class WCCategoryLookup(SQLModel, table=True):
    """WooCommerce category lookup (8jH_wc_category_lookup)"""
    __tablename__ = "8jH_wc_category_lookup"

    category_tree_id: int = Field(primary_key=True)
    category_id: int = Field(primary_key=True)


class WCOrderCouponLookup(SQLModel, table=True):
    """WooCommerce order coupon lookup (8jH_wc_order_coupon_lookup)"""
    __tablename__ = "8jH_wc_order_coupon_lookup"

    order_id: int = Field(primary_key=True)
    coupon_id: int = Field(primary_key=True)
    date_created: datetime = Field(default_factory=datetime.now)
    discount_amount: float = Field(default=0)


class WCOrderProductLookup(SQLModel, table=True):
    """WooCommerce order product lookup (8jH_wc_order_product_lookup)"""
    __tablename__ = "8jH_wc_order_product_lookup"

    order_item_id: int = Field(primary_key=True)
    order_id: int = Field(default=0)
    product_id: int = Field(default=0)
    variation_id: int = Field(default=0)
    customer_id: Optional[int] = Field(default=None)
    date_created: datetime = Field(default_factory=datetime.now)
    product_qty: int = Field(default=0)
    product_net_revenue: float = Field(default=0)
    product_gross_revenue: float = Field(default=0)
    coupon_amount: float = Field(default=0)
    tax_amount: float = Field(default=0)
    shipping_amount: float = Field(default=0)
    shipping_tax_amount: float = Field(default=0)


class WCDownloadLog(SQLModel, table=True):
    """WooCommerce download log (8jH_wc_download_log)"""
    __tablename__ = "8jH_wc_download_log"

    download_log_id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.now)
    permission_id: int = Field(default=0)
    user_id: Optional[int] = Field(default=None)
    user_ip_address: Optional[str] = Field(default="", max_length=100)


class WCLog(SQLModel, table=True):
    """WooCommerce logs (8jH_woocommerce_log)"""
    __tablename__ = "8jH_woocommerce_log"

    log_id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.now)
    level: int = Field(default=0)
    source: str = Field(max_length=200, default="")
    message: str = Field(default="")
    context: Optional[str] = Field(default=None)


class WCAttributeTaxonomy(SQLModel, table=True):
    """WooCommerce attribute taxonomies (8jH_woocommerce_attribute_taxonomies)"""
    __tablename__ = "8jH_woocommerce_attribute_taxonomies"

    attribute_id: Optional[int] = Field(default=None, primary_key=True)
    attribute_name: str = Field(max_length=200, default="")
    attribute_label: Optional[str] = Field(default=None, max_length=200)
    attribute_type: str = Field(max_length=20, default="")
    attribute_orderby: str = Field(max_length=20, default="")
    attribute_public: int = Field(default=1)
