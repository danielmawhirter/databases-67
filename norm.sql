drop table if exists dond_contestants cascade;
create table dond_contestants as select distinct id, broadcast_date, name, education, gender, age, stop_round, amount_won from dond;
alter table dond_contestants add primary key (id);

drop table if exists dond_rounds cascade;
CREATE TABLE dond_rounds as select id, round, deal_or_no_deal, "bank-offer", "0.01", "1", "5", "10", "25", "50", "75", "100", "200", "300", "400", "500", "750", "1,000", "5,000", "10,000", "25,000", "50,000", "75,000", "100,000", "200,000", "300,000", "400,000", "500,000", "750,000", "1,000,000", avg_money, optimism from dond;
alter table dond_rounds add primary key (id, round);
alter table dond_rounds add foreign key (id) references dond_contestants (id);

delete from weather where tmin=-9999;
delete from weather where tmax=-9999;
delete from weather where prcp=-9999;
update weather set mdpr=NULL where mdpr=-9999;
update weather set mdsf=NULL where mdsf=-9999;
update weather set dapr=NULL where dapr=-9999;
update weather set awnd=NULL where awnd=-9999;
update weather set snwd=NULL where snwd=-9999;
update weather set snow=NULL where snow=-9999;
update weather set tobs=NULL where tobs=-9999;
