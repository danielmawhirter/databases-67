
/*selecting closest weather station for date (califonia loc)*/
/*drop table if exists tb_dist;
create table tb_dist as (select distinct station, |/((34.0097051-latitude)^2 + (-118.321998-longitude)^2) dist from weather where date='2005-12-19');
select * from tb_dist where dist=(select min(dist) from tb_dist);
drop table tb_dist;*/

/*separated version of following query*/
/*create table d_to_sta as (select broadcast_date date, (case when (broadcast_date < '2006-01-01') then 'GHCND:USW00093134' else 'GHCND:USW00054767' end ) station from dond_contestants);

select distinct id, broadcast_date, d_to_sta.station, weather.tmax, weather.tmin, weather.prcp from dond_contestants, weather, d_to_sta where dond_contestants.broadcast_date=d_to_sta.date and weather.station=d_to_sta.station and dond_contestants.broadcast_date=weather.date order by id;*/

select distinct id, broadcast_date, d_to_sta.station, weather.tmax, weather.tmin, weather.prcp from dond_contestants, weather, (select broadcast_date date, (case when (broadcast_date < '2006-01-01') then 'GHCND:USW00093134' else 'GHCND:USW00054767' end ) station from dond_contestants) as d_to_sta where dond_contestants.broadcast_date=d_to_sta.date and weather.station=d_to_sta.station and dond_contestants.broadcast_date=weather.date order by id;


