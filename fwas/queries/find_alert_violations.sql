with alert_buffers as (
  select 
    id, 
    st_buffer(geom::geography, radius) as geom
  from alert
  where created_at + make_interval(hours => expires_in_hours::int) > timezone('utc', now()) 
),

data as (
  select 
    id, 
    forecasted_at,
    forecast_time,
    rast,
    st_band(rast, 1) as reflectivity,
    st_band(rast, 2) as lightening,
    st_band(rast, 4) as temperature,
    st_band(rast, 5) as relative_humidity,
    st_band(rast, 6) as wind,
    st_band(rast, 7) as precipitation
  from weather_raster
),

raster_stats as (
  select
    a.id as alert_id,
    d.id as raster_id,
    d.forecasted_at,
    d.forecast_time,
    st_summarystats(st_union(st_clip(d.reflectivity, a.geom::geometry, true))) as reflectivity,
    st_summarystats(st_union(st_clip(d.lightening, a.geom::geometry, true))) as lightening,
    st_summarystats(st_union(st_clip(d.temperature, a.geom::geometry, true))) as temperature,
    st_summarystats(st_union(st_clip(d.relative_humidity, a.geom::geometry, true))) as relative_humidity,
    st_summarystats(st_union(st_clip(d.wind, a.geom::geometry, true))) as wind,
    st_summarystats(st_union(st_clip(d.precipitation, a.geom::geometry, true))) as precipitation
  from alert_buffers as a, data as d
  where st_intersects(d.rast, a.geom::geometry)
  group by alert_id, raster_id, d.forecasted_at, d.forecast_time
),

weather_data as (
  select
    u.id as user_id,
    r.alert_id,
    r.raster_id,
    r.forecasted_at,
    r.forecast_time,

    a.reflectivity_limit,
    (r.reflectivity).max as reflectivity_max,
    (r.reflectivity).mean as reflectivity_mean,
    (r.reflectivity).min as reflectivity_min,
    ((r.reflectivity).max >= a.reflectivity_limit) as reflectivity_violated,

    a.temperature_limit,
    (r.temperature).max as temperature_max,
    (r.temperature).mean as temperature_mean,
    (r.temperature).min as temperature_min,
    ((r.temperature).max >= a.temperature_limit) as temperature_violated,

    a.relative_humidity_limit,
    (r.relative_humidity).max as relative_humidity_max,
    (r.relative_humidity).mean as relative_humidity_mean,
    (r.relative_humidity).min as relative_humidity_min,
    ((r.relative_humidity).max >= a.relative_humidity_limit) as relative_humidity_violated,

    a.wind_limit,
    (r.wind).max as wind_max,
    (r.wind).mean as wind_mean,
    (r.wind).min as wind_min,
    ((r.wind).max >= a.wind_limit) as wind_violated,

    a.precipitation_limit,
    (r.precipitation).max as precipitation_max,
    (r.precipitation).mean as precipitation_mean,
    (r.precipitation).min as precipitation_min,
    ((r.precipitation).max >= a.precipitation_limit) as precipitation_violated
  from raster_stats as r
  join alert as a
    on a.id = r.alert_id
  join public.user as u
    on a.user_id = u.id
  order by user_id, r.alert_id, r.forecast_time asc
)

select
  *
from weather_data
where reflectivity_violated
  or temperature_violated
  or relative_humidity_violated
  or wind_violated
  or precipitation_violated
