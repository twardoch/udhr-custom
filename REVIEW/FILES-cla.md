# FILES-cla.md: File System Catalog

## Repository Overview

This repository (`udhr-custom`) is a comprehensive collection of Universal Declaration of Human Rights (UDHR) translations in multiple languages and scripts, stored primarily in XML format with supporting Python tools for processing and management.

## File System Tree

```
/root/repo/
├── LICENSE                                    # Apache License 2.0
├── README.md                                  # Comprehensive project documentation
├── REVIEW/                                    # Review folder (this analysis)
│   ├── filesystem-tree.txt                   # Generated file listing
│   └── FILES-cla.md                          # This file catalog
├── data/                                      # Main data directory
│   ├── retired/                              # Deprecated/superseded files
│   │   ├── status_fuc.xml                    # Old status file for Fulah
│   │   ├── status_prq.xml                    # Old status file for Peruvian Quechua
│   │   ├── udhr_fuc.xml                      # Old UDHR translation (Fulah)
│   │   ├── udhr_fum.xml                      # Old UDHR translation (Fulah variant)
│   │   ├── udhr_prq.xml                      # Old UDHR translation (Peruvian Quechua)
│   │   └── udhr_tam.xml                      # Old UDHR translation (Tamil)
│   ├── status/                               # Language processing status files
│   │   ├── status_*.xml                      # 400+ status files tracking processing state
│   │   ├── status_kdh_*.jpg                  # Images related to Tem language processing
│   │   ├── status_kdh_report.pdf             # Report for Tem language status
│   │   └── template.xml                      # Template for status files
│   ├── udhr-manual/                          # Manually curated/verified translations
│   │   ├── index.xml                         # Index of manual translations
│   │   ├── status_egy_egyp.xml               # Status for Egyptian hieroglyphs
│   │   ├── udhr_cmn_nshu.xml                 # Chinese (Nüshu script)
│   │   ├── udhr_egy_egyp.xml                 # Egyptian hieroglyphs UDHR
│   │   ├── udhr_eng_brai.xml                 # English Braille
│   │   ├── udhr_eng_dsrt.xml                 # English Deseret script
│   │   ├── udhr_eng_shaw.xml                 # English Shavian script
│   │   ├── udhr_hmn_hmng.xml                 # Hmong (Pahawh Hmong script)
│   │   ├── udhr_hmn_hmnp.xml                 # Hmong (Nyiakeng Puachue Hmong)
│   │   ├── udhr_men_mend.xml                 # Mende (Mende script)
│   │   ├── udhr_rej_rjng.xml                 # Rejang script
│   │   ├── udhr_rhg_rohg.xml                 # Rohingya (Hanifi Rohingya script)
│   │   ├── udhr_smp_samr.xml                 # Samaritan script
│   │   └── udhr_syl_sylo.xml                 # Sylheti (Syloti Nagri script)
│   ├── udhr-translit/                        # Transliterated versions
│   │   ├── index.xml                         # General transliteration index
│   │   ├── index_aksharamukha.xml            # Aksharamukha transliterations index
│   │   ├── index_gimeltra.xml                # Gimeltra transliterations index
│   │   ├── udhr_aii_*.xml                    # Assyrian transliterations (various scripts)
│   │   ├── udhr_mar_modi.xml                 # Marathi in Modi script
│   │   └── udhr_san_*.xml                    # Sanskrit in various ancient scripts
│   └── udhr/                                 # Main UDHR translations collection
│       ├── index.xml                         # Master index of all translations
│       ├── schema.rnc                        # RELAX NG Compact schema
│       ├── schema.rng                        # RELAX NG XML schema
│       ├── template.xml                      # Template for new translations
│       └── udhr_*.xml                        # 500+ UDHR translations (various languages)
├── merged/                                   # Processed/merged data outputs
│   ├── test.py                               # Data validation script
│   ├── udhr-art1-omniglot-orig.yaml         # Original Omniglot Article 1 data
│   ├── udhr-art1-omniglot*.yaml             # Various versions of merged Omniglot data
│   ├── udhr-art1-omniglot7-lines.txt        # Text format of Article 1 data
│   ├── udhr-art1-omniglot7.yaml.zip         # Compressed YAML data
│   └── udhr-omniglot.yaml                   # Complete Omniglot integration
└── tools/                                   # Python processing tools
    ├── aksharamukha-scripts.yml              # Script configuration for Aksharamukha
    ├── aksharamukha_scripts.py               # Aksharamukha script processing
    ├── aksharamukha_scripts_sanskrit.py      # Sanskrit-specific transliteration
    ├── aksharamukha_transliterate.py         # General Aksharamukha transliteration
    ├── edit_omniglot.py                      # Omniglot data editor
    ├── gimeltra_transliterate.py             # Gimeltra transliteration system
    ├── install.sh                            # Installation script
    ├── make_index_xml.py                     # XML index generator
    ├── requirements.txt                      # Python dependencies
    ├── scripts.yaml                          # Script configuration
    ├── shavian/                              # Shavian alphabet tools
    │   ├── dave.dict                         # Dictionary file
    │   ├── shaw.py                           # Shavian processing script
    │   └── udhr_eng.html                     # English UDHR in HTML
    ├── test.py                               # General testing script
    ├── udhr-art1-omniglot.yaml              # Article 1 Omniglot data
    ├── udhr-omniglot-codes.yaml             # Language code mappings
    ├── udhr-omniglot.yaml                   # Complete Omniglot dataset
    ├── udhr_art1_aksharamukha.yaml          # Article 1 Aksharamukha data
    ├── udhr_art1_official.yaml              # Official Article 1 sources
    ├── udhr_art1_r12a.yaml                  # r12a.github.io Article 1 data
    ├── update_from_official_udhr.py         # Fetches updates from official sources
    ├── update_langnames_in_merged.py        # Updates language names in merged files
    └── update_omniglot.py                   # Updates Omniglot integration
```

## Detailed File/Folder Descriptions

### Root Level Files

- **LICENSE**: Apache License 2.0 governing the project's open-source distribution
- **README.md**: Comprehensive documentation explaining the project's purpose, structure, usage instructions, and technical details

### Main Data Directory (`data/`)

#### Core UDHR Collection (`data/udhr/`)
- **Purpose**: Primary repository of UDHR translations in standardized XML format
- **Contents**: 500+ translation files covering diverse languages and scripts
- **Schema**: Defined by RELAX NG schema files ensuring consistent XML structure
- **Naming**: Files follow `udhr_KEY.xml` pattern where KEY identifies language/variant
- **Metadata**: Each translation includes language codes (ISO 639-3, ISO 15924), direction, and linguistic metadata

#### Manual Curation (`data/udhr-manual/`)
- **Purpose**: Translations requiring special handling, manual verification, or unique scripts
- **Special Cases**: Includes rare scripts (hieroglyphs, Braille, Deseret, Shavian), constructed writing systems
- **Quality Control**: Manually reviewed for accuracy and formatting consistency

#### Transliterated Versions (`data/udhr-translit/`)
- **Purpose**: Programmatically generated transliterations between scripts
- **Systems**: Uses Aksharamukha and Gimeltra transliteration libraries
- **Applications**: Enables cross-script comparison and alternative script representations

#### Status Tracking (`data/status/`)
- **Purpose**: Metadata about processing state, quality, and completion status of translations
- **Coverage**: Tracks over 400 language varieties
- **Documentation**: Includes reports and images for complex processing cases

#### Deprecated Content (`data/retired/`)
- **Purpose**: Archive of superseded or obsolete translation files
- **Maintenance**: Preserves historical versions while keeping main collection current

### Processing Tools (`tools/`)

#### Core Processing Scripts
- **update_from_official_udhr.py**: Fetches latest translations from Unicode Consortium and other official sources
- **make_index_xml.py**: Generates XML indices for translation collections
- **test.py**: Validation and testing utilities

#### Transliteration Systems
- **aksharamukha_*.py**: Scripts using Aksharamukha library for Indic script transliteration
- **gimeltra_transliterate.py**: Alternative transliteration system for specific language pairs

#### Data Integration
- **update_omniglot.py**: Integrates data from Omniglot encyclopedia of writing systems
- **edit_omniglot.py**: Manual editing tools for Omniglot data
- **update_langnames_in_merged.py**: Maintains consistency in language naming across datasets

#### Configuration and Dependencies
- **requirements.txt**: Python package dependencies (lxml, aksharamukha, langcodes, etc.)
- **scripts.yaml**: Configuration for various processing scripts
- **aksharamukha-scripts.yml**: Specific configuration for transliteration scripts

### Processed Outputs (`merged/`)

#### YAML Datasets
- **Purpose**: Machine-readable aggregated datasets derived from XML sources
- **Focus**: Often extracts specific content (e.g., Article 1) for comparative analysis
- **Integration**: Combines UDHR data with external linguistic resources (Omniglot)
- **Formats**: Multiple versions optimized for different use cases

#### Validation
- **test.py**: Data integrity checking for merged datasets

### Special Features

#### Multi-Script Support
- Supports over 150 writing systems including Latin, Cyrillic, Arabic, Devanagari, CJK scripts
- Includes rare and historical scripts (Egyptian hieroglyphs, Linear B, ancient Mesopotamian)
- Alternative scripts for major languages (Braille, phonetic notations)

#### Linguistic Diversity
- Covers major world languages and many endangered/minority languages
- Regional variants and dialects documented separately
- Includes constructed languages and alternative orthographies

#### Technical Standards
- XML structure validated against RELAX NG schema
- Consistent metadata using ISO standards (639-3 for languages, 15924 for scripts)
- Unicode compliance for proper character representation
- Standardized file naming and organization

#### Quality Assurance
- Multi-tier organization (main, manual, transliterated) based on processing requirements
- Status tracking system monitoring translation quality and completeness
- Version control through git for change tracking
- Automated validation tools for data integrity

This repository serves as a comprehensive linguistic resource for researchers, developers, typographers, and anyone working with multilingual text processing, offering both raw translation data and sophisticated processing tools for analysis and manipulation.