# PROJECT TILE 
Student-Mental-Health-and-Support-System
# Student Mental Health and Support System

## Project Overview
The Student Mental Health and Support System is a web-based application designed to provide psychological support, mental health resources, and wellbeing tracking for students in higher education institutions.

---

## Development Progress

###  Project Title Finalization

- Selected project domain: Mental Health
- Finalized project title
- Defined project scope and target users

---

###  Requirement Gathering

#### Problem Statement
Students often face stress, anxiety, academic pressure, and emotional challenges. Many hesitate to seek professional help due to accessibility and privacy concerns.

#### Requirements Collected
- Student Registration
- Secure Login
- Mental Health Assessment
- Dashboard
- Support Resources
- Progress Tracking

---

###  Objective Definition

#### Objectives
1. Provide mental health support for students.
2. Monitor student wellbeing.
3. Offer self-assessment tools.
4. Enable secure access to resources.
5. Generate insights through reports.

---

###  User & Module Identification

#### Users
- Student
- Counselor/Admin

#### Modules
1. Authentication Module
2. Student Dashboard
3. Assessment Module
4. Resource Management Module
5. Report Module
6. Profile Management Module

---

### Use Case Diagram Preparation

#### Student Use Cases
- Register
- Login
- Update Profile
- Take Assessment
- View Dashboard
- Access Resources

#### Admin Use Cases
- Manage Users
- Manage Resources
- View Reports

---

###  Database Requirement Analysis

#### Database Tables

##### Users
| Field | Type |
|---------|---------|
| id | INT |
| name | VARCHAR |
| email | VARCHAR |
| password | VARCHAR |
| role | VARCHAR |

##### Assessments
| Field | Type |
|---------|---------|
| assessment_id | INT |
| user_id | INT |
| score | INT |
| date | DATE |

##### Resources
| Field | Type |
|---------|---------|
| resource_id | INT |
| title | VARCHAR |
| description | TEXT |

---

###  ER Diagram Design

#### Entities
- User
- Assessment
- Resource
- Report

#### Relationships
- User takes Assessment
- Assessment generates Report
- Admin manages Resources

Admin manages Resources
Student accesses Resources
Student takes Assessments
Assessment generates Reports
---
## Use Case Diagram

```text
                    +----------------+
                    |     Student    |
                    +----------------+
                           |
       --------------------------------------------
       |            |           |         |        |
       v            v           v         v        v
 +-----------+ +---------+ +----------+ +---------+ +--------------+
 | Register  | | Login   | | Profile  | | Take    | | View Mental  |
 |           | |         | | Update   | | Assessment | Health Resources |
 +-----------+ +---------+ +----------+ +---------+ +--------------+
                                            |
                                            v
                                     +-------------+
                                     | View Report |
                                     +-------------+


                    +----------------+
                    |     Admin      |
                    +----------------+
                           |
      ---------------------------------------------
      |                 |                 |
      v                 v                 v
+-------------+ +---------------+ +---------------+
| Manage Users| | Manage Content| | View Reports  |
+-------------+ +---------------+ +---------------+
```

###  Database Schema Creation

#### Tables Created
- users
- assessments
- resources
- reports

#### Relationships
- Foreign Key between Users and Assessments
- Foreign Key between Assessments and Reports

---

###  UI Wireframe Design

#### Planned Screens
1. Login Page
2. Registration Page
3. Dashboard
4. Assessment Page
5. Resources Page
6. Profile Page

---

### Login & Dashboard UI Design
#### Designed Components
- Login Form
- Dashboard Cards
- Navigation Sidebar
- Header Section

---

### Navigation & Form Design

#### Navigation Features
- Sidebar Menu
- Dashboard Navigation
- Form Validation

---

###  Design Review

#### Review Checklist
- UI Consistency
- User Experience
- Database Structure
- Module Design

---

###  Frontend Environment Setup

#### Setup Tasks
- Install Node.js
- Create React App
- Install Dependencies
- Configure Project Structure

---

###  Login Page Development

#### Features
- Email Validation
- Password Validation
- Login Form UI
- API Integration Ready

---

### Registration Page Development

#### Features
- Student Registration Form
- Input Validation
- Password Confirmation
- Form Submission

---

###  Dashboard Development

#### Dashboard Components
- Welcome Section
- Mental Health Summary
- Assessment History
- Quick Actions

---

###  CRUD Form Development


#### CRUD Operations
- Create Assessment
- Read Assessment Records
- Update User Data
- Delete Records

---

## Technologies Used

### Frontend
- React.js
- HTML
- CSS
- JavaScript

### Backend
- Spring Boot
- Java

### Database
- MySQL

### Tools
- Git
- GitHub
- Postman

---

## Project Status

| Phase | Status |
|---------|---------|
| Planning | Completed |
| Requirement Analysis | Completed |
| Database Design | In Progress |
| UI Design | In Progress |
| Frontend Development | Pending |
| Backend Development | Pending |
| Testing | Pending |

---

