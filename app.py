import streamlit as st
import pandas as pd

st.set_page_config(page_title="Palo Alto Networks | Employee Experience Analytics", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
.main { background:#f6f8fb; }
.block-container { max-width:1450px; padding-top:1.2rem; padding-bottom:3rem; }
.hero { padding:1.55rem 1.7rem; border-radius:18px; background:linear-gradient(135deg,#edf4ff 0%,#ffffff 58%,#f3f8ff 100%); border:1px solid #d9e5f5; margin-bottom:1rem; box-shadow:0 5px 18px rgba(16,24,40,.05); }
.hero h1 { margin:0 0 .4rem 0; font-size:2.15rem; letter-spacing:-.02em; }
.hero p { color:#475467; line-height:1.6; margin:0; font-size:.98rem; }
.section-note { color:#667085; font-size:.9rem; margin-top:-.35rem; margin-bottom:.8rem; }
div[data-testid="stMetric"] { background:#ffffff; border:1px solid #e4e7ec; border-radius:14px; padding:.85rem 1rem; box-shadow:0 2px 8px rgba(16,24,40,.045); min-height:105px; }
div[data-testid="stMetricLabel"] { font-size:.82rem; }
div[data-testid="stMetricValue"] { font-weight:700; }
.insight { background:#ffffff; border:1px solid #e4e7ec; border-left:4px solid #2563eb; border-radius:10px; padding:.9rem 1rem; margin:.6rem 0 1rem; box-shadow:0 2px 6px rgba(16,24,40,.035); }
.insight-title { font-weight:700; margin-bottom:.25rem; }
.section-card { background:#ffffff; border:1px solid #e4e7ec; border-radius:14px; padding:1rem 1.1rem; }
.footer { text-align:center; color:#667085; font-size:.8rem; padding-top:1.8rem; border-top:1px solid #e4e7ec; margin-top:2rem; }
[data-testid="stSidebar"] { background:#f8fafc; }
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { letter-spacing:-.01em; }
</style>
""", unsafe_allow_html=True)

# -------------------- DATA --------------------
SOURCE_COLUMN_COUNT = 31
FILE_PATH = "DATA/Palo Alto Networks.csv"
try:
    df = pd.read_csv(FILE_PATH)
except FileNotFoundError:
    st.error("Dataset not found. Expected: DATA/Palo Alto Networks.csv")
    st.stop()

engagement_cols = ["JobInvolvement", "JobSatisfaction", "EnvironmentSatisfaction", "RelationshipSatisfaction"]
df["EngagementIndex"] = df[engagement_cols].mean(axis=1)

def burnout(row):
    if row["OverTime"] == "Yes" and row["WorkLifeBalance"] <= 2:
        return "High"
    if row["OverTime"] == "Yes" or row["WorkLifeBalance"] <= 2:
        return "Medium"
    return "Low"

df["BurnoutRisk"] = df.apply(burnout, axis=1)

df["WorkloadStressIndicator"] = 0
df.loc[df["OverTime"] == "Yes", "WorkloadStressIndicator"] += 2
df.loc[df["BusinessTravel"] == "Travel_Frequently", "WorkloadStressIndicator"] += 2
df.loc[df["BusinessTravel"] == "Travel_Rarely", "WorkloadStressIndicator"] += 1
df.loc[df["DistanceFromHome"] >= 10, "WorkloadStressIndicator"] += 1

stability_cols = ["JobSatisfaction", "EnvironmentSatisfaction", "RelationshipSatisfaction", "JobInvolvement"]
df["SatisfactionStabilityScore"] = (1 - df[stability_cols].std(axis=1) / 1.5).clip(0, 1) * 100

# -------------------- SIDEBAR --------------------
st.sidebar.title("🎛️ Dashboard Filters")
st.sidebar.caption("Explore employee segments using the controls below.")

department = st.sidebar.selectbox("Department", ["All Departments"] + sorted(df.Department.unique().tolist()))
role = st.sidebar.selectbox("Job Role", ["All Job Roles"] + sorted(df.JobRole.unique().tolist()))
overtime = st.sidebar.checkbox("Show Overtime Employees Only")
threshold = st.sidebar.slider("Engagement Threshold", 1.0, 4.0, 2.5, 0.25)
min_years, max_years = int(df.YearsAtCompany.min()), int(df.YearsAtCompany.max())
tenure = st.sidebar.slider("Years at Company", min_years, max_years, (min_years, max_years), 1)

filtered = df.copy()
if department != "All Departments":
    filtered = filtered[filtered.Department == department]
if role != "All Job Roles":
    filtered = filtered[filtered.JobRole == role]
if overtime:
    filtered = filtered[filtered.OverTime == "Yes"]
filtered = filtered[filtered.YearsAtCompany.between(tenure[0], tenure[1])].copy()

if filtered.empty:
    st.warning("No employees match the selected filters. Please change the filters.")
    st.stop()

filtered["LowEngagement"] = filtered.EngagementIndex < threshold
filtered["PriorityIntervention"] = (
    (filtered.EngagementIndex < threshold) &
    (filtered.BurnoutRisk == "High") &
    (filtered.WorkLifeBalance <= 2)
)

# -------------------- HEADER --------------------
st.markdown("""
<div class="hero">
<h1>📊 Employee Engagement & Burnout Analytics</h1>
<p><b>Palo Alto Networks — Employee Experience Diagnostic Dashboard</b><br>
Analyze engagement, satisfaction, work-life balance, workload stress, burnout risk,
career stage and attrition to identify areas where preventive HR intervention may be useful.</p>
</div>
""", unsafe_allow_html=True)
st.info(f"📌 Current scope: {len(filtered):,} employees  •  Threshold: {threshold:.2f}  •  Tenure: {tenure[0]}–{tenure[1]} years")

# -------------------- KPIs --------------------
engagement = filtered.EngagementIndex.mean()
wlb = filtered.WorkLifeBalance.mean()
high_burnout = (filtered.BurnoutRisk == "High").mean() * 100
attrition = filtered.Attrition.mean() * 100
low_count = int(filtered.LowEngagement.sum())
low_pct = filtered.LowEngagement.mean() * 100
priority_count = int(filtered.PriorityIntervention.sum())
priority_pct = filtered.PriorityIntervention.mean() * 100

st.header("Executive Snapshot")
st.markdown('<div class="section-note">Key indicators for the currently selected employee segment.</div>', unsafe_allow_html=True)
k = st.columns(4)
k[0].metric("Engagement Index", f"{engagement:.2f}")
k[1].metric("Work-Life Balance", f"{wlb:.2f}")
k[2].metric("High Burnout Risk", f"{high_burnout:.2f}%")
k[3].metric("Attrition Rate", f"{attrition:.2f}%")
k = st.columns(4)
k[0].metric("Low Engagement Employees", f"{low_count:,}")
k[1].metric("Low Engagement %", f"{low_pct:.2f}%")
k[2].metric("Priority Employees", f"{priority_count:,}")
k[3].metric("Priority %", f"{priority_pct:.2f}%")

st.header("Dataset Overview")
k = st.columns(4)
k[0].metric("Employees in View", f"{len(filtered):,}")
k[1].metric("Departments", filtered.Department.nunique())
k[2].metric("Job Roles", filtered.JobRole.nunique())
k[3].metric("Source Variables", 31)

# -------------------- ENGAGEMENT --------------------
st.header("1. Engagement Health Overview")
st.markdown('<div class="section-note">Engagement Index = mean of Job Involvement, Job Satisfaction, Environment Satisfaction and Relationship Satisfaction.</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    attr = filtered.copy()
    attr["Status"] = attr.Attrition.map({0:"Stayed", 1:"Left"})
    data = attr.groupby("Status").EngagementIndex.mean().reindex(["Stayed", "Left"])
    st.subheader("Engagement Index vs Attrition")
    st.bar_chart(data, y_label="Average Engagement")
with c2:
    sat = pd.DataFrame({
        "Job Satisfaction": filtered.JobSatisfaction.value_counts().sort_index(),
        "Environment Satisfaction": filtered.EnvironmentSatisfaction.value_counts().sort_index(),
        "Relationship Satisfaction": filtered.RelationshipSatisfaction.value_counts().sort_index()
    }).fillna(0)
    st.subheader("Satisfaction Distributions")
    st.bar_chart(sat, y_label="Employees")
st.markdown(f'<div class="insight"><b>Interpretation:</b> Current average engagement is <b>{engagement:.2f}</b>. Employees below <b>{threshold:.2f}</b> are treated as the project-defined low-engagement group.</div>', unsafe_allow_html=True)

# -------------------- BURNOUT --------------------
st.header("2. Burnout Risk Dashboard")
st.markdown('<div class="section-note">Burnout Risk is a project-defined diagnostic classification using overtime and work-life balance.</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    counts = filtered.BurnoutRisk.value_counts().reindex(["Low", "Medium", "High"]).fillna(0)
    st.subheader("Burnout Risk Distribution")
    st.bar_chart(counts, y_label="Employees")
with c2:
    overtime_data = filtered.groupby("OverTime").EngagementIndex.mean().reindex(["No", "Yes"])
    st.subheader("Overtime vs Engagement")
    st.bar_chart(overtime_data, y_label="Average Engagement")

burn_dept = filtered.groupby("Department").BurnoutRisk.agg(High_Burnout_Employees=lambda x:(x=="High").sum(), Total_Employees="count")
burn_dept["High Burnout Risk %"] = burn_dept.High_Burnout_Employees / burn_dept.Total_Employees * 100
st.subheader("High Burnout Risk by Department")
st.dataframe(burn_dept.sort_values("High Burnout Risk %", ascending=False).round(2), use_container_width=True)

# -------------------- CAREER --------------------
st.header("3. Role & Career Stage")
c1, c2 = st.columns(2)
with c1:
    level = filtered.groupby("JobLevel").EngagementIndex.agg(["mean","count"]).rename(columns={"mean":"Average Engagement","count":"Employees"})
    st.subheader("Engagement by Job Level")
    st.bar_chart(level["Average Engagement"], y_label="Average Engagement")
with c2:
    career = filtered.copy()
    career["CareerStage"] = career.YearsAtCompany.apply(lambda x:"Early Career" if x<=3 else ("Mid Career" if x<=9 else "Experienced"))
    stage = career.groupby("CareerStage").EngagementIndex.agg(["mean","count"]).rename(columns={"mean":"Average Engagement","count":"Employees"}).reindex(["Early Career","Mid Career","Experienced"])
    st.subheader("Career Stage vs Engagement")
    st.bar_chart(stage["Average Engagement"], y_label="Average Engagement")

tenure_data = filtered.groupby("YearsAtCompany").EngagementIndex.agg(["mean","count"]).rename(columns={"mean":"Average Engagement","count":"Employees"}).sort_index()
st.subheader("Tenure vs Engagement")
st.line_chart(tenure_data["Average Engagement"], y_label="Average Engagement")
with st.expander("View tenure detail"):
    st.dataframe(tenure_data.round(2), use_container_width=True)

# -------------------- MANAGER ACTION --------------------
st.header("4. Manager Action Panel")
st.markdown('<div class="section-note">Identify departments and roles with higher proportions of employees below the selected engagement threshold.</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    low_dept = filtered.groupby("Department").LowEngagement.agg(["sum","count"])
    low_dept["Low Engagement %"] = low_dept["sum"] / low_dept["count"] * 100
    low_dept = low_dept.rename(columns={"sum":"Low Engagement Employees","count":"Total Employees"}).sort_values("Low Engagement %", ascending=False)
    st.subheader("Low Engagement by Department")
    st.dataframe(low_dept.round(2), use_container_width=True)
with c2:
    low_role = filtered.groupby("JobRole").LowEngagement.agg(["sum","count"])
    low_role["Low Engagement %"] = low_role["sum"] / low_role["count"] * 100
    low_role = low_role.rename(columns={"sum":"Low Engagement Employees","count":"Total Employees"}).sort_values("Low Engagement %", ascending=False)
    st.subheader("Low Engagement by Job Role")
    st.dataframe(low_role.round(2), use_container_width=True)

burn_role = filtered.groupby("JobRole").BurnoutRisk.agg(High_Burnout_Employees=lambda x:(x=="High").sum(), Total_Employees="count")
burn_role["High Burnout Risk %"] = burn_role.High_Burnout_Employees / burn_role.Total_Employees * 100
st.subheader("High Burnout Risk by Job Role")
st.dataframe(burn_role.sort_values("High Burnout Risk %", ascending=False).round(2), use_container_width=True)

# -------------------- PRIORITY --------------------
st.header("5. Priority Intervention Group")
st.markdown('<div class="insight"><b>Project-defined priority group:</b> Low Engagement + High Burnout Risk + Work-Life Balance ≤ 2. This is not a medical or psychological assessment.</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
c1.metric("Priority Employees", f"{priority_count:,}")
c2.metric("Priority %", f"{priority_pct:.2f}%")
c3.metric("Average Work-Life Balance", f"{wlb:.2f}")
priority_view = filtered[filtered.PriorityIntervention][["Age","Department","JobRole","OverTime","WorkLifeBalance","EngagementIndex","BurnoutRisk","YearsAtCompany","Attrition"]].sort_values(["EngagementIndex","WorkLifeBalance"])
if priority_view.empty:
    st.success("No employees currently meet all priority intervention conditions.")
else:
    st.dataframe(priority_view.round(2), use_container_width=True)

# -------------------- WORKLOAD --------------------
st.header("6. Workload & Stress Indicators")
st.markdown('<div class="section-note">Workload Stress Indicator is a project-defined score using overtime, travel frequency and commute distance.</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
c1.metric("Average Workload Stress", f"{filtered.WorkloadStressIndicator.mean():.2f}")
c2.metric("Maximum Stress Score", f"{filtered.WorkloadStressIndicator.max():.0f}")
st.bar_chart(filtered.WorkloadStressIndicator.value_counts().sort_index(), y_label="Employees")
travel = filtered.groupby("BusinessTravel").EngagementIndex.mean().reindex(["Non-Travel","Travel_Rarely","Travel_Frequently"])
st.subheader("Business Travel vs Engagement")
st.bar_chart(travel, y_label="Average Engagement")

# -------------------- WLB / COMMUTE --------------------
st.header("7. Work-Life Balance & Commute")
c1, c2 = st.columns(2)
with c1:
    st.subheader("Work-Life Balance Distribution")
    st.bar_chart(filtered.WorkLifeBalance.value_counts().sort_index(), y_label="Employees")
with c2:
    commute = filtered.copy()
    commute["CommuteGroup"] = commute.DistanceFromHome.apply(lambda x:"Short Commute" if x<10 else "Long Commute")
    commute_avg = commute.groupby("CommuteGroup").EngagementIndex.mean().reindex(["Short Commute","Long Commute"])
    st.subheader("Commute Group vs Engagement")
    st.bar_chart(commute_avg, y_label="Average Engagement")

# -------------------- STABILITY --------------------
st.header("8. Satisfaction Stability")
st.markdown('<div class="section-note">This project-defined 0–100 consistency score is not a validated psychometric scale.</div>', unsafe_allow_html=True)
st.metric("Average Satisfaction Stability", f"{filtered.SatisfactionStabilityScore.mean():.2f}%")
with st.expander("View satisfaction statistics"):
    st.dataframe(filtered[["JobSatisfaction","EnvironmentSatisfaction","RelationshipSatisfaction","JobInvolvement","SatisfactionStabilityScore"]].describe().round(2), use_container_width=True)

# -------------------- METHODOLOGY --------------------
st.header("Methodology & Definitions")
with st.expander("View metric definitions"):
    st.markdown(f"""
**Engagement Index:** Mean of Job Involvement, Job Satisfaction, Environment Satisfaction and Relationship Satisfaction.

**Burnout Risk:** High = Overtime Yes AND Work-Life Balance ≤ 2; Medium = either condition; Low = neither.

**Low Engagement:** Engagement Index < selected threshold (**{threshold:.2f}**).

**Priority Intervention:** Low Engagement + High Burnout Risk + Work-Life Balance ≤ 2.

**Workload Stress Indicator:** Overtime +2; frequent travel +2; rare travel +1; commute distance ≥10 +1.

**Satisfaction Stability Score:** Project-defined 0–100 consistency score based on the standard deviation of four satisfaction/involvement variables.
""")

st.markdown('<div class="footer">Palo Alto Networks Employee Engagement, Satisfaction & Burnout Diagnostic Analysis<br>Built for data-driven employee experience analysis and preventive HR decision support.</div>', unsafe_allow_html=True)
