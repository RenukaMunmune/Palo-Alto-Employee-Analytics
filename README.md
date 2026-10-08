# 📊 Palo Alto Networks — Employee Engagement & Burnout Analytics

This project analyzes employee engagement, satisfaction, work-life balance, workload stress, burnout risk, career stage, and attrition using Python and Streamlit.

## 🎯 Project Objective

The objective of this project is to analyze employee engagement, satisfaction, work-life balance, workload stress, burnout risk, career stage, and attrition to identify employee groups that may benefit from preventive HR attention.

## 💼 Business Problem

Organizations need early visibility into declining employee engagement, workload pressure, poor work-life balance, and potential burnout-related attrition.

This project provides a unified analytical view of these factors and helps identify employee segments that may require closer HR attention.

## 🎯 Objectives

1. Validate and prepare the employee dataset.
2. Create an Engagement Index using employee satisfaction and involvement measures.
3. Classify employees into project-defined burnout-risk groups.
4. Analyze workload, travel, commute, and work-life balance.
5. Compare engagement across departments, job roles, job levels, career stages, and tenure.
6. Compare engagement between employees who stayed and employees who left.
7. Build an interactive Streamlit dashboard for HR-oriented analysis.
8. Identify priority employee groups for preventive intervention.

## 📊 Dataset

The dataset contains:

- **1,470 employee records**
- **31 variables**
- Employee demographics
- Job and career information
- Satisfaction and involvement measures
- Work-life balance
- Overtime
- Business travel
- Attrition information

### Data Quality

The analysis verified:

- Missing values: **0**
- Duplicate rows: **0**
- Satisfaction and involvement scales: **1–4**
- Attrition values: **0/1**
- Overtime values: **Yes/No**

The original CSV dataset is excluded from the public GitHub repository using `.gitignore`.

## 🔬 Methodology

### 1. Engagement Index

The Engagement Index is calculated using the average of:

- Job Involvement
- Job Satisfaction
- Environment Satisfaction
- Relationship Satisfaction

The score ranges from **1 to 4**.

### 2. Burnout Risk

A project-defined burnout risk classification is used:

| Condition | Risk |
|---|---|
| Overtime = Yes AND Work-Life Balance ≤ 2 | High |
| Overtime = Yes OR Work-Life Balance ≤ 2 | Medium |
| Neither condition | Low |

> This is a project-defined analytical rule and is **not a clinical burnout assessment**.

### 3. Workload Stress Indicator

The project-defined workload stress indicator considers:

- Overtime
- Business travel frequency
- Distance from home

The maximum score is **5**.

### 4. Satisfaction Stability Score

A project-defined **0–100** consistency score is calculated using the variation across:

- Job Satisfaction
- Environment Satisfaction
- Relationship Satisfaction
- Job Involvement

> This is a project-defined metric and is **not a validated psychometric scale**.

### 5. Career Stage

Employees are grouped according to YearsAtCompany:

- **Early Career:** 0–3 years
- **Mid Career:** 4–9 years
- **Experienced:** 10+ years

## 📈 Key Findings

### Engagement

- Overall Engagement Index: **2.72 / 4**
- Low-engagement employees at the default threshold of 2.50: **353**
- Low-engagement share: **24.01%**

### Burnout Risk

- Low risk: **756 employees (51.43%)**
- Medium risk: **588 employees (40.00%)**
- High risk: **126 employees (8.57%)**

High-risk employees showed a higher attrition rate than the low-risk group in this dataset. This is an observed association and should not be interpreted as proof of causation.

### Work-Life Balance

- Average Work-Life Balance: **2.76 / 4**
- Employees with a Work-Life Balance score of 1 or 2: **424 (28.84%)**

### Attrition

- Employees who stayed: **1,233**
- Employees who left: **237**
- Overall attrition rate: **16.12%**

Average Engagement:

- Stayed: **2.76**
- Left: **2.51**

### Overtime

The overtime group did not automatically show lower engagement in this dataset.

- Overtime employees: **2.78**
- Non-overtime employees: **2.70**

This indicates that overtime should be considered together with other employee-experience factors rather than treated as an independent indicator of disengagement.

### Priority Intervention Group

A project-defined priority group uses:

- Engagement below the selected threshold
- High burnout risk
- Work-Life Balance ≤ 2

At the default threshold of 2.50:

- Priority employees: **23**
- Priority share: **1.56%**

This group is intended for analytical prioritization and is not a medical or psychological classification.

## 📊 Streamlit Dashboard

The interactive dashboard is organized into the following analytical modules:

### 1. Engagement Health Overview

- Engagement Index
- Satisfaction distributions
- Engagement vs Attrition
- Work-Life Balance

### 2. Burnout Risk Dashboard

- Burnout Risk Distribution
- Overtime vs Engagement
- High Burnout Risk by Department
- High Burnout Risk by Job Role

### 3. Role & Career Stage

- Engagement by Job Level
- Career Stage vs Engagement
- Tenure vs Engagement
- Business Travel vs Engagement
- Commute vs Engagement

### 4. Manager Action Panel

- Low Engagement by Department
- Low Engagement by Job Role
- High Burnout Risk by Job Role
- Priority Intervention Group
- Workload Stress Indicator
- Satisfaction Stability

### Interactive Filters

The dashboard allows users to filter the analysis by:

- Department
- Job Role
- Overtime
- Engagement Threshold
- Years at Company

## 🛠️ Technologies Used

- **Python 3.12**
- **Pandas** — Data loading and analysis
- **NumPy** — Numerical calculations
- **Matplotlib** — Data visualization
- **Seaborn** — Statistical visualization
- **Streamlit** — Interactive dashboard
- **Git & GitHub** — Version control and project hosting

## 📁 Project Structure

```text
Palo-Alto-Employee-Analytics/
│
├── DATA/
│   └── Palo Alto Networks.csv
│
├── analysis.py
├── app.py
├── README.md
└── .gitignore