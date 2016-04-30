drop table if exists tb_dist;
/*california*/
create table tb_dist as (select distinct station, |/((34.0097051-latitude)^2 + (-118.321998-longitude)^2) dist from weather where date='2005-12-19');
select * from tb_dist where dist=(select min(dist) from tb_dist);
drop table tb_dist;
