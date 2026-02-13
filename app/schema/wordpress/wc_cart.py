"""
WooCommerce Cart and Checkout Schemas.
Schemas for managing shopping cart and checkout process.
"""
from typing import List, Optional
from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, Field


class WCCartItem(BaseModel):
    """Single item in the cart"""
    product_id: int = Field(..., description="Product ID")
    variation_id: Optional[int] = Field(None, description="Variation ID for variable products")
    quantity: int = Field(1, ge=1, description="Quantity")
    product_name: Optional[str] = Field(None, description="Product name")
    product_price: Optional[Decimal] = Field(None, description="Unit price")
    line_total: Optional[Decimal] = Field(None, description="Total for this line item")
    product_image: Optional[str] = Field(None, description="Product thumbnail URL")

    class Config:
        from_attributes = True


class WCCart(BaseModel):
    """Full shopping cart"""
    user_id: int = Field(..., description="User ID")
    items: List[WCCartItem] = Field(default_factory=list, description="Cart items")
    subtotal: Decimal = Field(default=Decimal("0.00"), description="Subtotal before discounts/shipping")
    discount_total: Decimal = Field(default=Decimal("0.00"), description="Total discount")
    shipping_total: Decimal = Field(default=Decimal("0.00"), description="Shipping cost")
    tax_total: Decimal = Field(default=Decimal("0.00"), description="Tax total")
    total: Decimal = Field(default=Decimal("0.00"), description="Final total")
    item_count: int = Field(default=0, description="Total number of items")
    coupon_codes: List[str] = Field(default_factory=list, description="Applied coupon codes")
    created_at: Optional[datetime] = Field(None, description="Cart creation time")
    updated_at: Optional[datetime] = Field(None, description="Last update time")

    class Config:
        from_attributes = True


class WCAddToCartRequest(BaseModel):
    """Request to add item to cart"""
    product_id: int = Field(..., description="Product ID to add")
    variation_id: Optional[int] = Field(None, description="Variation ID for variable products")
    quantity: int = Field(1, ge=1, description="Quantity to add")


class WCUpdateCartItemRequest(BaseModel):
    """Request to update cart item quantity"""
    product_id: int = Field(..., description="Product ID to update")
    variation_id: Optional[int] = Field(None, description="Variation ID")
    quantity: int = Field(..., ge=0, description="New quantity (0 to remove)")


class WCApplyCouponRequest(BaseModel):
    """Request to apply a coupon"""
    coupon_code: str = Field(..., min_length=1, description="Coupon code to apply")


class WCAddress(BaseModel):
    """Billing or shipping address"""
    first_name: str = Field(..., max_length=100, description="First name")
    last_name: str = Field(..., max_length=100, description="Last name")
    company: Optional[str] = Field(None, max_length=200, description="Company name")
    address_1: str = Field(..., max_length=255, description="Street address")
    address_2: Optional[str] = Field(None, max_length=255, description="Apartment, suite, etc.")
    city: str = Field(..., max_length=100, description="City")
    state: str = Field(..., max_length=100, description="State/Province")
    postcode: str = Field(..., max_length=20, description="Postal/ZIP code")
    country: str = Field(..., max_length=2, description="Country code (ISO 3166-1 alpha-2)")
    email: Optional[str] = Field(None, max_length=200, description="Email address")
    phone: Optional[str] = Field(None, max_length=50, description="Phone number")


class WCCheckoutRequest(BaseModel):
    """Request to create an order from cart"""
    billing_address: WCAddress = Field(..., description="Billing address")
    shipping_address: Optional[WCAddress] = Field(None, description="Shipping address (if different)")
    use_same_for_shipping: bool = Field(True, description="Use billing address for shipping")
    payment_method: str = Field(..., description="Payment method ID (e.g., 'stripe', 'paypal')")
    payment_method_title: Optional[str] = Field(None, description="Payment method display name")
    customer_note: Optional[str] = Field(None, description="Order notes from customer")
    shipping_method: Optional[str] = Field(None, description="Shipping method ID")
    coupon_codes: List[str] = Field(default_factory=list, description="Coupon codes to apply")


class WCCheckoutResponse(BaseModel):
    """Response after successful checkout"""
    order_id: int = Field(..., description="Created order ID")
    order_key: str = Field(..., description="Order key for verification")
    order_status: str = Field(..., description="Order status")
    total: Decimal = Field(..., description="Order total")
    payment_url: Optional[str] = Field(None, description="URL to complete payment")
    redirect_url: Optional[str] = Field(None, description="URL to redirect after checkout")
    message: str = Field("Order created successfully", description="Status message")


class WCCartSession(BaseModel):
    """Cart session stored in database"""
    session_id: int = Field(..., description="Session ID")
    session_key: str = Field(..., max_length=32, description="Session key")
    session_value: str = Field(..., description="Serialized session data")
    session_expiry: int = Field(..., description="Unix timestamp of expiry")


class WCProductReviewCreate(BaseModel):
    """Request to create a product review"""
    rating: int = Field(..., ge=1, le=5, description="Rating from 1-5")
    review: str = Field(..., min_length=10, description="Review content")


class WCProductReviewRead(BaseModel):
    """Product review response"""
    id: int = Field(..., description="Comment/Review ID")
    product_id: int = Field(..., description="Product ID")
    reviewer: str = Field(..., description="Reviewer name")
    reviewer_email: Optional[str] = Field(None, description="Reviewer email")
    review: str = Field(..., description="Review content")
    rating: int = Field(..., description="Rating (1-5)")
    verified: bool = Field(False, description="Whether the reviewer purchased the product")
    date_created: datetime = Field(..., description="Review creation date")
    status: str = Field("approved", description="Review status")

    class Config:
        from_attributes = True


class WCUserOrderSummary(BaseModel):
    """Summary of user's orders"""
    total_orders: int = Field(0, description="Total number of orders")
    total_spent: Decimal = Field(default=Decimal("0.00"), description="Total amount spent")
    pending_orders: int = Field(0, description="Orders pending payment")
    processing_orders: int = Field(0, description="Orders being processed")
    completed_orders: int = Field(0, description="Completed orders")
