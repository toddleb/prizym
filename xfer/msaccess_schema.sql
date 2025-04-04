-- Cleaning Patterns Table
CREATE TABLE cleaning_patterns (
    id AUTOINCREMENT PRIMARY KEY,
    pattern TEXT(255) NOT NULL,
    replacement TEXT(255) DEFAULT '',
    pattern_type TEXT(50) NOT NULL,
    active YESNO DEFAULT TRUE,
    description MEMO,
    sort_order INTEGER DEFAULT 0
);

-- Compensation Components Table
CREATE TABLE comp_components (
    id AUTOINCREMENT PRIMARY KEY,
    plan_id INTEGER NOT NULL,
    name TEXT(255) NOT NULL,
    type TEXT(255),
    weight TEXT(255),
    target_amount TEXT(255),
    frequency TEXT(255),
    metrics MEMO, 
    structure MEMO,
    special_features MEMO
);

-- Compensation Plans Table
CREATE TABLE comp_plans (
    id AUTOINCREMENT PRIMARY KEY,
    title TEXT(255) NOT NULL,
    effective_dates TEXT(255),
    total_target TEXT(255),
    source_file TEXT(255),
    summary MEMO,
    created_at DATETIME DEFAULT Now(),
    updated_at DATETIME DEFAULT Now()
);

-- Compensation Provisions Table
CREATE TABLE comp_provisions (
    id AUTOINCREMENT PRIMARY KEY,
    plan_id INTEGER NOT NULL,
    provision MEMO
);

-- Compensation Tags Table
CREATE TABLE comp_tags (
    id AUTOINCREMENT PRIMARY KEY,
    component_id INTEGER NOT NULL,
    tag TEXT(255) NOT NULL
);

-- Processing Status Table
CREATE TABLE processing_status (
    id AUTOINCREMENT PRIMARY KEY,
    file_path TEXT(255) NOT NULL,
    status TEXT(255) NOT NULL,
    error_message MEMO,
    created_at DATETIME DEFAULT Now(),
    updated_at DATETIME DEFAULT Now()
);

-- Foreign Keys
ALTER TABLE comp_components ADD CONSTRAINT fk_comp_components_plan FOREIGN KEY (plan_id) REFERENCES comp_plans(id) ON DELETE CASCADE;
ALTER TABLE comp_provisions ADD CONSTRAINT fk_comp_provisions_plan FOREIGN KEY (plan_id) REFERENCES comp_plans(id) ON DELETE CASCADE;
ALTER TABLE comp_tags ADD CONSTRAINT fk_comp_tags_component FOREIGN KEY (component_id) REFERENCES comp_components(id) ON DELETE CASCADE;
