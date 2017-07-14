create or replace function cierre_factura(d1 text,d2 text) returns json as $$
declare
	id_factura json;
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
                		  o.activo=true and o.cerrada=true and o.pago=true) order by id desc
        ) p2);
    return (SELECT COALESCE(array_to_json(array_agg(row_to_json(p4))), '[]') from (
        	select case when total_f.valor is not null then total_f.valor else 0 end as total,
        			case when total_f.comosion is not null then total_f.comosion else 0 end as comi,
        		   case when total_f is not null then true else false end as existe,
        		   id_factura as facturas
        ) p4);
end;
$$language plpgsql;






CREATE OR REPLACE FUNCTION cierre_factura(
    d1 text,
    d2 text)
  RETURNS json AS
$BODY$
declare
	id_factura json;
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
                		  o.activo=true and o.cerrada=true and o.pago=true) order by id desc
        ) p2);
    return (SELECT COALESCE(array_to_json(array_agg(row_to_json(p4))), '[]') from (
        	select case when total_f.valor is not null then total_f.valor else 0 end as total,
        			case when total_f.comosion is not null then total_f.comosion else 0 end as comi,
        		   case when total_f is not null then true else false end as existe,
        		   id_factura as facturas
        ) p4);
end;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION cierre_factura(text, text)
  OWNER TO postgres;
	CREATE OR REPLACE FUNCTION cierre_factura_total(
	    d1 text,
	    d2 text)
	  RETURNS json AS
	$BODY$
	declare
	    total record;
	begin
	    return (SELECT COALESCE(array_to_json(array_agg(row_to_json(p4))), '[]') from (
	                select case when valor is not null then valor else 0 end as total,
	        				case when comi is not null then comi else 0 end as comosion
	        				from (select sum(valor) as valor, sum(comision) as comi
	                			from operacion_orden
	                        	where cast(fin as date) >= cast(d1 as date) and cast(fin as date) <= cast(d2 as date) and
	                              activo=true and cerrada=true and pago=true) as f
	            ) p4);
	end;
	$BODY$
	  LANGUAGE plpgsql VOLATILE
	  COST 100;
	ALTER FUNCTION cierre_factura_total(text, text)
	  OWNER TO postgres;
		-- Function: cierre_total_tipo_factura(text, text)

		-- DROP FUNCTION cierre_total_tipo_factura(text, text);

		CREATE OR REPLACE FUNCTION cierre_total_tipo_factura(
		    d1 text,
		    d2 text)
		  RETURNS json AS
		$BODY$
		declare
			id_factura json;
		    total_f record;
		begin
			select sum(valor) as valor, sum(comision) as comosion
		    		from operacion_orden
		            		where cast(fin as date) >= cast(d1 as date) and cast(fin as date) <= cast(d2 as date) and
		                		  activo=true and cerrada=true and pago=true into total_f;
		    id_factura := (SELECT COALESCE(array_to_json(array_agg(row_to_json(p2))), '[]') from (
		        	select f1.nombre,f1.cantidad,f1.costo,f1.total,f1.comision,f1.comi
		                    from (select  ts.id,ts.nombre,ts.costo,ts.comision,
		                                    sum(case when s.valor is not null then s.valor else 0 end) as total,
		                                    sum(case when s.comision is not null then s.comision else 0 end) as comi,
		                                    sum(case when s.id is not null then 1 else 0 end) as cantidad
		                         from operacion_orden as o
		                        inner join operacion_servicio as s on
		                                (s.orden_id=o.id and s.status=true and s.estado=true
		                                 and cast(o.fin as date) >= cast(d1 as date)
		                                 and cast(o.fin as date) <= cast(d2 as date)
		                                 and o.activo=true and o.cerrada=true and o.pago=true)
		                        inner join cliente_vehiculo as v on(
		                                o.vehiculo_id=v.id)
		                        right join operacion_tiposervicio as ts on(s.tipo_id=ts.id)
		                        group by ts.id,ts.nombre) as f1 order by f1.total desc
		        ) p2);
		    return (SELECT COALESCE(array_to_json(array_agg(row_to_json(p4))), '[]') from (
		        	select case when total_f.valor is not null then total_f.valor else 0 end as total,
		        			case when total_f.comosion is not null then total_f.comosion else 0 end as comi,
		        		   case when total_f is not null then true else false end as existe,
		        		   id_factura as facturas
		        ) p4);
		end;
		$BODY$
		  LANGUAGE plpgsql VOLATILE
		  COST 100;
		ALTER FUNCTION cierre_total_tipo_factura(text, text)
		  OWNER TO postgres;
