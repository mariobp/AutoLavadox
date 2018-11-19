/*create or replace function get_cierre_turno(id_turno integer,id_cuenta integer) returns json as $$
declare
 descripcion json;
 productos json;
 total json;
 productos_total json;
 turno record;
begin
	select (c.inicio + t.inicio) as inicio, (c.fin + t.fin) as fin into  turno from cierre_cierre as c inner join cierre_turno as t  on (c.turno_id=t.id) limit 1;
	descripcion := (
		SELECT COALESCE(array_to_json(array_agg(row_to_json(descr))), '[]') from (
				select tipo_ser.nombre,
					sum(case when servi.valor is not null then servi.valor else 0 end) as "valor",
					sum(case when servi.comision is not null then servi.comision else 0 end) as "comision"
					from operacion_tiposervicio as tipo_ser
						 left join (
							select ser.tipo_id, orden.activo, orden.pago, ser.valor, ser.comision from (select * from operacion_orden as orden_tem
									where  orden_tem.cuenta_id=id_cuenta and orden_tem.activo=true and orden_tem.pago=true
									and orden_tem.fin >= turno.inicio
									and orden_tem.fin <= turno.fin) as orden
								   left join operacion_servicio as ser on (orden.id=ser.orden_id and ser.status=true and ser.estado=true)
						 ) as servi on(tipo_ser.id=servi.tipo_id) group by tipo_ser.id, tipo_ser.nombre order by "valor" desc

			) descr
	);

	total:=(
		SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
			select
				sum(case when servi.valor is not null then servi.valor else 0 end) as "valor",
				sum(case when servi.comision is not null then servi.comision else 0 end) as "comision"
				from operacion_tiposervicio as tipo_ser
					 left join (
						select ser.tipo_id, orden.activo, orden.pago, ser.valor, ser.comision from (select * from operacion_orden as orden_tem
								where  orden_tem.cuenta_id=id_cuenta and orden_tem.activo=true and orden_tem.pago=true
								and orden_tem.fin >= turno.inicio
								and orden_tem.fin <= turno.fin) as orden
							   left join operacion_servicio as ser on (orden.id=ser.orden_id and ser.status=true and ser.estado=true)
					 ) as servi on(tipo_ser.id=servi.tipo_id)
		) p
	);

	productos_total:=(
		SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
			select
				sum(case when producto.total is not null then producto.total else 0 end) as "total"
			 from inventario_venta as pv
				 inner join inventario_producto as p on(pv.producto_ptr_id=p.id and p.cuenta_id=id_cuenta)
				 left join (
					select orden.activo, orden.pago, pro_ven.total,pro_ven.producto_id   from (select * from operacion_orden as orden_tem
							where  orden_tem.cuenta_id=id_cuenta /*and orden_tem.activo=true and orden_tem.pago=true */
							and orden_tem.fin >= turno.inicio
							and orden_tem.fin <= turno.fin) as orden
							left join operacion_productoventa as pro_ven on (orden.id=pro_ven.orden_id)
				 ) as producto on (producto.producto_id=p.id)
		) p
	);

	productos:=(
		SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
			select
				case when p.nombre is not null then p.nombre else 'No Asignado' end as "nombre",
				sum(case when producto.total is not null then producto.total else 0 end) as "total"
			 from inventario_venta as pv
				 inner join inventario_producto as p on(pv.producto_ptr_id=p.id and p.cuenta_id=id_cuenta)
				 left join (
					select orden.activo, orden.pago, pro_ven.total,pro_ven.producto_id   from (select * from operacion_orden as orden_tem
							where  orden_tem.cuenta_id=id_cuenta /*and orden_tem.activo=true and orden_tem.pago=true */
							and orden_tem.fin >= turno.inicio
							and orden_tem.fin <= turno.fin) as orden
						   left join operacion_productoventa as pro_ven on (orden.id=pro_ven.orden_id)
				 ) as producto on (producto.producto_id=p.id) group by p.nombre order by "total" desc

		) p
	);
	return (SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
				select total, descripcion, productos, productos_total
			) p);
end;
$$language plpgsql*/
-- Function: public.get_cierre_turno(integer, integer)

-- DROP FUNCTION public.get_cierre_turno(integer, integer);

CREATE OR REPLACE FUNCTION public.get_cierre_turno(
    id_turno integer,
    id_cuenta integer) RETURNS json AS $$
declare
   descripcion json;
   productos json;
   total json;
   productos_total json;
   turno record;
begin
	select (c.inicio + t.inicio) as inicio, (c.fin + t.fin) as fin into  turno from cierre_cierre as c inner join cierre_turno as t  on (c.turno_id=t.id) limit 1;
	descripcion := (
		SELECT COALESCE(array_to_json(array_agg(row_to_json(descr))), '[]') from (
				select case when tipo_ser.nombre is not null then tipo_ser.nombre else 'No Asignado' end as "nombre",
					sum(case when servi.valor is not null then servi.valor else 0 end) as "valor",
					sum(case when servi.comision is not null then servi.comision else 0 end) as "comision",
					sum(case when servi.comision is not null then servi.comision else 0 end + case when servi.valor is not null then servi.valor else 0 end) as "total"
					from operacion_tiposervicio as tipo_ser
						 left join (
							select ser.tipo_id, orden.activo, orden.pago, ser.valor, ser.comision from (select * from operacion_orden as orden_tem
									where  orden_tem.cuenta_id=id_cuenta and orden_tem.activo=true and orden_tem.pago=true
									and orden_tem.fin >= turno.inicio
									and orden_tem.fin <= turno.fin) as orden
								   left join operacion_servicio as ser on (orden.id=ser.orden_id and ser.status=true and ser.estado=true)
						 ) as servi on(tipo_ser.id=servi.tipo_id) group by tipo_ser.id, tipo_ser.nombre order by "total" desc

			) descr
	);

	total:=(
		SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
			select
				sum(case when servi.valor is not null then servi.valor else 0 end) as "valor",
				sum(case when servi.comision is not null then servi.comision else 0 end) as "comision",
				sum(case when servi.valor is not null then servi.valor else 0 end + case when servi.comision is not null then servi.comision else 0 end) as "total"
				from operacion_tiposervicio as tipo_ser
					 left join (
						select ser.tipo_id, orden.activo, orden.pago, ser.valor, ser.comision from (select * from operacion_orden as orden_tem
								where  orden_tem.cuenta_id=id_cuenta and orden_tem.activo=true and orden_tem.pago=true
								and orden_tem.fin >= turno.inicio
								and orden_tem.fin <= turno.fin) as orden
							   left join operacion_servicio as ser on (orden.id=ser.orden_id and ser.status=true and ser.estado=true)
					 ) as servi on(tipo_ser.id=servi.tipo_id)
		) p
	);

	productos_total:=(
		SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
			select
				sum(case when producto.total is not null then producto.total else 0 end) as "total"
			 from inventario_venta as pv
				 inner join inventario_producto as p on(pv.producto_ptr_id=p.id and p.cuenta_id=id_cuenta)
				 left join (
					select orden.activo, orden.pago, pro_ven.total,pro_ven.producto_id   from (select * from operacion_orden as orden_tem
							where  orden_tem.cuenta_id=id_cuenta /*and orden_tem.activo=true and orden_tem.pago=true */
							and orden_tem.fin >= turno.inicio
							and orden_tem.fin <= turno.fin) as orden
							left join operacion_productoventa as pro_ven on (orden.id=pro_ven.orden_id)
				 ) as producto on (producto.producto_id=p.id)
		) p
	);

	productos:=(
		SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
			select
				case when p.nombre is not null then p.nombre else 'No Asignado' end as "nombre",
				sum(case when producto.total is not null then producto.total else 0 end) as "total"
			 from inventario_venta as pv
				 inner join inventario_producto as p on(pv.producto_ptr_id=p.id and p.cuenta_id=id_cuenta)
				 left join (
					select orden.activo, orden.pago, pro_ven.total,pro_ven.producto_id   from (select * from operacion_orden as orden_tem
							where  orden_tem.cuenta_id=id_cuenta /*and orden_tem.activo=true and orden_tem.pago=true */
							and orden_tem.fin >= turno.inicio
							and orden_tem.fin <= turno.fin) as orden
						   left join operacion_productoventa as pro_ven on (orden.id=pro_ven.orden_id)
				 ) as producto on (producto.producto_id=p.id) group by p.nombre order by "total" desc

		) p
	);
	return (SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
				select total, descripcion, productos, productos_total
			) p);
end;
$$LANGUAGE plpgsql;