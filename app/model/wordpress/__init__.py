# WordPress Database Models
# These models map to the WordPress database tables with prefix 8jH_

# Core WordPress tables
from .core import (
    WPUser, WPUserMeta, WPPost, WPPostMeta,
    WPComment, WPCommentMeta, WPOption,
    WPTerm, WPTermMeta, WPTermTaxonomy, WPTermRelationship, WPLink
)

# WooCommerce tables
from .woocommerce import (
    WCOrder, WCOrderMeta, WCOrderAddress, WCOrderOperationalData,
    WCOrderItem, WCOrderItemMeta, WCOrderStats,
    WCCustomerLookup, WCProductMetaLookup, WCSession,
    WCWebhook, WCApiKey, WCDownloadableProductPermission,
    WCPaymentToken, WCPaymentTokenMeta,
    WCShippingZone, WCShippingZoneLocation, WCShippingZoneMethod,
    WCTaxRate, WCOrderTaxLookup, WCProductAttributeLookup,
    WCReservedStock, WCTaxRateClass, WCProductDownloadDirectory,
    WCRateLimit, WCCategoryLookup, WCOrderCouponLookup,
    WCOrderProductLookup, WCDownloadLog, WCLog, WCAttributeTaxonomy
)

# LearnPress LMS tables
from .learnpress import (
    LPSection, LPSectionItem, LPQuizQuestion,
    LPQuestionAnswer, LPQuestionAnswerMeta,
    LPUserItem, LPUserItemMeta, LPUserItemResult,
    LPOrderItem, LPOrderItemMeta, LPSession, LPReviewLog
)

# SWPM Membership tables
from .swpm import (
    SWPMMember, SWPMMembership, SWPMPayment, SWPMMembershipMeta
)

# Action Scheduler tables
from .actionscheduler import (
    ASAction, ASClaim, ASGroup, ASLog
)

# Security plugin tables (Wordfence, iThemes, BlogVault, Loginizer)
from .security import (
    # Wordfence
    WFConfig, WFBlocks, WFHits, WFLogins, WFIssues, WFStatus, WFNotifications,
    WFSecurityEvents, WFLockouts,
    # iThemes Security
    ITSecBan, ITSecLockout, ITSecLog, ITSecFingerprint, ITSecVulnerability,
    ITSecDashboardEvent, ITSecFirewallRule,
    # BlogVault
    BVActivityStore, BVFWRequest, BVIPStore, BVLPRequest,
    # Loginizer
    LoginizerLog
)

# Elementor page builder tables
from .elementor import (
    ElementorEvent, ElementorNote, ElementorNoteUserRelation,
    ElementorSubmission, ElementorSubmissionActionLog, ElementorSubmissionValue
)

# Marketing/Lead generation tables (Hustle, OptinPanda)
from .marketing import (
    HustleModule, HustleModuleMeta, HustleEntry, HustleEntryMeta, HustleTracking,
    OpandaLead, OpandaLeadField, OpandaStat, MTSLockerStats
)

# Form plugin tables (WPForms)
from .forms import (
    WPFormsLog, WPFormsPayment, WPFormsPaymentMeta, WPFormsTaskMeta
)

# SEO plugin tables (Yoast, Redirection)
from .seo import (
    YoastIndexable, YoastIndexableHierarchy, YoastMigration, YoastPrimaryTerm, YoastSEOLink,
    RedirectionGroup, RedirectionItem, RedirectionLog, Redirection404
)

# Cache plugin tables (LiteSpeed)
from .cache import (
    LiteSpeedUrl, LiteSpeedUrlFile
)

# Slider plugin tables (Smart Slider 3)
from .sliders import (
    SmartSliderImageStorage, SmartSliderSectionStorage,
    SmartSlider, SmartSliderXref, SmartSlide, SmartSliderGenerator
)

# User management plugin tables (WPUM, Ultimate Member)
from .users import (
    WPUMFieldsGroup, WPUMField, WPUMFieldMeta,
    WPUMRegistrationForm, WPUMRegistrationFormMeta, WPUMSearchField,
    WPUMStripeSubscription, WPUMStripeInvoice,
    UMMetadata
)

# Miscellaneous plugin tables
from .misc import (
    JetpackSyncQueue,
    WPMailSMTPDebugEvent, WPMailSMTPTaskMeta, WPMailLog,
    WPO404Detector,
    TMTask, TMTaskMeta,
    WPWebhooksAuth,
    XCurrency,
    SkrillTransactionLog,
    WCSPaymentRetry,
    WCAdminNote, WCAdminNoteAction,
    WPFMBackup,
    QuadsStats,
    OCRecipientsImport
)

__all__ = [
    # Core WordPress
    "WPUser", "WPUserMeta", "WPPost", "WPPostMeta",
    "WPComment", "WPCommentMeta", "WPOption",
    "WPTerm", "WPTermMeta", "WPTermTaxonomy", "WPTermRelationship", "WPLink",

    # WooCommerce
    "WCOrder", "WCOrderMeta", "WCOrderAddress", "WCOrderOperationalData",
    "WCOrderItem", "WCOrderItemMeta", "WCOrderStats",
    "WCCustomerLookup", "WCProductMetaLookup", "WCSession",
    "WCWebhook", "WCApiKey", "WCDownloadableProductPermission",
    "WCPaymentToken", "WCPaymentTokenMeta",
    "WCShippingZone", "WCShippingZoneLocation", "WCShippingZoneMethod",
    "WCTaxRate", "WCOrderTaxLookup", "WCProductAttributeLookup",
    "WCReservedStock", "WCTaxRateClass", "WCProductDownloadDirectory",
    "WCRateLimit", "WCCategoryLookup", "WCOrderCouponLookup",
    "WCOrderProductLookup", "WCDownloadLog", "WCLog", "WCAttributeTaxonomy",

    # LearnPress
    "LPSection", "LPSectionItem", "LPQuizQuestion",
    "LPQuestionAnswer", "LPQuestionAnswerMeta",
    "LPUserItem", "LPUserItemMeta", "LPUserItemResult",
    "LPOrderItem", "LPOrderItemMeta", "LPSession", "LPReviewLog",

    # SWPM
    "SWPMMember", "SWPMMembership", "SWPMPayment", "SWPMMembershipMeta",

    # Action Scheduler
    "ASAction", "ASClaim", "ASGroup", "ASLog",

    # Wordfence
    "WFConfig", "WFBlocks", "WFHits", "WFLogins", "WFIssues", "WFStatus",
    "WFNotifications", "WFSecurityEvents", "WFLockouts",

    # iThemes Security
    "ITSecBan", "ITSecLockout", "ITSecLog", "ITSecFingerprint", "ITSecVulnerability",
    "ITSecDashboardEvent", "ITSecFirewallRule",

    # BlogVault
    "BVActivityStore", "BVFWRequest", "BVIPStore", "BVLPRequest",

    # Loginizer
    "LoginizerLog",

    # Elementor
    "ElementorEvent", "ElementorNote", "ElementorNoteUserRelation",
    "ElementorSubmission", "ElementorSubmissionActionLog", "ElementorSubmissionValue",

    # Hustle
    "HustleModule", "HustleModuleMeta", "HustleEntry", "HustleEntryMeta", "HustleTracking",

    # OptinPanda
    "OpandaLead", "OpandaLeadField", "OpandaStat", "MTSLockerStats",

    # WPForms
    "WPFormsLog", "WPFormsPayment", "WPFormsPaymentMeta", "WPFormsTaskMeta",

    # Yoast SEO
    "YoastIndexable", "YoastIndexableHierarchy", "YoastMigration", "YoastPrimaryTerm", "YoastSEOLink",

    # Redirection
    "RedirectionGroup", "RedirectionItem", "RedirectionLog", "Redirection404",

    # LiteSpeed Cache
    "LiteSpeedUrl", "LiteSpeedUrlFile",

    # Smart Slider 3
    "SmartSliderImageStorage", "SmartSliderSectionStorage",
    "SmartSlider", "SmartSliderXref", "SmartSlide", "SmartSliderGenerator",

    # WP User Manager
    "WPUMFieldsGroup", "WPUMField", "WPUMFieldMeta",
    "WPUMRegistrationForm", "WPUMRegistrationFormMeta", "WPUMSearchField",
    "WPUMStripeSubscription", "WPUMStripeInvoice",

    # Ultimate Member
    "UMMetadata",

    # Jetpack
    "JetpackSyncQueue",

    # WP Mail SMTP
    "WPMailSMTPDebugEvent", "WPMailSMTPTaskMeta", "WPMailLog",

    # WP-Optimize
    "WPO404Detector",

    # Task Manager
    "TMTask", "TMTaskMeta",

    # WP Webhooks Pro
    "WPWebhooksAuth",

    # X Currency
    "XCurrency",

    # Skrill
    "SkrillTransactionLog",

    # WooCommerce Subscriptions
    "WCSPaymentRetry",

    # WC Admin
    "WCAdminNote", "WCAdminNoteAction",

    # WP File Manager
    "WPFMBackup",

    # Quads Ads
    "QuadsStats",

    # OC SMS
    "OCRecipientsImport",
]
