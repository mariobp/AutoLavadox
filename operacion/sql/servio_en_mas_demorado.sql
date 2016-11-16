select * from (select t2.nombre,case when t2.acu> 0 and t2.contador>0 then t2.acu/t2.contador else 0 end as total from (select t1.nombre,sum(t1.acumulado)as acu,sum(t1.conteo) as contador from (select t.id,t.nombre,
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
		 left join operacion_servicio as s on (t.state=true and s.orden_id=t.id and s.status=true and s.estado=true)
         left join operacion_orden as o on (s.orden_id=o.id and o.activo=true and o.pago=true) group by t.id,t.nombre,s.id) as t1 group by t1.nombre) as t2) as t3 order by total desc


         create or replace function get_tiempo_servicio(d1 date,d2 date) returns json as $$
         declare
         begin
             return (SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
                     select * from (select t2.nombre,case when t2.acu> 0 and t2.contador>0 then t2.acu/t2.contador else 0 end as total from (select t1.nombre,sum(t1.acumulado)as acu,sum(t1.conteo) as contador from (select t.id,t.nombre,
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
                      left join operacion_servicio as s on (t.state=true and s.orden_id=t.id and s.status=true and s.estado=true)
                      left join operacion_orden as o on (s.orden_id=o.id and o.activo=true and o.pago=true) group by t.id,t.nombre,s.id) as t1 group by t1.nombre) as t2) as t3 order by total desc
                 ) p);
         end;
         $$language plpgsql;
