create or replace function cierre_factura_total(d1 text,d2 text) returns json as $$
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
$$language plpgsql;
