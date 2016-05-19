# -*- coding: utf-8 -*-

import pandas as pd
import os
from ddf_utils.str import to_concept_id
from ddf_utils.index import create_index_file


source = '../source/gapdata001 v14.xlsx'
out_dir = '../../'


if __name__ == '__main__':

    # reading data
    data001 = pd.read_excel(source, sheetname='Data & metadata')

    # Entity
    area = data001['Area'].unique()
    area_id = list(map(to_concept_id, area))

    ent = pd.DataFrame([], columns=['area', 'name'])

    ent['area'] = area_id
    ent['name'] = area
    path = os.path.join(out_dir, 'ddf--entities--area.csv')
    ent.to_csv(path, index=False)

    # datapoint
    data001_dp = data001[['Area', 'Year', 'GDP per capita - with interpolations']].copy()

    dp_id = to_concept_id('GDP per capita by purchasing power parities')

    data001_dp.columns = ['area', 'year', dp_id]

    data001_dp['area'] = data001_dp['area'].map(to_concept_id)
    path = os.path.join(out_dir, 'ddf--datapoints--{}--by--area--year.csv'.format(dp_id))
    data001_dp.dropna().sort_values(by=['area', 'year']).to_csv(path, index=False)

    # concepts
    conc = [dp_id, 'area', 'year', 'name']
    cdf = pd.DataFrame([], columns=['concept', 'name', 'concept_type'])
    cdf['concept'] = conc
    cdf['name'] = ['GDP per capita by purchasing power parities', 'Area', 'Year', 'Name']
    cdf['concept_type'] = ['measure', 'entity_domain', 'time', 'string']

    path = os.path.join(out_dir, 'ddf--concepts.csv')
    cdf.to_csv(path, index=False)

    # index
    create_index_file(out_dir)

    print('Done.')
