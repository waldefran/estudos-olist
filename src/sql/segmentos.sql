
SELECT T1.*,
       CASE WHEN (PctReceita <= 0.5) AND (PctFrequencia<=0.5) THEN 'BaixoVF'
            WHEN (PctReceita > 0.5) AND (PctFrequencia <= 0.5) THEN 'AltoValor'
            WHEN (PctReceita <= 0.5) AND (PctFrequencia > 0.5) THEN 'AltaFrequencia'
            WHEN (PctReceita < 0.9) OR (PctFrequencia < 0.9) THEN 'Produtivo'
       ELSE 'SuperProdutivo'
       END AS SegValorFreq,

       CASE WHEN QtdDiasBase <=60 THEN 'Inicio'
            WHEN QtdDiaUltimaVenda >=300 THEN 'Rentencao'
            ELSE 'Ativo'
       END AS SegVida,

       '{date_end}' as DtSegmento

FROM(   
    SELECT R1.*,
        PERCENT_RANK() OVER (ORDER BY ReceitaTotal) as PctReceita,
        PERCENT_RANK() OVER (ORDER BY QtdPedidos) as PctFrequencia
    FROM(

        SELECT t2.seller_id,
            SUM(T2.price) AS ReceitaTotal,
            COUNT(DISTINCT(T1.order_id)) AS QtdPedidos,
            COUNT(T2.product_id) AS QtdProdutos,
            COUNT(DISTINCT(T2.product_id)) AS DistProduto,
            MIN( CAST(JULIANDAY('{date_end}') - JULIANDAY(T1.order_approved_at) AS INT)) AS QtdDiaUltimaVenda,
            MAX( CAST(JULIANDAY('{date_end}') - JULIANDAY(DtInicio) AS INT) ) AS QtdDiasBase

        FROM orders AS T1

        LEFT JOIN order_items AS T2
        ON T1.order_id = T2.order_id

        LEFT JOIN (
            SELECT T2.seller_id,
                MIN( DATE(T1.order_approved_at)) as DtInicio
            FROM orders AS T1
            LEFT JOIN order_items AS T2
            ON T1.order_id = T2.order_id
            GROUP BY T2.seller_id
        ) AS T3
        ON T2.seller_id = T3.seller_id

        WHERE T1.order_approved_at BETWEEN '{date_init}' AND '{date_end}'

        GROUP BY T2.seller_id
    ) AS R1
) AS T1

WHERE T1.seller_id