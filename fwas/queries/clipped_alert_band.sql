with alert_buffers as (
  select 
    id, 
    st_buffer(geom::geography, radius) as geom 
  from alert
),

data as (
  select 
    id, 
    st_band(rast, :band) as rast 
  from weather_raster
)


select
    a.id as alert_id,
    d.id as raster_id,
    st_clip(d.rast, a.geom::geometry) as rast
from alert_buffers as a, data as d
where st_intersects(d.rast, a.geom::geometry)
