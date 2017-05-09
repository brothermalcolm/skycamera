DROP PROCEDURE IF EXISTS sp_join_skyghi;

DELIMITER //
CREATE PROCEDURE sp_join_skyghi(ImageID int)
BEGIN
SELECT *
FROM SKY402 c
JOIN SIN402 s
ON FROM_UNIXTIME(c.ET) = s.Tm
WHERE ET = ImageID
ORDER BY c.ET DESC;
END  // 
DELIMITER ;
