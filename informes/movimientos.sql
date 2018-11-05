
create view inventario_movimientos as
select 
	movi.id,
	operacion,
	fecha,
	articulo.nombre_articulo as insumo,
	case when bodega_origen_id is null then bodega.bodega else bodega_o.bodega end as bodega_origen,
	case when bodega_destino_id is null then bodega.bodega else bodega_d.bodega end as bodega_destino,
	cantidad,
	"user".username as usuario

 from (
	select 
		(1 || id::text)::bigint as id,
		'salida' as operacion,
		fecha,
		insumo_id as insumo,
		null as bodega_origen_id,
		bodega_destino_id,
		cantidad,
		usuario_id
		from inventario_salidadebodega 
	union

	select 
		(2 || id::text)::bigint as id,
		'entrada' as operacion,
		fecha,
		insumo_destino_id as insumo,
		bodega_origen_id,
		null as bodega_destino_id,
		cantidad,
		usuario_id

	from inventario_entradadebodega
) as movi
	join inventario_insumo as insumo
		on insumo.id = movi.insumo
	join inventario_articuloinsumo as articulo
		on articulo.id = insumo.articulo_id
	left join inventario_bodega as bodega_o
		on bodega_o.id = bodega_origen_id
	left join inventario_bodega as bodega_d
		on bodega_d.id = bodega_destino_id
	left join inventario_bodega as bodega
		on bodega.id = insumo.bodega_id
	join auth_user as "user"
		on "user".id = usuario_id
order by fecha