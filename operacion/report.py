from import_export import resources
import models as operacion


class ServicioInform(resources.ModelResource):

    class Meta:
        model = operacion.Servicio
        fields = ('nombre','costo','comision')
        export_order = ('nombre','costo','comision')
    # end class
# end class
