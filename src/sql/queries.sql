
SELECT dt_sgmt, COUNT(DISTINCT seller_id) 
FROM tb_seller_sgmt
GROUP BY dt_sgmt


/*Vendedor que mais aparece */
/*
SELECT *
FROM tb_seller_sgmt
WHERE seller_id = 'fffd5413c0700ac820c7069d66d98c89'
ORDER BY dt_sgmt
*/