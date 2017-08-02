
CREATE OR REPLACE FUNCTION cierre_factura(
    d1 text,
    d2 text)
  RETURNS json AS
$BODY$
declare
	id_factura json;
	id_cerradas json;
	id_canceladas json;
    total_f record;
begin
	select sum(valor) as valor, sum(comision) as comosion
    		from operacion_orden
            		where cast(fin as date) >= cast(d1 as date) and cast(fin as date) <= cast(d2 as date) and
                		  activo=true and cerrada=true and pago=true into total_f;
    id_factura := (SELECT COALESCE(array_to_json(array_agg(row_to_json(p2))), '[]') from (
        	select  o.id,v.placa
        		,cast(entrada as date)||' '||case when extract(hour from entrada) < 10 then '0' else '' end||extract(hour from entrada)
				 ||'-'||case when extract(minute from entrada) < 10 then '0' else '' end||extract(minute from entrada)
               	 ||'-'||case when trunc(extract(second from entrada)) < 10 then '0' else '' end||trunc(extract(second from entrada)) as entrada
        		,cast(fin as date)||' '||case when extract(hour from fin) < 10 then '0' else '' end||extract(hour from fin)
				 ||'-'||case when extract(minute from fin) < 10 then '0' else '' end||extract(minute from fin)
               	 ||'-'||case when trunc(extract(second from fin)) < 10 then '0' else '' end||trunc(extract(second from fin)) as fin
        	    ,o.valor,o.comision
    		from operacion_orden as o
        	inner join cliente_vehiculo as v on(
            		o.vehiculo_id=v.id and cast(o.fin as date) >= cast(d1 as date) and cast(o.fin as date) <= cast(d2 as date) and
                		  o.activo=true and o.cerrada=true and o.pago=true and o.cancelada=false) order by id desc
        ) p2);
    id_cerradas := (SELECT COALESCE(array_to_json(array_agg(row_to_json(p3))), '[]') from (
        	select  o.id,v.placa
        		,cast(entrada as date)||' '||case when extract(hour from entrada) < 10 then '0' else '' end||extract(hour from entrada)
				 ||'-'||case when extract(minute from entrada) < 10 then '0' else '' end||extract(minute from entrada)
               	 ||'-'||case when trunc(extract(second from entrada)) < 10 then '0' else '' end||trunc(extract(second from entrada)) as entrada
        		,cast(fin as date)||' '||case when extract(hour from fin) < 10 then '0' else '' end||extract(hour from fin)
				 ||'-'||case when extract(minute from fin) < 10 then '0' else '' end||extract(minute from fin)
               	 ||'-'||case when trunc(extract(second from fin)) < 10 then '0' else '' end||trunc(extract(second from fin)) as fin
        	    ,o.valor,o.comision
    		from operacion_orden as o
        	inner join cliente_vehiculo as v on(
            		o.vehiculo_id=v.id and cast(o.fin as date) >= cast(d1 as date) and cast(o.fin as date) <= cast(d2 as date) and
                		  o.activo=true and o.cerrada=true and o.pago=false and o.cancelada=false) order by id desc
        ) p3);
     id_canceladas := (SELECT COALESCE(array_to_json(array_agg(row_to_json(p4))), '[]') from (
        	select  o.id,v.placa
        		,cast(entrada as date)||' '||case when extract(hour from entrada) < 10 then '0' else '' end||extract(hour from entrada)
				 ||'-'||case when extract(minute from entrada) < 10 then '0' else '' end||extract(minute from entrada)
               	 ||'-'||case when trunc(extract(second from entrada)) < 10 then '0' else '' end||trunc(extract(second from entrada)) as entrada
        		,cast(fin as date)||' '||case when extract(hour from fin) < 10 then '0' else '' end||extract(hour from fin)
				 ||'-'||case when extract(minute from fin) < 10 then '0' else '' end||extract(minute from fin)
               	 ||'-'||case when trunc(extract(second from fin)) < 10 then '0' else '' end||trunc(extract(second from fin)) as fin
        	    ,o.valor,o.comision
    		from operacion_orden as o
        	inner join cliente_vehiculo as v on(
            		o.vehiculo_id=v.id and cast(o.fin as date) >= cast(d1 as date) and cast(o.fin as date) <= cast(d2 as date) and
                		  o.activo=true and o.cancelada=true) order by id desc
        ) p4);
    return (SELECT COALESCE(array_to_json(array_agg(row_to_json(p5))), '[]') from (
        	select case when total_f.valor is not null then total_f.valor else 0 end as total,
        			case when total_f.comosion is not null then total_f.comosion else 0 end as comi,
        		   case when total_f is not null then true else false end as existe,
        		   id_factura as facturas,id_cerradas as cerradas, id_canceladas as canceladas
        ) p5);
end;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION cierre_factura(text, text)
  OWNER TO postgres;
