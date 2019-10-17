with alert_buffers as (
  select 
    id, 
    st_buffer(geom::geography, radius) as geom
    expires_at,
    reflectivity_limit,
    temperature_limit,
    relative_humidity_limit,
    wind_limit,
    precipitation_limit
  from alert
  where expires_at > timezone('utc', now()) 
),

data as (
  select 
    id, 
    st_band(rast, :band) as rast 
  from weather_raster
),

raster_stats as (
  select
    a.id as alert_id,
    d.id as raster_id,
    st_summarystats(st_union(st_clip(d.rast, a.geom::geometry, true))) as stats
  from alert_buffers as a, data as d
  where st_intersects(d.rast, a.geom::geometry)
  group by alert_id, raster_id
)


select
  alert_id,
  raster_id,
  (stats).max,
  (stats).mean,
  (stats).min
from raster_stats
