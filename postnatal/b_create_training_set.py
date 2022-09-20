"""Training set
"""

import numpy as np
import pandas as pd
import plotly.express as px

df = pd.read_csv("/home/INT/pron.a/code/article_synthseg/data/postnatal/dhcp.csv")
df["scan_age"] = pd.to_timedelta(df["scan_age"])
df["scan_age_weeks"] = df["scan_age"].dt.days / 7
df["birth_age"] = pd.to_timedelta(df["birth_age"])
df["birth_age_weeks"] = df["birth_age"].dt.days / 7
print(df.dtypes)
# sampling set : non longitudinal scans without any findings that has all
# necessary input and derived MRI volumes
sampling_set = df.loc[(df["has_all_mri"] == True) ].copy()
sampling_set = sampling_set[
    [
        "participant_id",
        "gender",
        "birth_weight",
        "birth_age_weeks",
        "scan_age_weeks",
        "scan_head_circumference",
        "radiology_score",
        "sedation",
        "t2",
        "drawem9",
        "drawem87",
        "ribbon",
        "has_all_mri",
    ]
]

#print("unique subjects",len(sampling_set['participant_id'].unique()))

sex_statistics = sampling_set.drop_duplicates('participant_id')
#print("sex statistics", sex_statistics['gender'].describe())

sampling_set.sort_values(by="scan_age_weeks", inplace=True)
sampling_set.reset_index(inplace=True, drop=True)
print("Number of scans available for sampling", sampling_set.shape)
sampling_set.to_csv(
    "/home/INT/pron.a/code/article_synthseg/data/postnatal\
/dhcp-sampling_set.csv",
    index=False,
)
#print(sampling_set["scan_age_weeks"].describe())
#print(sampling_set["gender"].describe())
values, counts = np.unique(sampling_set['radiology_score'].to_numpy(),
                           return_counts=True)
print(values, counts)

# training_set = sampling_set.iloc[:100].copy()
# print(training_set["scan_age_weeks"].describe())
# print(training_set["gender"].describe())
# training_set.to_csv(
#     "/home/INT/pron.a/code/article_synthseg/data/postnatal\
# /dhcp-training_set.csv",
#     index=False,
# )

# training set age coverage
fig = px.histogram(
    sampling_set,
    x="scan_age_weeks",
    color="gender",
    barmode="group",
    labels={"scan_age_weeks": "Post Menstrual " "Age (Weeks)"},
)
fig.update_layout(
    xaxis=dict(
        tickmode="array",
        tickvals=0.5 + np.arange(29, 41, 1),
        ticktext=np.arange(29, 41, 1),
    )
)
fig.write_image(
    "/home/INT/pron.a/code/article_synthseg/figures"
    "/dhcp_sampling_set_age_coverage.svg"
)
