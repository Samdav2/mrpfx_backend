-- MRPFX Final Complete Database Schema (MySQL)
SET FOREIGN_KEY_CHECKS = 0;

-- Table Name: 8jH_actionscheduler_actions
CREATE TABLE IF NOT EXISTS `8jH_actionscheduler_actions` (
	action_id INTEGER NOT NULL AUTO_INCREMENT, 
	hook VARCHAR(191) NOT NULL, 
	status VARCHAR(20) NOT NULL, 
	scheduled_date_gmt DATETIME, 
	scheduled_date_local DATETIME, 
	args VARCHAR(191), 
	schedule VARCHAR(255), 
	group_id INTEGER NOT NULL, 
	attempts INTEGER NOT NULL, 
	last_attempt_gmt DATETIME, 
	last_attempt_local DATETIME, 
	claim_id INTEGER NOT NULL, 
	extended_args VARCHAR(8000), 
	priority INTEGER NOT NULL, 
	PRIMARY KEY (action_id)
);

-- Table Name: 8jH_actionscheduler_claims
CREATE TABLE IF NOT EXISTS `8jH_actionscheduler_claims` (
	claim_id INTEGER NOT NULL AUTO_INCREMENT, 
	date_created_gmt DATETIME NOT NULL, 
	PRIMARY KEY (claim_id)
);

-- Table Name: 8jH_actionscheduler_groups
CREATE TABLE IF NOT EXISTS `8jH_actionscheduler_groups` (
	group_id INTEGER NOT NULL AUTO_INCREMENT, 
	slug VARCHAR(255) NOT NULL, 
	PRIMARY KEY (group_id)
);

-- Table Name: 8jH_bv_activities_store
CREATE TABLE IF NOT EXISTS `8jH_bv_activities_store` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	site_id INTEGER NOT NULL, 
	user_id INTEGER, 
	username VARCHAR(255), 
	request_id VARCHAR(255), 
	ip VARCHAR(50), 
	event_type VARCHAR(60) NOT NULL, 
	event_data VARCHAR(255) NOT NULL, 
	time INTEGER, 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_bv_fw_requests
CREATE TABLE IF NOT EXISTS `8jH_bv_fw_requests` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	ip VARCHAR(50) NOT NULL, 
	status INTEGER NOT NULL, 
	time INTEGER NOT NULL, 
	path VARCHAR(100) NOT NULL, 
	host VARCHAR(100) NOT NULL, 
	method VARCHAR(100) NOT NULL, 
	resp_code INTEGER NOT NULL, 
	category INTEGER NOT NULL, 
	referer VARCHAR(200) NOT NULL, 
	user_agent VARCHAR(200) NOT NULL, 
	filenames VARCHAR(255), 
	query_string VARCHAR(255), 
	rules_info VARCHAR(255), 
	request_id VARCHAR(200), 
	matched_rules VARCHAR(255), 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_bv_ip_store
CREATE TABLE IF NOT EXISTS `8jH_bv_ip_store` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	start_ip_range BLOB NOT NULL, 
	end_ip_range BLOB NOT NULL, 
	is_fw INTEGER NOT NULL, 
	is_lp INTEGER NOT NULL, 
	type INTEGER NOT NULL, 
	is_v6 INTEGER NOT NULL, 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_bv_lp_requests
CREATE TABLE IF NOT EXISTS `8jH_bv_lp_requests` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	ip VARCHAR(50) NOT NULL, 
	status INTEGER NOT NULL, 
	username VARCHAR(50) NOT NULL, 
	message VARCHAR(100) NOT NULL, 
	category INTEGER NOT NULL, 
	time INTEGER NOT NULL, 
	request_id VARCHAR(200), 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_e_events
CREATE TABLE IF NOT EXISTS `8jH_e_events` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	event_data VARCHAR(255), 
	created_at DATETIME NOT NULL, 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_e_notes
CREATE TABLE IF NOT EXISTS `8jH_e_notes` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	route_url VARCHAR(255), 
	route_title VARCHAR(255), 
	route_post_id INTEGER, 
	post_id INTEGER, 
	element_id VARCHAR(60), 
	parent_id INTEGER NOT NULL, 
	author_id INTEGER, 
	author_display_name VARCHAR(250), 
	status VARCHAR(20) NOT NULL, 
	position VARCHAR(255), 
	content VARCHAR(255), 
	is_resolved INTEGER NOT NULL, 
	is_public INTEGER NOT NULL, 
	last_activity_at DATETIME, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_e_submissions
CREATE TABLE IF NOT EXISTS `8jH_e_submissions` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	type VARCHAR(60), 
	hash_id VARCHAR(60) NOT NULL, 
	main_meta_id INTEGER NOT NULL, 
	post_id INTEGER NOT NULL, 
	referer VARCHAR(500) NOT NULL, 
	referer_title VARCHAR(300), 
	element_id VARCHAR(20) NOT NULL, 
	form_name VARCHAR(60) NOT NULL, 
	campaign_id INTEGER NOT NULL, 
	user_id INTEGER, 
	user_ip VARCHAR(46) NOT NULL, 
	user_agent VARCHAR(255) NOT NULL, 
	actions_count INTEGER, 
	actions_succeeded_count INTEGER, 
	status VARCHAR(20) NOT NULL, 
	is_read INTEGER NOT NULL, 
	meta VARCHAR(255), 
	created_at_gmt DATETIME NOT NULL, 
	updated_at_gmt DATETIME NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_hustle_modules
CREATE TABLE IF NOT EXISTS `8jH_hustle_modules` (
	module_id INTEGER NOT NULL AUTO_INCREMENT, 
	blog_id INTEGER NOT NULL, 
	module_name VARCHAR(255) NOT NULL, 
	module_type VARCHAR(100) NOT NULL, 
	active INTEGER, 
	module_mode VARCHAR(100) NOT NULL, 
	PRIMARY KEY (module_id)
);

-- Table Name: 8jH_itsec_bans
CREATE TABLE IF NOT EXISTS `8jH_itsec_bans` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	host VARCHAR(64) NOT NULL, 
	type VARCHAR(20) NOT NULL, 
	created_at DATETIME NOT NULL, 
	actor_type VARCHAR(20), 
	actor_id VARCHAR(128), 
	comment VARCHAR(255) NOT NULL, 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_itsec_dashboard_events
CREATE TABLE IF NOT EXISTS `8jH_itsec_dashboard_events` (
	event_id INTEGER NOT NULL AUTO_INCREMENT, 
	event_slug VARCHAR(128) NOT NULL, 
	event_time DATETIME NOT NULL, 
	event_count INTEGER NOT NULL, 
	event_consolidated INTEGER NOT NULL, 
	PRIMARY KEY (event_id)
);

-- Table Name: 8jH_itsec_fingerprints
CREATE TABLE IF NOT EXISTS `8jH_itsec_fingerprints` (
	fingerprint_id INTEGER NOT NULL AUTO_INCREMENT, 
	fingerprint_user INTEGER NOT NULL, 
	fingerprint_hash VARCHAR(32) NOT NULL, 
	fingerprint_created_at DATETIME NOT NULL, 
	fingerprint_approved_at DATETIME NOT NULL, 
	fingerprint_data VARCHAR(255) NOT NULL, 
	fingerprint_snapshot VARCHAR(255) NOT NULL, 
	fingerprint_last_seen DATETIME NOT NULL, 
	fingerprint_uses INTEGER NOT NULL, 
	fingerprint_status VARCHAR(20) NOT NULL, 
	fingerprint_uuid VARCHAR(36) NOT NULL, 
	PRIMARY KEY (fingerprint_id)
);

-- Table Name: 8jH_itsec_firewall_rules
CREATE TABLE IF NOT EXISTS `8jH_itsec_firewall_rules` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	provider VARCHAR(20) NOT NULL, 
	provider_ref VARCHAR(128) NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	vulnerability VARCHAR(128) NOT NULL, 
	config VARCHAR(255) NOT NULL, 
	created_at DATETIME NOT NULL, 
	paused_at DATETIME, 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_itsec_lockouts
CREATE TABLE IF NOT EXISTS `8jH_itsec_lockouts` (
	lockout_id INTEGER NOT NULL AUTO_INCREMENT, 
	lockout_type VARCHAR(25) NOT NULL, 
	lockout_start DATETIME NOT NULL, 
	lockout_start_gmt DATETIME NOT NULL, 
	lockout_expire DATETIME NOT NULL, 
	lockout_expire_gmt DATETIME NOT NULL, 
	lockout_host VARCHAR(40), 
	lockout_user INTEGER, 
	lockout_username VARCHAR(60), 
	lockout_active INTEGER NOT NULL, 
	lockout_context VARCHAR(255), 
	PRIMARY KEY (lockout_id)
);

-- Table Name: 8jH_itsec_logs
CREATE TABLE IF NOT EXISTS `8jH_itsec_logs` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	parent_id INTEGER NOT NULL, 
	module VARCHAR(50) NOT NULL, 
	code VARCHAR(100) NOT NULL, 
	data VARCHAR(255) NOT NULL, 
	type VARCHAR(20) NOT NULL, 
	timestamp DATETIME, 
	init_timestamp DATETIME, 
	memory_current INTEGER NOT NULL, 
	memory_peak INTEGER NOT NULL, 
	url VARCHAR(500) NOT NULL, 
	blog_id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	remote_ip VARCHAR(50) NOT NULL, 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_itsec_vulnerabilities
CREATE TABLE IF NOT EXISTS `8jH_itsec_vulnerabilities` (
	id VARCHAR(128) NOT NULL, 
	software_type VARCHAR(20) NOT NULL, 
	software_slug VARCHAR(255) NOT NULL, 
	first_seen DATETIME NOT NULL, 
	last_seen DATETIME NOT NULL, 
	resolved_at DATETIME, 
	resolved_by INTEGER NOT NULL, 
	resolution VARCHAR(20) NOT NULL, 
	details VARCHAR(255) NOT NULL, 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_jetpack_sync_queue
CREATE TABLE IF NOT EXISTS `8jH_jetpack_sync_queue` (
	`ID` INTEGER NOT NULL AUTO_INCREMENT, 
	queue_id VARCHAR(50) NOT NULL, 
	event_id VARCHAR(100) NOT NULL, 
	event_payload VARCHAR(255) NOT NULL, 
	timestamp DATETIME, 
	PRIMARY KEY (`ID`)
);

-- Table Name: 8jH_learnpress_order_items
CREATE TABLE IF NOT EXISTS `8jH_learnpress_order_items` (
	order_item_id INTEGER NOT NULL AUTO_INCREMENT, 
	order_item_name VARCHAR(255) NOT NULL, 
	order_id INTEGER NOT NULL, 
	item_id INTEGER NOT NULL, 
	item_type VARCHAR(45) NOT NULL, 
	PRIMARY KEY (order_item_id)
);

-- Table Name: 8jH_learnpress_question_answers
CREATE TABLE IF NOT EXISTS `8jH_learnpress_question_answers` (
	question_answer_id INTEGER NOT NULL AUTO_INCREMENT, 
	question_id INTEGER NOT NULL, 
	title VARCHAR(255) NOT NULL, 
	value VARCHAR(32) NOT NULL, 
	`order` INTEGER NOT NULL, 
	is_true VARCHAR(3), 
	PRIMARY KEY (question_answer_id)
);

-- Table Name: 8jH_learnpress_quiz_questions
CREATE TABLE IF NOT EXISTS `8jH_learnpress_quiz_questions` (
	quiz_question_id INTEGER NOT NULL AUTO_INCREMENT, 
	quiz_id INTEGER NOT NULL, 
	question_id INTEGER NOT NULL, 
	question_order INTEGER NOT NULL, 
	PRIMARY KEY (quiz_question_id)
);

-- Table Name: 8jH_learnpress_sections
CREATE TABLE IF NOT EXISTS `8jH_learnpress_sections` (
	section_id INTEGER NOT NULL AUTO_INCREMENT, 
	section_name VARCHAR(255) NOT NULL, 
	section_course_id INTEGER NOT NULL, 
	section_order INTEGER NOT NULL, 
	section_description VARCHAR(255) NOT NULL, 
	PRIMARY KEY (section_id)
);

-- Table Name: 8jH_learnpress_sessions
CREATE TABLE IF NOT EXISTS `8jH_learnpress_sessions` (
	session_id INTEGER NOT NULL AUTO_INCREMENT, 
	session_key VARCHAR(32) NOT NULL, 
	session_value VARCHAR(255) NOT NULL, 
	session_expiry INTEGER NOT NULL, 
	PRIMARY KEY (session_id)
);

-- Table Name: 8jH_links
CREATE TABLE IF NOT EXISTS `8jH_links` (
	link_id INTEGER NOT NULL AUTO_INCREMENT, 
	link_url VARCHAR(255) NOT NULL, 
	link_name VARCHAR(255) NOT NULL, 
	link_image VARCHAR(255) NOT NULL, 
	link_target VARCHAR(25) NOT NULL, 
	link_description VARCHAR(255) NOT NULL, 
	link_visible VARCHAR(20) NOT NULL, 
	link_owner INTEGER NOT NULL, 
	link_rating INTEGER NOT NULL, 
	link_updated VARCHAR(255) NOT NULL, 
	link_rel VARCHAR(255) NOT NULL, 
	link_notes VARCHAR(255) NOT NULL, 
	link_rss VARCHAR(255) NOT NULL, 
	PRIMARY KEY (link_id)
);

-- Table Name: 8jH_litespeed_url
CREATE TABLE IF NOT EXISTS `8jH_litespeed_url` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	url VARCHAR(500) NOT NULL, 
	cache_tags VARCHAR(1000) NOT NULL, 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_loginizer_logs
CREATE TABLE IF NOT EXISTS `8jH_loginizer_logs` (
	ip VARCHAR(255) NOT NULL, 
	username VARCHAR(255) NOT NULL, 
	time INTEGER NOT NULL, 
	count INTEGER NOT NULL, 
	lockout INTEGER NOT NULL, 
	url VARCHAR(255) NOT NULL, 
	PRIMARY KEY (ip)
);

-- Table Name: 8jH_mts_locker_stats
CREATE TABLE IF NOT EXISTS `8jH_mts_locker_stats` (
	`ID` INTEGER NOT NULL AUTO_INCREMENT, 
	aggregate_date DATETIME NOT NULL, 
	post_id INTEGER NOT NULL, 
	locker_id INTEGER NOT NULL, 
	metric_name VARCHAR(50) NOT NULL, 
	metric_value INTEGER NOT NULL, 
	PRIMARY KEY (`ID`)
);

-- Table Name: 8jH_nextend2_image_storage
CREATE TABLE IF NOT EXISTS `8jH_nextend2_image_storage` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	hash VARCHAR(32) NOT NULL, 
	image VARCHAR(255) NOT NULL, 
	value VARCHAR(255) NOT NULL, 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_nextend2_section_storage
CREATE TABLE IF NOT EXISTS `8jH_nextend2_section_storage` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	application VARCHAR(20) NOT NULL, 
	section VARCHAR(128) NOT NULL, 
	referencekey VARCHAR(128) NOT NULL, 
	value VARCHAR(255) NOT NULL, 
	`isSystem` INTEGER NOT NULL, 
	editable INTEGER NOT NULL, 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_nextend2_smartslider3_generators
CREATE TABLE IF NOT EXISTS `8jH_nextend2_smartslider3_generators` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	`group` VARCHAR(254) NOT NULL, 
	type VARCHAR(254) NOT NULL, 
	params VARCHAR(255) NOT NULL, 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_nextend2_smartslider3_sliders
CREATE TABLE IF NOT EXISTS `8jH_nextend2_smartslider3_sliders` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	alias VARCHAR(255), 
	title VARCHAR(255) NOT NULL, 
	type VARCHAR(30) NOT NULL, 
	params VARCHAR(255) NOT NULL, 
	slider_status VARCHAR(50) NOT NULL, 
	time DATETIME NOT NULL, 
	thumbnail VARCHAR(255) NOT NULL, 
	ordering INTEGER NOT NULL, 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_oc_recipients_import
CREATE TABLE IF NOT EXISTS `8jH_oc_recipients_import` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	phone_number INTEGER NOT NULL, 
	country_code INTEGER NOT NULL, 
	post_id INTEGER NOT NULL, 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_opanda_leads
CREATE TABLE IF NOT EXISTS `8jH_opanda_leads` (
	`ID` INTEGER NOT NULL AUTO_INCREMENT, 
	lead_display_name VARCHAR(255), 
	lead_name VARCHAR(100), 
	lead_family VARCHAR(100), 
	lead_email VARCHAR(50) NOT NULL, 
	lead_date INTEGER NOT NULL, 
	lead_email_confirmed INTEGER NOT NULL, 
	lead_subscription_confirmed INTEGER NOT NULL, 
	lead_ip VARCHAR(45), 
	lead_item_id INTEGER, 
	lead_post_id INTEGER, 
	lead_item_title VARCHAR(255), 
	lead_post_title VARCHAR(255), 
	lead_referer VARCHAR(255), 
	lead_confirmation_code VARCHAR(32), 
	lead_temp VARCHAR(255), 
	PRIMARY KEY (`ID`)
);

-- Table Name: 8jH_opanda_leads_fields
CREATE TABLE IF NOT EXISTS `8jH_opanda_leads_fields` (
	lead_id INTEGER NOT NULL AUTO_INCREMENT, 
	field_name VARCHAR(150) NOT NULL, 
	field_value VARCHAR(255) NOT NULL, 
	field_custom INTEGER NOT NULL, 
	PRIMARY KEY (lead_id, field_name)
);

-- Table Name: 8jH_opanda_stats_v2
CREATE TABLE IF NOT EXISTS `8jH_opanda_stats_v2` (
	`ID` INTEGER NOT NULL AUTO_INCREMENT, 
	aggregate_date DATETIME NOT NULL, 
	post_id INTEGER NOT NULL, 
	item_id INTEGER NOT NULL, 
	metric_name VARCHAR(50) NOT NULL, 
	metric_value INTEGER NOT NULL, 
	PRIMARY KEY (`ID`)
);

-- Table Name: 8jH_options
CREATE TABLE IF NOT EXISTS `8jH_options` (
	option_id INTEGER NOT NULL AUTO_INCREMENT, 
	option_name VARCHAR(191) NOT NULL, 
	option_value VARCHAR(255) NOT NULL, 
	autoload VARCHAR(20) NOT NULL, 
	PRIMARY KEY (option_id)
);
CREATE INDEX `ix_8jH_options_autoload` ON `8jH_options` (autoload);
CREATE UNIQUE INDEX `ix_8jH_options_option_name` ON `8jH_options` (option_name);

-- Table Name: 8jH_quads_stats
CREATE TABLE IF NOT EXISTS `8jH_quads_stats` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	ad_id INTEGER NOT NULL, 
	ad_thetime INTEGER NOT NULL, 
	ad_clicks INTEGER NOT NULL, 
	ad_impressions INTEGER NOT NULL, 
	ad_device_name VARCHAR(20) NOT NULL, 
	ip_address VARCHAR(20) NOT NULL, 
	`URL` VARCHAR(255) NOT NULL, 
	browser VARCHAR(20) NOT NULL, 
	referrer VARCHAR(255) NOT NULL, 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_redirection_404
CREATE TABLE IF NOT EXISTS `8jH_redirection_404` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created DATETIME NOT NULL, 
	url VARCHAR(255) NOT NULL, 
	domain VARCHAR(255), 
	agent VARCHAR(255), 
	referrer VARCHAR(255), 
	http_code INTEGER NOT NULL, 
	request_method VARCHAR(10), 
	request_data VARCHAR(255), 
	ip VARCHAR(45), 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_redirection_groups
CREATE TABLE IF NOT EXISTS `8jH_redirection_groups` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	name VARCHAR(50) NOT NULL, 
	tracking INTEGER NOT NULL, 
	module_id INTEGER NOT NULL, 
	status VARCHAR(10) NOT NULL, 
	position INTEGER NOT NULL, 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_skrill_transaction_log
CREATE TABLE IF NOT EXISTS `8jH_skrill_transaction_log` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	order_id INTEGER NOT NULL, 
	transaction_id VARCHAR(100), 
	mb_transaction_id VARCHAR(50) NOT NULL, 
	payment_method_id VARCHAR(30), 
	payment_type VARCHAR(16) NOT NULL, 
	payment_status VARCHAR(30), 
	amount NUMERIC NOT NULL, 
	refunded_amount NUMERIC, 
	currency VARCHAR(3) NOT NULL, 
	customer_id INTEGER, 
	date DATETIME NOT NULL, 
	additional_information VARCHAR(255), 
	payment_response VARCHAR(255), 
	active INTEGER NOT NULL, 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_swpm_members_tbl
CREATE TABLE IF NOT EXISTS `8jH_swpm_members_tbl` (
	member_id INTEGER NOT NULL AUTO_INCREMENT, 
	user_name VARCHAR(255) NOT NULL, 
	first_name VARCHAR(64), 
	last_name VARCHAR(64), 
	password VARCHAR(255) NOT NULL, 
	member_since DATE NOT NULL, 
	membership_level INTEGER NOT NULL, 
	more_membership_levels VARCHAR(100), 
	account_state VARCHAR(20), 
	last_accessed DATETIME NOT NULL, 
	last_accessed_from_ip VARCHAR(128) NOT NULL, 
	email VARCHAR(255), 
	phone VARCHAR(64), 
	address_street VARCHAR(255), 
	address_city VARCHAR(255), 
	address_state VARCHAR(255), 
	address_zipcode VARCHAR(255), 
	home_page VARCHAR(255), 
	country VARCHAR(255), 
	gender VARCHAR(15), 
	referrer VARCHAR(255), 
	extra_info VARCHAR(255), 
	reg_code VARCHAR(255), 
	subscription_starts DATE, 
	initial_membership_level INTEGER, 
	txn_id VARCHAR(255), 
	subscr_id VARCHAR(255), 
	company_name VARCHAR(255), 
	notes VARCHAR(255), 
	flags INTEGER, 
	profile_image VARCHAR(255), 
	PRIMARY KEY (member_id)
);

-- Table Name: 8jH_swpm_membership_tbl
CREATE TABLE IF NOT EXISTS `8jH_swpm_membership_tbl` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	alias VARCHAR(127) NOT NULL, 
	`role` VARCHAR(255) NOT NULL, 
	permissions INTEGER NOT NULL, 
	subscription_period VARCHAR(11) NOT NULL, 
	subscription_duration_type INTEGER NOT NULL, 
	subscription_unit VARCHAR(20), 
	loginredirect_page VARCHAR(255), 
	category_list VARCHAR(255), 
	page_list VARCHAR(255), 
	post_list VARCHAR(255), 
	comment_list VARCHAR(255), 
	attachment_list VARCHAR(255), 
	custom_post_list VARCHAR(255), 
	disable_bookmark_list VARCHAR(255), 
	options VARCHAR(255), 
	protect_older_posts BOOL NOT NULL, 
	campaign_name VARCHAR(255) NOT NULL, 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_swpm_payments_tbl
CREATE TABLE IF NOT EXISTS `8jH_swpm_payments_tbl` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	email VARCHAR(255), 
	first_name VARCHAR(64), 
	last_name VARCHAR(64), 
	member_id VARCHAR(16), 
	membership_level VARCHAR(64), 
	txn_date DATE NOT NULL, 
	txn_id VARCHAR(255) NOT NULL, 
	subscr_id VARCHAR(255) NOT NULL, 
	reference VARCHAR(255) NOT NULL, 
	payment_amount VARCHAR(32) NOT NULL, 
	gateway VARCHAR(32), 
	status VARCHAR(255), 
	ip_address VARCHAR(128), 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_terms
CREATE TABLE IF NOT EXISTS `8jH_terms` (
	term_id INTEGER NOT NULL AUTO_INCREMENT, 
	name VARCHAR(200) NOT NULL, 
	slug VARCHAR(200) NOT NULL, 
	term_group INTEGER NOT NULL, 
	PRIMARY KEY (term_id)
);

-- Table Name: 8jH_traders
CREATE TABLE IF NOT EXISTS `8jH_traders` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	trader_id VARCHAR(191) NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	type VARCHAR(255) NOT NULL, 
	strategy VARCHAR(255) NOT NULL, 
	description VARCHAR(255), 
	profit_factor VARCHAR(255) NOT NULL, 
	avg_trade_duration VARCHAR(255) NOT NULL, 
	best_trade VARCHAR(255) NOT NULL, 
	worst_trade VARCHAR(255) NOT NULL, 
	PRIMARY KEY (id)
);
CREATE UNIQUE INDEX `ix_8jH_traders_trader_id` ON `8jH_traders` (trader_id);

-- Table Name: 8jH_users
CREATE TABLE IF NOT EXISTS `8jH_users` (
	`ID` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT, 
	user_login VARCHAR(60) NOT NULL, 
	user_pass VARCHAR(255) NOT NULL, 
	user_nicename VARCHAR(50) NOT NULL, 
	user_email VARCHAR(100) NOT NULL, 
	user_url VARCHAR(100) NOT NULL, 
	user_registered VARCHAR(255) NOT NULL, 
	user_activation_key VARCHAR(255) NOT NULL, 
	user_status INTEGER NOT NULL, 
	display_name VARCHAR(250) NOT NULL, 
	PRIMARY KEY (`ID`)
);
CREATE INDEX `ix_8jH_users_user_login` ON `8jH_users` (user_login);
CREATE INDEX `ix_8jH_users_user_nicename` ON `8jH_users` (user_nicename);
CREATE INDEX `ix_8jH_users_user_email` ON `8jH_users` (user_email);

-- Table Name: 8jH_wc_admin_notes
CREATE TABLE IF NOT EXISTS `8jH_wc_admin_notes` (
	note_id INTEGER NOT NULL AUTO_INCREMENT, 
	name VARCHAR(255) NOT NULL, 
	type VARCHAR(20) NOT NULL, 
	locale VARCHAR(20) NOT NULL, 
	title VARCHAR(255) NOT NULL, 
	content VARCHAR(255) NOT NULL, 
	content_data VARCHAR(255), 
	status VARCHAR(200) NOT NULL, 
	source VARCHAR(200) NOT NULL, 
	date_created DATETIME, 
	date_reminder DATETIME, 
	is_snoozable INTEGER NOT NULL, 
	layout VARCHAR(20) NOT NULL, 
	image VARCHAR(200), 
	is_deleted INTEGER NOT NULL, 
	icon VARCHAR(200) NOT NULL, 
	is_read INTEGER NOT NULL, 
	PRIMARY KEY (note_id)
);

-- Table Name: 8jH_wc_category_lookup
CREATE TABLE IF NOT EXISTS `8jH_wc_category_lookup` (
	category_tree_id INTEGER NOT NULL, 
	category_id INTEGER NOT NULL, 
	PRIMARY KEY (category_tree_id, category_id)
);

-- Table Name: 8jH_wc_download_log
CREATE TABLE IF NOT EXISTS `8jH_wc_download_log` (
	download_log_id INTEGER NOT NULL AUTO_INCREMENT, 
	timestamp DATETIME NOT NULL, 
	permission_id INTEGER NOT NULL, 
	user_id INTEGER, 
	user_ip_address VARCHAR(100), 
	PRIMARY KEY (download_log_id)
);

-- Table Name: 8jH_wc_order_coupon_lookup
CREATE TABLE IF NOT EXISTS `8jH_wc_order_coupon_lookup` (
	order_id INTEGER NOT NULL, 
	coupon_id INTEGER NOT NULL, 
	date_created DATETIME NOT NULL, 
	discount_amount FLOAT NOT NULL, 
	PRIMARY KEY (order_id, coupon_id)
);

-- Table Name: 8jH_wc_order_product_lookup
CREATE TABLE IF NOT EXISTS `8jH_wc_order_product_lookup` (
	order_item_id INTEGER NOT NULL AUTO_INCREMENT, 
	order_id INTEGER NOT NULL, 
	product_id INTEGER NOT NULL, 
	variation_id INTEGER NOT NULL, 
	customer_id INTEGER, 
	date_created DATETIME NOT NULL, 
	product_qty INTEGER NOT NULL, 
	product_net_revenue FLOAT NOT NULL, 
	product_gross_revenue FLOAT NOT NULL, 
	coupon_amount FLOAT NOT NULL, 
	tax_amount FLOAT NOT NULL, 
	shipping_amount FLOAT NOT NULL, 
	shipping_tax_amount FLOAT NOT NULL, 
	PRIMARY KEY (order_item_id)
);

-- Table Name: 8jH_wc_order_stats
CREATE TABLE IF NOT EXISTS `8jH_wc_order_stats` (
	order_id INTEGER NOT NULL AUTO_INCREMENT, 
	parent_id INTEGER NOT NULL, 
	date_created DATETIME NOT NULL, 
	date_created_gmt DATETIME NOT NULL, 
	num_items_sold INTEGER NOT NULL, 
	total_sales FLOAT NOT NULL, 
	tax_total FLOAT NOT NULL, 
	shipping_total FLOAT NOT NULL, 
	net_total FLOAT NOT NULL, 
	returning_customer BOOL, 
	status VARCHAR(20) NOT NULL, 
	customer_id INTEGER NOT NULL, 
	date_paid DATETIME, 
	date_completed DATETIME, 
	PRIMARY KEY (order_id)
);

-- Table Name: 8jH_wc_order_tax_lookup
CREATE TABLE IF NOT EXISTS `8jH_wc_order_tax_lookup` (
	order_id INTEGER NOT NULL, 
	tax_rate_id INTEGER NOT NULL, 
	date_created DATETIME NOT NULL, 
	shipping_tax FLOAT NOT NULL, 
	order_tax FLOAT NOT NULL, 
	total_tax FLOAT NOT NULL, 
	PRIMARY KEY (order_id, tax_rate_id)
);

-- Table Name: 8jH_wc_orders
CREATE TABLE IF NOT EXISTS `8jH_wc_orders` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	status VARCHAR(20), 
	currency VARCHAR(10), 
	type VARCHAR(20), 
	tax_amount NUMERIC, 
	total_amount NUMERIC, 
	customer_id INTEGER, 
	billing_email VARCHAR(320), 
	date_created_gmt DATETIME, 
	date_updated_gmt DATETIME, 
	parent_order_id INTEGER, 
	payment_method VARCHAR(100), 
	payment_method_title VARCHAR(255), 
	transaction_id VARCHAR(100), 
	ip_address VARCHAR(100), 
	user_agent VARCHAR(255), 
	customer_note VARCHAR(255), 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_wc_product_attributes_lookup
CREATE TABLE IF NOT EXISTS `8jH_wc_product_attributes_lookup` (
	product_id INTEGER NOT NULL AUTO_INCREMENT, 
	product_or_parent_id INTEGER NOT NULL, 
	taxonomy VARCHAR(32) NOT NULL, 
	term_id INTEGER NOT NULL, 
	is_variation_attribute BOOL NOT NULL, 
	in_stock BOOL NOT NULL, 
	PRIMARY KEY (product_id)
);

-- Table Name: 8jH_wc_product_download_directories
CREATE TABLE IF NOT EXISTS `8jH_wc_product_download_directories` (
	url_id INTEGER NOT NULL AUTO_INCREMENT, 
	url VARCHAR(256) NOT NULL, 
	enabled BOOL NOT NULL, 
	PRIMARY KEY (url_id)
);

-- Table Name: 8jH_wc_product_meta_lookup
CREATE TABLE IF NOT EXISTS `8jH_wc_product_meta_lookup` (
	product_id INTEGER NOT NULL AUTO_INCREMENT, 
	sku VARCHAR(100), 
	`virtual` BOOL, 
	downloadable BOOL, 
	min_price NUMERIC, 
	max_price NUMERIC, 
	onsale BOOL, 
	stock_quantity FLOAT, 
	stock_status VARCHAR(100), 
	rating_count INTEGER, 
	average_rating NUMERIC, 
	total_sales INTEGER, 
	tax_status VARCHAR(100), 
	tax_class VARCHAR(100), 
	global_unique_id VARCHAR(100), 
	PRIMARY KEY (product_id)
);

-- Table Name: 8jH_wc_rate_limits
CREATE TABLE IF NOT EXISTS `8jH_wc_rate_limits` (
	rate_limit_id INTEGER NOT NULL AUTO_INCREMENT, 
	rate_limit_key VARCHAR(200) NOT NULL, 
	rate_limit_expiry INTEGER NOT NULL, 
	rate_limit_remaining INTEGER NOT NULL, 
	PRIMARY KEY (rate_limit_id)
);

-- Table Name: 8jH_wc_reserved_stock
CREATE TABLE IF NOT EXISTS `8jH_wc_reserved_stock` (
	order_id INTEGER NOT NULL, 
	product_id INTEGER NOT NULL, 
	stock_quantity FLOAT NOT NULL, 
	timestamp DATETIME NOT NULL, 
	expires DATETIME NOT NULL, 
	PRIMARY KEY (order_id, product_id)
);

-- Table Name: 8jH_wc_tax_rate_classes
CREATE TABLE IF NOT EXISTS `8jH_wc_tax_rate_classes` (
	tax_rate_class_id INTEGER NOT NULL AUTO_INCREMENT, 
	name VARCHAR(200) NOT NULL, 
	slug VARCHAR(200) NOT NULL, 
	PRIMARY KEY (tax_rate_class_id)
);

-- Table Name: 8jH_wcs_payment_retries
CREATE TABLE IF NOT EXISTS `8jH_wcs_payment_retries` (
	retry_id INTEGER NOT NULL AUTO_INCREMENT, 
	order_id INTEGER NOT NULL, 
	status VARCHAR(255) NOT NULL, 
	date_gmt DATETIME, 
	rule_raw VARCHAR(255), 
	PRIMARY KEY (retry_id)
);

-- Table Name: 8jH_wfblocks7
CREATE TABLE IF NOT EXISTS `8jH_wfblocks7` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	type INTEGER NOT NULL, 
	`IP` BLOB NOT NULL, 
	`blockedTime` INTEGER NOT NULL, 
	reason VARCHAR(255) NOT NULL, 
	`lastAttempt` INTEGER, 
	`blockedHits` INTEGER, 
	expiration INTEGER NOT NULL, 
	parameters VARCHAR(255), 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_wfconfig
CREATE TABLE IF NOT EXISTS `8jH_wfconfig` (
	name VARCHAR(100) NOT NULL, 
	val BLOB, 
	autoload VARCHAR(3) NOT NULL, 
	PRIMARY KEY (name)
);

-- Table Name: 8jH_wfhits
CREATE TABLE IF NOT EXISTS `8jH_wfhits` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	`attackLogTime` FLOAT NOT NULL, 
	ctime FLOAT NOT NULL, 
	`IP` BLOB, 
	`jsRun` INTEGER, 
	`statusCode` INTEGER NOT NULL, 
	`isGoogle` INTEGER NOT NULL, 
	`userID` INTEGER NOT NULL, 
	`newVisit` INTEGER NOT NULL, 
	`URL` VARCHAR(255), 
	referer VARCHAR(255), 
	`UA` VARCHAR(255), 
	action VARCHAR(64) NOT NULL, 
	`actionDescription` VARCHAR(255), 
	`actionData` VARCHAR(255), 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_wfissues
CREATE TABLE IF NOT EXISTS `8jH_wfissues` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	time INTEGER NOT NULL, 
	`lastUpdated` INTEGER NOT NULL, 
	status VARCHAR(10) NOT NULL, 
	type VARCHAR(20) NOT NULL, 
	severity INTEGER NOT NULL, 
	`ignoreP` VARCHAR(32) NOT NULL, 
	`ignoreC` VARCHAR(32) NOT NULL, 
	`shortMsg` VARCHAR(255) NOT NULL, 
	`longMsg` VARCHAR(255), 
	data VARCHAR(255), 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_wflocs
CREATE TABLE IF NOT EXISTS `8jH_wflocs` (
	`IP` VARBINARY(16) NOT NULL, 
	ctime INTEGER NOT NULL, 
	failed INTEGER NOT NULL, 
	city VARCHAR(255), 
	region VARCHAR(255), 
	`countryName` VARCHAR(255), 
	`countryCode` VARCHAR(2), 
	lat FLOAT, 
	lon FLOAT, 
	PRIMARY KEY (`IP`)
);

-- Table Name: 8jH_wflogins
CREATE TABLE IF NOT EXISTS `8jH_wflogins` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	`hitID` INTEGER, 
	ctime FLOAT NOT NULL, 
	fail INTEGER NOT NULL, 
	action VARCHAR(40) NOT NULL, 
	username VARCHAR(255) NOT NULL, 
	`userID` INTEGER NOT NULL, 
	`IP` BLOB, 
	`UA` VARCHAR(255), 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_wfnotifications
CREATE TABLE IF NOT EXISTS `8jH_wfnotifications` (
	id VARCHAR(32) NOT NULL, 
	new INTEGER NOT NULL, 
	category VARCHAR(255) NOT NULL, 
	priority INTEGER NOT NULL, 
	ctime INTEGER NOT NULL, 
	html VARCHAR(255) NOT NULL, 
	links VARCHAR(255) NOT NULL, 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_wfsecurityevents
CREATE TABLE IF NOT EXISTS `8jH_wfsecurityevents` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	type VARCHAR(255) NOT NULL, 
	data VARCHAR(255) NOT NULL, 
	event_time FLOAT NOT NULL, 
	state VARCHAR(10) NOT NULL, 
	state_timestamp DATETIME, 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_wfstatus
CREATE TABLE IF NOT EXISTS `8jH_wfstatus` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	ctime FLOAT NOT NULL, 
	level INTEGER NOT NULL, 
	type VARCHAR(5) NOT NULL, 
	msg VARCHAR(1000) NOT NULL, 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_woocommerce_attribute_taxonomies
CREATE TABLE IF NOT EXISTS `8jH_woocommerce_attribute_taxonomies` (
	attribute_id INTEGER NOT NULL AUTO_INCREMENT, 
	attribute_name VARCHAR(200) NOT NULL, 
	attribute_label VARCHAR(200), 
	attribute_type VARCHAR(20) NOT NULL, 
	attribute_orderby VARCHAR(20) NOT NULL, 
	attribute_public INTEGER NOT NULL, 
	PRIMARY KEY (attribute_id)
);

-- Table Name: 8jH_woocommerce_log
CREATE TABLE IF NOT EXISTS `8jH_woocommerce_log` (
	log_id INTEGER NOT NULL AUTO_INCREMENT, 
	timestamp DATETIME NOT NULL, 
	level INTEGER NOT NULL, 
	source VARCHAR(200) NOT NULL, 
	message VARCHAR(255) NOT NULL, 
	context VARCHAR(255), 
	PRIMARY KEY (log_id)
);

-- Table Name: 8jH_woocommerce_sessions
CREATE TABLE IF NOT EXISTS `8jH_woocommerce_sessions` (
	session_id INTEGER NOT NULL AUTO_INCREMENT, 
	session_key VARCHAR(32) NOT NULL, 
	session_value VARCHAR(255) NOT NULL, 
	session_expiry INTEGER NOT NULL, 
	PRIMARY KEY (session_id)
);

-- Table Name: 8jH_woocommerce_shipping_zones
CREATE TABLE IF NOT EXISTS `8jH_woocommerce_shipping_zones` (
	zone_id INTEGER NOT NULL AUTO_INCREMENT, 
	zone_name VARCHAR(200) NOT NULL, 
	zone_order INTEGER NOT NULL, 
	PRIMARY KEY (zone_id)
);

-- Table Name: 8jH_woocommerce_tax_rates
CREATE TABLE IF NOT EXISTS `8jH_woocommerce_tax_rates` (
	tax_rate_id INTEGER NOT NULL AUTO_INCREMENT, 
	tax_rate_country VARCHAR(2) NOT NULL, 
	tax_rate_state VARCHAR(200) NOT NULL, 
	tax_rate VARCHAR(8) NOT NULL, 
	tax_rate_name VARCHAR(200) NOT NULL, 
	tax_rate_priority INTEGER NOT NULL, 
	tax_rate_compound INTEGER NOT NULL, 
	tax_rate_shipping INTEGER NOT NULL, 
	tax_rate_order INTEGER NOT NULL, 
	tax_rate_class VARCHAR(200) NOT NULL, 
	PRIMARY KEY (tax_rate_id)
);

-- Table Name: 8jH_wpfm_backup
CREATE TABLE IF NOT EXISTS `8jH_wpfm_backup` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	backup_name VARCHAR(255), 
	backup_date VARCHAR(255), 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_wpforms_logs
CREATE TABLE IF NOT EXISTS `8jH_wpforms_logs` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	title VARCHAR(255) NOT NULL, 
	message VARCHAR(255) NOT NULL, 
	types VARCHAR(255) NOT NULL, 
	create_at DATETIME NOT NULL, 
	form_id INTEGER, 
	entry_id INTEGER, 
	user_id INTEGER, 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_wpforms_payments
CREATE TABLE IF NOT EXISTS `8jH_wpforms_payments` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	form_id INTEGER NOT NULL, 
	status VARCHAR(10) NOT NULL, 
	subtotal_amount NUMERIC NOT NULL, 
	discount_amount NUMERIC NOT NULL, 
	total_amount NUMERIC NOT NULL, 
	currency VARCHAR(3) NOT NULL, 
	entry_id INTEGER NOT NULL, 
	gateway VARCHAR(20) NOT NULL, 
	type VARCHAR(12) NOT NULL, 
	mode VARCHAR(4) NOT NULL, 
	transaction_id VARCHAR(40) NOT NULL, 
	customer_id VARCHAR(40) NOT NULL, 
	subscription_id VARCHAR(40) NOT NULL, 
	subscription_status VARCHAR(10) NOT NULL, 
	title VARCHAR(255) NOT NULL, 
	date_created_gmt DATETIME NOT NULL, 
	date_updated_gmt DATETIME NOT NULL, 
	is_published INTEGER NOT NULL, 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_wpforms_tasks_meta
CREATE TABLE IF NOT EXISTS `8jH_wpforms_tasks_meta` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	action VARCHAR(255) NOT NULL, 
	data VARCHAR(255) NOT NULL, 
	date DATETIME NOT NULL, 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_wpmailsmtp_debug_events
CREATE TABLE IF NOT EXISTS `8jH_wpmailsmtp_debug_events` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	content VARCHAR(255), 
	initiator VARCHAR(255), 
	event_type INTEGER NOT NULL, 
	created_at DATETIME, 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_wpmailsmtp_tasks_meta
CREATE TABLE IF NOT EXISTS `8jH_wpmailsmtp_tasks_meta` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	action VARCHAR(255) NOT NULL, 
	data VARCHAR(255) NOT NULL, 
	date DATETIME NOT NULL, 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_wpml_mails
CREATE TABLE IF NOT EXISTS `8jH_wpml_mails` (
	mail_id INTEGER NOT NULL AUTO_INCREMENT, 
	timestamp DATETIME, 
	host VARCHAR(200) NOT NULL, 
	receiver VARCHAR(200) NOT NULL, 
	subject VARCHAR(200) NOT NULL, 
	message VARCHAR(255), 
	headers VARCHAR(255), 
	attachments VARCHAR(800) NOT NULL, 
	error VARCHAR(400), 
	plugin_version VARCHAR(200) NOT NULL, 
	PRIMARY KEY (mail_id)
);

-- Table Name: 8jH_wpo_404_detector
CREATE TABLE IF NOT EXISTS `8jH_wpo_404_detector` (
	`ID` INTEGER NOT NULL AUTO_INCREMENT, 
	url VARCHAR(255) NOT NULL, 
	request_timestamp INTEGER NOT NULL, 
	request_count INTEGER NOT NULL, 
	referrer VARCHAR(255) NOT NULL, 
	PRIMARY KEY (`ID`)
);

-- Table Name: 8jH_wpum_fieldsgroups
CREATE TABLE IF NOT EXISTS `8jH_wpum_fieldsgroups` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	group_order INTEGER NOT NULL, 
	is_primary INTEGER NOT NULL, 
	name VARCHAR(190) NOT NULL, 
	description VARCHAR(255), 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_wpum_registration_forms
CREATE TABLE IF NOT EXISTS `8jH_wpum_registration_forms` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	name VARCHAR(255) NOT NULL, 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_wpum_search_fields
CREATE TABLE IF NOT EXISTS `8jH_wpum_search_fields` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	meta_key VARCHAR(255) NOT NULL, 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_wpwhpro_authentication
CREATE TABLE IF NOT EXISTS `8jH_wpwhpro_authentication` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	name VARCHAR(100), 
	auth_type VARCHAR(100), 
	template VARCHAR(255), 
	log_time DATETIME, 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_x_currency
CREATE TABLE IF NOT EXISTS `8jH_x_currency` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	active INTEGER, 
	name VARCHAR(100) NOT NULL, 
	code VARCHAR(50) NOT NULL, 
	symbol VARCHAR(5) NOT NULL, 
	flag INTEGER, 
	rate FLOAT NOT NULL, 
	rate_type VARCHAR(100) NOT NULL, 
	extra_fee FLOAT NOT NULL, 
	extra_fee_type VARCHAR(100) NOT NULL, 
	thousand_separator VARCHAR(50) NOT NULL, 
	rounding VARCHAR(50), 
	max_decimal INTEGER NOT NULL, 
	decimal_separator VARCHAR(50) NOT NULL, 
	symbol_position VARCHAR(50) NOT NULL, 
	disable_payment_gateways VARCHAR(255) NOT NULL, 
	geo_countries_status VARCHAR(50), 
	disable_countries VARCHAR(255), 
	welcome_country VARCHAR(50), 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_yoast_indexable
CREATE TABLE IF NOT EXISTS `8jH_yoast_indexable` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	permalink VARCHAR(255), 
	permalink_hash VARCHAR(40), 
	object_id INTEGER, 
	object_type VARCHAR(32) NOT NULL, 
	object_sub_type VARCHAR(32), 
	author_id INTEGER, 
	post_parent INTEGER, 
	title VARCHAR(255), 
	description VARCHAR(255), 
	breadcrumb_title VARCHAR(255), 
	post_status VARCHAR(20), 
	is_public INTEGER, 
	is_protected INTEGER, 
	has_public_posts INTEGER, 
	number_of_pages INTEGER, 
	canonical VARCHAR(255), 
	primary_focus_keyword VARCHAR(191), 
	primary_focus_keyword_score INTEGER, 
	readability_score INTEGER, 
	is_cornerstone INTEGER, 
	is_robots_noindex INTEGER, 
	is_robots_nofollow INTEGER, 
	is_robots_noarchive INTEGER, 
	is_robots_noimageindex INTEGER, 
	is_robots_nosnippet INTEGER, 
	twitter_title VARCHAR(255), 
	twitter_image VARCHAR(255), 
	twitter_description VARCHAR(255), 
	twitter_image_id VARCHAR(191), 
	twitter_image_source VARCHAR(255), 
	open_graph_title VARCHAR(255), 
	open_graph_description VARCHAR(255), 
	open_graph_image VARCHAR(255), 
	open_graph_image_id VARCHAR(191), 
	open_graph_image_source VARCHAR(255), 
	open_graph_image_meta VARCHAR(255), 
	link_count INTEGER, 
	incoming_link_count INTEGER, 
	prominent_words_version INTEGER, 
	created_at DATETIME, 
	updated_at DATETIME, 
	blog_id INTEGER NOT NULL, 
	language VARCHAR(32), 
	region VARCHAR(32), 
	schema_page_type VARCHAR(64), 
	schema_article_type VARCHAR(64), 
	has_ancestors INTEGER, 
	estimated_reading_time_minutes INTEGER, 
	version INTEGER, 
	object_last_modified DATETIME, 
	object_published_at DATETIME, 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_yoast_indexable_hierarchy
CREATE TABLE IF NOT EXISTS `8jH_yoast_indexable_hierarchy` (
	indexable_id INTEGER NOT NULL, 
	ancestor_id INTEGER NOT NULL, 
	depth INTEGER, 
	blog_id INTEGER NOT NULL, 
	PRIMARY KEY (indexable_id, ancestor_id)
);

-- Table Name: 8jH_yoast_migrations
CREATE TABLE IF NOT EXISTS `8jH_yoast_migrations` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	version VARCHAR(191), 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_yoast_primary_term
CREATE TABLE IF NOT EXISTS `8jH_yoast_primary_term` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	post_id INTEGER, 
	term_id INTEGER, 
	taxonomy VARCHAR(32) NOT NULL, 
	created_at DATETIME, 
	updated_at DATETIME, 
	blog_id INTEGER NOT NULL, 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_yoast_seo_links
CREATE TABLE IF NOT EXISTS `8jH_yoast_seo_links` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	url VARCHAR(255), 
	post_id INTEGER, 
	target_post_id INTEGER, 
	type VARCHAR(8), 
	indexable_id INTEGER, 
	target_indexable_id INTEGER, 
	height INTEGER, 
	width INTEGER, 
	size INTEGER, 
	language VARCHAR(32), 
	region VARCHAR(32), 
	PRIMARY KEY (id)
);

-- Table Name: 8jH_account_management_connections
CREATE TABLE IF NOT EXISTS `8jH_account_management_connections` (
	id CHAR(32) NOT NULL, 
	user_id BIGINT UNSIGNED, 
	account_id VARCHAR(255) NOT NULL, 
	password VARCHAR(255) NOT NULL, 
	server VARCHAR(255) NOT NULL, 
	broker VARCHAR(255) NOT NULL, 
	capital FLOAT NOT NULL, 
	manager VARCHAR(255) NOT NULL, 
	agreed BOOL NOT NULL, 
	status VARCHAR(255) NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES `8jH_users` (`ID`)
);
CREATE INDEX `ix_8jH_account_management_connections_user_id` ON `8jH_account_management_connections` (user_id);
CREATE INDEX `ix_8jH_account_management_connections_status` ON `8jH_account_management_connections` (status);

-- Table Name: 8jH_actionscheduler_logs
CREATE TABLE IF NOT EXISTS `8jH_actionscheduler_logs` (
	log_id INTEGER NOT NULL AUTO_INCREMENT, 
	action_id INTEGER NOT NULL, 
	message VARCHAR(255) NOT NULL, 
	log_date_gmt DATETIME, 
	log_date_local DATETIME, 
	PRIMARY KEY (log_id), 
	FOREIGN KEY(action_id) REFERENCES `8jH_actionscheduler_actions` (action_id)
);

-- Table Name: 8jH_copy_trading_connections
CREATE TABLE IF NOT EXISTS `8jH_copy_trading_connections` (
	id CHAR(32) NOT NULL, 
	user_id BIGINT UNSIGNED, 
	account_id VARCHAR(255) NOT NULL, 
	password VARCHAR(255) NOT NULL, 
	server VARCHAR(255) NOT NULL, 
	status VARCHAR(255) NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES `8jH_users` (`ID`)
);
CREATE INDEX `ix_8jH_copy_trading_connections_status` ON `8jH_copy_trading_connections` (status);
CREATE INDEX `ix_8jH_copy_trading_connections_user_id` ON `8jH_copy_trading_connections` (user_id);

-- Table Name: 8jH_cryptopayments
CREATE TABLE IF NOT EXISTS `8jH_cryptopayments` (
	id CHAR(32) NOT NULL, 
	user_id BIGINT UNSIGNED NOT NULL, 
	payment_id VARCHAR(255), 
	invoice_id VARCHAR(255), 
	order_id VARCHAR(255), 
	order_description VARCHAR(255), 
	price_amount FLOAT NOT NULL, 
	price_currency VARCHAR(255) NOT NULL, 
	pay_amount FLOAT, 
	pay_currency VARCHAR(255), 
	pay_address VARCHAR(255), 
	payin_extra_id VARCHAR(255), 
	payment_status VARCHAR(255) NOT NULL, 
	actually_paid FLOAT, 
	purchase_id VARCHAR(255), 
	outcome_amount FLOAT, 
	outcome_currency VARCHAR(255), 
	ipn_callback_url VARCHAR(255), 
	invoice_url VARCHAR(255), 
	is_fixed_rate BOOL NOT NULL, 
	is_fee_paid_by_user BOOL NOT NULL, 
	extra_data JSON, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES `8jH_users` (`ID`)
);
CREATE INDEX `ix_8jH_cryptopayments_order_id` ON `8jH_cryptopayments` (order_id);
CREATE INDEX `ix_8jH_cryptopayments_user_id` ON `8jH_cryptopayments` (user_id);
CREATE INDEX `ix_8jH_cryptopayments_invoice_id` ON `8jH_cryptopayments` (invoice_id);
CREATE INDEX `ix_8jH_cryptopayments_payment_id` ON `8jH_cryptopayments` (payment_id);
CREATE INDEX `ix_8jH_cryptopayments_payment_status` ON `8jH_cryptopayments` (payment_status);

-- Table Name: 8jH_e_notes_users_relations
CREATE TABLE IF NOT EXISTS `8jH_e_notes_users_relations` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	type VARCHAR(60) NOT NULL, 
	note_id INTEGER NOT NULL, 
	user_id BIGINT UNSIGNED NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(note_id) REFERENCES `8jH_e_notes` (id), 
	FOREIGN KEY(user_id) REFERENCES `8jH_users` (`ID`)
);

-- Table Name: 8jH_e_submissions_actions_log
CREATE TABLE IF NOT EXISTS `8jH_e_submissions_actions_log` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	submission_id INTEGER NOT NULL, 
	action_name VARCHAR(60) NOT NULL, 
	action_label VARCHAR(60), 
	status VARCHAR(20) NOT NULL, 
	log VARCHAR(255), 
	created_at_gmt DATETIME NOT NULL, 
	updated_at_gmt DATETIME NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(submission_id) REFERENCES `8jH_e_submissions` (id)
);

-- Table Name: 8jH_e_submissions_values
CREATE TABLE IF NOT EXISTS `8jH_e_submissions_values` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	submission_id INTEGER NOT NULL, 
	`key` VARCHAR(60), 
	value VARCHAR(255), 
	PRIMARY KEY (id), 
	FOREIGN KEY(submission_id) REFERENCES `8jH_e_submissions` (id)
);

-- Table Name: 8jH_hustle_entries
CREATE TABLE IF NOT EXISTS `8jH_hustle_entries` (
	entry_id INTEGER NOT NULL AUTO_INCREMENT, 
	entry_type VARCHAR(191) NOT NULL, 
	module_id INTEGER NOT NULL, 
	date_created DATETIME, 
	PRIMARY KEY (entry_id), 
	FOREIGN KEY(module_id) REFERENCES `8jH_hustle_modules` (module_id)
);

-- Table Name: 8jH_hustle_modules_meta
CREATE TABLE IF NOT EXISTS `8jH_hustle_modules_meta` (
	meta_id INTEGER NOT NULL AUTO_INCREMENT, 
	module_id INTEGER NOT NULL, 
	meta_key VARCHAR(191), 
	meta_value VARCHAR(255), 
	PRIMARY KEY (meta_id), 
	FOREIGN KEY(module_id) REFERENCES `8jH_hustle_modules` (module_id)
);

-- Table Name: 8jH_hustle_tracking
CREATE TABLE IF NOT EXISTS `8jH_hustle_tracking` (
	tracking_id INTEGER NOT NULL AUTO_INCREMENT, 
	module_id INTEGER NOT NULL, 
	page_id INTEGER NOT NULL, 
	module_type VARCHAR(100) NOT NULL, 
	action VARCHAR(100) NOT NULL, 
	ip VARCHAR(191), 
	counter INTEGER NOT NULL, 
	date_created DATETIME, 
	date_updated DATETIME, 
	PRIMARY KEY (tracking_id), 
	FOREIGN KEY(module_id) REFERENCES `8jH_hustle_modules` (module_id)
);

-- Table Name: 8jH_learnpress_order_itemmeta
CREATE TABLE IF NOT EXISTS `8jH_learnpress_order_itemmeta` (
	meta_id INTEGER NOT NULL AUTO_INCREMENT, 
	learnpress_order_item_id INTEGER NOT NULL, 
	meta_key VARCHAR(255) NOT NULL, 
	meta_value VARCHAR(255), 
	extra_value VARCHAR(255), 
	PRIMARY KEY (meta_id), 
	FOREIGN KEY(learnpress_order_item_id) REFERENCES `8jH_learnpress_order_items` (order_item_id)
);

-- Table Name: 8jH_learnpress_question_answermeta
CREATE TABLE IF NOT EXISTS `8jH_learnpress_question_answermeta` (
	meta_id INTEGER NOT NULL AUTO_INCREMENT, 
	learnpress_question_answer_id INTEGER NOT NULL, 
	meta_key VARCHAR(255) NOT NULL, 
	meta_value VARCHAR(255), 
	PRIMARY KEY (meta_id), 
	FOREIGN KEY(learnpress_question_answer_id) REFERENCES `8jH_learnpress_question_answers` (question_answer_id)
);

-- Table Name: 8jH_learnpress_review_logs
CREATE TABLE IF NOT EXISTS `8jH_learnpress_review_logs` (
	review_log_id INTEGER NOT NULL AUTO_INCREMENT, 
	course_id INTEGER NOT NULL, 
	user_id BIGINT UNSIGNED NOT NULL, 
	message VARCHAR(255) NOT NULL, 
	date DATETIME, 
	status VARCHAR(45) NOT NULL, 
	user_type VARCHAR(45) NOT NULL, 
	PRIMARY KEY (review_log_id), 
	FOREIGN KEY(user_id) REFERENCES `8jH_users` (`ID`)
);

-- Table Name: 8jH_learnpress_section_items
CREATE TABLE IF NOT EXISTS `8jH_learnpress_section_items` (
	section_item_id INTEGER NOT NULL AUTO_INCREMENT, 
	section_id INTEGER NOT NULL, 
	item_id INTEGER NOT NULL, 
	item_order INTEGER NOT NULL, 
	item_type VARCHAR(45), 
	PRIMARY KEY (section_item_id), 
	FOREIGN KEY(section_id) REFERENCES `8jH_learnpress_sections` (section_id)
);

-- Table Name: 8jH_learnpress_user_items
CREATE TABLE IF NOT EXISTS `8jH_learnpress_user_items` (
	user_item_id INTEGER NOT NULL AUTO_INCREMENT, 
	user_id BIGINT UNSIGNED NOT NULL, 
	item_id INTEGER NOT NULL, 
	start_time DATETIME, 
	end_time DATETIME, 
	item_type VARCHAR(45) NOT NULL, 
	status VARCHAR(45) NOT NULL, 
	graduation VARCHAR(20), 
	access_level INTEGER NOT NULL, 
	ref_id INTEGER NOT NULL, 
	ref_type VARCHAR(45), 
	parent_id INTEGER NOT NULL, 
	PRIMARY KEY (user_item_id), 
	FOREIGN KEY(user_id) REFERENCES `8jH_users` (`ID`)
);

-- Table Name: 8jH_litespeed_url_file
CREATE TABLE IF NOT EXISTS `8jH_litespeed_url_file` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	url_id INTEGER NOT NULL, 
	vary VARCHAR(32) NOT NULL, 
	filename VARCHAR(32) NOT NULL, 
	type INTEGER NOT NULL, 
	expired INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(url_id) REFERENCES `8jH_litespeed_url` (id)
);

-- Table Name: 8jH_nextend2_smartslider3_sliders_xref
CREATE TABLE IF NOT EXISTS `8jH_nextend2_smartslider3_sliders_xref` (
	group_id INTEGER NOT NULL, 
	slider_id INTEGER NOT NULL, 
	ordering INTEGER NOT NULL, 
	PRIMARY KEY (group_id, slider_id), 
	FOREIGN KEY(slider_id) REFERENCES `8jH_nextend2_smartslider3_sliders` (id)
);

-- Table Name: 8jH_nextend2_smartslider3_slides
CREATE TABLE IF NOT EXISTS `8jH_nextend2_smartslider3_slides` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	title VARCHAR(255), 
	slider INTEGER NOT NULL, 
	publish_up DATETIME, 
	publish_down DATETIME, 
	published INTEGER NOT NULL, 
	first INTEGER NOT NULL, 
	slide VARCHAR(255), 
	description VARCHAR(255) NOT NULL, 
	thumbnail VARCHAR(255), 
	params VARCHAR(255) NOT NULL, 
	ordering INTEGER NOT NULL, 
	generator_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(slider) REFERENCES `8jH_nextend2_smartslider3_sliders` (id)
);

-- Table Name: 8jH_posts
CREATE TABLE IF NOT EXISTS `8jH_posts` (
	`ID` INTEGER NOT NULL AUTO_INCREMENT, 
	post_author BIGINT UNSIGNED NOT NULL, 
	post_date VARCHAR(255) NOT NULL, 
	post_date_gmt VARCHAR(255) NOT NULL, 
	post_content VARCHAR(255) NOT NULL, 
	post_title VARCHAR(255) NOT NULL, 
	post_excerpt VARCHAR(255) NOT NULL, 
	post_status VARCHAR(20) NOT NULL, 
	comment_status VARCHAR(20) NOT NULL, 
	ping_status VARCHAR(20) NOT NULL, 
	post_password VARCHAR(255) NOT NULL, 
	post_name VARCHAR(200) NOT NULL, 
	to_ping VARCHAR(255) NOT NULL, 
	pinged VARCHAR(255) NOT NULL, 
	post_modified VARCHAR(255) NOT NULL, 
	post_modified_gmt VARCHAR(255) NOT NULL, 
	post_content_filtered VARCHAR(255) NOT NULL, 
	post_parent INTEGER NOT NULL, 
	guid VARCHAR(255) NOT NULL, 
	menu_order INTEGER NOT NULL, 
	post_type VARCHAR(20) NOT NULL, 
	post_mime_type VARCHAR(100) NOT NULL, 
	comment_count INTEGER NOT NULL, 
	PRIMARY KEY (`ID`), 
	FOREIGN KEY(post_author) REFERENCES `8jH_users` (`ID`)
);
CREATE INDEX `ix_8jH_posts_post_name` ON `8jH_posts` (post_name);
CREATE INDEX `ix_8jH_posts_post_parent` ON `8jH_posts` (post_parent);
CREATE INDEX `ix_8jH_posts_post_type` ON `8jH_posts` (post_type);

-- Table Name: 8jH_prop_firm_registrations
CREATE TABLE IF NOT EXISTS `8jH_prop_firm_registrations` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	user_id BIGINT UNSIGNED, 
	login_id VARCHAR(255) NOT NULL, 
	password VARCHAR(255) NOT NULL, 
	propfirm_name VARCHAR(255) NOT NULL, 
	propfirm_website_link VARCHAR(255) NOT NULL, 
	server_name VARCHAR(255) NOT NULL, 
	server_type VARCHAR(255) NOT NULL, 
	challenges_step INTEGER NOT NULL, 
	propfirm_account_cost FLOAT NOT NULL, 
	account_size FLOAT NOT NULL, 
	account_phases INTEGER NOT NULL, 
	trading_platform VARCHAR(255) NOT NULL, 
	propfirm_rules VARCHAR(255) NOT NULL, 
	whatsapp_no VARCHAR(255) NOT NULL, 
	telegram_username VARCHAR(255) NOT NULL, 
	status VARCHAR(255) NOT NULL, 
	payment_status VARCHAR(255) NOT NULL, 
	payment_method VARCHAR(255) NOT NULL, 
	order_id VARCHAR(255), 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES `8jH_users` (`ID`)
);
CREATE INDEX `ix_8jH_prop_firm_registrations_status` ON `8jH_prop_firm_registrations` (status);
CREATE INDEX `ix_8jH_prop_firm_registrations_payment_method` ON `8jH_prop_firm_registrations` (payment_method);
CREATE INDEX `ix_8jH_prop_firm_registrations_user_id` ON `8jH_prop_firm_registrations` (user_id);
CREATE INDEX `ix_8jH_prop_firm_registrations_payment_status` ON `8jH_prop_firm_registrations` (payment_status);
CREATE INDEX `ix_8jH_prop_firm_registrations_order_id` ON `8jH_prop_firm_registrations` (order_id);

-- Table Name: 8jH_redirection_items
CREATE TABLE IF NOT EXISTS `8jH_redirection_items` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	url VARCHAR(255) NOT NULL, 
	match_url VARCHAR(2000), 
	match_data VARCHAR(255), 
	regex INTEGER NOT NULL, 
	position INTEGER NOT NULL, 
	last_count INTEGER NOT NULL, 
	last_access DATETIME, 
	group_id INTEGER NOT NULL, 
	status VARCHAR(10) NOT NULL, 
	action_type VARCHAR(20) NOT NULL, 
	action_code INTEGER NOT NULL, 
	action_data VARCHAR(255), 
	match_type VARCHAR(20) NOT NULL, 
	title VARCHAR(255), 
	PRIMARY KEY (id), 
	FOREIGN KEY(group_id) REFERENCES `8jH_redirection_groups` (id)
);

-- Table Name: 8jH_swpm_membership_meta_tbl
CREATE TABLE IF NOT EXISTS `8jH_swpm_membership_meta_tbl` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	level_id INTEGER NOT NULL, 
	meta_key VARCHAR(255) NOT NULL, 
	meta_label VARCHAR(255), 
	meta_value VARCHAR(255), 
	meta_type VARCHAR(255) NOT NULL, 
	meta_default VARCHAR(255), 
	meta_context VARCHAR(255) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(level_id) REFERENCES `8jH_swpm_membership_tbl` (id)
);

-- Table Name: 8jH_term_taxonomy
CREATE TABLE IF NOT EXISTS `8jH_term_taxonomy` (
	term_taxonomy_id INTEGER NOT NULL AUTO_INCREMENT, 
	term_id INTEGER NOT NULL, 
	taxonomy VARCHAR(32) NOT NULL, 
	description VARCHAR(255) NOT NULL, 
	parent INTEGER NOT NULL, 
	count INTEGER NOT NULL, 
	PRIMARY KEY (term_taxonomy_id), 
	FOREIGN KEY(term_id) REFERENCES `8jH_terms` (term_id)
);

-- Table Name: 8jH_termmeta
CREATE TABLE IF NOT EXISTS `8jH_termmeta` (
	meta_id INTEGER NOT NULL AUTO_INCREMENT, 
	term_id INTEGER NOT NULL, 
	meta_key VARCHAR(255), 
	meta_value VARCHAR(255), 
	PRIMARY KEY (meta_id), 
	FOREIGN KEY(term_id) REFERENCES `8jH_terms` (term_id)
);

-- Table Name: 8jH_tm_tasks
CREATE TABLE IF NOT EXISTS `8jH_tm_tasks` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	user_id BIGINT UNSIGNED NOT NULL, 
	type VARCHAR(300) NOT NULL, 
	class_identifier VARCHAR(300), 
	attempts INTEGER, 
	description VARCHAR(300), 
	time_created DATETIME, 
	last_locked_at INTEGER, 
	status VARCHAR(300), 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES `8jH_users` (`ID`)
);

-- Table Name: 8jH_trader_performance
CREATE TABLE IF NOT EXISTS `8jH_trader_performance` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	trader_id VARCHAR(191) NOT NULL, 
	month VARCHAR(255) NOT NULL, 
	date_timestamp DATETIME NOT NULL, 
	win_rate VARCHAR(255) NOT NULL, 
	monthly_roi VARCHAR(255) NOT NULL, 
	max_drawdown VARCHAR(255) NOT NULL, 
	total_trades VARCHAR(255) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(trader_id) REFERENCES `8jH_traders` (trader_id)
);
CREATE INDEX `ix_8jH_trader_performance_trader_id` ON `8jH_trader_performance` (trader_id);

-- Table Name: 8jH_um_metadata
CREATE TABLE IF NOT EXISTS `8jH_um_metadata` (
	umeta_id INTEGER NOT NULL AUTO_INCREMENT, 
	user_id BIGINT UNSIGNED NOT NULL, 
	um_key VARCHAR(255), 
	um_value VARCHAR(255), 
	PRIMARY KEY (umeta_id), 
	FOREIGN KEY(user_id) REFERENCES `8jH_users` (`ID`)
);

-- Table Name: 8jH_usermeta
CREATE TABLE IF NOT EXISTS `8jH_usermeta` (
	umeta_id INTEGER NOT NULL AUTO_INCREMENT, 
	user_id BIGINT UNSIGNED NOT NULL, 
	meta_key VARCHAR(255), 
	meta_value VARCHAR(255), 
	PRIMARY KEY (umeta_id), 
	FOREIGN KEY(user_id) REFERENCES `8jH_users` (`ID`)
);
CREATE INDEX `ix_8jH_usermeta_user_id` ON `8jH_usermeta` (user_id);
CREATE INDEX `ix_8jH_usermeta_meta_key` ON `8jH_usermeta` (meta_key);

-- Table Name: 8jH_wc_admin_note_actions
CREATE TABLE IF NOT EXISTS `8jH_wc_admin_note_actions` (
	action_id INTEGER NOT NULL AUTO_INCREMENT, 
	note_id INTEGER NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	label VARCHAR(255) NOT NULL, 
	query VARCHAR(255) NOT NULL, 
	status VARCHAR(255) NOT NULL, 
	actioned_text VARCHAR(255) NOT NULL, 
	nonce_action VARCHAR(255), 
	nonce_name VARCHAR(255), 
	PRIMARY KEY (action_id), 
	FOREIGN KEY(note_id) REFERENCES `8jH_wc_admin_notes` (note_id)
);

-- Table Name: 8jH_wc_customer_lookup
CREATE TABLE IF NOT EXISTS `8jH_wc_customer_lookup` (
	customer_id INTEGER NOT NULL AUTO_INCREMENT, 
	user_id BIGINT UNSIGNED, 
	username VARCHAR(60) NOT NULL, 
	first_name VARCHAR(255) NOT NULL, 
	last_name VARCHAR(255) NOT NULL, 
	email VARCHAR(100), 
	date_last_active DATETIME, 
	date_registered DATETIME, 
	country VARCHAR(2) NOT NULL, 
	postcode VARCHAR(20) NOT NULL, 
	city VARCHAR(100) NOT NULL, 
	state VARCHAR(100) NOT NULL, 
	PRIMARY KEY (customer_id), 
	FOREIGN KEY(user_id) REFERENCES `8jH_users` (`ID`)
);

-- Table Name: 8jH_wc_order_addresses
CREATE TABLE IF NOT EXISTS `8jH_wc_order_addresses` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	order_id INTEGER NOT NULL, 
	address_type VARCHAR(20), 
	first_name VARCHAR(255), 
	last_name VARCHAR(255), 
	company VARCHAR(255), 
	address_1 VARCHAR(255), 
	address_2 VARCHAR(255), 
	city VARCHAR(255), 
	state VARCHAR(255), 
	postcode VARCHAR(255), 
	country VARCHAR(255), 
	email VARCHAR(320), 
	phone VARCHAR(100), 
	PRIMARY KEY (id), 
	FOREIGN KEY(order_id) REFERENCES `8jH_wc_orders` (id)
);

-- Table Name: 8jH_wc_order_operational_data
CREATE TABLE IF NOT EXISTS `8jH_wc_order_operational_data` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	order_id INTEGER, 
	created_via VARCHAR(100), 
	woocommerce_version VARCHAR(20), 
	prices_include_tax BOOL, 
	coupon_usages_are_counted BOOL, 
	download_permission_granted BOOL, 
	cart_hash VARCHAR(100), 
	new_order_email_sent BOOL, 
	order_key VARCHAR(100), 
	order_stock_reduced BOOL, 
	date_paid_gmt DATETIME, 
	date_completed_gmt DATETIME, 
	shipping_tax_amount NUMERIC, 
	shipping_total_amount NUMERIC, 
	discount_tax_amount NUMERIC, 
	discount_total_amount NUMERIC, 
	recorded_sales BOOL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(order_id) REFERENCES `8jH_wc_orders` (id)
);

-- Table Name: 8jH_wc_orders_meta
CREATE TABLE IF NOT EXISTS `8jH_wc_orders_meta` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	order_id INTEGER, 
	meta_key VARCHAR(255), 
	meta_value VARCHAR(255), 
	PRIMARY KEY (id), 
	FOREIGN KEY(order_id) REFERENCES `8jH_wc_orders` (id)
);

-- Table Name: 8jH_wc_webhooks
CREATE TABLE IF NOT EXISTS `8jH_wc_webhooks` (
	webhook_id INTEGER NOT NULL AUTO_INCREMENT, 
	status VARCHAR(200) NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	user_id BIGINT UNSIGNED NOT NULL, 
	delivery_url VARCHAR(255) NOT NULL, 
	secret VARCHAR(255) NOT NULL, 
	topic VARCHAR(200) NOT NULL, 
	date_created DATETIME NOT NULL, 
	date_created_gmt DATETIME NOT NULL, 
	date_modified DATETIME NOT NULL, 
	date_modified_gmt DATETIME NOT NULL, 
	api_version INTEGER NOT NULL, 
	failure_count INTEGER NOT NULL, 
	pending_delivery BOOL NOT NULL, 
	PRIMARY KEY (webhook_id), 
	FOREIGN KEY(user_id) REFERENCES `8jH_users` (`ID`)
);

-- Table Name: 8jH_woocommerce_api_keys
CREATE TABLE IF NOT EXISTS `8jH_woocommerce_api_keys` (
	key_id INTEGER NOT NULL AUTO_INCREMENT, 
	user_id BIGINT UNSIGNED NOT NULL, 
	description VARCHAR(200), 
	permissions VARCHAR(10) NOT NULL, 
	consumer_key VARCHAR(64) NOT NULL, 
	consumer_secret VARCHAR(43) NOT NULL, 
	nonces VARCHAR(255), 
	truncated_key VARCHAR(7) NOT NULL, 
	last_access DATETIME, 
	PRIMARY KEY (key_id), 
	FOREIGN KEY(user_id) REFERENCES `8jH_users` (`ID`)
);

-- Table Name: 8jH_woocommerce_downloadable_product_permissions
CREATE TABLE IF NOT EXISTS `8jH_woocommerce_downloadable_product_permissions` (
	permission_id INTEGER NOT NULL AUTO_INCREMENT, 
	download_id VARCHAR(36) NOT NULL, 
	product_id INTEGER NOT NULL, 
	order_id INTEGER NOT NULL, 
	order_key VARCHAR(200) NOT NULL, 
	user_email VARCHAR(200) NOT NULL, 
	user_id BIGINT UNSIGNED, 
	downloads_remaining VARCHAR(9), 
	access_granted DATETIME NOT NULL, 
	access_expires DATETIME, 
	download_count INTEGER NOT NULL, 
	PRIMARY KEY (permission_id), 
	FOREIGN KEY(user_id) REFERENCES `8jH_users` (`ID`)
);

-- Table Name: 8jH_woocommerce_order_items
CREATE TABLE IF NOT EXISTS `8jH_woocommerce_order_items` (
	order_item_id INTEGER NOT NULL AUTO_INCREMENT, 
	order_item_name VARCHAR(255) NOT NULL, 
	order_item_type VARCHAR(200) NOT NULL, 
	order_id INTEGER NOT NULL, 
	PRIMARY KEY (order_item_id), 
	FOREIGN KEY(order_id) REFERENCES `8jH_wc_orders` (id)
);

-- Table Name: 8jH_woocommerce_payment_tokens
CREATE TABLE IF NOT EXISTS `8jH_woocommerce_payment_tokens` (
	token_id INTEGER NOT NULL AUTO_INCREMENT, 
	gateway_id VARCHAR(200) NOT NULL, 
	token VARCHAR(255) NOT NULL, 
	user_id BIGINT UNSIGNED NOT NULL, 
	type VARCHAR(200) NOT NULL, 
	is_default BOOL NOT NULL, 
	PRIMARY KEY (token_id), 
	FOREIGN KEY(user_id) REFERENCES `8jH_users` (`ID`)
);

-- Table Name: 8jH_woocommerce_shipping_zone_locations
CREATE TABLE IF NOT EXISTS `8jH_woocommerce_shipping_zone_locations` (
	location_id INTEGER NOT NULL AUTO_INCREMENT, 
	zone_id INTEGER NOT NULL, 
	location_code VARCHAR(200) NOT NULL, 
	location_type VARCHAR(40) NOT NULL, 
	PRIMARY KEY (location_id), 
	FOREIGN KEY(zone_id) REFERENCES `8jH_woocommerce_shipping_zones` (zone_id)
);

-- Table Name: 8jH_woocommerce_shipping_zone_methods
CREATE TABLE IF NOT EXISTS `8jH_woocommerce_shipping_zone_methods` (
	instance_id INTEGER NOT NULL AUTO_INCREMENT, 
	zone_id INTEGER NOT NULL, 
	method_id VARCHAR(200) NOT NULL, 
	method_order INTEGER NOT NULL, 
	is_enabled BOOL NOT NULL, 
	PRIMARY KEY (instance_id), 
	FOREIGN KEY(zone_id) REFERENCES `8jH_woocommerce_shipping_zones` (zone_id)
);

-- Table Name: 8jH_wpforms_payment_meta
CREATE TABLE IF NOT EXISTS `8jH_wpforms_payment_meta` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	payment_id INTEGER NOT NULL, 
	meta_key VARCHAR(255), 
	meta_value VARCHAR(255), 
	PRIMARY KEY (id), 
	FOREIGN KEY(payment_id) REFERENCES `8jH_wpforms_payments` (id)
);

-- Table Name: 8jH_wpum_fields
CREATE TABLE IF NOT EXISTS `8jH_wpum_fields` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	group_id INTEGER NOT NULL, 
	field_order INTEGER NOT NULL, 
	type VARCHAR(20) NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	description VARCHAR(255), 
	PRIMARY KEY (id), 
	FOREIGN KEY(group_id) REFERENCES `8jH_wpum_fieldsgroups` (id)
);

-- Table Name: 8jH_wpum_registration_formmeta
CREATE TABLE IF NOT EXISTS `8jH_wpum_registration_formmeta` (
	meta_id INTEGER NOT NULL AUTO_INCREMENT, 
	wpum_registration_form_id INTEGER NOT NULL, 
	meta_key VARCHAR(255), 
	meta_value VARCHAR(255), 
	PRIMARY KEY (meta_id), 
	FOREIGN KEY(wpum_registration_form_id) REFERENCES `8jH_wpum_registration_forms` (id)
);

-- Table Name: 8jH_wpum_stripe_invoices
CREATE TABLE IF NOT EXISTS `8jH_wpum_stripe_invoices` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	user_id BIGINT UNSIGNED NOT NULL, 
	invoice_id VARCHAR(255) NOT NULL, 
	total NUMERIC NOT NULL, 
	currency VARCHAR(20) NOT NULL, 
	gateway_mode VARCHAR(4) NOT NULL, 
	created_at DATETIME, 
	updated_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES `8jH_users` (`ID`)
);

-- Table Name: 8jH_wpum_stripe_subscriptions
CREATE TABLE IF NOT EXISTS `8jH_wpum_stripe_subscriptions` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	user_id BIGINT UNSIGNED NOT NULL, 
	customer_id VARCHAR(255) NOT NULL, 
	plan_id VARCHAR(255) NOT NULL, 
	subscription_id VARCHAR(255) NOT NULL, 
	trial_ends_at DATETIME, 
	ends_at DATETIME, 
	gateway_mode VARCHAR(4) NOT NULL, 
	created_at DATETIME, 
	updated_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES `8jH_users` (`ID`)
);

-- Table Name: 8jH_comments
CREATE TABLE IF NOT EXISTS `8jH_comments` (
	`comment_ID` INTEGER NOT NULL AUTO_INCREMENT, 
	`comment_post_ID` INTEGER NOT NULL, 
	comment_author VARCHAR(255) NOT NULL, 
	comment_author_email VARCHAR(100) NOT NULL, 
	comment_author_url VARCHAR(200) NOT NULL, 
	`comment_author_IP` VARCHAR(100) NOT NULL, 
	comment_date VARCHAR(255) NOT NULL, 
	comment_date_gmt VARCHAR(255) NOT NULL, 
	comment_content VARCHAR(255) NOT NULL, 
	comment_karma INTEGER NOT NULL, 
	comment_approved VARCHAR(20) NOT NULL, 
	comment_agent VARCHAR(255) NOT NULL, 
	comment_type VARCHAR(20) NOT NULL, 
	comment_parent INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	PRIMARY KEY (`comment_ID`), 
	FOREIGN KEY(`comment_post_ID`) REFERENCES `8jH_posts` (`ID`)
);

-- Table Name: 8jH_hustle_entries_meta
CREATE TABLE IF NOT EXISTS `8jH_hustle_entries_meta` (
	meta_id INTEGER NOT NULL AUTO_INCREMENT, 
	entry_id INTEGER NOT NULL, 
	meta_key VARCHAR(191), 
	meta_value VARCHAR(255), 
	date_created DATETIME, 
	date_updated DATETIME, 
	PRIMARY KEY (meta_id), 
	FOREIGN KEY(entry_id) REFERENCES `8jH_hustle_entries` (entry_id)
);

-- Table Name: 8jH_learnpress_user_item_results
CREATE TABLE IF NOT EXISTS `8jH_learnpress_user_item_results` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	user_item_id INTEGER NOT NULL, 
	result VARCHAR(255), 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_item_id) REFERENCES `8jH_learnpress_user_items` (user_item_id)
);

-- Table Name: 8jH_learnpress_user_itemmeta
CREATE TABLE IF NOT EXISTS `8jH_learnpress_user_itemmeta` (
	meta_id INTEGER NOT NULL AUTO_INCREMENT, 
	learnpress_user_item_id INTEGER NOT NULL, 
	meta_key VARCHAR(255) NOT NULL, 
	meta_value VARCHAR(255), 
	extra_value VARCHAR(255), 
	PRIMARY KEY (meta_id), 
	FOREIGN KEY(learnpress_user_item_id) REFERENCES `8jH_learnpress_user_items` (user_item_id)
);

-- Table Name: 8jH_postmeta
CREATE TABLE IF NOT EXISTS `8jH_postmeta` (
	meta_id INTEGER NOT NULL AUTO_INCREMENT, 
	post_id INTEGER NOT NULL, 
	meta_key VARCHAR(255), 
	meta_value VARCHAR(255), 
	PRIMARY KEY (meta_id), 
	FOREIGN KEY(post_id) REFERENCES `8jH_posts` (`ID`)
);
CREATE INDEX `ix_8jH_postmeta_meta_key` ON `8jH_postmeta` (meta_key);
CREATE INDEX `ix_8jH_postmeta_post_id` ON `8jH_postmeta` (post_id);

-- Table Name: 8jH_redirection_logs
CREATE TABLE IF NOT EXISTS `8jH_redirection_logs` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created DATETIME NOT NULL, 
	url VARCHAR(255) NOT NULL, 
	domain VARCHAR(255), 
	sent_to VARCHAR(255), 
	agent VARCHAR(255), 
	referrer VARCHAR(255), 
	http_code INTEGER NOT NULL, 
	request_method VARCHAR(10), 
	request_data VARCHAR(255), 
	redirect_by VARCHAR(50), 
	redirection_id INTEGER, 
	ip VARCHAR(45), 
	PRIMARY KEY (id), 
	FOREIGN KEY(redirection_id) REFERENCES `8jH_redirection_items` (id)
);

-- Table Name: 8jH_term_relationships
CREATE TABLE IF NOT EXISTS `8jH_term_relationships` (
	object_id INTEGER NOT NULL, 
	term_taxonomy_id INTEGER NOT NULL, 
	term_order INTEGER NOT NULL, 
	PRIMARY KEY (object_id, term_taxonomy_id), 
	FOREIGN KEY(term_taxonomy_id) REFERENCES `8jH_term_taxonomy` (term_taxonomy_id)
);

-- Table Name: 8jH_tm_taskmeta
CREATE TABLE IF NOT EXISTS `8jH_tm_taskmeta` (
	meta_id INTEGER NOT NULL AUTO_INCREMENT, 
	task_id INTEGER NOT NULL, 
	meta_key VARCHAR(255), 
	meta_value VARCHAR(255), 
	PRIMARY KEY (meta_id), 
	FOREIGN KEY(task_id) REFERENCES `8jH_tm_tasks` (id)
);

-- Table Name: 8jH_woocommerce_order_itemmeta
CREATE TABLE IF NOT EXISTS `8jH_woocommerce_order_itemmeta` (
	meta_id INTEGER NOT NULL AUTO_INCREMENT, 
	order_item_id INTEGER NOT NULL, 
	meta_key VARCHAR(255), 
	meta_value VARCHAR(255), 
	PRIMARY KEY (meta_id), 
	FOREIGN KEY(order_item_id) REFERENCES `8jH_woocommerce_order_items` (order_item_id)
);

-- Table Name: 8jH_woocommerce_payment_tokenmeta
CREATE TABLE IF NOT EXISTS `8jH_woocommerce_payment_tokenmeta` (
	meta_id INTEGER NOT NULL AUTO_INCREMENT, 
	payment_token_id INTEGER NOT NULL, 
	meta_key VARCHAR(255), 
	meta_value VARCHAR(255), 
	PRIMARY KEY (meta_id), 
	FOREIGN KEY(payment_token_id) REFERENCES `8jH_woocommerce_payment_tokens` (token_id)
);

-- Table Name: 8jH_wpum_fieldmeta
CREATE TABLE IF NOT EXISTS `8jH_wpum_fieldmeta` (
	meta_id INTEGER NOT NULL AUTO_INCREMENT, 
	wpum_field_id INTEGER NOT NULL, 
	meta_key VARCHAR(255), 
	meta_value VARCHAR(255), 
	PRIMARY KEY (meta_id), 
	FOREIGN KEY(wpum_field_id) REFERENCES `8jH_wpum_fields` (id)
);

-- Table Name: 8jH_commentmeta
CREATE TABLE IF NOT EXISTS `8jH_commentmeta` (
	meta_id INTEGER NOT NULL AUTO_INCREMENT, 
	comment_id INTEGER NOT NULL, 
	meta_key VARCHAR(255), 
	meta_value VARCHAR(255), 
	PRIMARY KEY (meta_id), 
	FOREIGN KEY(comment_id) REFERENCES `8jH_comments` (`comment_ID`)
);


SET FOREIGN_KEY_CHECKS = 1;
