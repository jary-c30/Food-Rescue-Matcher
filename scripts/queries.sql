-- Practice queries. Run one at a time, or the whole file:
--   docker compose exec -T db psql -U food_rescue < scripts/queries.sql
-- Sample data comes from: python -m scripts.seed

-- 1. Filtering + ordering: available donations expiring within 6 hours, soonest first.
SELECT id, description, quantity_lbs, expires_at
FROM donations
WHERE status = 'available'
  AND expires_at < now() + interval '6 hours'
ORDER BY expires_at;

-- 2. JOIN: each donation with the donor who posted it.
SELECT d.name AS donor, n.description, n.quantity_lbs, n.status
FROM donations n
JOIN donors d ON d.id = n.donor_id
ORDER BY d.name, n.expires_at;

-- 3. GROUP BY: how many donations and how many pounds in each status.
SELECT status, count(*) AS donations, sum(quantity_lbs) AS total_lbs
FROM donations
GROUP BY status
ORDER BY total_lbs DESC;

-- 4. LEFT JOIN: donors who have never posted a donation.
SELECT d.name
FROM donors d
LEFT JOIN donations n ON n.donor_id = d.id
WHERE n.id IS NULL;

-- 5. Distance math: recipients nearest to the first donor, in miles (haversine formula).
--    3959 is Earth's radius in miles. This is the same math the routing code will use later.
SELECT r.name,
       round((2 * 3959 * asin(sqrt(
           power(sin(radians(r.latitude - d.latitude) / 2), 2) +
           cos(radians(d.latitude)) * cos(radians(r.latitude)) *
           power(sin(radians(r.longitude - d.longitude) / 2), 2)
       )))::numeric, 2) AS miles_away
FROM donors d
CROSS JOIN recipients r
WHERE d.id = (SELECT min(id) FROM donors)
ORDER BY miles_away;

-- 6. Subquery + HAVING: donors whose total available food is over 50 lbs.
SELECT d.name, sum(n.quantity_lbs) AS available_lbs
FROM donors d
JOIN donations n ON n.donor_id = d.id
WHERE n.status = 'available'
GROUP BY d.name
HAVING sum(n.quantity_lbs) > 50;
