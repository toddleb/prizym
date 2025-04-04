"""
Database module for the KPMG Edge application.
Handles database connections and operations.
"""

import logging
import json
from typing import List, Dict, Any, Optional, Tuple
import psycopg2
from psycopg2.extras import execute_values, DictCursor
from utils.config import config
from utils.database_schema import CREATE_TABLES

# Configure logger
logger = logging.getLogger("database")

def get_db_connection():
    """Create and return a new PostgreSQL connection."""
    try:
        return psycopg2.connect(
            dbname=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            host=config.DB_HOST,
            port=config.DB_PORT
        )
    except Exception as e:
        logger.error(f"❌ Error connecting to PostgreSQL database: {e}")
        return None


class DatabaseManager:
    """
    Database manager for KPMG Edge application.
    Handles connections, transactions, and data operations.
    """

    def __init__(self):
        """Initialize the database manager with a connection to PostgreSQL."""
        self.conn = None
        self.cursor = None
        self.connected = False
        
        try:
            self.conn = psycopg2.connect(
                dbname=config.DB_NAME,
                user=config.DB_USER,
                password=config.DB_PASSWORD,
                host=config.DB_HOST,
                port=config.DB_PORT
            )
            self.cursor = self.conn.cursor()
            self.connected = True
            logger.info("✅ Database connection established successfully")
        except Exception as e:
            logger.error(f"❌ Error connecting to PostgreSQL database: {e}")
            logger.warning("Application will run in limited mode without database features")
    
    def is_connected(self):
        """Check if the database is connected"""
        return self.connected
    
    def init_db(self):
        """Initialize the database with required tables if they don't exist."""
        if not self.connected:
            logger.warning("Cannot initialize database - no connection")
            return False
            
        try:
            # Execute all table creation statements from database_schema
            for create_table_sql in CREATE_TABLES:
                self.cursor.execute(create_table_sql)
            
            self.conn.commit()
            logger.info("✅ Database tables initialized successfully")
            return True
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            logger.error(f"❌ Error initializing database tables: {e}")
            return False

    # Project Management Methods
    def save_project(self, project_data: Dict[str, Any]) -> int:
        """
        Save a project to the database.
        Returns the project ID or -1 if operation fails.
        """
        if not self.connected:
            logger.warning("Cannot save project - no database connection")
            return -1
            
        try:
            self.cursor.execute("""
                INSERT INTO projects (
                    name, client, type, start_date, end_date, 
                    status, progress, description
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (
                project_data.get("name", ""),
                project_data.get("client", ""),
                project_data.get("type", ""),
                project_data.get("start_date", ""),
                project_data.get("end_date", ""),
                project_data.get("status", "Not Started"),
                project_data.get("progress", 0),
                project_data.get("description", "")
            ))
            
            project_id = self.cursor.fetchone()[0]
            
            # Save project components if available
            if "components" in project_data and isinstance(project_data["components"], list):
                for component in project_data["components"]:
                    if isinstance(component, dict):
                        component_name = component.get("name", component)
                        component_type = component.get("type", "Standard")
                    else:
                        component_name = component
                        component_type = "Standard"
                        
                    self.cursor.execute("""
                        INSERT INTO project_components (
                            project_id, component_name, component_type, status
                        )
                        VALUES (%s, %s, %s, %s)
                    """, (
                        project_id,
                        component_name,
                        component_type,
                        "Not Started"  # Default status
                    ))
            
            self.conn.commit()
            logger.info(f"✅ Project saved successfully: ID {project_id}")
            return project_id
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            logger.error(f"❌ Error saving project: {e}")
            return -1
    
    def update_project(self, project_id: int, project_data: Dict[str, Any]) -> bool:
        """
        Update an existing project in the database.
        Returns True if successful, False otherwise.
        """
        if not self.connected:
            logger.warning("Cannot update project - no database connection")
            return False
            
        try:
            self.cursor.execute("""
                UPDATE projects SET
                    name = %s,
                    client = %s,
                    type = %s,
                    start_date = %s,
                    end_date = %s,
                    status = %s,
                    progress = %s,
                    description = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            """, (
                project_data.get("name", ""),
                project_data.get("client", ""),
                project_data.get("type", ""),
                project_data.get("start_date", ""),
                project_data.get("end_date", ""),
                project_data.get("status", ""),
                project_data.get("progress", 0),
                project_data.get("description", ""),
                project_id
            ))
            
            self.conn.commit()
            logger.info(f"✅ Project updated successfully: ID {project_id}")
            return True
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            logger.error(f"❌ Error updating project {project_id}: {e}")
            return False
    
    def get_all_projects(self) -> List[Dict[str, Any]]:
        """
        Get all projects from the database.
        Returns a list of project dictionaries.
        """
        if not self.connected:
            logger.warning("Cannot get projects - no database connection")
            return []
            
        try:
            self.cursor.execute("""
                SELECT id, name, client, type, start_date, end_date, 
                       status, progress, description, created_at
                FROM projects
                ORDER BY created_at DESC
            """)
            
            projects = []
            for row in self.cursor.fetchall():
                project = {
                    "id": row[0],
                    "name": row[1],
                    "client": row[2],
                    "type": row[3],
                    "start_date": row[4].strftime("%Y-%m-%d") if row[4] else "",
                    "end_date": row[5].strftime("%Y-%m-%d") if row[5] else "",
                    "status": row[6],
                    "progress": row[7],
                    "description": row[8],
                    "created_at": row[9].strftime("%Y-%m-%d %H:%M:%S") if row[9] else ""
                }
                projects.append(project)
            
            return projects
        except Exception as e:
            logger.error(f"❌ Error fetching projects: {e}")
            return []
    
    def get_project_by_id(self, project_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a project by ID from the database.
        Returns a project dictionary or None if not found.
        """
        if not self.connected:
            logger.warning("Cannot get project - no database connection")
            return None
            
        try:
            self.cursor.execute("""
                SELECT id, name, client, type, start_date, end_date, 
                       status, progress, description, created_at
                FROM projects
                WHERE id = %s
            """, (project_id,))
            
            row = self.cursor.fetchone()
            if not row:
                return None
                
            project = {
                "id": row[0],
                "name": row[1],
                "client": row[2],
                "type": row[3],
                "start_date": row[4].strftime("%Y-%m-%d") if row[4] else "",
                "end_date": row[5].strftime("%Y-%m-%d") if row[5] else "",
                "status": row[6],
                "progress": row[7],
                "description": row[8],
                "created_at": row[9].strftime("%Y-%m-%d %H:%M:%S") if row[9] else ""
            }
            
            # Get project components
            self.cursor.execute("""
                SELECT component_name, component_type, status
                FROM project_components
                WHERE project_id = %s
            """, (project_id,))
            
            components = []
            for comp_row in self.cursor.fetchall():
                components.append({
                    "name": comp_row[0],
                    "type": comp_row[1],
                    "status": comp_row[2]
                })
            
            project["components"] = components
            
            return project
        except Exception as e:
            logger.error(f"❌ Error fetching project {project_id}: {e}")
            return None
    
    def delete_project(self, project_id: int) -> bool:
        """
        Delete a project from the database.
        Returns True if successful, False otherwise.
        """
        if not self.connected:
            logger.warning("Cannot delete project - no database connection")
            return False
            
        try:
            # Delete all related project data
            # The ON DELETE CASCADE constraints will handle the deletion of related records
            self.cursor.execute("DELETE FROM projects WHERE id = %s", (project_id,))
            self.conn.commit()
            logger.info(f"✅ Project deleted successfully: ID {project_id}")
            return True
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            logger.error(f"❌ Error deleting project {project_id}: {e}")
            return False
    
    # Resource Management Methods
    def save_resource(self, resource_data: Dict[str, Any]) -> int:
        """
        Save a resource (team member) to the database.
        Returns the resource ID or -1 if operation fails.
        """
        if not self.connected:
            logger.warning("Cannot save resource - no database connection")
            return -1
            
        try:
            # Convert skills list to PostgreSQL array if provided
            skills = resource_data.get("skills", [])
            if skills and not isinstance(skills, list):
                skills = [skills]
                
            # Convert availability JSON if provided
            availability = resource_data.get("availability", {})
            if availability and isinstance(availability, dict):
                availability = json.dumps(availability)
            
            self.cursor.execute("""
                INSERT INTO resources (
                    name, role, email, phone, skills, availability, notes
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (
                resource_data.get("name", ""),
                resource_data.get("role", ""),
                resource_data.get("email", ""),
                resource_data.get("phone", ""),
                skills,
                availability,
                resource_data.get("notes", "")
            ))
            
            resource_id = self.cursor.fetchone()[0]
            self.conn.commit()
            logger.info(f"✅ Resource saved successfully: ID {resource_id}")
            return resource_id
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            logger.error(f"❌ Error saving resource: {e}")
            return -1
    
    def update_resource(self, resource_id: int, resource_data: Dict[str, Any]) -> bool:
        """
        Update an existing resource in the database.
        Returns True if successful, False otherwise.
        """
        if not self.connected:
            logger.warning("Cannot update resource - no database connection")
            return False
            
        try:
            # Convert skills list to PostgreSQL array if provided
            skills = resource_data.get("skills", [])
            if skills and not isinstance(skills, list):
                skills = [skills]
                
            # Convert availability JSON if provided
            availability = resource_data.get("availability", {})
            if availability and isinstance(availability, dict):
                availability = json.dumps(availability)
            
            self.cursor.execute("""
                UPDATE resources SET
                    name = %s,
                    role = %s,
                    email = %s,
                    phone = %s,
                    skills = %s,
                    availability = %s,
                    notes = %s
                WHERE id = %s
            """, (
                resource_data.get("name", ""),
                resource_data.get("role", ""),
                resource_data.get("email", ""),
                resource_data.get("phone", ""),
                skills,
                availability,
                resource_data.get("notes", ""),
                resource_id
            ))
            
            self.conn.commit()
            logger.info(f"✅ Resource updated successfully: ID {resource_id}")
            return True
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            logger.error(f"❌ Error updating resource {resource_id}: {e}")
            return False
    
    def get_all_resources(self) -> List[Dict[str, Any]]:
        """
        Get all resources from the database.
        Returns a list of resource dictionaries.
        """
        if not self.connected:
            logger.warning("Cannot get resources - no database connection")
            return []
            
        try:
            self.cursor.execute("""
                SELECT id, name, role, email, phone, skills, availability, notes, created_at
                FROM resources
                ORDER BY name
            """)
            
            resources = []
            for row in self.cursor.fetchall():
                # Parse availability JSON
                availability = row[6]
                if availability and isinstance(availability, str):
                    try:
                        availability = json.loads(availability)
                    except:
                        availability = {"status": "Available", "percentage": 100}
                
                resources.append({
                    "id": row[0],
                    "name": row[1],
                    "role": row[2],
                    "email": row[3],
                    "phone": row[4],
                    "skills": row[5] if row[5] else [],
                    "availability": availability,
                    "notes": row[7],
                    "created_at": row[8].strftime("%Y-%m-%d %H:%M:%S") if row[8] else ""
                })
            
            return resources
        except Exception as e:
            logger.error(f"❌ Error fetching resources: {e}")
            return []
    
    def get_resource_by_id(self, resource_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a resource by ID from the database.
        Returns a resource dictionary or None if not found.
        """
        if not self.connected:
            logger.warning("Cannot get resource - no database connection")
            return None
            
        try:
            self.cursor.execute("""
                SELECT id, name, role, email, phone, skills, availability, notes, created_at
                FROM resources
                WHERE id = %s
            """, (resource_id,))
            
            row = self.cursor.fetchone()
            if not row:
                return None
            
            # Parse availability JSON
            availability = row[6]
            if availability and isinstance(availability, str):
                try:
                    availability = json.loads(availability)
                except:
                    availability = {"status": "Available", "percentage": 100}
            
            return {
                "id": row[0],
                "name": row[1],
                "role": row[2],
                "email": row[3],
                "phone": row[4],
                "skills": row[5] if row[5] else [],
                "availability": availability,
                "notes": row[7],
                "created_at": row[8].strftime("%Y-%m-%d %H:%M:%S") if row[8] else ""
            }
        except Exception as e:
            logger.error(f"❌ Error fetching resource {resource_id}: {e}")
            return None
    
    def delete_resource(self, resource_id: int) -> bool:
        """
        Delete a resource from the database.
        Returns True if successful, False otherwise.
        """
        if not self.connected:
            logger.warning("Cannot delete resource - no database connection")
            return False
            
        try:
            # Check if resource is assigned to any projects
            self.cursor.execute("""
                SELECT COUNT(*) FROM project_resources WHERE resource_id = %s
            """, (resource_id,))
            
            count = self.cursor.fetchone()[0]
            if count > 0:
                logger.warning(f"Cannot delete resource {resource_id} - assigned to {count} projects")
                return False
            
            # Delete resource
            self.cursor.execute("DELETE FROM resources WHERE id = %s", (resource_id,))
            self.conn.commit()
            logger.info(f"✅ Resource deleted successfully: ID {resource_id}")
            return True
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            logger.error(f"❌ Error deleting resource {resource_id}: {e}")
            return False
    
    def get_resources_by_project(self, project_id: int) -> List[Dict[str, Any]]:
        """
        Get all resources assigned to a specific project.
        Returns a list of resource dictionaries with assignment details.
        """
        if not self.connected:
            logger.warning("Cannot get project resources - no database connection")
            return []
            
        try:
            self.cursor.execute("""
                SELECT r.id, r.name, r.role as resource_role, r.email, r.phone,
                       pr.role as project_role, pr.allocation_percentage,
                       pr.start_date, pr.end_date
                FROM resources r
                JOIN project_resources pr ON r.id = pr.resource_id
                WHERE pr.project_id = %s
                ORDER BY r.name
            """, (project_id,))
            
            resources = []
            for row in self.cursor.fetchall():
                resources.append({
                    "id": row[0],
                    "name": row[1],
                    "resource_role": row[2],
                    "email": row[3],
                    "phone": row[4],
                    "project_role": row[5],
                    "allocation": row[6],
                    "start_date": row[7].strftime("%Y-%m-%d") if row[7] else "",
                    "end_date": row[8].strftime("%Y-%m-%d") if row[8] else ""
                })
            
            return resources
        except Exception as e:
            logger.error(f"❌ Error fetching resources for project {project_id}: {e}")
            return []
    
    def assign_resource_to_project(self, project_id: int, resource_id: int, 
                                 role: str, allocation: int = 100,
                                 start_date: str = None, end_date: str = None) -> bool:
        """
        Assign a resource to a project.
        Returns True if successful, False otherwise.
        """
        if not self.connected:
            logger.warning("Cannot assign resource - no database connection")
            return False
            
        try:
            self.cursor.execute("""
                INSERT INTO project_resources (
                    project_id, resource_id, role, allocation_percentage, start_date, end_date
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (project_id, resource_id, role) 
                DO UPDATE SET
                    allocation_percentage = %s,
                    start_date = %s,
                    end_date = %s
            """, (
                project_id, resource_id, role, allocation, start_date, end_date,
                allocation, start_date, end_date  # Values for UPDATE
            ))
            
            self.conn.commit()
            logger.info(f"✅ Resource {resource_id} assigned to project {project_id}")
            return True
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            logger.error(f"❌ Error assigning resource to project: {e}")
            return False
    
    def remove_resource_from_project(self, project_id: int, resource_id: int, role: str = None) -> bool:
        """
        Remove a resource from a project.
        If role is provided, only that specific role assignment is removed.
        Otherwise, all assignments for that resource on the project are removed.
        Returns True if successful, False otherwise.
        """
        if not self.connected:
            logger.warning("Cannot remove resource - no database connection")
            return False
            
        try:
            if role:
                self.cursor.execute("""
                    DELETE FROM project_resources
                    WHERE project_id = %s AND resource_id = %s AND role = %s
                """, (project_id, resource_id, role))
            else:
                self.cursor.execute("""
                    DELETE FROM project_resources
                    WHERE project_id = %s AND resource_id = %s
                """, (project_id, resource_id))
            
            self.conn.commit()
            logger.info(f"✅ Resource {resource_id} removed from project {project_id}")
            return True
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            logger.error(f"❌ Error removing resource from project: {e}")
            return False
    
    # Task Management Methods
    def save_task(self, task_data: Dict[str, Any]) -> int:
        """
        Save a task to the database.
        Returns the task ID or -1 if operation fails.
        """
        if not self.connected:
            logger.warning("Cannot save task - no database connection")
            return -1
            
        try:
            self.cursor.execute("""
                INSERT INTO tasks (
                    project_id, title, description, status, priority,
                    estimated_hours, parent_task_id, start_date, due_date
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (
                task_data.get("project_id"),
                task_data.get("title", ""),
                task_data.get("description", ""),
                task_data.get("status", "Not Started"),
                task_data.get("priority", "Medium"),
                task_data.get("estimated_hours"),
                task_data.get("parent_task_id"),
                task_data.get("start_date"),
                task_data.get("due_date")
            ))
            
            task_id = self.cursor.fetchone()[0]
            
            # Assign resources if provided
            if "assigned_resources" in task_data and isinstance(task_data["assigned_resources"], list):
                for resource_id in task_data["assigned_resources"]:
                    self.cursor.execute("""
                        INSERT INTO task_assignments (task_id, resource_id)
                        VALUES (%s, %s)
                        ON CONFLICT (task_id, resource_id) DO NOTHING
                    """, (task_id, resource_id))
            
            self.conn.commit()
            logger.info(f"✅ Task saved successfully: ID {task_id}")
            return task_id
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            logger.error(f"❌ Error saving task: {e}")
            return -1
    
    def update_task(self, task_id: int, task_data: Dict[str, Any]) -> bool:
        """
        Update an existing task in the database.
        Returns True if successful, False otherwise.
        """
        if not self.connected:
            logger.warning("Cannot update task - no database connection")
            return False
            
        try:
            self.cursor.execute("""
                UPDATE tasks SET
                    title = %s,
                    description = %s,
                    status = %s,
                    priority = %s,
                    estimated_hours = %s,
                    actual_hours = %s,
                    parent_task_id = %s,
                    start_date = %s,
                    due_date = %s,
                    completed_date = CASE WHEN %s = 'Completed' AND completed_date IS NULL 
                                         THEN CURRENT_DATE ELSE completed_date END,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            """, (
                task_data.get("title", ""),
                task_data.get("description", ""),
                task_data.get("status", ""),
                task_data.get("priority", ""),
                task_data.get("estimated_hours"),
                task_data.get("actual_hours"),
                task_data.get("parent_task_id"),
                task_data.get("start_date"),
                task_data.get("due_date"),
                task_data.get("status", ""),  # For the CASE statement
                task_id
            ))
            
            # Update resource assignments if provided
            if "assigned_resources" in task_data and isinstance(task_data["assigned_resources"], list):
                # Remove existing assignments
                self.cursor.execute("DELETE FROM task_assignments WHERE task_id = %s", (task_id,))
                
                # Add new assignments
                for resource_id in task_data["assigned_resources"]:
                    self.cursor.execute("""
                        INSERT INTO task_assignments (task_id, resource_id)
                        VALUES (%s, %s)
                    """, (task_id, resource_id))
            
            self.conn.commit()
            logger.info(f"✅ Task updated successfully: ID {task_id}")
            return True
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            logger.error(f"❌ Error updating task {task_id}: {e}")
            return False
    
    def get_tasks_by_project(self, project_id: int) -> List[Dict[str, Any]]:
        """
        Get all tasks for a specific project.
        Returns a list of task dictionaries.
        """
        if not self.connected:
            logger.warning("Cannot get project tasks - no database connection")
            return []
            
        try:
            # Use DictCursor for named columns
            dict_cursor = self.conn.cursor(cursor_factory=DictCursor)
            dict_cursor.execute("""
                SELECT t.id, t.title, t.description, t.status, t.priority,
                       t.estimated_hours, t.actual_hours, t.parent_task_id,
                       t.start_date, t.due_date, t.completed_date, t.created_at,
                       (SELECT array_agg(resource_id) FROM task_assignments WHERE task_id = t.id) as assigned_resources
                FROM tasks t
                WHERE t.project_id = %s
                ORDER BY t.parent_task_id NULLS FIRST, t.start_date, t.due_date
            """, (project_id,))
            
            tasks = []
            for row in dict_cursor.fetchall():
                # Convert date fields to strings
                date_fields = ['start_date', 'due_date', 'completed_date', 'created_at']
                for field in date_fields:
                    if row[field]:
                        row[field] = row[field].strftime("%Y-%m-%d")
                    else:
                        row[field] = None
                
                tasks.append(dict(row))
            
            dict_cursor.close()
            return tasks
        except Exception as e:
            logger.error(f"❌ Error fetching tasks for project {project_id}: {e}")
            return []
    
    def get_task_details(self, task_id: int) -> Optional[Dict[str, Any]]:
        """
        Get detailed information for a specific task, including assignments.
        Returns a task dictionary or None if not found.
        """
        if not self.connected:
            logger.warning("Cannot get task details - no database connection")
            return None
            
        try:
            dict_cursor = self.conn.cursor(cursor_factory=DictCursor)
            dict_cursor.execute("""
                SELECT t.*, 
                       (SELECT array_agg(resource_id) FROM task_assignments WHERE task_id = t.id) as assigned_resources,
                       (SELECT array_agg(dependency_task_id) FROM dependencies 
                        WHERE task_id = t.id) as dependencies
                FROM tasks t
                WHERE t.id = %s
            """, (task_id,))
            
            row = dict_cursor.fetchone()
            if not row:
                return None
                
            task = dict(row)
            
            # Convert date fields to strings
            date_fields = ['start_date', 'due_date', 'completed_date', 'created_at', 'updated_at']
            for field in date_fields:
                if task[field]:
                    task[field] = task[field].strftime("%Y-%m-%d")
                else:
                    task[field] = None
            
            # Get resource details
            if task['assigned_resources']:
                dict_cursor.execute("""
                    SELECT r.id, r.name, r.role
                    FROM resources r
                    WHERE r.id = ANY(%s)
                """, (task['assigned_resources'],))
                
                task['assigned_resource_details'] = [dict(r) for r in dict_cursor.fetchall()]
            else:
                task['assigned_resource_details'] = []
            
            dict_cursor.close()
            return task
        except Exception as e:
            logger.error(f"❌ Error fetching task details for task {task_id}: {e}")
            return None
    
    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task from the database.
        Returns True if successful, False otherwise.
        """
        if not self.connected:
            logger.warning("Cannot delete task - no database connection")
            return False
            
        try:
            # Delete the task (related assignments will be deleted by CASCADE)
            self.cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
            self.conn.commit()
            logger.info(f"✅ Task deleted successfully: ID {task_id}")
            return True
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            logger.error(f"❌ Error deleting task {task_id}: {e}")
            return False
    
    # Milestone Management Methods
    def save_milestone(self, milestone_data: Dict[str, Any]) -> int:
        """
        Save a milestone to the database.
        Returns the milestone ID or -1 if operation fails.
        """
        if not self.connected:
            logger.warning("Cannot save milestone - no database connection")
            return -1
            
        try:
            self.cursor.execute("""
                INSERT INTO milestones (
                    project_id, title, description, due_date, status
                )
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            """, (
                milestone_data.get("project_id"),
                milestone_data.get("title", ""),
                milestone_data.get("description", ""),
                milestone_data.get("due_date"),
                milestone_data.get("status", "Not Started")
            ))
            
            milestone_id = self.cursor.fetchone()[0]
            self.conn.commit()
            logger.info(f"✅ Milestone saved successfully: ID {milestone_id}")
            return milestone_id
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            logger.error(f"❌ Error saving milestone: {e}")
            return -1
    
    def update_milestone(self, milestone_id: int, milestone_data: Dict[str, Any]) -> bool:
        """
        Update an existing milestone in the database.
        Returns True if successful, False otherwise.
        """
        if not self.connected:
            logger.warning("Cannot update milestone - no database connection")
            return False
            
        try:
            self.cursor.execute("""
                UPDATE milestones SET
                    title = %s,
                    description = %s,
                    due_date = %s,
                    status = %s
                WHERE id = %s
            """, (
                milestone_data.get("title", ""),
                milestone_data.get("description", ""),
                milestone_data.get("due_date"),
                milestone_data.get("status", ""),
                milestone_id
            ))
            
            self.conn.commit()
            logger.info(f"✅ Milestone updated successfully: ID {milestone_id}")
            return True
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            logger.error(f"❌ Error updating milestone {milestone_id}: {e}")
            return False
    
    def get_milestones_by_project(self, project_id: int) -> List[Dict[str, Any]]:
        """
        Get all milestones for a specific project.
        Returns a list of milestone dictionaries.
        """
        if not self.connected:
            logger.warning("Cannot get project milestones - no database connection")
            return []
            
        try:
            dict_cursor = self.conn.cursor(cursor_factory=DictCursor)
            dict_cursor.execute("""
                SELECT id, title, description, due_date, status, created_at
                FROM milestones
                WHERE project_id = %s
                ORDER BY due_date
            """, (project_id,))
            
            milestones = []
            for row in dict_cursor.fetchall():
                milestone = dict(row)
                
                # Convert date fields to strings
                if milestone['due_date']:
                    milestone['due_date'] = milestone['due_date'].strftime("%Y-%m-%d")
                if milestone['created_at']:
                    milestone['created_at'] = milestone['created_at'].strftime("%Y-%m-%d")
                
                milestones.append(milestone)
            
            dict_cursor.close()
            return milestones
        except Exception as e:
            logger.error(f"❌ Error fetching milestones for project {project_id}: {e}")
            return []
    
    def delete_milestone(self, milestone_id: int) -> bool:
        """
        Delete a milestone from the database.
        Returns True if successful, False otherwise.
        """
        if not self.connected:
            logger.warning("Cannot delete milestone - no database connection")
            return False
            
        try:
            self.cursor.execute("DELETE FROM milestones WHERE id = %s", (milestone_id,))
            self.conn.commit()
            logger.info(f"✅ Milestone deleted successfully: ID {milestone_id}")
            return True
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            logger.error(f"❌ Error deleting milestone {milestone_id}: {e}")
            return False
    
    # Dependency Management Methods
    def add_task_dependency(self, project_id: int, task_id: int, dependency_task_id: int, 
                           dependency_type: str = "Finish to Start", lag_days: int = 0) -> bool:
        """
        Add a dependency relationship between two tasks.
        Returns True if successful, False otherwise.
        """
        if not self.connected:
            logger.warning("Cannot add task dependency - no database connection")
            return False
            
        try:
            self.cursor.execute("""
                INSERT INTO dependencies (
                    project_id, task_id, dependency_task_id, dependency_type, lag_days
                )
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (task_id, dependency_task_id) 
                DO UPDATE SET
                    dependency_type = %s,
                    lag_days = %s
            """, (
                project_id, task_id, dependency_task_id, dependency_type, lag_days,
                dependency_type, lag_days  # Values for UPDATE
            ))
            
            self.conn.commit()
            logger.info(f"✅ Dependency added: Task {task_id} depends on Task {dependency_task_id}")
            return True
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            logger.error(f"❌ Error adding task dependency: {e}")
            return False
    
    def remove_task_dependency(self, task_id: int, dependency_task_id: int) -> bool:
        """
        Remove a dependency relationship between two tasks.
        Returns True if successful, False otherwise.
        """
        if not self.connected:
            logger.warning("Cannot remove task dependency - no database connection")
            return False
            
        try:
            self.cursor.execute("""
                DELETE FROM dependencies
                WHERE task_id = %s AND dependency_task_id = %s
            """, (task_id, dependency_task_id))
            
            self.conn.commit()
            logger.info(f"✅ Dependency removed: Task {task_id} no longer depends on Task {dependency_task_id}")
            return True
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            logger.error(f"❌ Error removing task dependency: {e}")
            return False
    
    def get_task_dependencies(self, project_id: int) -> List[Dict[str, Any]]:
        """
        Get all task dependencies for a project.
        Returns a list of dependency dictionaries.
        """
        if not self.connected:
            logger.warning("Cannot get task dependencies - no database connection")
            return []
            
        try:
            dict_cursor = self.conn.cursor(cursor_factory=DictCursor)
            dict_cursor.execute("""
                SELECT d.id, d.task_id, d.dependency_task_id, d.dependency_type, d.lag_days,
                       t1.title as task_title, t2.title as dependency_title
                FROM dependencies d
                JOIN tasks t1 ON d.task_id = t1.id
                JOIN tasks t2 ON d.dependency_task_id = t2.id
                WHERE d.project_id = %s
            """, (project_id,))
            
            dependencies = [dict(row) for row in dict_cursor.fetchall()]
            dict_cursor.close()
            return dependencies
        except Exception as e:
            logger.error(f"❌ Error fetching task dependencies for project {project_id}: {e}")
            return []
    
    # Reporting Methods
    def get_project_status_report(self) -> List[Dict[str, Any]]:
        """
        Get a status report for all projects.
        Returns a list of project status dictionaries.
        """
        if not self.connected:
            logger.warning("Cannot get project status report - no database connection")
            return []
            
        try:
            dict_cursor = self.conn.cursor(cursor_factory=DictCursor)
            dict_cursor.execute("""
                SELECT 
                    p.id, p.name, p.client, p.status, p.progress, 
                    p.start_date, p.end_date,
                    (SELECT COUNT(*) FROM tasks t WHERE t.project_id = p.id) as total_tasks,
                    (SELECT COUNT(*) FROM tasks t WHERE t.project_id = p.id AND t.status = 'Completed') as completed_tasks,
                    (SELECT COUNT(*) FROM resources r JOIN project_resources pr ON r.id = pr.resource_id WHERE pr.project_id = p.id) as resource_count
                FROM projects p
                ORDER BY p.start_date DESC
            """)
            
            projects = []
            for row in dict_cursor.fetchall():
                project = dict(row)
                
                # Convert date fields to strings
                if project['start_date']:
                    project['start_date'] = project['start_date'].strftime("%Y-%m-%d")
                if project['end_date']:
                    project['end_date'] = project['end_date'].strftime("%Y-%m-%d")
                
                # Calculate days remaining
                if project['end_date']:
                    try:
                        end_date = datetime.strptime(project['end_date'], "%Y-%m-%d").date()
                        today = datetime.now().date()
                        project['days_remaining'] = (end_date - today).days
                    except:
                        project['days_remaining'] = None
                else:
                    project['days_remaining'] = None
                
                # Calculate completion percentage based on tasks
                if project['total_tasks'] > 0:
                    project['task_completion'] = round(project['completed_tasks'] / project['total_tasks'] * 100, 1)
                else:
                    project['task_completion'] = 0
                
                projects.append(project)
            
            dict_cursor.close()
            return projects
        except Exception as e:
            logger.error(f"❌ Error fetching project status report: {e}")
            return []
    
    def get_resource_allocation_report(self) -> List[Dict[str, Any]]:
        """
        Get a resource allocation report.
        Returns a list of resource allocation dictionaries.
        """
        if not self.connected:
            logger.warning("Cannot get resource allocation report - no database connection")
            return []
            
        try:
            dict_cursor = self.conn.cursor(cursor_factory=DictCursor)
            dict_cursor.execute("""
                SELECT 
                    r.id, r.name, r.role,
                    (SELECT json_agg(json_build_object(
                        'project_id', pr.project_id,
                        'project_name', p.name,
                        'role', pr.role,
                        'allocation', pr.allocation_percentage,
                        'start_date', pr.start_date,
                        'end_date', pr.end_date
                    ))
                    FROM project_resources pr
                    JOIN projects p ON pr.project_id = p.id
                    WHERE pr.resource_id = r.id
                    ) as assignments,
                    (SELECT SUM(pr.allocation_percentage) 
                    FROM project_resources pr 
                    WHERE pr.resource_id = r.id) as total_allocation
                FROM resources r
                ORDER BY r.name
            """)
            
            resources = []
            for row in dict_cursor.fetchall():
                resource = dict(row)
                
                # Set default values if None
                if resource['assignments'] is None:
                    resource['assignments'] = []
                    
                if resource['total_allocation'] is None:
                    resource['total_allocation'] = 0
                
                # Format dates in assignments
                for assignment in resource['assignments']:
                    if assignment.get('start_date'):
                        assignment['start_date'] = assignment['start_date'].strftime("%Y-%m-%d")
                    if assignment.get('end_date'):
                        assignment['end_date'] = assignment['end_date'].strftime("%Y-%m-%d")
                
                # Calculate available allocation
                resource['available_allocation'] = max(0, 100 - resource['total_allocation'])
                
                resources.append(resource)
            
            dict_cursor.close()
            return resources
        except Exception as e:
            logger.error(f"❌ Error fetching resource allocation report: {e}")
            return []
    
    def get_task_completion_report(self) -> Dict[str, Any]:
        """
        Get a task completion report.
        Returns a dictionary with task completion statistics.
        """
        if not self.connected:
            logger.warning("Cannot get task completion report - no database connection")
            return {}
            
        try:
            dict_cursor = self.conn.cursor(cursor_factory=DictCursor)
            
            # Get overall statistics
            dict_cursor.execute("""
                SELECT
                    COUNT(*) as total_tasks,
                    SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) as completed_tasks,
                    SUM(CASE WHEN status = 'In Progress' THEN 1 ELSE 0 END) as in_progress_tasks,
                    SUM(CASE WHEN status = 'Not Started' THEN 1 ELSE 0 END) as not_started_tasks,
                    SUM(CASE WHEN status = 'On Hold' THEN 1 ELSE 0 END) as on_hold_tasks,
                    ROUND(AVG(CASE WHEN status = 'Completed' THEN 100
                              WHEN status = 'In Progress' THEN 50
                              ELSE 0 END), 1) as avg_completion
                FROM tasks
            """)
            
            overall = dict(dict_cursor.fetchone())
            
            # Get completion by project
            dict_cursor.execute("""
                SELECT
                    p.id as project_id,
                    p.name as project_name,
                    COUNT(t.id) as total_tasks,
                    SUM(CASE WHEN t.status = 'Completed' THEN 1 ELSE 0 END) as completed_tasks,
                    ROUND(SUM(CASE WHEN t.status = 'Completed' THEN 1 ELSE 0 END)::float / 
                          NULLIF(COUNT(t.id), 0) * 100, 1) as completion_percentage
                FROM tasks t
                JOIN projects p ON t.project_id = p.id
                GROUP BY p.id, p.name
                ORDER BY p.name
            """)
            
            by_project = [dict(row) for row in dict_cursor.fetchall()]
            
            # Get recently completed tasks
            dict_cursor.execute("""
                SELECT
                    t.id, t.title, t.completed_date, p.name as project_name,
                    (SELECT string_agg(r.name, ', ')
                     FROM resources r
                     JOIN task_assignments ta ON r.id = ta.resource_id
                     WHERE ta.task_id = t.id) as assigned_to
                FROM tasks t
                JOIN projects p ON t.project_id = p.id
                WHERE t.status = 'Completed'
                AND t.completed_date IS NOT NULL
                ORDER BY t.completed_date DESC
                LIMIT 10
            """)
            
            recent_completions = []
            for row in dict_cursor.fetchall():
                task = dict(row)
                if task['completed_date']:
                    task['completed_date'] = task['completed_date'].strftime("%Y-%m-%d")
                recent_completions.append(task)
            
            # Get overdue tasks
            dict_cursor.execute("""
                SELECT
                    t.id, t.title, t.due_date, p.name as project_name,
                    t.priority,
                    (CURRENT_DATE - t.due_date) as days_overdue,
                    (SELECT string_agg(r.name, ', ')
                     FROM resources r
                     JOIN task_assignments ta ON r.id = ta.resource_id
                     WHERE ta.task_id = t.id) as assigned_to
                FROM tasks t
                JOIN projects p ON t.project_id = p.id
                WHERE t.status != 'Completed'
                AND t.due_date < CURRENT_DATE
                ORDER BY t.due_date ASC
                LIMIT 10
            """)
            
            overdue_tasks = []
            for row in dict_cursor.fetchall():
                task = dict(row)
                if task['due_date']:
                    task['due_date'] = task['due_date'].strftime("%Y-%m-%d")
                overdue_tasks.append(task)
            
            dict_cursor.close()
            
            return {
                "overall": overall,
                "by_project": by_project,
                "recent_completions": recent_completions,
                "overdue_tasks": overdue_tasks
            }
        except Exception as e:
            logger.error(f"❌ Error fetching task completion report: {e}")
            return {}
    
    def close(self):
        """Close the database connection."""
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
            logger.info("Database connection closed")