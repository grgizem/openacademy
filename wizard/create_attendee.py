from osv import osv, fields


class CreateAttendeeWizard(osv.TransientModel):
	_name = 'openacademy.create_attendee_wizard'
	_columns = {'session_id': fields.many2one('openacademy.session', "Session", required=True),
	            'attendee_ids': fields.many2many('res.partner', required=True, domain=[('instructor', '=', False)])}

	def _get_active_session(self, cr, uid, context):
		if context.get('active_model') == 'openacademy.session':
			return context.get('active_id', False)
		return False

	_defaults = {'session_id': _get_active_session,}


	def action_add_attendees(self, cr, uid, ids, context=None):
		attendee_model = self.pool.get('openacademy.attendee')
		wizard = self.browse(cr, uid, ids[0], context=context)
		for attendee in wizard.attendee_ids:
			attendee_model.create(cr, uid, {'partner_id': attendee.id,
											'session_id': wizard.session_id.id,})
		return {}