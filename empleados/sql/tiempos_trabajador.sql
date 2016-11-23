-- FUNCTION: public.informe_time_operarios(text, text)

-- DROP FUNCTION public.informe_time_operarios(text, text);

CREATE OR REPLACE FUNCTION public.informe_time_operarios(
	f1 text,
	f2 text)
RETURNS json
    LANGUAGE 'plpgsql'
    COST 100.0

AS $function$

declare
  tipos_servi json;
  empleados json;
 begin
 	empleados:=(SELECT COALESCE(array_to_json(array_agg(row_to_json(p2))), '[]') from (
		select p.identificacion,u.first_name,u.last_name,p.telefono ,
		(SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
			select d2.nombre,case when d2.min>0 and d2.exis>0 then trunc(cast((d2.min/d2.exis) as numeric),2) else 0 end as total from (select d1.id,d1.nombre,sum(minutos) as min, sum(existencia) as exis from (select t.id,t.nombre,
       case when s.inicio is not null and s.fin is not null then
       			(EXTRACT(EPOCH FROM s.fin)-EXTRACT(EPOCH FROM s.inicio))/60
             else
             	 0
             end as minutos,
       case when s.inicio is not null and s.fin is not null then
       		1
         else
            0
         end as existencia
       from operacion_tiposervicio t
             left join operacion_servicio as s on (t.state=true and s.orden_id=t.id and s.status=true and s.estado=true)
             left join operacion_orden as o on (s.orden_id=o.id and o.activo=true and o.pago=true and cast(o.fin as date)>= cast(f1 as date) and cast(o.fin as date)<= cast(f2 as date))
             left join operacion_servicio_operario as operario
                   on (operario.servicio_id =s.id and operario.empleado_id=p.user_ptr_id)group by t.id,t.nombre,s.id)
                   as d1 group by d1.id,d1.nombre) as d2 order by d2.id asc
        ) p) as servicios
		 from empleados_empleado as e
		 inner join empleados_persona as p on (e.persona_ptr_id=p.user_ptr_id)
         inner join auth_user as u on (u.id=p.user_ptr_id)
      ) p2);
      tipos_servi := (SELECT COALESCE(array_to_json(array_agg(row_to_json(p22))), '[]') from (
		select nombre from operacion_tiposervicio order by id asc
      ) p22);
      return (SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
		select empleados ,tipos_servi as servicios
	) p);
 end;


$function$;

ALTER FUNCTION public.informe_time_operarios(text, text)
    OWNER TO postgres;

/******************************************************/
CREATE FUNCTION informe_time_operarios(f1 text,f2 text) RETURNS json
    LANGUAGE plpgsql
    AS $$
		declare
		  tipos_servi json;
		  empleados json;
		 begin
		 	empleados:=(SELECT COALESCE(array_to_json(array_agg(row_to_json(p2))), '[]') from (
				select p.identificacion,u.first_name,u.last_name,p.telefono ,
				(SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
					select d2.nombre,case when d2.min>0 and d2.exis>0 then trunc(cast((d2.min/d2.exis) as numeric),2) else 0 end as total from (select d1.id,d1.nombre,sum(minutos) as min, sum(existencia) as exis from (select t.id,t.nombre,
		       case when s.inicio is not null and s.fin is not null then
		       			(EXTRACT(EPOCH FROM s.fin)-EXTRACT(EPOCH FROM s.inicio))/60
		             else
		             	 0
		             end as minutos,
		       case when s.inicio is not null and s.fin is not null then
		       		1
		         else
		            0
		         end as existencia
		       from operacion_tiposervicio t
		             left join operacion_servicio as s on (t.state=true and s.orden_id=t.id and s.status=true and s.estado=true)
		             left join operacion_orden as o on (s.orden_id=o.id and o.activo=true and o.pago=true and cast(o.fin as date)>= cast(f1 as date) and cast(o.fin as date)<= cast(f2 as date))
		             left join operacion_servicio_operario as operario
		                   on (operario.servicio_id =s.id and operario.empleado_id=p.user_ptr_id)group by t.id,t.nombre,s.id)
		                   as d1 group by d1.id,d1.nombre) as d2 order by d2.id asc
		        ) p) as servicios
				 from empleados_empleado as e
				 inner join empleados_persona as p on (e.persona_ptr_id=p.user_ptr_id)
		         inner join auth_user as u on (u.id=p.user_ptr_id)
		      ) p2);
		      tipos_servi := (SELECT COALESCE(array_to_json(array_agg(row_to_json(p22))), '[]') from (
				select nombre from operacion_tiposervicio order by id asc
		      ) p22);
		      return (SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
				select empleados ,tipos_servi as servicios
			) p);
end;$$;
