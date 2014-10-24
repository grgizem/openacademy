from openerp.osv import osv, fields

				
class Attendee(osv.Model):
	_name = "openacademy.attendee"
	
	_columns = {'partner_id': fields.many2one('res.partner',
		                                      "Partner",
		                                      domain=[('instructor', '=', False)]),
				'session_id': fields.many2one('openacademy.session',
							                  "Session")
			   }

	_sql_constraints = [
		('partner_unique_in_session_check',
		'UNIQUE(partner_id, session_id)',
		'You can not add the same attendee multiple times.')
	]	