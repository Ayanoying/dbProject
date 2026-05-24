-- Request 1 : top 10 users with the most points
SELECT id_user, username, profile_points
FROM users
ORDER BY profile_points DESC
LIMIT 10;

-- Request 2 : users who have published summaries for at least 3 different courses
SELECT u.id_user, u.username
FROM users u
JOIN summaries s ON u.id_user = s.user_id
GROUP BY u.id_user, u.username
HAVING COUNT(DISTINCT s.course_id) >= 3;

-- Request 3 : course with the most summaries published
SELECT c.id_course, c.course_title, COUNT(s.id_summary) AS nb_summaries
FROM courses c
JOIN summaries s ON c.id_course = s.course_id
GROUP BY c.id_course, c.course_title
ORDER BY nb_summaries DESC
LIMIT 1;

-- Request 4 : best average summaries note for each course
SELECT s1.id_summary, s1.title, s1.course_id, s1.average_rating
FROM summaries s1
WHERE s1.average_rating = (
    SELECT MAX(s2.average_rating)
    FROM summaries s2
    WHERE s2.course_id = s1.course_id
);

-- Request 5 : users who have not published any summary
SELECT u.id_user, u.username
FROM users u
LEFT JOIN summaries s ON u.id_user = s.user_id
WHERE s.id_summary IS NULL;

-- Request 6 : most purchased cosmetic item
SELECT c.id_item, c.name, COUNT(*) AS purchases_count
FROM cosmetic_items c
JOIN transactions t ON c.id_item = t.item_id
WHERE t.transaction_type = 'purchase_item'
GROUP BY c.id_item, c.name
ORDER BY purchases_count DESC
LIMIT 1;

-- Request 7 : users who have spent more points than they currently have
SELECT u.id_user, u.username, u.profile_points, SUM(ABS(t.amount)) AS total_spent
FROM users u
JOIN transactions t ON u.id_user = t.user_id
WHERE t.transaction_type = 'purchase_item'
GROUP BY u.id_user, u.username, u.profile_points
HAVING SUM(ABS(t.amount)) > u.profile_points;

-- Request 8 : average number of summaries published per user
SELECT AVG(nb_summaries) AS average_summaries
FROM (
    SELECT COUNT(*) AS nb_summaries
    FROM summaries
    GROUP BY user_id
) AS stats;
