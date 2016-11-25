create or replace function report_empleados_comision (d1 text,d2 text) returns json as $$
declare
	traba json;
    servi json;
begin
  traba := (SELECT COALESCE(array_to_json(array_agg(row_to_json(p2))), '[]') from (
		select p.identificacion,u.last_name as apellido,u.first_name as nombre,p.direccion,p.telefono ,
        (SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
                select t2.id, t2.nombre,t2.total from
                (
                    select t1.id,t1.nombre,sum(case when t1.comi > 0 and t1.ope_t>0 then (t1.comi/t1.ope_t) else 0 end) as total
                            from
                                (
                                   select tp.id as id,tp.nombre as nombre,case when s.comision is not null and ser_ope.empleado_id is not null then s.comision else 0 end as comi,
                                   case when s.id is not null and ser_ope.empleado_id is not null then (select count(id)from operacion_servicio_operario as oper where oper.servicio_id=s.id) else 0 end as ope_t
                                              from operacion_orden as o
                                              left join operacion_servicio as s on (s.orden_id=o.id and o.pago=true and cast(o.fin as date)>= cast(d1 as date) and cast(o.fin as date)<= cast(d2 as date))
                                              left join operacion_servicio_operario as ser_ope on (ser_ope.servicio_id=s.id and ser_ope.empleado_id=p.user_ptr_id)
                                              right join operacion_tiposervicio as tp on (tp.id=s.tipo_id)
                                ) as t1 group by t1.id,t1.nombre
                ) as t2 order by t2.id asc
            ) p) as trabajos
		from empleados_empleado as e
		 inner join empleados_persona as p on (e.persona_ptr_id=p.user_ptr_id)
         inner join auth_user as u on(u.id=p.user_ptr_id)
	) p2);
    servi := (SELECT COALESCE(array_to_json(array_agg(row_to_json(p3))), '[]') from (
		select nombre from operacion_tiposervicio order by id asc
	) p3);
    return (SELECT COALESCE(array_to_json(array_agg(row_to_json(p4))), '[]') from (
		select servi,traba
	) p4);
end;
$$language plpgsql;
