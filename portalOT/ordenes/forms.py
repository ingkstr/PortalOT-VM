"""Forms de la aplicación de órdenes"""
from django import forms
from ordenes.models import Orden
from catalogos.models import *
from datetime import datetime

class OrdenForm (forms.ModelForm):
	"""Clase de form de alta de órden"""

	fecha_inicio = forms.DateField(
		widget=forms.DateInput(format='%d/%m/%Y'),
		input_formats=('%d/%m/%Y',)
		)
	fecha_fin = forms.DateField(
		widget=forms.DateInput(format='%d/%m/%Y'),
		input_formats=('%d/%m/%Y',)
		)

	class Meta:
		"""Configuraciones del formulario"""
		model = Orden
		fields = {'actividad','gerencia','supervisor','contacto','asunto',
			'detalle','localidades','fecha_inicio','hora_inicio','fecha_fin',
			'hora_fin',}
		error_messages = {
			'gerencia':  {
				'invalid_choice' : "Se requiere conocer la gerencia a cargo de la actividad",
			} ,
			'supervisor':  {
				'invalid_choice' : "Se requiere conocer al responsable a cargo de la actividad",
			} ,
			'contacto':  {
				'required' : "Se requiere tener un teléfono de contacto del supervisor",
				'max_length' : "Requerimos un contacto de 10 digitos",
			},
			'asunto':  {
				'required' : "Es obligatorio redactar el asunto de la actividad",
				'max_length' : "Requerimos que el asunto no rebase de 50 caracteres",
			} ,
			'detalle':  {
				'required' : "Es obligatorio redactar el detalle de la actividad",
				'max_length' : "Requerimos que el detalle no rebase de 250 caracteres",
			} ,
			'localidades':  {
				'required' : "Es obligatorio seleccionar al menos una localidad",
			} ,
			'fecha_inicio': {
				'required' : "Es obligatorio insertar una fecha de inicio de la actividad",
			} ,
			'hora_inicio': {
				'required' : "Es obligatorio insertar una hora de inicio de la actividad",
			} ,
			'fecha_fin': {
				'required' : "Es obligatorio insertar una fecha de fin de la actividad",
			} ,
			'hora_fin': {
				'required' : "Es obligatorio insertar una hora de fin de la actividad",
			} ,
		}

	def clean(self):
		"""Función de validaciones especiales de formulario"""
		data = super().clean()
		print(data)
		"""Validación de fechas de actividad"""
		hoy = datetime.now()
		inicio = datetime.combine(data['fecha_inicio'], data['hora_inicio'])
		fin = datetime.combine(data['fecha_fin'], data['hora_fin'])

		if (hoy > inicio):
			self.add_error('fecha_inicio','La fecha de inicio no puede ser una que ya haya sucedido')
			raise forms.ValidationError('La fecha de inicio no puede ser una que ya haya sucedido')

		if (hoy > fin):
			self.add_error('fecha_fin','La fecha de término no puede ser una que ya haya sucedido')
			raise forms.ValidationError('La fecha de término no puede ser una que ya haya sucedido')

		if (inicio > fin):
			self.add_error('fecha_inicio','Las fecha de inicio no puede ser después de la fecha de término')
			raise forms.ValidationError('Las fecha de inicio no puede ser después de la fecha de término')

		return data

#	def __init__(self, *args, **kwargs):
#		super().__init__(*args, **kwargs)
#		self.fields['supervisor'].queryset = Supervisor.objects.none()
#		if 'gerencia' in self.data:
#			try:
#				gerencia_id = int(self.data.get('gerencia'))
#				self.fields['supervisor'].queryset = Superviso.objects.filter(gerencia_id=gerencia_id).order_by('nombre')
#			except (ValueError, TypeError):
#				pass  # invalid input from the client; ignore and fallback to empty City queryset
#		elif self.instance.pk:
#				self.fields['supervisor'].queryset = self.instance.gerencia.supervisor_set.order_by('nombre')

		#self.fields['city'].queryset = City.objects.none()
		#if 'proveedor' in self.data:
		#if 'country' in self.data:
		#	try:
		#		proveedorid = int(self.data.get('proveedot'))
		#		self.fields['city'].queryset = City.objects.filter(gerencia_id=gerencia_id).order_by('nombre')
		#	except (ValueError, TypeError):
		#		pass  # invalid input from the client; ignore and fallback to empty City queryset
		#elif self.instance.pk:
		#	self.fields['supervisor'].queryset = self.instance.gerencia.supervisor_set.order_by('nombre')
