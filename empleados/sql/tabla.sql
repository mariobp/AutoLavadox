select * from public.operacion_tiposervicio
select * from public.cliente_tipovehiculo
select * from public.operacion_tiposervicio_vehiculos
select * from public.cliente_tipovehiculo as tv
        inner join public.operacion_tiposervicio_vehiculos as ts_tv
        on(tv.id=ts_tv.tipovehiculo_id)

insert into public.operacion_tiposervicio (nombre,costo,comision,state) select nombre||' CAM',costo+10000,35,state from public.operacion_tiposervicio
insert into public.operacion_tiposervicio_vehiculos (tiposervicio_id,tipovehiculo_id) select id, 3 from public.operacion_tiposervicio where id > 11
delete from public.operacion_tiposervicio_vehiculos where id>11
