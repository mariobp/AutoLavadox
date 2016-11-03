select * from public.operacion_tiposervicio
select * from public.cliente_tipovehiculo
select * from public.operacion_tiposervicio_vehiculos
select ts.nombre from public.cliente_tipovehiculo as tv
        inner join public.operacion_tiposervicio_vehiculos as ts_tv
        on(tv.id=ts_tv.tipovehiculo_id)
        inner join public.operacion_tiposervicio as ts
        on (ts.id=ts_tv.tiposervicio_id) order by ts_tv.tipovehiculo_id asc,ts.id

insert into public.operacion_tiposervicio (nombre,costo,comision,state) select nombre||' CAM',costo+10000,35,state from public.operacion_tiposervicio
insert into public.operacion_tiposervicio_vehiculos (tiposervicio_id,tipovehiculo_id) select id, 3 from public.operacion_tiposervicio where id > 11
delete from public.operacion_tiposervicio_vehiculos where id>11


select * from public.cliente_tipovehiculo as tv
            inner join public.operacion_tiposervicio_vehiculos as ts_tv
            on(tv.id=ts_tv.tipovehiculo_id)
            inner join public.operacion_tiposervicio as ts
            on (ts.id=ts_tv.tiposervicio_id)
            left join public.operacion_servicio as s on (s.tipo_id=ts.id )
            order by ts_tv.tipovehiculo_id asc,ts.id

select * from public.operacion_servicio

select * from (select ts.id,ts.nombre,ts_tv.tipovehiculo_id as tipo,
           sum(
              case when s.id is null then 0
                    when s.status=false then 0
                    when s.estado=false then 0
                    when ts.comision <=0 then 0
                    else (ts.costo*ts.comision/100) end ) as total from public.cliente_tipovehiculo as tv
            inner join public.operacion_tiposervicio_vehiculos as ts_tv
            on(tv.id=ts_tv.tipovehiculo_id)
            inner join public.operacion_tiposervicio as ts
            on (ts.id=ts_tv.tiposervicio_id)
            left join public.operacion_servicio as s on (s.tipo_id=ts.id and s.status=true)
            group by ts.id,ts.nombre,ts_tv.tipovehiculo_id) as tabla
            order by tabla.tipo asc,tabla.id asc

select * from public.operacion_servicio
update public.operacion_servicio set estado=true where id in (1,3)
select * from public.cliente_tipovehiculo as tv
            inner join public.operacion_tiposervicio_vehiculos as ts_tv
            on(tv.id=ts_tv.tipovehiculo_id)
            inner join public.operacion_tiposervicio as ts
            on (ts.id=ts_tv.tiposervicio_id)
            left join public.operacion_servicio as s on (s.tipo_id=ts.id and s.status=true)
            group by ts.id,ts.nombre
            order by ts_tv.tipovehiculo_id asc,ts.id

select* from(select ts.id,ts.nombre,ts_tv.tipovehiculo_id as tipo,
           sum(
              case when s.id is null then 0
                    when s.status=false then 0
                    when s.estado=false then 0
                    when ts.comision <=0 then 0
                    else (ts.costo*ts.comision/100) end ) as total from (select * from public.empleados_empleado as r where r.persona_ptr_id=2) as o
       cross join public.cliente_tipovehiculo  as tv
       inner join public.operacion_tiposervicio_vehiculos as ts_tv
       on(tv.id=ts_tv.tipovehiculo_id)
       inner join public.operacion_tiposervicio as ts
       on (ts.id=ts_tv.tiposervicio_id)
       left join public.operacion_servicio as s on (s.tipo_id=ts.id and s.status=true and o.persona_ptr_id=s.operario_id and s.inicio::timestamp::date >= '2016-12-12'::date and s.inicio::timestamp::date <= '2016-12-13'::date)
       group by ts.id,ts.nombre,ts_tv.tipovehiculo_id) as tabla
       order by tabla.tipo asc,tabla.id asc

       select fin::timestamp::date,fin,'2016-11-22'::date from public.operacion_servicio
       select * from public.operacion_servicio
select u.id,p.identificacion,u.first_name as nombre, u.last_name from public.empleados_empleado as o
         inner join public.auth_user as u on (o.persona_ptr_id=u.id)
         inner join public.empleados_persona as p on (p.user_ptr_id=u.id)

select * from public.empleados_empleado as o
        inner join public.auth_user as u on (o.persona_ptr_id=u.id)
        inner join public.empleados_persona as p on (p.user_ptr_id=u.id)


        select * from public.auth_user
        select * from public.empleados_persona


§§§§§§§§§§§§§§§§§§
select id,nombre,tipo, from(select ts.id,ts.nombre,ts_tv.tipovehiculo_id as tipo,
           sum(
              case when s.id is null then 0
                    when s.status=false then 0
                    when s.estado=false then 0
                    when ts.comision <=0 then 0
                    else (ts.costo*ts.comision/100) end ) as total from (select * from public.empleados_empleado as r where r.persona_ptr_id=2) as o
       cross join public.cliente_tipovehiculo  as tv
       inner join public.operacion_tiposervicio_vehiculos as ts_tv
       on(tv.id=ts_tv.tipovehiculo_id)
       inner join public.operacion_tiposervicio as ts
       on (ts.id=ts_tv.tiposervicio_id)
       left join public.operacion_servicio as s on (s.tipo_id=ts.id and s.status=true and o.persona_ptr_id=s.operario_id)
       group by ts.id,ts.nombre,ts_tv.tipovehiculo_id) as tabla
       order by tabla.tipo asc,tabla.id asc
