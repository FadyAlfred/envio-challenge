from django.db import models, connection

from core.utils import dict_fetchall


class ReadingManager(models.Manager):
    def aggregate_readings(self, start_date, end_date, interval, customer_id, device_id):
        customer_filter = f'AND customer_id={customer_id}' if customer_id else ''
        device_filter = f'AND device_id={device_id}' if device_id else ''
        start_date_filter = f'AND timestamp>=\'{start_date}\'' if start_date else ''
        end_date_filter = f'AND timestamp<=\'{end_date}\'' if end_date else ''

        cursor = connection.cursor()
        cursor.execute(
            f'''
            SELECT * FROM  (
                SELECT customer_id, device_id, 
                       generate_series(min(timestamp), max(timestamp), interval '{interval} min') AS timestamp 
                FROM core_reading 
                WHERE customer_id IS NOT NULL 
                AND device_id IS NOT NULL
                {customer_filter}
                {device_filter} 
                {start_date_filter} 
                {end_date_filter} 
                GROUP BY customer_id, device_id
            ) grid 
            CROSS JOIN LATERAL(
                SELECT ROUND(AVG(value)::numeric, 2) AS value_avg 
                FROM core_reading 
                WHERE timestamp >= grid.timestamp 
                AND timestamp <  grid.timestamp + interval '{interval} min'                            
            ) avg
            WHERE value_avg IS NOT NULL;'''
        )
        records = dict_fetchall(cursor)
        return records
