import pandas as pd

# Load the employee dataset
file_path = "DATA/Palo Alto Networks.csv"

df = pd.read_csv(file_path)

# Show basic information
print("====================================")
print("PALO ALTO NETWORKS EMPLOYEE ANALYSIS")
print("====================================")

print("\nDataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\nFirst 5 Rows:")
print(df.head())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("\n====================================")
print("IMPORTANT VALUE CHECKS")
print("====================================")

print("\nEnvironment Satisfaction:")
print(sorted(df["EnvironmentSatisfaction"].unique()))

print("\nJob Involvement:")
print(sorted(df["JobInvolvement"].unique()))

print("\nJob Satisfaction:")
print(sorted(df["JobSatisfaction"].unique()))

print("\nRelationship Satisfaction:")
print(sorted(df["RelationshipSatisfaction"].unique()))

print("\nWork-Life Balance:")
print(sorted(df["WorkLifeBalance"].unique()))

print("\nAttrition:")
print(sorted(df["Attrition"].unique()))

print("\nOverTime:")
print(df["OverTime"].unique())

print("\nBusiness Travel:")
print(df["BusinessTravel"].unique())

# ====================================
# ENGAGEMENT INDEX
# ====================================

engagement_columns = [
    "JobInvolvement",
    "JobSatisfaction",
    "EnvironmentSatisfaction",
    "RelationshipSatisfaction"
]

df["EngagementIndex"] = df[engagement_columns].mean(axis=1)

print("\n====================================")
print("ENGAGEMENT INDEX")
print("====================================")

print("\nFirst 10 Engagement Scores:")
print(df["EngagementIndex"].head(10))

print("\nAverage Engagement Index:")
print(round(df["EngagementIndex"].mean(), 2))

print("\nMinimum Engagement Index:")
print(round(df["EngagementIndex"].min(), 2))

print("\nMaximum Engagement Index:")
print(round(df["EngagementIndex"].max(), 2))

# ====================================
# BURNOUT RISK
# ====================================

def calculate_burnout_risk(row):

    if row["OverTime"] == "Yes" and row["WorkLifeBalance"] <= 2:
        return "High"

    elif row["OverTime"] == "Yes" or row["WorkLifeBalance"] <= 2:
        return "Medium"

    else:
        return "Low"


df["BurnoutRisk"] = df.apply(calculate_burnout_risk, axis=1)

print("\n====================================")
print("BURNOUT RISK")
print("====================================")

print("\nBurnout Risk Counts:")
print(df["BurnoutRisk"].value_counts())

print("\nBurnout Risk Percentages:")
print(
    round(
        df["BurnoutRisk"].value_counts(normalize=True) * 100,
        2
    )
)

# ====================================
# WORK-LIFE BALANCE INDEX
# ====================================

df["WorkLifeBalanceIndex"] = df["WorkLifeBalance"]

print("\n====================================")
print("WORK-LIFE BALANCE INDEX")
print("====================================")

print("\nAverage Work-Life Balance:")
print(round(df["WorkLifeBalanceIndex"].mean(), 2))

print("\nMinimum Work-Life Balance:")
print(df["WorkLifeBalanceIndex"].min())

print("\nMaximum Work-Life Balance:")
print(df["WorkLifeBalanceIndex"].max())

print("\nWork-Life Balance Distribution:")
print(df["WorkLifeBalanceIndex"].value_counts().sort_index())

# ====================================
# SATISFACTION STABILITY SCORE
# ====================================

satisfaction_columns = [
    "JobSatisfaction",
    "EnvironmentSatisfaction",
    "RelationshipSatisfaction",
    "JobInvolvement"
]

df["SatisfactionStabilityScore"] = (
    1 - (df[satisfaction_columns].std(axis=1) / 1.5)
).clip(0, 1) * 100

print("\n====================================")
print("SATISFACTION STABILITY SCORE")
print("====================================")

print("\nAverage Satisfaction Stability Score:")
print(round(df["SatisfactionStabilityScore"].mean(), 2))

print("\nMinimum Satisfaction Stability Score:")
print(round(df["SatisfactionStabilityScore"].min(), 2))

print("\nMaximum Satisfaction Stability Score:")
print(round(df["SatisfactionStabilityScore"].max(), 2))


# ====================================
# WORKLOAD STRESS INDICATOR
# ====================================

df["WorkloadStressIndicator"] = 0

# Overtime adds stress
df.loc[df["OverTime"] == "Yes", "WorkloadStressIndicator"] += 2

# Frequent business travel adds stress
df.loc[
    df["BusinessTravel"] == "Travel_Frequently",
    "WorkloadStressIndicator"
] += 2

# Rare travel adds a smaller amount
df.loc[
    df["BusinessTravel"] == "Travel_Rarely",
    "WorkloadStressIndicator"
] += 1

# Long commute adds stress
df.loc[
    df["DistanceFromHome"] >= 10,
    "WorkloadStressIndicator"
] += 1

print("\n====================================")
print("WORKLOAD STRESS INDICATOR")
print("====================================")

print("\nAverage Workload Stress Indicator:")
print(round(df["WorkloadStressIndicator"].mean(), 2))

print("\nMinimum Workload Stress Indicator:")
print(df["WorkloadStressIndicator"].min())

print("\nMaximum Workload Stress Indicator:")
print(df["WorkloadStressIndicator"].max())

print("\nStress Indicator Distribution:")
print(df["WorkloadStressIndicator"].value_counts().sort_index())

# ====================================
# ENGAGEMENT VS ATTRITION
# ====================================

print("\n====================================")
print("ENGAGEMENT VS ATTRITION")
print("====================================")

engagement_by_attrition = df.groupby("Attrition")["EngagementIndex"].mean()

print("\nAverage Engagement by Attrition:")
print(engagement_by_attrition.round(2))

print("\nAttrition Meaning:")
print("0 = Stayed")
print("1 = Left")

# ====================================
# ATTRITION RATE
# ====================================

print("\n====================================")
print("ATTRITION RATE")
print("====================================")

attrition_counts = df["Attrition"].value_counts()

print("\nAttrition Counts:")
print(attrition_counts)

print("\nAttrition Rate:")
print(round(df["Attrition"].mean() * 100, 2), "%")

# ====================================
# OVERTIME VS ENGAGEMENT
# ====================================

print("\n====================================")
print("OVERTIME VS ENGAGEMENT")
print("====================================")

overtime_engagement = df.groupby("OverTime")["EngagementIndex"].agg(
    ["mean", "count"]
)

print("\nEngagement by Overtime:")
print(overtime_engagement.round(2))

# ====================================
# BURNOUT RISK VS ATTRITION
# ====================================

print("\n====================================")
print("BURNOUT RISK VS ATTRITION")
print("====================================")

burnout_attrition = df.groupby("BurnoutRisk")["Attrition"].agg(
    ["mean", "count"]
)

burnout_attrition["AttritionRate"] = (
    burnout_attrition["mean"] * 100
)

print("\nAttrition by Burnout Risk:")
print(
    burnout_attrition[
        ["count", "AttritionRate"]
    ].round(2)
)

# ====================================
# HIGH BURNOUT RISK BY DEPARTMENT
# ====================================

print("\n====================================")
print("HIGH BURNOUT RISK BY DEPARTMENT")
print("====================================")

high_burnout_department = (
    df[df["BurnoutRisk"] == "High"]
    .groupby("Department")
    .size()
    .sort_values(ascending=False)
)

print("\nHigh Burnout Risk Employees by Department:")
print(high_burnout_department)

# ====================================
# HIGH BURNOUT RISK % BY DEPARTMENT
# ====================================

print("\n====================================")
print("HIGH BURNOUT RISK % BY DEPARTMENT")
print("====================================")

department_burnout = (
    df.groupby("Department")["BurnoutRisk"]
    .apply(lambda x: (x == "High").mean() * 100)
    .sort_values(ascending=False)
)

print("\nHigh Burnout Risk Percentage by Department:")
print(department_burnout.round(2))

# ====================================
# HIGH BURNOUT RISK BY JOB ROLE
# ====================================

print("\n====================================")
print("HIGH BURNOUT RISK BY JOB ROLE")
print("====================================")

high_burnout_roles = (
    df[df["BurnoutRisk"] == "High"]
    .groupby("JobRole")
    .size()
    .sort_values(ascending=False)
)

print("\nHigh Burnout Risk Employees by Job Role:")
print(high_burnout_roles)

# ====================================
# HIGH BURNOUT RISK % BY JOB ROLE
# ====================================

print("\n====================================")
print("HIGH BURNOUT RISK % BY JOB ROLE")
print("====================================")

role_burnout = (
    df.groupby("JobRole")["BurnoutRisk"]
    .apply(lambda x: (x == "High").mean() * 100)
    .sort_values(ascending=False)
)

print("\nHigh Burnout Risk Percentage by Job Role:")
print(role_burnout.round(2))

# ====================================
# TENURE VS ENGAGEMENT
# ====================================

print("\n====================================")
print("TENURE VS ENGAGEMENT")
print("====================================")

tenure_engagement = (
    df.groupby("YearsAtCompany")["EngagementIndex"]
    .mean()
)

print("\nAverage Engagement by Years at Company:")
print(tenure_engagement.round(2))

# ====================================
# CAREER STAGE VS ENGAGEMENT
# ====================================

def career_stage(years):
    if years <= 3:
        return "Early Career"
    elif years <= 9:
        return "Mid Career"
    else:
        return "Experienced"


df["CareerStage"] = df["YearsAtCompany"].apply(career_stage)

print("\n====================================")
print("CAREER STAGE VS ENGAGEMENT")
print("====================================")

career_engagement = (
    df.groupby("CareerStage")["EngagementIndex"]
    .agg(["mean", "count"])
)

print("\nEngagement by Career Stage:")
print(career_engagement.round(2))

# ====================================
# CAREER STAGNATION VS ENGAGEMENT
# ====================================

df["PotentialStagnation"] = (
    (df["YearsInCurrentRole"] >= 5) &
    (df["YearsSinceLastPromotion"] >= 3)
)

print("\n====================================")
print("CAREER STAGNATION VS ENGAGEMENT")
print("====================================")

stagnation_engagement = (
    df.groupby("PotentialStagnation")["EngagementIndex"]
    .agg(["mean", "count"])
)

print("\nEngagement by Potential Stagnation:")
print(stagnation_engagement.round(2))

# ====================================
# JOB LEVEL VS ENGAGEMENT
# ====================================

print("\n====================================")
print("JOB LEVEL VS ENGAGEMENT")
print("====================================")

joblevel_engagement = (
    df.groupby("JobLevel")["EngagementIndex"]
    .agg(["mean", "count"])
)

print("\nEngagement by Job Level:")
print(joblevel_engagement.round(2))

# ====================================
# BUSINESS TRAVEL VS ENGAGEMENT
# ====================================

print("\n====================================")
print("BUSINESS TRAVEL VS ENGAGEMENT")
print("====================================")

travel_engagement = (
    df.groupby("BusinessTravel")["EngagementIndex"]
    .agg(["mean", "count"])
)

print("\nEngagement by Business Travel:")
print(travel_engagement.round(2))

# ====================================
# COMMUTE DISTANCE VS ENGAGEMENT
# ====================================

def commute_group(distance):
    if distance < 10:
        return "Short Commute"
    else:
        return "Long Commute"


df["CommuteGroup"] = df["DistanceFromHome"].apply(commute_group)

print("\n====================================")
print("COMMUTE DISTANCE VS ENGAGEMENT")
print("====================================")

commute_engagement = (
    df.groupby("CommuteGroup")["EngagementIndex"]
    .agg(["mean", "count"])
)

print("\nEngagement by Commute Group:")
print(commute_engagement.round(2))

# ====================================
# LOW ENGAGEMENT ANALYSIS
# ====================================

df["LowEngagement"] = df["EngagementIndex"] < 2.5

print("\n====================================")
print("LOW ENGAGEMENT ANALYSIS")
print("====================================")

print("\nLow Engagement Employees:")
print(df["LowEngagement"].value_counts())

print("\nLow Engagement Percentage:")
print(
    round(
        df["LowEngagement"].mean() * 100,
        2
    )
)

# ====================================
# LOW ENGAGEMENT BY DEPARTMENT
# ====================================

low_engagement_department = (
    df.groupby("Department")["LowEngagement"]
    .agg(["sum", "count"])
)

low_engagement_department["LowEngagementPercentage"] = (
    low_engagement_department["sum"]
    / low_engagement_department["count"]
) * 100

print("\n====================================")
print("LOW ENGAGEMENT BY DEPARTMENT")
print("====================================")

print(
    low_engagement_department
    .round(2)
    .sort_values("LowEngagementPercentage", ascending=False)
)

# ====================================
# LOW ENGAGEMENT BY JOB ROLE
# ====================================

low_engagement_role = (
    df.groupby("JobRole")["LowEngagement"]
    .agg(["sum", "count"])
)

low_engagement_role["LowEngagementPercentage"] = (
    low_engagement_role["sum"]
    / low_engagement_role["count"]
) * 100

print("\n====================================")
print("LOW ENGAGEMENT BY JOB ROLE")
print("====================================")

print(
    low_engagement_role
    .round(2)
    .sort_values("LowEngagementPercentage", ascending=False)
)

# ====================================
# PRIORITY INTERVENTION GROUP
# ====================================

df["PriorityIntervention"] = (
    (df["LowEngagement"] == True) &
    (df["BurnoutRisk"] == "High") &
    (df["WorkLifeBalance"] <= 2)
)

print("\n====================================")
print("PRIORITY INTERVENTION GROUP")
print("====================================")

print("\nPriority Intervention Employees:")
print(df["PriorityIntervention"].value_counts())

print("\nPriority Intervention Percentage:")
print(
    round(
        df["PriorityIntervention"].mean() * 100,
        2
    )
)