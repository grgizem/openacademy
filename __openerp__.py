{
	"name": "Open Academy",
	"version": "1.0",
	"category": "Test",
	"depends": ["base", "report_webkit"],
	"author": "Gizem Gur",
	"description": """\
	Open Academy is a module to documentation, tracking, reporting and delivery of e-learning education courses or training programs.
	""",
	"data": [
		"view/menu.xml",
		"view/course.xml",
		"view/session.xml",
		"view/attendee.xml",
		"view/partner.xml",
		"workflow/session_workflow.xml",
		"wizard/create_attendee_view.xml",
		"report/openacademy.xml"
	],
	"update_xml": [
		"security/groups.xml",
		"security/ir.model.access.csv"
		],
	"demo": [],
	"test": [],
	"installable": True,
	"auto_install": False,
}