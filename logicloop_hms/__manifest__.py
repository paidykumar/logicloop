{

    "name": "Hospital Management",
    "version": "1.0",
    "depends": ["base", 'mail'],
    "data": [
        'security/hospital_groups.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/main_menu_file.xml',
        'views/medical_appointment.xml',
        'views/medical_patient.xml',
        'views/medical_physician.xml',
        'views/res_partner.xml',
        'views/assets.xml',

    ],
    "installable": True,
    "application": True,
    "auto_install": False,
    "qweb": ['static/src/xml/template.xml']

}
