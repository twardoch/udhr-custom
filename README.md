# UDHR Custom: A Curated Collection of Universal Declaration of Human Rights Translations

This repository, `udhr-custom`, provides a comprehensive and structured collection of the Universal Declaration of Human Rights (UDHR) translated into a multitude of languages and writing scripts. The translations are primarily stored in XML format, and the repository also includes a suite of Python tools for processing, managing, and utilizing this valuable linguistic data.

This project is a custom fork/adaptation, building upon the foundational work of collecting UDHR translations, often sourced from initiatives like the Unicode Consortium's UDHR project and OHCHR.

## What is This?

At its core, `udhr-custom` is a digital library of the UDHR. Each translation is meticulously organized and encoded, making it accessible for both human reading and machine processing. Beyond the raw data, a set of Python scripts are provided to help users:

*   Fetch and update translations from official sources.
*   Generate and maintain an index of available translations.
*   Transliterate text between different scripts for certain languages.
*   Extract specific text samples (like Article 1) for various uses.

## Who is This For?

This repository is a valuable resource for a diverse range of users:

*   **Linguists:** For comparative linguistic studies, analyzing translation choices, and researching script variations.
*   **Typographers and Font Designers:** To test font rendering across a wide array of scripts and languages, ensuring correct display of characters and text flow.
*   **Software Developers & Engineers:** For internationalization (i18n) and localization (l10n) tasks, such as sourcing sample text for UI testing, or building NLP models, especially for low-resource languages.
*   **Researchers:** Anyone studying language, script usage, digital humanities, or the global dissemination of human rights information.
*   **Language Enthusiasts:** Individuals interested in exploring the UDHR in different languages.

## Why is This Useful?

The UDHR is a landmark document, and its translation into numerous languages makes it a unique multilingual corpus. `udhr-custom` harnesses this by providing:

*   **A Structured Dataset:** Machine-readable XML files allow for easy parsing and data extraction.
*   **Rich Linguistic Diversity:** Covers a vast number of languages and scripts, including many that are less commonly found in digital resources.
*   **Support for Typographic Testing:** The variety of scripts and text structures is ideal for testing font rendering capabilities.
*   **Aid for NLP Development:** Can serve as a foundational dataset for training or evaluating NLP models, particularly for tasks like language identification, machine translation, or transliteration.
*   **Facilitation of Comparative Studies:** Enables easy comparison of translations and linguistic features across languages.
*   **Preservation and Accessibility:** Contributes to the digital preservation and accessibility of these important translations.

## Getting Started

### Prerequisites

*   **For Data Access:** A tool to clone a Git repository (like the `git` command-line tool).
*   **For Using Python Tools:**
    *   Python 3.7 or newer.
    *   `pip` (Python package installer).
    *   It is highly recommended to use a Python virtual environment.

### Installation

1.  **Clone the Repository:**
    ```bash
    # Replace YOUR_USERNAME/udhr-custom.git with the actual repository URL
    git clone https://github.com/YOUR_USERNAME/udhr-custom.git
    cd udhr-custom
    ```

2.  **Install Dependencies (for Python tools):**
    If you plan to use the Python scripts located in the `tools` directory, you'll need to install the necessary dependencies.
    ```bash
    # Navigate to the tools directory
    cd tools

    # Create and activate a virtual environment (recommended)
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

    # Install requirements
    pip install -r requirements.txt
    ```

## How to Use

### Accessing the Data

The UDHR translations are located in the `data` directory, primarily as XML files. You can browse these files directly or use any XML parsing library in your preferred programming language to process them.

Each translation typically follows a naming convention like `udhr_KEY.xml` (e.g., `udhr_fra.xml` for French, where "fra" is the key).

### Using the Python Tools (Command Line)

The `tools` directory contains several Python scripts. Here are a few key examples:

*   **Updating/Fetching Translations (`update_from_official_udhr.py`):**
    This script can be used to fetch the latest versions of UDHR translations from external sources (like the Unicode Consortium or r12a.github.io) and process them into a standardized format, often outputting YAML files with extracted data.
    ```bash
    # Ensure you are in the 'tools' directory and your virtual environment is active
    python update_from_official_udhr.py
    ```
    *(Note: Configuration for sources and output paths are within the script itself and may need adjustment.)*

*   **Generating the Data Index (`make_index_xml.py`):**
    This script scans the UDHR XML files (typically in `data/udhr-manual/`) and generates or updates an `index.xml` file, which acts as a manifest for the available translations in that directory.
    ```bash
    # Ensure you are in the 'tools' directory
    python make_index_xml.py
    ```

### Using the Data Programmatically (Python Example)

You can easily parse the XML data using Python's built-in `xml.etree.ElementTree` or a more powerful library like `lxml` (which is included in `tools/requirements.txt`).

Here's a basic example using `lxml` to parse an XML file and extract some information:

```python
from lxml import etree

# Example: Parse the French UDHR translation
# Adjust the path as per your cloned repository structure and where you run this script.
# This example assumes the script is run from a directory like 'tools/' or a custom 'scripts/' dir,
# and 'data/' is a sibling directory.
udhr_file_path = "../data/udhr/udhr_fra.xml"

try:
    tree = etree.parse(udhr_file_path)
    root = tree.getroot()

    # Get the language name from the 'n' attribute of the root element
    language_name = root.get("n")
    print(f"Language: {language_name}")

    # Iterate through articles and print their titles and first paragraphs
    for article in root.findall(".//article"): # Using .//article to find articles anywhere under the root
        title_element = article.find("title")
        title = title_element.text if title_element is not None else "No Title"

        para_element = article.find("para") # Finds the first para directly under article
        first_paragraph_text = ""
        if para_element is not None:
            first_paragraph_text = "".join(para_element.itertext()).strip() # Get all text within para, including <sup>
        else: # Check if content is within listitem/para for articles with ordered lists
            list_item_para = article.find(".//orderedlist/listitem/para")
            if list_item_para is not None:
                 first_paragraph_text = "".join(list_item_para.itertext()).strip()
            else:
                first_paragraph_text = "No content found"

        print(f"  Article {article.get('number')}: {title}")
        # print(f"    First paragraph: {first_paragraph_text[:70]}...") # Print first 70 chars

except FileNotFoundError:
    print(f"Error: UDHR file not found at '{udhr_file_path}'. Adjust the path if necessary.")
except Exception as e:
    print(f"An error occurred: {e}")

```
This script provides a starting point for programmatically accessing the rich data contained within the UDHR XML files.

## Technical Details

This section provides a deeper dive into the structure of the data, the functionality of the provided tools, and guidelines for contributing to the repository.

### Data Structure

The UDHR translations are primarily stored in XML files, organized within the `data` directory.

*   **Core UDHR Translations (`data/udhr/`):**
    *   Contains the main set of UDHR translations in XML format.
    *   Files are typically named `udhr_KEY.xml`, where `KEY` is a unique identifier for the translation, often corresponding to a BCP47 tag or a combination of language and script codes (e.g., `udhr_eng.xml`, `udhr_fra_fr_pinyn.xml`).
    *   The structure of these XML files is defined by a RELAX NG schema, available in both XML syntax (`data/udhr/schema.rng`) and compact syntax (`data/udhr/schema.rnc`). Key elements include:
        *   `<udhr>`: The root element, containing metadata attributes like:
            *   `xml:lang`: Language code (e.g., "en", "fr").
            *   `iso639-3`: ISO 639-3 language code (e.g., "eng", "fra").
            *   `iso15924`: ISO 15924 script code (e.g., "Latn", "Cyrl").
            *   `dir`: Text direction ("ltr" or "rtl").
            *   `key`: A unique key for the translation (e.g., "eng", "fra_pinyn").
            *   `n`: The name of the language/translation (e.g., "English", "French Pinyin").
        *   `<title>`: The title of the document (e.g., "Universal Declaration of Human Rights").
        *   `<preamble>`: Contains the preamble of the UDHR, typically with its own `<title>` and one or more `<para>` (paragraph) elements.
        *   `<article>`: Represents each of the 30 articles. It has a `number` attribute.
            *   Each `<article>` contains a `<title>` (the article title, often just the article number) and one or more `<para>` elements for the article's text.
            *   Some articles with multiple clauses are structured using `<orderedlist>` and `<listitem>` elements, where each `<listitem>` contains a `<para>`.
        *   `<note>`: Optional notes that can appear at various points, containing one or more `<para>` elements.
    *   `data/udhr/index.xml`: An XML file that serves as a master index for the translations available in the `data/udhr/` directory, listing metadata for each. It may require manual updates or a dedicated script if one exists for it (distinct from `make_index_xml.py` which targets `data/udhr-manual/`).

*   **Manually Curated/Verified Translations (`data/udhr-manual/`):**
    *   This directory often holds translations that have undergone specific manual review, formatting, or are from particular sources that might require careful handling.
    *   Files here generally follow the same XML structure and naming conventions.
    *   `data/udhr-manual/index.xml`: An index specific to the translations in this subdirectory, generated by `tools/make_index_xml.py`.

*   **Status Files (`data/status/`):**
    *   These XML files (e.g., `status_aar.xml`) seem to hold metadata or status information about specific translations or languages, possibly related to their processing stage or inclusion criteria. The exact schema and usage may vary.

*   **Retired Files (`data/retired/`):**
    *   Contains older or superseded versions of UDHR files.

*   **Transliteration Data (`data/udhr-translit/`):**
    *   This directory appears to store transliterated versions of UDHR texts, likely generated by tools using libraries like Aksharamukha.
    *   `index_aksharamukha.xml` and `index_gimeltra.xml` suggest specific transliteration schemes or tools being indexed.

*   **Merged Data (`merged/`):**
    *   Contains YAML files (e.g., `udhr-art1-omniglot.yaml`) which are likely the output of processing scripts. These files often aggregate specific parts of the UDHR (like Article 1) from various translations, sometimes enriched with additional metadata (e.g., from Omniglot).

### Key Scripts and Their Functionality

The `tools` directory houses Python scripts for managing and processing the UDHR data.

*   **`update_from_official_udhr.py`:**
    *   **Purpose:** Fetches UDHR translation data from specified external sources (e.g., Unicode's UDHR project, r12a.github.io, as defined by the `SOURCE` variable in the script).
    *   **Functionality:** Parses the source XMLs (or HTMLs), extracts relevant information (like preamble, articles, language codes, names), and typically outputs a structured representation, such as a YAML file (e.g., `tools/udhr_art1_official.yaml` or `tools/udhr_art1_r12a.yaml`), often focusing on specific content like Article 1.
    *   **Dependencies:** `lxml`, `langcodes`, `yaplon`, `notodata.db`.

*   **`make_index_xml.py`:**
    *   **Purpose:** Generates or updates the `index.xml` file for a specified directory of UDHR XML files (defaulting to `data/udhr-manual/`).
    *   **Functionality:** Scans all `udhr_*.xml` files in the target directory, extracts metadata attributes from the root `<udhr>` element of each file, and compiles this into a new `index.xml` file.
    *   **Dependencies:** `lxml`.

*   **Transliteration Scripts:**
    *   **`aksharamukha_scripts.py`, `aksharamukha_scripts_sanskrit.py`, `aksharamukha_transliterate.py`:** These scripts leverage the `aksharamukha` library to perform transliteration of text between various Indic and other scripts. They likely read input text (possibly from UDHR XMLs or other sources) and output transliterated versions.
    *   **`gimeltra_transliterate.py`:** Suggests a tool or system named "Gimeltra" is used for transliteration, possibly for specific language pairs or scripts.
    *   **Dependencies:** `aksharamukha`.

*   **Omniglot-related Scripts:**
    *   **`edit_omniglot.py`, `update_omniglot.py`:** These scripts are likely used to integrate or cross-reference data with Omniglot, a comprehensive online encyclopedia of writing systems and languages. This might involve fetching language/script information or sample texts.
    *   The YAML files in `merged/` like `udhr-art1-omniglot.yaml` are probable outputs of these processes.

*   **Other Utility Scripts:**
    *   **`shavian/shaw.py`:** A script related to the Shavian alphabet.
    *   **`update_langnames_in_merged.py`:** Suggests a utility to update language names in the YAML files within the `merged/` directory.

### Typical Workflow

A common workflow when dealing with this repository might involve:

1.  **Adding/Updating Translations:**
    *   A new UDHR translation XML file is created or an existing one is modified. It must conform to the schema (`data/udhr/schema.rng`).
    *   The file is placed in the appropriate directory (e.g., `data/udhr/` or `data/udhr-manual/`).
2.  **Updating Index:**
    *   If files in `data/udhr-manual/` are changed, `tools/make_index_xml.py` is run to regenerate `data/udhr-manual/index.xml`.
    *   The main `data/udhr/index.xml` may require manual updates or a similar script (if one exists for it).
3.  **Processing Data:**
    *   Scripts like `update_from_official_udhr.py` might be run to refresh derived data (e.g., YAML files in `merged/` or `tools/`) based on the XML sources.
    *   Transliteration scripts might be used to generate new versions of texts in different scripts.

### Contributing to the Project

Contributions are welcome! Please follow these guidelines:

*   **Coding Conventions (Python):**
    *   Follow PEP 8 style guidelines.
    *   Write clear, well-commented code.
    *   Ensure scripts are executable and have necessary shebangs (e.g., `#!/usr/bin/env python3`).
    *   Include docstrings for modules, classes, and functions.

*   **Data Format (XML):**
    *   When adding or modifying UDHR XML files, strictly adhere to the schema defined in `data/udhr/schema.rng` (or `.rnc`).
    *   Ensure all required metadata attributes (`xml:lang`, `iso639-3`, `iso15924`, `dir`, `key`, `n`) are correctly specified in the `<udhr>` element.
    *   Validate your XML against the schema if possible.

*   **Commit Messages:**
    *   Write clear and concise commit messages.
    *   Use the imperative mood (e.g., "Add French translation" not "Added French translation").
    *   A short subject line (max 50 chars) is preferred, followed by a blank line and a more detailed body if necessary.

*   **Testing:**
    *   Currently, the repository does not have a comprehensive automated test suite.
    *   If you modify existing scripts or add new ones, manually test your changes thoroughly.
    *   Consider adding unit tests for new functionalities if appropriate (e.g., using Python's `unittest` or `pytest` frameworks). The script `merged/test.py` is an example of a very specific data check, not a general testing utility.

*   **Adding New Translations:**
    1.  Obtain the translation from a reputable source.
    2.  Format it as an XML file according to the schema (`data/udhr/schema.rng`). Pay close attention to metadata attributes and structural tags.
    3.  Name the file appropriately (e.g., `udhr_NEWKEY.xml`) and place it in `data/udhr/`. If it requires special handling/verification that might warrant inclusion in `data/udhr-manual/`, please discuss this in your PR or issue.
    4.  If applicable, update the relevant `index.xml` file (e.g., run `tools/make_index_xml.py` if the file is in `data/udhr-manual/`, or manually update `data/udhr/index.xml`).
    5.  Reference the source of the translation in your commit message or PR description.

*   **Bug Reports and Feature Requests:**
    *   Use the GitHub Issues tracker for the repository.
    *   Provide detailed information, including steps to reproduce for bugs.

*   **Pull Requests (PRs):**
    1.  Fork the repository.
    2.  Create a new branch for your changes (`git checkout -b feature/your-feature-name` or `bugfix/issue-number`).
    3.  Make your changes, commit them with clear messages.
    4.  Push your branch to your fork.
    5.  Open a Pull Request against the main repository branch.
    6.  Clearly describe the changes made in your PR.
    7.  Ensure your PR addresses a single issue or implements a cohesive feature.
