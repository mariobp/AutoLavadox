CREATE OR REPLACE FUNCTION public.get_orden_cliente(
    id_orden integer,
    id_cuenta integer)
  RETURNS json AS
$BODY$
declare
begin
	 return (SELECT COALESCE(array_to_json(array_agg(row_to_json(p4))), '[]') from (
		select (SELECT COALESCE(array_to_json(array_agg(row_to_json(p1))), '[]') from (
				select
				   case when a.first_name is not null then a.first_name else '' end as nombre,
				   case when cli.invima is not null then cli.invima else '' end as invima,
				   case when cli.nit is not null then cli.nit else '' end as nit,
				   case when cli.impresora is not null then cli.impresora else '' end as impresora,
				   case when cli.direccion is not null then cli.direccion else '' end as direccion
				from subcripcion_cuenta as cuent
			        inner join subcripcion_cliente as cli on (cli.user_ptr_id=cuent.cliente_id and cuent.id=id_cuenta)
			        inner join auth_user as a on (a.id=cuent.cliente_id) limit 1
			    ) p1) as cuenta,
			    (SELECT COALESCE(array_to_json(array_agg(row_to_json(p1))), '[]') from (
				select case when v.placa is not null then v.placa else '' end as placa,
				       case when c.nombre is not null then c.nombre else '' end as nombre,
				       case when c.apellidos is not null then c.apellidos else '' end as apellidos,
				       case when c.dirreccion is not null then c.dirreccion else '' end as dirreccion,
				       case when c.identificacion is not null then c.identificacion else '' end as identificacion
				from operacion_orden as o_t
				inner join cliente_vehiculo as v on (o_t.vehiculo_id=v.id and o_t.id=o.id)
				inner join cliente_cliente as c on (c.id=v.cliente_id) limit 1
			    ) p1) as cliente,
			    (SELECT COALESCE(array_to_json(array_agg(row_to_json(p1))), '[]') from (
				select tp_ser.nombre,
				 to_char(ser.valor, 'FM999,999,999,990') as valor
				from operacion_servicio as ser
				inner join operacion_tiposervicio as tp_ser on ( ser.tipo_id=tp_ser.id and ser.orden_id=id_orden)
			    ) p1) as servicios,
			    (SELECT COALESCE(array_to_json(array_agg(row_to_json(p1))), '[]') from (
				select pro_tem.nombre,  to_char(pro_ven.total, 'FM999,999,999,990') as valor
				from  operacion_productoventa as pro_ven
				inner join inventario_producto as pro_tem on (pro_ven.orden_id=id_orden and pro_ven.producto_id=pro_tem.id)
			    ) p1) as productos,
			    (
				select to_char(
				case when (
						select sum(tp_ser.valor) from (select torden.id from operacion_orden as torden where torden.id=448) as orden
									inner join operacion_servicio as tp_ser on (tp_ser.orden_id=orden.id)
					 ) is not null then
						(
							select sum(tp_ser.valor) from (select torden.id from operacion_orden as torden where torden.id=448) as orden
							inner join operacion_servicio as tp_ser on (tp_ser.orden_id=orden.id)
						) else 0 end +
				case when (
						select sum(pro_ven.total) from (select torden.id from operacion_orden as torden where torden.id=448) as orden
						left join operacion_productoventa as pro_ven on (pro_ven.orden_id=orden.id)
					) is not null then (
						select sum(pro_ven.total) from (select torden.id from operacion_orden as torden where torden.id=448) as orden
						left join operacion_productoventa as pro_ven on (pro_ven.orden_id=orden.id)
					) else 0 end
				, 'FM999,999,999,990')
			    ) as total,cast(o.id as text) as id, cast(o.numero as text) as identificador,cast(o.entrada as date) as entrada, case when o.fin is null then cast(o.entrada as date) else cast(o.fin as date) end as salida
	        from operacion_orden as o where o.id= id_orden
        ) p4);
end;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.get_orden_cliente(integer, integer)
  OWNER TO postgres;