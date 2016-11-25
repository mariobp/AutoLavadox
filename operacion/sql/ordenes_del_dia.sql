create or replace function ordenes_dia () returns json as $$
begin
    return (SELECT COALESCE(array_to_json(array_agg(row_to_json(p4))), '[]') from (
            select sum(case when activo=true and pago=true and cerrada=true then 1 else 0 end) pagas,
           sum(case when activo=true and pago=false and cerrada=false then 1 else 0 end) cerradas
                from operacion_orden where cast(now() as date) = cast(entrada as date) and activo=true
        ) p4);
end;
$$language plpgsql;
