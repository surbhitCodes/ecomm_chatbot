"""
Data storage in a dictionary, could use json or other document storage NoSQL dbms.
"""

materials_data = {
    "product_catalog": [
        {
            "id": "LUM-2x4-8-PT",
            "category": "Lumber",
            "name": "Pressure Treated Lumber 2x4x8",
            "manufacturer": "TimberTech Pro",
            "specifications": {
                "dimensions": "1.5\" x 3.5\" x 96\"",
                "grade": "Construction Grade",
                "species": "Southern Yellow Pine",
                "treatment": "Pressure Treated",
                "moisture_content": "19% or less",
                "weight_per_piece": "12.5 lbs",
                "treatment_retention": "0.40 pcf",
                "grade_stamp": "SPIB",
                "use_category": "UC4A - Ground Contact"
            },
            "applications": [
                "Ground contact applications",
                "Deck framing",
                "General construction",
                "Outdoor structures"
            ],
            "technical_details": {
                "bending_strength": "875-1,200 psi",
                "modulus_of_elasticity": "1,400,000 psi",
                "fastener_requirements": "Hot-dipped galvanized or stainless steel",
                "installation_temperature": "40°F to 90°F",
                "warranty": "25 years limited"
            },
            "price_history": [
                {"date": "2024-01-01", "price": 8.97},
                {"date": "2024-02-01", "price": 9.25},
                {"date": "2024-03-01", "price": 8.89}
            ],
            "current_stock": {
                "san_francisco": 1200,
                "los_angeles": 850,
                "seattle": 950
            }
        },
        {
            "id": "PLY-CDX-23/32",
            "category": "Plywood",
            "name": "CDX Plywood 23/32\" 4x8",
            "manufacturer": "PlyPro Industries",
            "specifications": {
                "dimensions": "23/32\" x 48\" x 96\"",
                "grade": "CDX",
                "material": "Softwood",
                "core_type": "Veneer",
                "face_grade": "C",
                "back_grade": "D",
                "weight_per_sheet": "52 lbs",
                "thickness_tolerance": "+/- 1/32\""
            },
            "applications": [
                "Roof sheathing",
                "Wall sheathing",
                "Subflooring",
                "General construction"
            ],
            "technical_details": {
                "span_rating": "24/16",
                "strength_axis": "48\" direction",
                "water_resistance": "Exposure 1",
                "flame_spread_rating": "Class C",
                "formaldehyde_emission": "PS 1-09 compliant"
            },
            "price_history": [
                {"date": "2024-01-01", "price": 45.99},
                {"date": "2024-02-01", "price": 43.75},
                {"date": "2024-03-01", "price": 44.50}
            ]
        }
    ],

    "technical_documents": [
        {
            "id": "TD-001",
            "product_id": "LUM-2x4-8-PT",
            "title": "Pressure Treated Lumber Installation Guide",
            "content": """
Pressure Treated Lumber Installation Guidelines

1. Storage and Handling
- Store lumber off the ground
- Keep material dry and covered
- Allow wood to acclimate to local conditions

2. Cutting and Installation
- Always wear appropriate PPE
- Seal cut ends with preservative
- Use appropriate fasteners
- Maintain proper ventilation

3. Fastener Requirements
- Use hot-dipped galvanized or stainless steel fasteners
- Minimum coating requirement G-185
- Do not use standard steel or aluminum fasteners

4. Recommended Applications
- Ground contact applications
- Deck framing
- Fence posts
- Outdoor structures

5. Safety Considerations
- Wear dust mask when cutting
- Work in ventilated area
- Clean up sawdust
- Dispose of waste properly
            """
        }
    ],

    "building_codes": [
        {
            "code_id": "IBC-2021-2304",
            "title": "General Construction Requirements - Wood",
            "jurisdiction": "International Building Code",
            "applicable_products": ["LUM-2x4-8-PT", "PLY-CDX-23/32"],
            "summary": """
Wood Construction Guidelines - IBC 2021 Section 2304

1. General Requirements
- Design requirements for lumber grades
- Load-bearing capacity specifications
- Connection details and requirements

2. Protection Against Decay
- Required treatments for ground contact
- Ventilation requirements
- Moisture control measures

3. Fire-Retardant Requirements
- Treatment specifications
- Testing requirements
- Labeling requirements
            """
        }
    ],

    "installation_guides": [
        {
            "guide_id": "IG-PT-001",
            "product_id": "LUM-2x4-8-PT",
            "title": "Deck Framing Installation Guide",
            "content": """
Deck Framing Installation Best Practices

Step 1: Planning and Layout
- Determine joist spacing (16" O.C. typical)
- Plan for proper drainage (1/4" per foot slope)
- Account for ventilation requirements

Step 2: Material Preparation
- Allow lumber to acclimate
- Sort material for best pieces
- Pre-cut to required lengths

Step 3: Installation Process
1. Install ledger board
   - Use proper flashing
   - Install with lag screws
   - Maintain proper spacing

2. Set support posts
   - Minimum depth requirements
   - Use proper concrete footings
   - Ensure plumb installation

3. Install beams and joists
   - Use proper hangers
   - Maintain level installation
   - Install blocking as required
            """
        }
    ],

    "safety_documents": [
        {
            "doc_id": "SD-PT-001",
            "product_id": "LUM-2x4-8-PT",
            "title": "Pressure Treated Lumber Safety Guide",
            "content": """
Safety Guidelines for Pressure Treated Lumber

1. Personal Protective Equipment
- Wear safety glasses
- Use dust mask when cutting
- Wear work gloves
- Use hearing protection

2. Safe Handling Practices
- Proper lifting techniques
- Clean work area
- Proper tool selection
- Ventilation requirements

3. First Aid Measures
- Eye contact procedures
- Skin contact procedures
- Inhalation procedures
- Emergency contacts

4. Environmental Considerations
- Proper disposal methods
- Recycling guidelines
- Environmental impact
- Storage requirements
            """
        }
    ],

    "material_alternatives": [
        {
            "primary_product_id": "LUM-2x4-8-PT",
            "alternatives": [
                {
                    "id": "COMP-2x4-8",
                    "name": "Composite Lumber 2x4",
                    "comparison": {
                        "durability": "Higher",
                        "cost": "300% more",
                        "maintenance": "Lower",
                        "sustainability": "Higher",
                        "installation_difficulty": "Similar"
                    }
                },
                {
                    "id": "STEEL-2x4",
                    "name": "Steel Stud 2x4",
                    "comparison": {
                        "durability": "Higher",
                        "cost": "200% more",
                        "maintenance": "Lower",
                        "sustainability": "Lower",
                        "installation_difficulty": "Higher"
                    }
                }
            ]
        }
    ],

    "typical_queries": [
        {
            "query": "What size lumber do I need for a deck joist spanning 12 feet?",
            "context": "Residential deck construction",
            "relevant_products": ["LUM-2x4-8-PT"],
            "relevant_codes": ["IBC-2021-2304"],
            "considerations": [
                "Load requirements",
                "Spacing",
                "Environmental conditions"
            ]
        },
        {
            "query": "Can I use regular screws with pressure treated lumber?",
            "context": "Deck construction",
            "relevant_products": ["LUM-2x4-8-PT"],
            "relevant_documents": ["TD-001", "SD-PT-001"],
            "key_points": [
                "Corrosion resistance",
                "Material compatibility",
                "Safety considerations"
            ]
        }
    ]
}
