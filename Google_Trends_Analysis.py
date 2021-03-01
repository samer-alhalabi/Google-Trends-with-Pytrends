#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# pip install pytrends


# In[ ]:


# pip install altair


# In[20]:


import pandas as pd
from pytrends.request import TrendReq
import altair as alt
import plotly.graph_objects as go
import plotly.express as px


pytrends = TrendReq(hl='en-US', tz=360)

#1 keyword = input('Type the trend you are interested in seeing here: ')

#2 timeframe
# trends for last 5 years : timeframe= 'today 5-y', trends for the last 7 days timeframe= 'now 7-d'

#3 location
# example for Ohio state geo = 'GB-US-OH'


# In[2]:


keyword = input('Type the trend you are interested in seeing here: ')


# In[15]:


# case: keyword= sports, timeframe= last 7 days, geo= Ohio
pytrends.build_payload([keyword], cat=0, timeframe='now 7-d', geo='US-OH', gprop=''


# In[14]:


top_queries = pytrends.related_queries()[keyword]['top']


# In[7]:


top_queries


# #### Related queries

# In[8]:


import plotly.express as px

fig = px.bar(top_queries, 
      x='query',
      y='value')
fig.show()


# #### Interest over Time

# In[9]:


int_over_time = pytrends.interest_over_time().reset_index()
int_over_time.rename(columns={keyword : 'search_volume'}, inplace=True)


# In[10]:


int_over_time_plot= alt.Chart(int_over_time).encode(x='date', y='search_volume').mark_area(line=True).interactive().properties(width=700)


# In[11]:


int_over_time_plot


# #### Geographical Interest

# In[16]:


regions = pytrends.interest_by_region(resolution='COUNTRY', inc_geo_code=True)
regions.rename(columns={keyword : 'search_volume'}, inplace=True)
regions.reset_index()


# In[17]:


bar = px.bar(regions.reset_index().sort_values(by='search_volume', ascending=False)[:20],
      x='geoName',
      y='search_volume')
bar.show()


# #### World Map

# In[26]:


# world trend for Pizza 

pytrends = TrendReq(hl='en-US', tz=360)

pytrends.build_payload(['pizza'], cat=0)

regions = pytrends.interest_by_region(resolution='COUNTRY', inc_geo_code=True)
regions.rename(columns={'pizza' : 'search_volume'}, inplace=True)
regions.reset_index()


# In[27]:


bar = px.bar(regions.reset_index().sort_values(by='search_volume', ascending=False)[:20],
      x='geoName',
      y='search_volume')
bar.show()


# In[59]:


# Get geo code

geo_code= px.data.gapminder().query("year==2007")


# In[62]:


geo_code[['country', 'iso_alpha']]


# In[72]:


df = regions.reset_index()


# In[73]:


# merge with out dataframe

df = df.merge(geo_code, how='left', left_on='geoName', right_on='country')


# In[74]:


df = df[['country', 'iso_alpha', 'search_volume']]


# In[89]:


# remove nulls

df = df[df.country.isnull() == False]


# In[103]:


# create map

import plotly.express as px

fig = px.choropleth(df, locations=df.iso_alpha, title= "Global Trend for Keyword = Pizza",
                    color=df.search_volume,
                    hover_name="country",
                    color_continuous_scale=px.colors.sequential.Blues)
fig.show()


# ##### US Map

# In[37]:


# world trend for Pizza 

pytrends = TrendReq(hl='en-US', tz=360)

pytrends.build_payload(['pizza'], cat=0, geo="US")

regions = pytrends.interest_by_region(resolution='COUNTRY', inc_geo_code=True)
regions.rename(columns={'pizza' : 'search_volume'}, inplace=True)
regions.reset_index(inplace=True)
regions


# In[38]:


regions['geoCode'] = regions.geoCode.str[3:]


# In[39]:


regions


# In[49]:


df = regions

fig = px.choropleth(df, locations="geoCode",
                    title= "US Trend for Keyword = Pizza",
                    locationmode="USA-states", 
                    color="search_volume", 
                    scope="usa",
                    hover_name="geoName",
                    color_continuous_scale=px.colors.sequential.Blues)
fig.show()


# In[ ]:




