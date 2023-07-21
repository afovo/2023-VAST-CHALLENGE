import pandas as pd
import json

v1=json.load(open('../../mc1_vis_system/public/MC1.json'))
nodes_df=pd.DataFrame(v1['nodes'])
links_df=pd.DataFrame(v1['links'])

merged_info=links_df.merge(nodes_df,how='left',left_on='source',right_on='id')
merged_info=merged_info.merge(nodes_df,how='left',left_on='target',right_on='id')
merged_info.drop(['id_x','id_y','weightlcoat','dataset','dataset_y'],axis=1,inplace=True)
merged_info.rename(columns={'type_x':'link_type','type_y':'source_type','country_x':'source_country','country':'source_country',
                            'type':'target_type','country_y':'target_country'},inplace=True)
merged_info.head()