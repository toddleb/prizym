# Medtronic SPM Solution Design Document
## Territory and Quota Management (TQM) & Incentive Compensation Management (ICM) Delivery

**Document Version:** 1.0  
**Date:** March 28, 2025  
**Status:** Draft  
**Author:** [Your Name]  
**Approvers:** [Key Stakeholders]

---

## 1. Executive Summary

This document provides the detailed solution design for implementing an integrated Sales Performance Management (SPM) platform across Medtronic's global operations, encompassing both Territory and Quota Management (TQM) and Incentive Compensation Management (ICM). The solution addresses the current fragmented landscape of territory management and sales compensation systems to create a unified, global approach to sales performance management.

**Strategic Objectives:**
- Create a single source of truth for territory definitions, quota management, and sales compensation globally
- Replace ad-hoc territory management and compensation processes with standardized workflows and governance
- Enable dynamic territory adjustments and compensation plan changes with robust approval processes
- Support parallel sales team alignment and crediting with accurate commission calculations
- Drive sales performance through transparent incentives aligned with corporate objectives
- Ensure data security with role-based access control
- Provide a scalable platform that supports 23,550+ users across all regions and business units
- Reduce operational costs through system consolidation and process automation

---

## 2. Current State Overview

Medtronic currently lacks a robust Territory Management System, resulting in several challenges:

- No single source of truth across all businesses for territories and quotas
- Multiple custom Global Sales Reporting (GSR) applications to compensate for limited territory functionality
- Complex data landscape with 25+ integrations across 6 different datasets
- Difficulty standardizing operations, reporting, and analytics
- High platform management costs across multiple systems

### 2.1 Existing GSR Applications and Compensation Systems

The following applications currently support territory management and sales compensation:

1. **Parallel Sales Team Apps:**
   - US CV Strategic Sales Team App
   - US CV Co-Sell App
   - OUS Parallel Sales Team App

2. **Territory Alignment Apps:**
   - Implanter Reassignment App (for US CV and NS Implant Territory Realignment)
   
3. **Security Management:**
   - Exception Security App (for user access to sales and inventory data)

4. **Adjustment Management:**
   - Manual Sales Adjustment App

5. **Compensation Systems:**
   - COMPASS (1,200 users)
   - SAP CALLIDUS (7,500 users)
   - SIP 2.0 (12,650 users)
   - VARICENT (2,200 users)

### 2.2 Current User Landscape

Total user count: 23,550, distributed across:
- COMPASS: 1,200
- SAP CALLIDUS: 7,500
- SIP 2.0: 12,650
- VARICENT: 2,200

User distribution by region:
- US: ~9,400
- Europe: ~4,200
- Japan: ~1,650
- ANZ: ~700
- China: ~3,000
- Other regions: ~4,600

---

## 3. Target Solution Architecture

### 3.1 System Landscape

The TQM solution will be implemented as a cloud-native application, integrating with the following systems:

```
┌───────────────────┐     ┌───────────────────┐     ┌───────────────────┐
│                   │     │                   │     │                   │
│    Source Systems │────▶│   SPM Platform    │────▶│  Target Systems   │
│    (SAP, DTRAK)   │     │   (TQM + ICM)     │     │                   │
│                   │     │                   │     │                   │
└───────────────────┘     └───────────────────┘     └───────────────────┘
         ▲                        │                         ▲
         │                        ▼                         │
         │                ┌───────────────────┐            │
         │                │                   │            │
         └────────────────│  Data Platform    │────────────┘
                          │  (Snowflake)      │
                          └───────────────────┘
```

### 3.2 Component Architecture

The SPM platform consists of the following core components:

1. **Territory Structure Management**
   - Global, regional, and business unit hierarchies
   - Territory definitions and attributes
   - Customer-to-territory mapping

2. **Quota Management**
   - Top-down and bottom-up quota allocation
   - Quota approval workflows
   - Quota adjustments and tracking

3. **Parallel Team Management**
   - Team definition and configuration
   - Alignment rules engine
   - Credit assignment rules

4. **Incentive Compensation Management**
   - Plan design and configuration
   - Calculation engine
   - Payment processing and approvals
   - Dispute resolution
   - Statement generation

5. **Data Integration Layer**
   - ETL processes for SAP, DTRAK, and other sources
   - Data validation and enrichment
   - Historical data management

6. **Security and Access Control**
   - Role-based access for 23,550+ users
   - Row-level security for territories and sales data
   - Audit logging and compliance controls

7. **Analytics and Reporting**
   - Performance dashboards
   - Compensation analytics
   - Territory effectiveness reporting
   - Quota attainment tracking

8. **User Experience Layer**
   - Territory manager workbench
   - Sales rep compensation portal
   - Administrator console

---

## 4. Detailed Technical Design

### 4.1 Territory Management 

#### Core Capabilities
- Territory definitions with multi-level hierarchies
- Customer-to-territory alignment with rule-based assignment
- Support for both primary and parallel sales teams
- Territory changes with approval workflows
- Time-based territory snapshots and historical tracking

#### Key Data Entities
- Territory Definitions
- Territory Hierarchies  
- Customer Segmentation
- Customer-Territory Relationships
- Territory Assignments

#### Workflows
1. **Territory Creation/Modification**
   - Territory request initiated
   - Approvals based on hierarchy
   - Effective dating for changes
   - Notification to affected stakeholders

2. **Customer Assignment**
   - Rule-based customer assignments
   - Manual reassignments with approval
   - Overlap detection and resolution
   - History tracking of all changes

3. **Parallel Team Alignment**
   - Definition of parallel teams by region/business
   - Configuration of alignment rules
   - Credit split configurations
   - Territory document distribution

### 4.2 Quota Management

#### Core Capabilities
- Top-down quota allocation with protection rules
- Bottom-up quota aggregation and tracking
- Quota adjustments with approval workflows
- Integration with sales planning systems
- Performance tracking against quotas

#### Key Data Entities
- Quota Plans
- Quota Allocations
- Quota Adjustments
- Attainment Tracking
- Quota History

#### Workflows
1. **Quota Setting**
   - Annual/quarterly quota planning
   - Top-down allocation to territories
   - Review and approval process
   - Finalization and communication

2. **Quota Adjustment**
   - Mid-period adjustment requests
   - Approval based on materiality
   - Documentation of adjustment reasons
   - Recalculation of dependent quotas

3. **Performance Tracking**
   - Real-time attainment visibility
   - Forecast to goal calculations
   - Reporting by territory/region/product
   - Alerting for performance issues

### 4.3 Incentive Compensation Management

#### Core Capabilities
- Flexible plan design and configuration
- Complex calculation rules and crediting
- Multiple currency support
- Performance-based incentives
- Approval workflows for payouts
- Statement generation and distribution
- Dispute management

#### Key Data Entities
- Compensation Plans
- Plan Components
- Calculation Rules
- Credits and Transactions
- Payments and Statements
- Disputes and Resolutions

#### Workflows
1. **Plan Design and Administration**
   - Plan creation with components
   - Eligibility rules definition
   - Crediting configuration
   - Approval and activation process

2. **Calculation Process**
   - Transaction data ingestion
   - Credit assignment based on territory and rules
   - Formula calculation
   - Aggregation and summary
   - Approval before payment

3. **Statement Generation and Distribution**
   - Periodic statement creation
   - Detailed calculation breakdown
   - Digital distribution to reps
   - Archival for compliance

4. **Dispute Resolution**
   - Rep-initiated disputes
   - Manager review process
   - Resolution approval
   - Adjustment application
   - Communication to stakeholders

### 4.4 Integration Architecture

#### Inbound Data Flows
1. **SAP/Centerpiece**
   - Customer master data
   - Product hierarchy information
   - Base sales structure
   - Transaction data (sales, orders, invoices)

2. **DTRAK**
   - Implant data for US CV and NS
   - Implanting physician information

3. **HR Systems**
   - Employee information
   - Organizational hierarchy
   - Position and job data

4. **Financial Systems**
   - Exchange rates
   - GL accounts
   - Accrual information

#### Outbound Data Flows
1. **Snowflake**
   - Territory and customer alignments
   - Performance metrics
   - Compensation data for analytics

2. **Payroll Systems**
   - Payment instructions
   - Accrual data
   - Tax information

3. **Reporting Systems**
   - Territory structure snapshots
   - Performance data
   - Compensation analytics
   - Dashboards and KPIs

4. **Finance Systems**
   - Commission expense data
   - Accrual information
   - Audit trails

### 4.5 Security Model

The security model will replace the current Exception Security App with a robust role-based access control system:

1. **User Roles**
   - Territory Managers
   - Sales Operations
   - Sales Representatives
   - Regional Managers
   - Compensation Administrators
   - Finance Users
   - HR Personnel
   - System Administrators

2. **Access Controls**
   - Territory-based access (view/edit)
   - Customer-level security
   - Product hierarchy security
   - Compensation plan view/edit permissions
   - Payment approval authorities
   - Dispute resolution access
   - Approval workflow permissions

3. **Audit & Compliance**
   - Complete audit trails for all changes
   - Documentation of approvals
   - Calculation versioning and history
   - Payment authorization tracking
   - SOX compliance controls
   - Segregation of duties enforcement

---

## 5. Data Migration Strategy

### 5.1 Legacy Data Sources

The implementation will migrate data from the following sources:

1. **GSR Applications**
   - Parallel Sales Team apps (US CV Strategic, Co-Sell, OUS Parallel)
   - Implanter Reassignment App
   - Manual Sales Adjustment App
   - Exception Security App

2. **SAP/Centerpiece**
   - Current territory structures
   - Customer assignments

3. **Local Systems**
   - Excel-based territory definitions
   - Regional quota allocations

### 5.2 Migration Approach

1. **Assessment & Mapping**
   - Inventory all data sources
   - Develop data mapping specifications
   - Validate completeness of source data

2. **Transformation Rules**
   - Define normalization rules
   - Establish validation criteria
   - Create exception handling processes

3. **Migration Execution**
   - Extract legacy data
   - Transform to target model
   - Load into new platform
   - Validate data integrity

4. **Historical Data Management**
   - Load 12-24 months of historical data
   - Establish archiving policies
   - Enable historical reporting

---

## 6. Implementation Approach

### 6.1 Phased Implementation

The implementation will follow a phased approach to minimize business disruption:

**Phase 0: Assessment & Design (Current Phase)**
- Detailed requirements analysis
- Solution design and architecture
- Migration strategy development
- Implementation planning

**Phase 1: Core Territory Management & Base Compensation**
- Global territory structure setup
- Basic customer assignment capabilities
- Core compensation plan configuration
- Data migration from legacy systems
- Initial rollout to pilot group (US Neuroscience)

**Phase 2: Advanced Territory Management & Enhanced Compensation**
- Parallel team configurations
- Enhanced approval workflows
- Complex calculation rules implementation
- Dispute resolution process
- Expanded rollout to major regions (US Cardiovascular, Europe)

**Phase 3: Quota Management & Full Compensation Deployment**
- Quota allocation framework
- Advanced crediting rules
- Performance tracking dashboards
- Advanced analytics and reporting
- Complete global deployment
- Retirement of legacy systems

**Phase 4: Optimization & Advanced Analytics**
- AI-driven territory optimization
- Predictive performance modeling
- Advanced compensation analytics
- Enhanced mobile capabilities

### 6.2 Testing Strategy

1. **Unit Testing**
   - Component-level validation
   - Rule engine verification
   - Integration endpoint testing

2. **System Integration Testing**
   - End-to-end process validation
   - Data flow verification
   - Performance under load

3. **User Acceptance Testing**
   - Business scenario validation
   - Regional process verification
   - Legacy system comparison

4. **Parallel Testing**
   - Side-by-side operation with legacy systems
   - Results comparison and reconciliation
   - Discrepancy resolution

### 6.3 Deployment Strategy

1. **Technical Deployment**
   - Environment setup and configuration
   - Data migration execution
   - Integration enablement
   - Security implementation

2. **Business Deployment**
   - User training and enablement
   - Process transition support
   - Hypercare period
   - Performance monitoring

---

## 7. Organizational Impact and Change Management

### 7.1 Impacted Stakeholders

1. **Sales Representatives (20,000+)**
   - Access to territory information
   - Visibility into customer assignments
   - Performance tracking against quotas

2. **Sales Operations (500+)**
   - Territory management workflows
   - Quota allocation processes
   - System administration

3. **Sales Leadership (1,000+)**
   - Territory performance visibility
   - Resource allocation decisions
   - Strategic planning capabilities

4. **IT Support (50+)**
   - System support transition
   - Integration management
   - Data governance

### 7.2 Change Management Approach

1. **Awareness & Education**
   - Executive sponsorship messaging
   - Regional change champion network
   - Role-specific communication plans

2. **Training & Enablement**
   - Role-based training curriculum
   - Self-service learning materials
   - Hands-on system workshops

3. **Transition Support**
   - Hypercare for initial deployment
   - Super-user network development
   - Feedback collection and incorporation

4. **Metrics & Monitoring**
   - System adoption tracking
   - Process compliance monitoring
   - Business impact assessment

---

## 8. Risk Management

| Risk | Impact | Likelihood | Mitigation Strategy |
|------|--------|------------|---------------------|
| Data quality issues from legacy systems | High | High | Implement data cleansing and validation routines prior to migration. Establish data governance processes. |
| User resistance to new processes | Medium | Medium | Engage stakeholders early. Develop comprehensive training and communication plan. Highlight benefits. |
| Complex approval workflows delay implementation | High | Medium | Start with simplified workflows and evolve. Pilot with key business units first. |
| Integration challenges with compensation systems | High | Medium | Conduct early integration testing. Develop fallback procedures for critical processes. |
| Performance issues with large user base | Medium | Low | Performance test with realistic data volumes. Scale infrastructure appropriately. |
| Regional compliance requirements | Medium | Medium | Engage regional compliance teams early. Design flexible framework to accommodate variations. |

---

## 9. Timeline and Milestones

| Milestone | Target Date | Deliverables |
|-----------|-------------|--------------|
| Solution Design Approval | April 30, 2025 | Approved solution design document |
| Phase 1 Implementation | July 15, 2025 | Core territory management deployed to pilot regions |
| Phase 2 Implementation | October 1, 2025 | Advanced territory management and initial quota capabilities |
| Phase 3 Implementation | January 15, 2026 | Complete quota management and global rollout |
| Legacy System Retirement | April 15, 2026 | Decommissioning of GSR applications |

---

## 10. Operational Considerations

### 10.1 System Administration

1. **User Management**
   - User provisioning processes
   - Role assignment workflows
   - Access request procedures

2. **Configuration Management**
   - Change control processes
   - Environment management
   - Release management

3. **Data Management**
   - Data quality controls
   - Master data governance
   - Archiving and retention

### 10.2 Support Model

1. **Tier 1 Support**
   - User access and basic usage issues
   - Knowledge base and self-help resources
   - Initial issue triage

2. **Tier 2 Support**
   - Configuration issues
   - Process exceptions
   - Complex workflow problems

3. **Tier 3 Support**
   - System issues requiring vendor involvement
   - Complex integration problems
   - Performance optimization

---

## 11. Success Metrics

| Metric | Current State | Target | Measurement Approach |
|--------|--------------|--------|----------------------|
| Territory change cycle time | 7-10 days | 1-2 days | Track time from request to implementation |
| Quota allocation accuracy | 85% | 99% | Measure discrepancies and adjustments |
| Data integration timeliness | 24 hours | 3 hours | Monitor ETL completion times |
| Compensation calculation accuracy | 95% | 99.9% | Audit compensation results against manual calculations |
| Commission payment timeliness | 15-20 days | 5-7 days | Measure time from period close to payment |
| Dispute resolution time | 14+ days | 3-5 days | Track dispute lifecycle time |
| Calculation processing time | 24-48 hours | 2-4 hours | Measure processing runtime |
| User adoption | N/A | 95% | Track active users vs. eligible users |
| Territory data accuracy | 90% | 99.5% | Audit customer-territory assignments |
| Performance reporting timeliness | 48 hours | Real-time | Measure data refresh to reporting delay |
| System consolidation | 4 systems | 1 platform | Count of active compensation systems |
| Total cost of ownership | Current baseline | 30% reduction | Measure annual operating costs |

---

## 12. Appendices

### Appendix A: Current State GSR Applications Detail

#### Parallel Sales Team Apps
Currently, Medtronic uses several applications to manage parallel sales teams:
- US CV Strategic Sales Team App: Enables support for strategic customer accounts in Cardiovascular
- US CV Co-Sell App: Enables the Co-Sell process for sales teams by providing a foundation to define Co-sell teams and credit both Diagnostic and Coronary Sales Reps
- OUS Parallel Sales Team App: Contains configuration for automatic generation of sales credit to non-primary sales teams

#### Implanter Reassignment App
Used to re-align implanting physicians to territories other than the primary rep assignment driven by SAP. This reduces "moving parts" and enables near-real-time reporting of territory changes.

#### Exception Security App
Enables GSR admins to view and maintain user access to GSR Sales and Inventory data, providing security at the sales structure, location/country/entity, and business/customer levels.

#### Manual Sales Adjustment App
Standard interface for entering revenue and quantity adjustments post-generation of invoices.

### Appendix B: User Volume Analysis

| Region | User Count |
|--------|------------|
| US | 9,400 |
| Europe | 4,200 |
| Japan | 1,650 |
| ANZ | 700 |
| China | 3,000 |
| EMEA RLM | 1,650 |
| LATAM | 1,400 |
| Canada | 300 |
| Asia RLM | 2,000 |
| China RLM | 350 |

| Operating Unit | User Count |
|----------------|------------|
| Neuroscience | 3,600 |
| Cardiovascular | 2,500 |
| Surgical | 1,100 |
| Diabetes | 1,200 |

### Appendix C: Glossary of Terms

| Term | Definition |
|------|------------|
| TQM | Territory Quota Management |
| ICM | Incentive Compensation Management |
| SPM | Sales Performance Management |
| GSR | Global Sales Reporting |
| OCM | Organizational Change Management |
| Parallel Team | Secondary sales team that receives credit for sales but may not be the primary team |
| Alignment Rules | Business rules that determine how customers and sales are assigned to territories |
| Crediting | The process of assigning sales transaction values to specific sales representatives |
| Split Credit | When multiple sales representatives receive partial credit for the same transaction |
| Shadow Credit | Credit given to a sales representative for influence on a sale without being the primary rep |
| Compensation Component | Building block of an incentive plan (e.g., quota-based commission, bonus, SPIF) |
| Attainment | Percentage of quota achieved within a specified period |
| Accelerator | Increased commission rate that applies after reaching certain performance thresholds |
| True-up | Adjustment made to compensate for prior period corrections or changes |
| Clawback | Recovery of previously paid compensation due to policy violations or corrections |

---

*End of Document*
