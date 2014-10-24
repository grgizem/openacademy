from openerp.osv import osv, fields


class Partner(osv.Model):
	"""Inherited res.partner"""
	_name = 'res.partner'
	_inherit = 'res.partner'
	_columns = {'instructor': fields.boolean("Instructor")
			   }