
CREATE OR REPLACE FUNCTION public.get_cierre_inventario(
    id_cierre integer,
    id_cuenta integer) RETURNS json AS $$
declare
   venta json;
   venta_total json;
   operacion json;
   operacion_total json;
   cierre record;
begin
	select inicio, fin into cierre from inventario_cierre where id=id_cierre limit 1;
	venta := (
		SELECT COALESCE(array_to_json(array_agg(row_to_json(descr))), '[]') from (
			select
				case when p.nombre is not null then p.nombre else 'No Asignado' end as "nombre",
				sum(case when productos.cantidad is not null then productos.cantidad else 0 end) as "cantidad",
				p.existencias,
				sum(case when productos.compra is not null then productos.compra else 0 end) as "compra",
				sum(case when productos.total is not null then productos.total else 0 end) as "total",
				(sum(case when productos.total is not null then productos.total else 0 end) - sum(case when productos.compra is not null then productos.compra else 0 end)) as "utilidad"

			from inventario_producto as p
				 left join inventario_venta as v on (p.id=v.producto_ptr_id and p.cuenta_id=id_cuenta)
				 /*left join inventario_operacion as o on (p.id=o.producto_ptr_id)*/
				 left join (select * from (
							select orden_tem.id,orden_tem.activo,orden_tem.pago from operacion_orden as orden_tem
								where  orden_tem.cuenta_id=id_cuenta /*and orden_tem.activo=true and orden_tem.pago=true*/
								and cast(orden_tem.fin as date) >= cierre.inicio
								and cast(orden_tem.fin as date) <= cierre.fin
						) as orden left join operacion_historiadeservicioventa as hv on (hv.orden_id=orden.id)

				 ) as productos on (productos.producto_id=p.id) group by p.id,p.nombre order by "total" desc

		) descr
	);

	venta_total:=(
		SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
				select
					sum(case when productos.compra is not null then productos.compra else 0 end) as "compra",
					sum(case when productos.total is not null then productos.total else 0 end) as "total",
					(sum(case when productos.total is not null then productos.total else 0 end) - sum(case when productos.compra is not null then productos.compra else 0 end)) as "utilidad"

				from inventario_producto as p
					 left join inventario_venta as v on (p.id=v.producto_ptr_id and p.cuenta_id=id_cuenta)
					 /*left join inventario_operacion as o on (p.id=o.producto_ptr_id)*/
					 left join (select * from (
								select orden_tem.id,orden_tem.activo,orden_tem.pago from operacion_orden as orden_tem
									where  orden_tem.cuenta_id=id_cuenta /*and orden_tem.activo=true and orden_tem.pago=true*/
									and cast(orden_tem.fin as date) >= cierre.inicio
									and cast(orden_tem.fin as date) <= cierre.fin
							) as orden left join operacion_historiadeservicioventa as hv on (hv.orden_id=orden.id)

					 ) as productos on (productos.producto_id=p.id)

		) p
	);

	operacion:=(
		SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
				select
					case when p.nombre is not null then p.nombre else 'No Asignado' end as "nombre",
					sum(case when productos.cantidad is not null then productos.cantidad else 0 end) as "cantidad",
					p.existencias,
					sum(case when productos.compra is not null then productos.compra else 0 end) as "compra",
					sum(case when productos.total is not null then productos.total else 0 end) as "total",
					(sum(case when productos.total is not null then productos.total else 0 end) - sum(case when productos.compra is not null then productos.compra else 0 end)) as "utilidad"

				from inventario_producto as p
					 left join inventario_operacion as o on (p.id=o.producto_ptr_id and p.cuenta_id=id_cuenta)
					 left join (select * from (
								select orden_tem.id,orden_tem.activo,orden_tem.pago from operacion_orden as orden_tem
									where  orden_tem.cuenta_id=id_cuenta /*and orden_tem.activo=true and orden_tem.pago=true*/
									and cast(orden_tem.fin as date) >= cierre.inicio
									and cast(orden_tem.fin as date) <= cierre.fin
							) as orden left join operacion_historiadeserviciooperacion as hv on (hv.orden_id=orden.id)

					 ) as productos on (productos.producto_id=p.id) group by p.id,p.nombre order by "total" desc

			) p
	);

	operacion_total:=(
		SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
				select
					sum(case when productos.compra is not null then productos.compra else 0 end) as "compra",
					sum(case when productos.total is not null then productos.total else 0 end) as "total",
					(sum(case when productos.total is not null then productos.total else 0 end) - sum(case when productos.compra is not null then productos.compra else 0 end)) as "utilidad"

				from inventario_producto as p
					 left join inventario_operacion as o on (p.id=o.producto_ptr_id and p.cuenta_id=id_cuenta)
					 left join (select * from (
								select orden_tem.id,orden_tem.activo,orden_tem.pago from operacion_orden as orden_tem
									where  orden_tem.cuenta_id=id_cuenta /*and orden_tem.activo=true and orden_tem.pago=true*/
									and cast(orden_tem.fin as date) >= cierre.inicio
									and cast(orden_tem.fin as date) <= cierre.fin
							) as orden left join operacion_historiadeserviciooperacion as hv on (hv.orden_id=orden.id)

					 ) as productos on (productos.producto_id=p.id)
		) p
	);
	return (SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
				select venta, venta_total, operacion, operacion_total
			) p);
end;
$$LANGUAGE plpgsql;