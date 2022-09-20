import os
import pandas as pd
dir_test = '/home/INT/pron.a/data/romain/fetal/prediction_post_fine_tuning'
df = pd.read_csv('/data/fetal/extract_prediction_set_fine_tuning.csv')
for index, row in df.iterrows():

    df['path'] = os.path.join(dir_test, df['marsfet_subject_id'] + '_' + df[
    'marsfet_session_id'] + '_' + 'haste_t2_masked.nii.gz')
    df['to_keep'] = os.path.exists(df['path'])
