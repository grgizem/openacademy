from tools.translate import _
from datetime import datetime, timedelta

from openerp.osv import osv, fields


class Session(osv.Model):
	_name = "openacademy.session"

	def action_draft(self, cr, uid, ids, context=None):
		return self.write(cr, uid, ids, {'state': 'draft'}, context=context)

	def action_confirm(self, cr, uid, ids, context=None):
		return self.write(cr, uid, ids, {'state': 'confirmed'}, context=context)

	def action_done(self, cr, uid, ids, context=None):
		return self.write(cr, uid, ids, {'state': 'done'}, context=context)

	def _is_instructor_not_in_attendees(self, cr, uid, ids, context=None):
		for session in self.browse(cr, uid, ids, context):
			partners = [att.partner_id for att in session.attendee_ids]
			if session.instructor_id and session.instructor_id in partners:
				return False
		return True

	def _seats_percent(self, seats, attendee_ids):
		if seats == 0:
			return 0
		else:
			return (len(attendee_ids) * 100.0) / seats

	def _taken_seats(self, cr, uid, ids, field, arg, context=None):
		res = {}
		for session in self.browse(cr, uid, ids, context=context):
			taken_seats = self._seats_percent(session.seats, session.attendee_ids)
			res[session.id] = taken_seats
		return res

	def onchange_taken_seats(self, cr, uid, ids, seats, attendee_ids):
		attendee_records = self.resolve_2many_commands(cr, uid, 'attendee_ids', attendee_ids, ['id'])
		res = {
			'value': {
				'taken_seats': self._seats_percent(seats, attendee_records)
			}
		}
		if seats < 0:
			res['warning'] = {'title': "Warning!",
							  'message': _("You cannot have negative number of seats.")}
		elif seats < len(attendee_records):
			res['warning'] = {'title': "Warning!",
							  'message': _("You need more seats for this session.")}
		return res

	def _determin_end_date(self, cr, uid, ids, field, arg, context=None):
		result = {}
		for session in self.browse(cr, uid, ids, context=context):
			if session.start_date and session.duration:
				start_date = datetime.strptime(session.start_date, "%Y-%m-%d")
				duration = timedelta(days=(session.duration - 1))
				end_date = start_date + duration
				result[session.id] = end_date.strftime("%Y-%m-%d")
			else:
				result[session.id] = session.start_date
		return result

	def _set_end_date(self, cr, uid, id, field, value, arg, context=None):
		session = self.browse(cr, uid, id, context=context)
		if session.start_date and value:
			start_date = datetime.strptime(session.start_date, "%Y-%m-%d")
			end_date = datetime.strptime(value[:10], "%Y-%m-%d")
			duration = end_date - start_date
			self.write(cr, uid, id, {'duration' : (duration.days + 1)}, context=context)

	def _determin_hours_from_duration(self, cr, uid, ids, field, arg, context=None):
		result = {}
		sessions = self.browse(cr, uid, ids, context=context)
		for session in sessions:
			result[session.id] = (session.duration * 24 if session.duration else 0)
		return result

	def _set_hours(self, cr, uid, id, field, value, arg, context=None):
		if value:
			self.write(cr, uid, id, {'duration' : (value / 24)}, context=context)

	def _get_attendee_count(self, cr, uid, ids, field, arg, context=None):
		res = {}
		sessions = self.browse(cr, uid, ids, context=context)
		for session in sessions:
			res[session.id] = len(session.attendee_ids)
		return res

	_columns = {'name' : fields.char("Title",
									 256,
									 translate=True,
									 required=True,
									 select=1),
				'instructor_id': fields.many2one('res.partner',
					"Instructor", domain=['|', ('instructor', '=', True),
						('category_id.name', 'ilike', 'teacher')]),
				'course_id': fields.many2one('openacademy.course',
											 "Course"),
				'attendee_ids': fields.one2many('openacademy.attendee',
					                            'session_id',
					                            "Attendees"),
				'start_date' : fields.date("Start Date",
										   translate=True),
				'duration': fields.float("Duration",
										 digits=(6,2),
										 help="Duration time in days"),
				'seats': fields.integer("Number of Seats",
										required=True),
				'color': fields.integer("Color"),
				'state' : fields.selection([('draft', 'Draft'),
											('confirmed', 'Confirmed'),
											('done', 'Done')],
										   string="State"),
				'active': fields.boolean("Active"),
				'taken_seats': fields.function(_taken_seats,
					string="Taken Seats Percent", type='float'),
				'attendee_count': fields.function(_get_attendee_count,
					type='integer', string='Attendee Count', store=True),
				'end_date': fields.function(_determin_end_date,
					fnct_inv=_set_end_date, type='date', string="End Date"),
				'hours': fields.function(_determin_hours_from_duration,
					fnct_inv=_set_hours, type='float', string="Hours"),
				}

	_defaults = {'active': True,
				 'state': 'draft'}

	_constraints = [
		(_is_instructor_not_in_attendees,
		 "The instructor can not be in an attendee list.",
		 ['instructor_id', 'attendee_ids']),
		]
