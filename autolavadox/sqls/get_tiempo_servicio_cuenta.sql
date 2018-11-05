-- Function: public.get_tiempo_servicio_cuenta(text, text, integer)

-- DROP FUNCTION public.get_tiempo_servicio_cuenta(text, text, integer);

CREATE OR REPLACE FUNCTION public.get_tiempo_servicio_cuenta(
    d1 text,
    d2 text,
    id_cuenta integer)
  RETURNS json AS
$BODY$

declare
begin
    return (SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
            select t3.nombre,trunc(cast(t3.total as numeric),2)||' Minutos' as total from (select t2.nombre,case when t2.acu> 0 and t2.contador>0 then t2.acu/t2.contador else 0 end as total from (select t1.nombre,sum(t1.acumulado)as acu,sum(t1.conteo) as contador from (select t.id,t.nombre,
                    sum(case when s.inicio is not null and s.fin is not null then
                                  (EXTRACT(EPOCH FROM s.fin)-EXTRACT(EPOCH FROM s.inicio))/60
                             else
                                    0
                             end
                       ) as acumulado,
                       sum(
                            case when s.inicio is not null and s.fin is not null then
                                        1
                                 else
                                        0
                                 end

                       ) as conteo
             from operacion_tiposervicio t
             left join operacion_servicio as s on (s.cuenta_id=id_cuenta and t.cuenta_id=id_cuenta and t.state=true and s.orden_id=t.id and s.status=true and s.estado=true)
             left join operacion_orden as o on (o.cuenta_id=id_cuenta and s.orden_id=o.id and o.activo=true and o.pago=true) group by t.id,t.nombre,s.id) as t1 group by t1.nombre) as t2) as t3 order by total desc
        ) p);
end;

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.get_tiempo_servicio_cuenta(text, text, integer)
  OWNER TO postgres;
