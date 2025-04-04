"""
Database schema definitions for the KPMG Edge application.
"""

# SQL statements to create database tables

# Projects table
CREATE_PROJECTS_TABLE = """
CREATE TABLE IF NOT EXISTS projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    client VARCHAR(255) NOT NULL,
    type VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status VARCHAR(50) DEFAULT 'Not Started',
    progress INTEGER DEFAULT 0,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

# Project components table
CREATE_PROJECT_COMPONENTS_TABLE = """
CREATE TABLE IF NOT EXISTS project_components (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    component_name VARCHAR(255) NOT NULL,
    component_type VARCHAR(100) NOT NULL,
    status VARCHAR(50) DEFAULT 'Not Started',
    start_date DATE,
    end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

# Resources (team members) table
CREATE_RESOURCES_TABLE = """
CREATE TABLE IF NOT EXISTS resources (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(50),
    skills TEXT[],
    availability JSONB DEFAULT '{"status": "Available", "percentage": 100}'::jsonb,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

# Project resources (assignments) table
CREATE_PROJECT_RESOURCES_TABLE = """
CREATE TABLE IF NOT EXISTS project_resources (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    resource_id INTEGER REFERENCES resources(id) ON DELETE CASCADE,
    role VARCHAR(100) NOT NULL,
    allocation_percentage INTEGER DEFAULT 100,
    start_date DATE,
    end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(project_id, resource_id, role)
)
"""

# Tasks table
CREATE_TASKS_TABLE = """
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'Not Started',
    priority VARCHAR(50) DEFAULT 'Medium',
    estimated_hours FLOAT,
    actual_hours FLOAT DEFAULT 0,
    parent_task_id INTEGER REFERENCES tasks(id) ON DELETE SET NULL,
    start_date DATE,
    due_date DATE,
    completed_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

# Task assignments table
CREATE_TASK_ASSIGNMENTS_TABLE = """
CREATE TABLE IF NOT EXISTS task_assignments (
    id SERIAL PRIMARY KEY,
    task_id INTEGER REFERENCES tasks(id) ON DELETE CASCADE,
    resource_id INTEGER REFERENCES resources(id) ON DELETE CASCADE,
    assigned_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(task_id, resource_id)
)
"""

# Milestones table
CREATE_MILESTONES_TABLE = """
CREATE TABLE IF NOT EXISTS milestones (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    due_date DATE NOT NULL,
    status VARCHAR(50) DEFAULT 'Not Started',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

# Project dependencies table
CREATE_DEPENDENCIES_TABLE = """
CREATE TABLE IF NOT EXISTS dependencies (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    task_id INTEGER REFERENCES tasks(id) ON DELETE CASCADE,
    dependency_task_id INTEGER REFERENCES tasks(id) ON DELETE CASCADE,
    dependency_type VARCHAR(50) DEFAULT 'Finish to Start', -- FS, SS, FF, SF
    lag_days INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(task_id, dependency_task_id),
    CHECK (task_id != dependency_task_id)
)
"""

# List of all table creation statements
CREATE_TABLES = [
    CREATE_PROJECTS_TABLE,
    CREATE_PROJECT_COMPONENTS_TABLE,
    CREATE_RESOURCES_TABLE,
    CREATE_PROJECT_RESOURCES_TABLE,
    CREATE_TASKS_TABLE,
    CREATE_TASK_ASSIGNMENTS_TABLE,
    CREATE_MILESTONES_TABLE,
    CREATE_DEPENDENCIES_TABLE
]