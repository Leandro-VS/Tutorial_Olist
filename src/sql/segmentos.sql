/*
Com estas querys e subquerys podemos modelar as regras de negócio!
Criaremos então rótulos para identifcar os vendedores de acordo com suas metricas, que no caso são:
    valor de venda e frequencia de vendas
Tais rótulos são:
    SP -> Super produtivos
    P  -> Produtivos
    AF -> Alta frequencia 
    AV -> Alto valor
    BV -> Baixa frequencia e Baixo valor
*/
SELECT T1.*, 
    CASE WHEN pct_receita <= 0.5 AND pct_freq <= 0.5 THEN 'Baixo Valor'
        WHEN pct_receita > 0.5 AND pct_freq <= 0.5 THEN 'Alto Valor'
        WHEN pct_receita <= 0.5 AND pct_freq > 0.5 THEN 'Alta Freq'
        WHEN pct_receita < 0.9 OR pct_freq < 0.9 THEN 'Produtivo'
        ELSE 'Super Produtivo'
    END AS Segmento_valor_freq, 

    /*
    Precisamos agora saber do momento atual do vendedor
    */
    CASE WHEN qtd_dias_base <= 60 THEN 'Inicio' 
        WHEN dias_ultima_venda >= 300  THEN 'Retenção'
        ELSE 'Ativo'
    END AS Segmento_vida,

    '{date_end}' AS dt_sgmt


FROM(
    SELECT T1.*, 
        percent_rank() OVER(order by  receita_total ASC) AS pct_receita, 
        percent_rank() OVER(order by  qtde_pedidos ASC) AS pct_freq

    FROM(

        SELECT T2.seller_id, 
                SUM(T2.price) AS receita_total,
                COUNT(T1.order_id) AS qtde_pedidos,
                COUNT(T2.product_id) AS qtde_produtos,
                COUNT(DISTINCT T2.product_id) AS qtde_produtos_distinc,
                MIN(CAST(julianday('{date_end}') - julianday(T1.order_approved_at) AS INT)) AS dias_ultima_venda,
                MAX(CAST(julianday('{date_end}') - julianday(dt_inicio) AS INT)) AS qtd_dias_base

        FROM tb_orders as T1

        LEFT JOIN tb_order_items as T2
        ON T1.order_id = T2.order_id

        LEFT JOIN(
            SELECT T2.seller_id, 
                MIN(DATE(T1.order_approved_at)) AS dt_inicio
            FROM tb_orders AS T1

            LEFT JOIN tb_order_items AS T2
            ON T1.order_id = T2.order_id

            GROUP BY T2.seller_id
        ) AS T3
        ON T2.seller_id = T3.seller_id
        WHERE T1.order_approved_at BETWEEN '{date_init}' AND '{date_end}'

        GROUP BY T2.seller_id

    ) AS T1
) AS T1

WHERE seller_id IS NOT NULL
