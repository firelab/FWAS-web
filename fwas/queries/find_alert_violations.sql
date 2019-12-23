with alert_buffers as (
  select 
    id, 
    st_buffer(geom::geography, radius) as geom
  from alert
  where expires_at is null 
    or expires_at > timezone('utc', now()) 
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

    a.temperature_limit,
    (r.temperature).max as temperature_max,
    ((r.temperature).max >= a.temperature_limit) as temperature_violated,
    case when ((r.temperature).max >= a.temperature_limit) then r.forecast_time end as temperature_violated_at,

    a.relative_humidity_limit,
    (r.relative_humidity).max as relative_humidity_max,
    ((r.relative_humidity).max >= a.relative_humidity_limit) as relative_humidity_violated,
    case when ((r.relative_humidity).max >= a.relative_humidity_limit) then r.forecast_time end as relative_humidity_violated_at,

    a.wind_limit,
    (r.wind).max as wind_max,
    ((r.wind).max >= a.wind_limit) as wind_violated,
    case when ((r.wind).max >= a.wind_limit) then r.forecast_time end as wind_violated_at,

    a.precipitation_limit,
    (r.precipitation).max as precipitation_max,
    ((r.precipitation).max >= a.precipitation_limit) as precipitation_violated,
    case when ((r.precipitation).max >= a.precipitation_limit) then r.forecast_time end as precipitation_violated_at
  from raster_stats as r
  join alert as a
    on a.id = r.alert_id
  join public.user as u
    on a.user_id = u.id
  order by user_id, r.alert_id, r.forecast_time asc
)


-- Condense each violation into a single view for each
-- user, alert, and forecasted_at combinitation. 
-- Each resulting record should map 1:1 to notifications
-- that need to be sent.
select
  user_id,
  alert_id,
  bool_or(temperature_violated) as temperature_violated,
  min(temperature_violated_at) as temperature_violated_at,
  max(temperature_max) as temperature_value,

  bool_or(relative_humidity_violated) as relative_humidity_violated,
  min(relative_humidity_violated_at) as relative_humidity_violated_at,
  max(relative_humidity_max) as relative_humidity_value,

  bool_or(wind_violated) as wind_violated,
  min(wind_violated_at) as wind_violated_at,
  max(wind_max) as wind_value,
  
  bool_or(precipitation_violated) as precipitation_violated,
  min(precipitation_violated_at) as precipitation_violated_at,
  max(precipitation_max) as precipitation_value
from weather_data
where temperature_violated
  or relative_humidity_violated
  or wind_violated
  or precipitation_violated
group by 
  user_id,
  alert_id
