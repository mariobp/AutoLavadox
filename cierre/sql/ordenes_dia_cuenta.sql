-- Function: ordenes_dia()

-- DROP FUNCTION ordenes_dia();

CREATE OR REPLACE FUNCTION ordenes_dia_cuenta(id_cuenta integer)
  RETURNS json AS
$BODY$
begin
    return (SELECT COALESCE(array_to_json(array_agg(row_to_json(p4))), '[]') from (
            select sum(case when activo=true and pago=true and cerrada=true then 1 else 0 end) pagas,
           sum(case when activo=true and pago=false and cerrada=false then 1 else 0 end) cerradas
                from operacion_orden where cuenta_id=id_cuenta and cast(now() as date) = cast(entrada as date) and activo=true
        ) p4);
end;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION ordenes_dia_cuenta(integer)
  OWNER TO postgres;
