CREATE SCHEMA visa;

--make sure to add PostGis extension to visa

CREATE TABLE visa.nyc_purchases(
	p_ID serial PRIMARY KEY,
	c_ID bigint NOT NULL,
	s_ID varchar(100) NOT NULL,
	s_category varchar(100) NOT NULL,
	s_coords geography(POINT,4326) NOT NULL,
	price decimal(10,2) NOT NULL,
	p_time timestamp NOT NULL
);

--DROP TABLE visa.nyc_purchases CASCADE;

CREATE OR REPLACE VIEW visa.purchases_last5m AS(
	SELECT p.s_coords
	FROM visa.nyc_purchases p
	WHERE p.p_time >= current_timestamp - interval '5 minutes'
	ORDER BY p.p_time DESC
);

CREATE OR REPLACE VIEW visa.purchases_last10m AS(
	SELECT p.s_coords
	FROM visa.nyc_purchases p
	WHERE p.p_time >= current_timestamp - interval '10 minutes'
	ORDER BY p.p_time DESC
);

CREATE OR REPLACE VIEW visa.purchases_last30m AS(
	SELECT p.s_coords
	FROM visa.nyc_purchases p
	WHERE p.p_time >= current_timestamp - interval '30 minutes'
	ORDER BY p.p_time DESC
);

--SELECT * FROM visa.purchases_last30m;
--SELECT * FROM visa.nyc_purchases;
--DELETE FROM visa.nyc_purchases;

--Query 1
SELECT count(p.*) AS quanity, SUM(p.price) AS amount, p.s_category
	FROM visa.nyc_purchases p
	WHERE p.p_time >= current_timestamp - interval '15 minutes'
	GROUP BY s_category;

--Query 2
SELECT p.s_category
	FROM visa.nyc_purchases p
	WHERE
		p.p_time >= current_timestamp - interval '30 minutes'
	AND
		ST_DWithin(p.s_coords, (
			SELECT geom
			FROM visa.nyc_subway_stations s
			WHERE s.name = 'Broad St'), 500)
	AND p.price >= ALL (
		SELECT price
		FROM visa.nyc_purchases p1
		WHERE p1.p_time >= current_timestamp - interval '30 minutes'
		AND ST_DWithin(p1.s_coords, (
			SELECT geom
			FROM visa.nyc_subway_stations s
			WHERE s.name = 'Broad St'), 500));

--Query 3
SELECT count(p)/(ST_Area(Geography(ST_Transform(n.geom,4326)))/1000000.0) as purchases_for_km
	FROM visa.nyc_neighborhoods n
	JOIN visa.nyc_purchases p ON ST_Intersects(p.s_coords, Geography(ST_Transform(n.geom,4326)))
	WHERE p.p_time >= current_timestamp - interval '15 minutes'
	GROUP BY n.id, n.geom;
