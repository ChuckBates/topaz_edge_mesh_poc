package example

import rego.v1

default allow := false

allow if {
	input.requestType = "evaluate"
	input.action in user_permissions
	location_is_valid
	product_type_is_valid
	company_party_is_valid
	pss_right_is_valid
}

allow if {
	input.requestType = "generate_query"
	input.action in permission_sets["nominations"]
	input.action in user_permissions
	pss_right_is_valid
	allowedNominations[x]
}

allow  if {
	input.requestType = "generate_query"
	input.action in permission_sets["tickets"]
	input.action in user_permissions
	pss_right_is_valid
	allowedTickets[x]
}

allowedNominations[x] if {
	data.nominations[x].location = inherited_locations[_]
	data.nominations[x].productType = inherited_product_types[_]
	data.nominations[x].company = inherited_companies[_]
	data.nominations[x].subscriber = inherited_subscribers[_]
}

allowedTickets[x] if {
	data.tickets[x].location = inherited_locations[_]
	data.tickets[x].productType = inherited_product_types[_]
	data.tickets[x].company = inherited_companies[_]
	data.tickets[x].subscriber = inherited_subscribers[_]
}

principal := principals[input.principal]

user_permissions contains permission if {
	some inherited_permission in inherited_permissions
	some permission in permissions_by_role[inherited_permission.role].valid_actions
	permission in subscriber_permissions
}

pss_right_is_valid if permissions[input.action].pss_right == ""
pss_right_is_valid if permissions[input.action].pss_right in principal.pss_rights

company_party_is_valid if permissions[input.action].companyParty == ""
company_party_is_valid if permissions[input.action].companyParty in input.context.companyParties

location_is_valid if "*" in inherited_locations
location_is_valid if {
	every location in input.context.locations {
		location in inherited_locations
	}
}

product_type_is_valid if "*" in inherited_product_types
product_type_is_valid if {
	every productType in input.context.productTypes {
		productType in inherited_product_types
	}
}

inherited_permissions contains permission if {
	some permission in principal.permissions
	permission.subscriber = input.context.subscriber
	permission.company in input.context.companies
}

inherited_companies contains company if {
	some permission in inherited_permissions
	company = permission.company
}

inherited_subscribers contains subscriber if {
	some permission in inherited_permissions
	subscriber = permission.subscriber
}

subscriber_permissions contains subscriber_permission if {
	some subscriber_permission in subscribers[input.context.subscriber].permissions
}

inherited_product_types contains productType if {
	some permission in inherited_permissions
	some company_permission in companies[permission.company].permissions
	company_permission.subscriber = input.context.subscriber
	some productType in company_permission.productTypes
}

inherited_locations contains location if {
	some permission in inherited_permissions
	some company_permission in companies[permission.company].permissions
	company_permission.subscriber = input.context.subscriber
	some location in company_permission.locations
}

principals := {
    "bob": {
        "permissions": [
			{
                "role": "companyAdministrator",
                "company": "EXN",
                "subscriber": "CPL",
                "locations": [
                    "DVD",
					"SAN",
					"STL"
                ],
                "productTypes": [
                    "GAS",
					"JET"
                ]
            },
            {
                "role": "scheduler",
                "company": "EXN",
                "subscriber": "CPL",
                "locations": [
                    "*"
                ],
                "productTypes": [
                    "*"
                ]
            }            
        ],
        "pss_rights": [
            "pss_nomination_create"
        ]
    },
	"alice": {
		"permissions": [
			{
				"role": "inspector",
				"company": "P66",
				"subscriber": "KMO",
				"locations": [
					"DVD"
				],
				"productTypes": [
					"GAS"
				]
			}           
		],
		"pss_rights": []
	}
}

companies := {
    "EXN": {
        "permissions": [
            {
                "subscriber": "CPL",
                "role": "scheduler",
                "locations": [
                    "DVD",
                    "SAN"
                ],
                "productTypes": [
                    "GAS",
                    "JET"
                ]
            },
            {
                "subscriber": "CPL",
                "role": "compayAdministrator",
                "locations": [
                    "DVD",
                    "SAN"
                ],
                "productTypes": [
                    "GAS",
                    "JET"
                ]
            }
        ]
    },
	"P66": {
		"permissions": [
			{
				"subscriber": "KMO",
				"role": "inspector",
				"locations": [
					"DVD"
				],
				"productTypes": [
					"GAS"
				]
			}
		]
	}
}

permissions_by_role := {
  "scheduler": {
    "valid_actions": [
      "nomination_create",
      "nomination_edit",
      "nomination_view",
      "ticket_create",
      "ticket_edit",
      "ticket_view"
    ]
  },
  "companyAdministrator": {
    "valid_actions": [
	  "nomination_subscriber_confirm",
      "nomination_create",
      "nomination_edit",
      "nomination_view",
      "ticket_create",
      "ticket_edit",
      "ticket_view"
    ]
  },
  "pipelineEmployee": {
    "valid_actions": [
      "nomination_create",
      "nomination_edit",
      "nomination_view",
      "ticket_create",
      "ticket_edit",
      "ticket_view"
    ]
  },
  "inspector": {
    "valid_actions": [
      "nomination_view",
      "ticket_view"
    ]
  }
}

subscribers := {
    "CPL": {
        "permissions": [
			"nomination_subscriber_confirm",
            "nomination_create",
            "nomination_edit",
            "nomination_view",
            "ticket_create",
            "ticket_edit",
            "ticket_view"
        ]
    },
	"KMO": {
		"permissions": [
			"ticket_create",
			"ticket_edit",
			"ticket_view"
		]
	}
}

permissions := {
	"admin_add_application": {},
    "nomination_create": {
        "pss_right": "pss_nomination_create",
        "companyParty": "shipper"
    },
    "nomination_edit": {
        "pss_right": "",
        "companyParty": "shipper"
    },
    "nomination_subscriber_confirm": {
        "pss_right": "pss_nomination_subscriber_confirm",
        "companyParty": "carrier"
    },
    "nomination_supCon_confirm": {
        "pss_right": "",
        "companyParty": "supCon"
    },
    "nomination_tankage_confirm": {
        "pss_right": "",
        "companyParty": "tankage"
    },
    "nomination_view": {
        "pss_right": "",
        "companyParty": ""
    },
    "ticket_create": {
        "pss_right": "",
        "companyParty": "subscriber"
    },
    "ticket_edit": {
        "pss_right": "",
        "companyParty": "subscriber"
    },
    "ticket_view": {
        "pss_right": "",
        "companyParty": ""
    }
}

permission_sets := {
	"nominations": [
		"nomination_create",
		"nomination_edit",
		"nomination_subscriber_confirm",
		"nomination_supCon_confirm",
		"nomination_tankage_confirm",
		"nomination_view",
	],
	"tickets": [
		"ticket_create",
		"ticket_edit",
		"ticket_view"
	]
}
