from osv import osv, fields


class CreateAttendeeWizard(osv.TransientModel):
	_name = 'openacademy.create_attendee_wizard'
	_columns = {'session_id': fields.many2one('openacademy.session', "Session", required=True),
	            'attendee_id': fields.many2one('res.partner', "Attendees", required=True, domain=[('instructor', '=', False)])}
