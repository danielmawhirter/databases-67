CREATE TABLE jojsmith.optimism(id text, FOREIGN KEY (id) REFERENCES jojsmith.dond_contestants, optimism_rating int);
INSERT INTO jojsmith.optimism(id, optimism_rating) (SELECT id, COUNT(*) FROM jojsmith.dond_rounds WHERE deal_or_no_deal='ND' AND optimism IS TRUE GROUP BY id);

CREATE TABLE jojsmith.dond_weather as (
select distinct id, broadcast_date, d_to_sta.station, weather.tmax, weather.tmin, weather.prcp 
from dond_contestants, weather, (
  select broadcast_date date, (
    case when (broadcast_date < '2006-01-01') 
      then 'GHCND:USW00093134' 
      else 'GHCND:USW00054767' 
    end 
  ) station from dond_contestants
) as d_to_sta
where dond_contestants.broadcast_date=d_to_sta.date 
  and weather.station=d_to_sta.station 
  and dond_contestants.broadcast_date=weather.date 
order by id);
SELECT * FROM dond_weather LEFT JOIN optimism ON dond_weather.id=optimism.id;
