import pandas as pd
from pathlib import Path

PROJECT_ROOT= Path.cwd()
data_path_origen = Path(PROJECT_ROOT,"data/raw/Coffee_Shop_Sales.xlsx")
data_path_destino = Path(PROJECT_ROOT,"data/processed/Coffee_Shop_Sales.csv")
data=pd.read_excel(data_path_origen,dtype=str)
data['transaction_date'] = pd.to_datetime(data['transaction_date'], format='%Y-%m-%d %H:%M:%S').dt.date
data['transaction_timing'] = pd.to_datetime(
    data['transaction_date'].astype(str) + ' ' + data['transaction_time'].astype(str),
    errors='coerce'
)
data['transaction_qty']=data['transaction_qty'].astype(int)
data['store_id']=data['store_id'].astype(int)
data['product_id']=data['product_id'].astype(int)
data['unit_price']=data['unit_price'].astype(float)
data['total_venta']=data['transaction_qty']*data['unit_price']
data.rename(columns={'transaction_id':'transaction_id','transaction_date':'fecha_transaccion','transaction_time':'hora_transaccion',\
                     'transaction_qty':'cantidad_transaccion','store_id':'id_tienda','store_location':'ubicacion_tienda',\
                     'product_id':'id_producto','unit_price':'precio_unitario','product_category':'categoria_producto',
                     'product_type':'tipo_producto','transaction_timing':'tiempo_transaccion','total_venta':'total_venta'}, inplace=True)

data.to_csv(data_path_destino,index=False)
