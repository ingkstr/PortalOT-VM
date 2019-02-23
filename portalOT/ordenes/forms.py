"""Forms de la aplicación de órdenes"""
from django import forms
from ordenes.models import Orden
from catalogos.models import *
from datetime import datetime

class OrdenForm (forms.ModelForm):
	"""Clase de form de alta de órden"""

	fecha_inicio = forms.DateField(
		widget = forms.DateInput(format='%d/%m/%Y'),
		input_formats = ('%d/%m/%Y',),
		)
	fecha_fin = forms.DateField(
		widget=forms.DateInput(format='%d/%m/%Y'),
		input_formats=('%d/%m/%Y',),
		)

	class Meta:
		"""Configuraciones del formulario"""
		model = Orden
		fields = {'actividad','gerencia','supervisor','contacto','asunto',
			'detalle','localidades','fecha_inicio','hora_inicio','fecha_fin',
			'hora_fin','fecha_inicio_afectacion','hora_inicio_afectacion','fecha_fin_afectacion',
			'hora_fin_afectacion','proveedor','ejecutores','mop','servicios','clientes_afectados','comentarios'}

	def clean(self):
		"""Función de validaciones especiales de formulario"""
		cleaned_data = super(OrdenForm, self).clean()
		hoy = datetime.now()
		"""Validación de fechas de actividad"""
		fecha_inicio = cleaned_data.get("fecha_inicio")
		fecha_fin = cleaned_data.get("fecha_fin")
		hora_inicio = cleaned_data.get("hora_inicio")
		hora_fin = cleaned_data.get("hora_fin")
		actividad = cleaned_data.get("actividad")
		omision_elementos_afectados = False
		omision_periodo_actividad = False
		omision_periodo_afectacion = False
		if not fecha_inicio or not fecha_fin or not hora_inicio or not hora_fin:
			omision_periodo_actividad = True
		else:
			inicio = datetime.combine(fecha_inicio, hora_inicio)
			fin = datetime.combine(fecha_fin, hora_fin)

			if (hoy >= inicio):
				self.add_error('fecha_inicio','El horario de inicio no puede ser una que ya haya sucedido')
				omision_periodo_actividad = True

			if (hoy >= fin):
				self.add_error('fecha_fin','El horario de término no puede ser una que ya haya sucedido')
				omision_periodo_actividad = True

			if (inicio >= fin):
				self.add_error('fecha_inicio','El horario de inicio no puede ser después del término')
				omision_periodo_actividad = True

		"""Validación de periodo y puntos de afectacion"""

		if actividad == "VM":
			servicios = cleaned_data.get("servicios")
			if not servicios:
				self.add_error('servicios','Este campo es obligatorio en ventanas de mtto')
				omision_elementos_afectados = True
			clientes_afectados = cleaned_data.get("clientes_afectados")
			if not clientes_afectados:
				self.add_error('clientes_afectados','Este campo es obligatorio en ventanas de mtto')
				omision_elementos_afectados = True

			if omision_periodo_actividad:
				self.add_error('fecha_inicio_afectacion','Primero hay que corregir el horario de actividad general')
				self.add_error('fecha_fin_afectacion','Primero hay que corregir el horario de actividad general')
				self.add_error('hora_inicio_afectacion','Primero hay que corregir el horario de actividad general')
				self.add_error('hora_fin_afectacion','Primero hay que corregir el horario de actividad general')
			else:
				fecha_inicio_afectacion = cleaned_data.get("fecha_inicio_afectacion")
				if not fecha_inicio_afectacion:
					self.add_error('fecha_inicio_afectacion','Este campo es obligatorio en ventanas de mtto')
					omision_periodo_afectacion = True
				fecha_fin_afectacion = cleaned_data.get("fecha_fin_afectacion")
				if not fecha_fin_afectacion:
					self.add_error('fecha_fin_afectacion','Este campo es obligatorio en ventanas de mtto')
					omision_periodo_afectacion = True
				hora_inicio_afectacion = cleaned_data.get("hora_inicio_afectacion")
				if not hora_inicio_afectacion:
					self.add_error('hora_inicio_afectacion','Este campo es obligatorio en ventanas de mtto')
					omision_periodo_afectacion = True
				hora_fin_afectacion = cleaned_data.get("hora_fin_afectacion")
				if not hora_fin_afectacion:
					self.add_error('hora_fin_afectacion','Este campo es obligatorio en ventanas de mtto')
					omision_periodo_afectacion = True

				if not omision_periodo_afectacion:

					inicio_afectacion = datetime.combine(fecha_inicio_afectacion, hora_inicio_afectacion)
					fin_afectacion = datetime.combine(fecha_fin_afectacion, hora_fin_afectacion)

					if (inicio_afectacion >= fin_afectacion):
						self.add_error('fecha_inicio_afectacion','El inicio de afectación no puede ser después del término de afectación')
						omision_periodo_afectacion = True
					if (inicio_afectacion < inicio):
						self.add_error('fecha_inicio_afectacion','El inicio de afectación no puede ser antes que el inicio de la actividad')
						omision_periodo_afectacion = True
					if (fin_afectacion > fin):
						self.add_error('fecha_fin_afectacion','El fin de afectación no puede ser después que el fin de la actividad')
						omision_periodo_afectacion = True

		if not omision_periodo_actividad and not omision_periodo_afectacion and not omision_elementos_afectados:
			return cleaned_data
		else:
			raise forms.ValidationError('Validación no pasada!!!')
