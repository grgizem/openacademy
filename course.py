from openerp.osv import osv, fields


class Course(osv.Model):
	_name = "openacademy.course"

	def copy(self, cr, uid, id, default, context=None):
		course = self.browse(cr, uid, id, context=context)
		new_name = "Copy of %s" % course.name
		others_count = self.search(cr, uid, [('name', '=like', new_name+'%')],
								   count=True, context=context)
		if others_count > 0:
			new_name = "%s (%s)" % (new_name, others_count+1)
			default['name'] = new_name
		return super(Course, self).copy(cr, uid, id, default, context=context)

	def _get_attendee_count(self, cr, uid, ids, name, args, context=None):
		res = {}
		for course in self.browse(cr, uid, ids, context=context):
			res[course.id] = 0
			for session in course.session_ids:
				res[course.id] += len(session.attendee_ids)
		return res

	def _get_courses_from_sessions(self, cr, uid, ids, context=None):
		sessions = self.browse(cr, uid, ids, context=context)
		return list(set(session.course_id.id for session in sessions))

	_columns = {'name' : fields.char("Title",
									  256,
									  translate=True,
									  required=True,
									  select=1),
				'start_date': fields.date("Start Date"),
				'description' : fields.text("Description",
											translate=True),
				'active': fields.boolean("Active"),
				'responsible_id': fields.many2one('res.users',
					                              "Responsible"),
				'session_ids': fields.one2many('openacademy.session',
					                           'course_id',
					                           "Sessions"),
				'code': fields.char("Code",
					                100,
					                required=True,
					                help="Course Code",
					                select=1),
				'status': fields.selection((('ok','Opened'), ('nok','Not Opened')),
                   						   "Status", required=True),
				'attendee_count': fields.function(_get_attendee_count, type='integer', string="Attendee Count",
					store={'openacademy.session': (_get_courses_from_sessions, ['attendee_ids'], 0)}),
			   }

	_defaults = {'start_date': fields.date.today,
				 'active': True
				}

	_sql_constraints = [
		('name_description_equality_check',
		 'CHECK(name <> description)',
		 'Course name and description can not be same.'),
		('name_unique_check',
		 'UNIQUE(name)',
		 'Course name should be unique.')
		]